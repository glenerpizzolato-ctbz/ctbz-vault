#!/usr/bin/env python3
"""
Investiga, para UMA empresa (CNPJ), por que ela recebeu ou não as notificações de guias de imposto em PRODUÇÃO, somente leitura:
a do agrupamento (empacotamento do dia 15, microsservico-agrupamento-guias) e a avulsa (guia individual, experts-service).

Cruza, por competência:
  - banco do agrupamento (prd_atendimento_canais_ms_agrupamento_guias): grupo_guia, historico_processamento_grupo_guia,
    item_grupo_guia + controle_guias (o que trava o grupo), controle_guias da empresa (guias que existiam) e controle_notificacao;
  - WhatsApp ativo (prd_crm_atendimento_zendesk, opcional): status real da mensagem pelo external_id;
  - experts-service (prd_experts_experts_service): task_scheduler com event_source_type = guia-imposto-notifier (avulsas);
  - BigQuery (contabilizei-dataflow.saude_empresa.empresa): plano e status da empresa mês a mês (snapshot mensal).
e classifica cada competência com um código de causa (ver CAUSAS) e o que fazer.

Uso:
  investigar.py <cnpj> [--desde AAAAMM] [--ate AAAAMM] [--saida DIR] [--sem-bq] [--sem-wpp]
Padrões: --ate = competência anterior ao mês atual; --desde = 12 competências antes de --ate;
DIR = ~/Downloads/investigacoes/notificacoes-guias/<cnpj>/<AAAA-MM-DD_HHMM>/ (resumo.md e dados.json).
Proxies de prd: sql_atendimento_prd (5443) e sql_exp_prd (5445) obrigatórios; sql_crm_prd (5444) opcional (WhatsApp ativo).
Nunca grava e-mail, telefone ou nome de contato nas saídas.
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Sao_Paulo")
SVC_AGRUP = "prd_atendimento_canais_ms_agrupamento_guias"
SVC_EXP = "prd_experts_experts_service"
SVC_CRM = "prd_crm_atendimento_zendesk"
EXPERTS = {"EXPERT_ESSENCIAL", "EXPERT_PRO"}
BP = {"BASICO", "AVANCADO", "PREMIUM", "MULTIBENEFICIOS"}
# Até 2026-10-22 (commit 2d62f7b2 do plataforma-faturamento-worker) só EXPERT_ESSENCIAL era enviado ao agrupamento;
# depois, os lotes passaram a ser Experts SN/LP (ESSENCIAL e PRO), BP LP e BP Simples.
VIRADA_LOTES = dt.date(2026, 10, 22)

CAUSAS = {
    "ENVIADO": "Agrupamento notificado com sucesso",
    "ENVIADO_PARCIAL": "Agrupamento notificado só em parte dos canais",
    "FORA_DO_AGRUPAMENTO_PLANO": "Empresa fora do agrupamento pelo plano no dia 15 (sem grupo)",
    "SEM_GATILHO": "Plano elegível e guias existentes, mas o agrupamento nunca foi disparado (sem grupo nem histórico)",
    "SEM_GUIA": "Sem guia agrupável na montagem (AGRUPAMENTO_SEM_GUIA ou nenhuma guia no microsserviço)",
    "AGUARDANDO_GERACAO": "Grupo preso em GUIAS_AGUARDANDO_GERACAO (guia sem PDF no dia 15, nunca retentado)",
    "GUIA_TRAVANDO": "Grupo preso por guia sem arquivo dentro dele (duplicata/guia órfã em AGUARDANDO_EMISSAO)",
    "GUIAS_COM_ERRO": "Grupo em GUIAS_COM_ERRO (guia com erro de processamento/upload trava o grupo)",
    "ERRO_GUIA_ALTERADA": "Guias mudaram depois do agrupamento (ERRO_GUIA_ALTERADA*/ERRO_NOVA_GUIA): sem renotificação",
    "ERRO_PROCESSAMENTO": "Erro de processamento do grupo (ERRO_SISTEMA/ERRO_GERACAO_PDF_AGRUPAMENTO, reprocessável)",
    "SEGMENTO_SEM_NOTIFICACAO": "Grupo OK, mas o segmento não tem notificação (BP Simples, plano nulo, WhatsApp do BASICO)",
    "ELEGIVEL_NAO_NOTIFICADO": "Grupo em SUCESSO_AGRUPAMENTO sem controle de notificação (cron não pegou ou ainda vai rodar)",
    "FALHA_NOTIFICACAO": "Notificação com FALHA/DADOS_INCOMPLETO/BLOQUEADA_OPTOUT (crons não renotificam)",
    "OUTRO": "Status não mapeado: ler o grupo e o histórico",
}
ACAO = {
    "FORA_DO_AGRUPAMENTO_PLANO": "Confirmar com CS/Faturamento a troca de plano no período. Não é falha do agrupamento; a avulsa do experts-service também só vale para plano Experts.",
    "SEM_GATILHO": "Procurar nos logs do plataforma-faturamento-worker (projeto contabilizei-impostos) o envio para o idEmpresa no dia 15; logs só ficam 30 dias. Republicar pela rota envia-empresa-ms-agrupamento-guia/{idEmpresa} é decisão do usuário.",
    "SEM_GUIA": "Conferir se a plataforma tinha guias agrupáveis antes do dia 15; se tinha, o problema é a sincronização das guias com o microsserviço.",
    "AGUARDANDO_GERACAO": "Grupo não é retentado (ReprocessamentoErrosJobImpl só pega ERRO_SISTEMA/ERRO_GERACAO_PDF_AGRUPAMENTO; AnalisaAlteracaoGuia ignora guia depois do vencimento/virada). Candidato à ACR PRD-174011.",
    "GUIA_TRAVANDO": "Confirmar no sistema de impostos (Fiscal) o status da guia travando; se cancelada/substituída, o evento não chegou ao microsserviço. Tirar a guia do grupo e reprocessar (data fix entregue ao usuário).",
    "GUIAS_COM_ERRO": "Ver a guia com ERRO_PROCESSAR_GUIA/FALHA_UPLOAD; só sai se a guia mudar de novo.",
    "ERRO_GUIA_ALTERADA": "Não há renotificação com as guias novas (decisão de Produto).",
    "ERRO_PROCESSAMENTO": "Deveria ser pego pelo reprocessa-erros; se não foi, investigar o job.",
    "ELEGIVEL_NAO_NOTIFICADO": "Se as crons dos dias 15 a 19 já passaram, só disparo manual (decisão do usuário).",
    "FALHA_NOTIFICACAO": "Ver motivo; WhatsApp: status no mensagem_ativa. Data fix só com controle em falha.",
}


def psql_json(service, sql, opcional=False):
    q = f"select coalesce(json_agg(t), '[]'::json) from ({sql}) t"
    r = subprocess.run(["psql", "-w", f"service={service}", "-X", "-q", "-At", "-v", "ON_ERROR_STOP=1", "-c", q], capture_output=True, text=True)
    if r.returncode != 0:
        msg = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "erro"
        if opcional:
            return None
        if "refused" in msg or "running on that host" in r.stderr:
            msg += "\n→ suba o proxy: sql_atendimento_prd (5443) / sql_exp_prd (5445) / sql_crm_prd (5444)"
        sys.exit(f"erro no psql ({service}): {msg}")
    return json.loads(r.stdout or "[]")


def bq_json(sql):
    r = subprocess.run(["bq", "query", "--project_id", "contabilizei-dataflow", "--use_legacy_sql=false", "--format=json", "--max_rows=1000", sql],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    out = r.stdout.strip()
    i = out.find("[")
    return json.loads(out[i:]) if i >= 0 else []


def comp_add(c, n):
    a, m = divmod(int(c) // 100 * 12 + int(c) % 100 - 1 + n, 12)
    return a * 100 + m + 1


def comps(desde, ate):
    c, out = desde, []
    while c <= ate:
        out.append(c)
        c = comp_add(c, 1)
    return out


def coletar(cnpj, desde, ate, usar_bq, usar_wpp):
    d = {"cnpj": cnpj, "desde": desde, "ate": ate, "avisos": []}
    grupos = psql_json(SVC_AGRUP, f"""
        select id, id_empresa, periodo_apuracao::int comp, status, regime_tributario, plano_pagamento_empresa plano,
               created_at, updated_at, path is not null tem_pdf
        from grupo_guia where cnpj = '{cnpj}' order by periodo_apuracao, id""")
    ids_emp = sorted({g["id_empresa"] for g in grupos})
    if not ids_emp:  # empresa sem nenhum grupo: tentar achar o id pela tabela de guias não dá (sem cnpj); pelo controle_notificacao também não
        d["avisos"].append("Nenhum grupo_guia para o CNPJ: a empresa nunca entrou no agrupamento. id_empresa desconhecido; guias do microsserviço não consultadas.")
    lista_emp = ",".join(str(i) for i in ids_emp) or "null"
    d["id_empresa"] = ids_emp
    d["grupos"] = grupos
    d["historico"] = psql_json(SVC_AGRUP, f"""
        select periodo_apuracao::int comp, status, created_at from historico_processamento_grupo_guia
        where id_empresa in ({lista_emp}) and periodo_apuracao between {desde} and {ate} order by created_at""")
    d["guias"] = psql_json(SVC_AGRUP, f"""
        select id, periodo_apuracao::int comp, imposto, status, id_guia, nullif(id_arquivo, '') is not null tem_arquivo,
               data_para_pagamento::date venc, created_at, updated_at
        from controle_guias where id_empresa in ({lista_emp}) and periodo_apuracao between {desde} and {ate}
        order by periodo_apuracao, imposto, created_at""")
    d["itens"] = psql_json(SVC_AGRUP, f"""
        select ig.grupo_guia_id, gg.periodo_apuracao::int comp, cg.id controle_guia_id, cg.imposto, cg.status, cg.id_guia,
               nullif(cg.id_arquivo, '') is not null tem_arquivo, cg.data_para_pagamento::date venc, cg.updated_at,
               ig.controle_parcela_id
        from item_grupo_guia ig join grupo_guia gg on gg.id = ig.grupo_guia_id
        left join controle_guias cg on cg.id = ig.controle_guia_id
        where gg.cnpj = '{cnpj}' and gg.periodo_apuracao between {desde} and {ate} order by comp, cg.imposto""")
    d["notificacoes"] = psql_json(SVC_AGRUP, f"""
        select cn.id, cn.grupo_guia_id, gg.periodo_apuracao::int comp, cn.tipo_notificacao canal, cn.status, cn.motivo,
               cn.external_id, cn.created_at
        from controle_notificacao cn left join grupo_guia gg on gg.id = cn.grupo_guia_id
        where cn.cnpj = '{cnpj}' order by cn.created_at""")
    # WhatsApp ativo (opcional)
    ext = [n["external_id"] for n in d["notificacoes"] if n["canal"] == "WHATSAPP" and n["external_id"]]
    d["wpp_ativo"] = {}
    if usar_wpp and ext:
        lst = ",".join("'" + re.sub(r"[^A-Za-z0-9_-]", "", e) + "'" for e in ext)
        r = psql_json(SVC_CRM, f"""
            select m.id_message_broker, m.template, coalesce(s.status::text, 'PROCESSANDO') status, left(s.erro, 160) erro
            from mensagem_ativa m left join lateral (select st.status, st.erro from mensagem_ativa_status st where st.id_mensagem = m.id
                 order by st.created_at desc, st.id desc limit 1) s on true
            where m.id_message_broker in ({lst})""", opcional=True)
        if r is None:
            d["avisos"].append("WhatsApp ativo não consultado (proxy sql_crm_prd 5444 fora do ar?): status do WhatsApp só pelo controle.")
        else:
            d["wpp_ativo"] = {a["id_message_broker"]: a for a in r}
    # Avulsas (experts-service)
    d["avulsas"] = psql_json(SVC_EXP, f"""
        select id, created_at, sent_date, is_sent, case when topic like '%whatsapp%' then 'WHATSAPP' else 'EMAIL' end canal,
               event_source_id, retry, left(coalesce(error::text, ''), 120) erro
        from task_scheduler where cnpj = '{cnpj}' and event_source_type = 'guia-imposto-notifier' order by created_at""")
    # Plano mês a mês
    d["planos"] = None
    if usar_bq:
        r = bq_json(f"""SELECT periodo, status, motivo_status, CAST(data_inativacao AS STRING) data_inativacao, plano, regime_tributario
            FROM `contabilizei-dataflow.saude_empresa.empresa` WHERE cnpj = '{cnpj}' AND periodo BETWEEN {desde} AND {comp_add(ate, 1)}
            ORDER BY periodo""")
        if r is None:
            d["avisos"].append("BigQuery não consultado (bq falhou): sem histórico de plano; a causa FORA_DO_AGRUPAMENTO_PLANO não pode ser confirmada.")
        else:
            d["planos"] = {int(p["periodo"]): p for p in r}
    return d


def classificar(d):
    por_comp = []
    guias_por_id = {}
    for g in d["guias"]:
        guias_por_id[str(g["id_guia"])] = g
    for c in comps(d["desde"], d["ate"]):
        dia15 = dt.date(comp_add(c, 1) // 100, comp_add(c, 1) % 100, 15)
        grupos = [g for g in d["grupos"] if g["comp"] == c]
        g = grupos[-1] if grupos else None
        hist = [h for h in d["historico"] if h["comp"] == c]
        guias = [x for x in d["guias"] if x["comp"] == c]
        itens = [i for i in d["itens"] if i["comp"] == c]
        notifs = [n for n in d["notificacoes"] if n["comp"] == c]
        snap = (d["planos"] or {}).get(int(comp_add(c, 1)))  # snapshot do mês do dia 15 (aproximação: o snapshot é mensal)
        snap_ant = (d["planos"] or {}).get(int(c))
        plano = (g or {}).get("plano") or (snap or {}).get("plano")
        plano_fonte = "grupo" if (g or {}).get("plano") else ("bq" if snap else None)
        regime = (g or {}).get("regime_tributario") or (snap or {}).get("regime_tributario")
        r = {"comp": c, "dia_15": dia15.isoformat(), "grupo_id": (g or {}).get("id"), "status_grupo": (g or {}).get("status"),
             "tem_pdf": (g or {}).get("tem_pdf"), "plano": plano, "plano_fonte": plano_fonte, "regime": regime,
             "plano_snapshot_mes_dia15": (snap or {}).get("plano"), "plano_snapshot_mes_comp": (snap_ant or {}).get("plano"),
             "status_empresa": (snap or {}).get("status"), "eventos_reprocessamento": max(len(hist) - 2, 0),
             "guias": [f"{x['imposto']} {x['status']} venc {x['venc']}{'' if x['tem_arquivo'] else ' (sem PDF)'}" for x in guias],
             "travando": [], "canais": {}, "causa": None, "detalhe": ""}
        for canal in ("EMAIL", "WHATSAPP"):
            ns = [n for n in notifs if n["canal"] == canal]
            if ns:
                n = ns[-1]
                a = d["wpp_ativo"].get(n["external_id"]) if canal == "WHATSAPP" else None
                r["canais"][canal] = n["status"] + (f" / {n['motivo']}" if n["motivo"] else "") + (f" (ativo: {a['status']})" if a else "")
        st = r["status_grupo"]
        if not g:
            if not hist and plano and plano not in EXPERTS and (dia15 < VIRADA_LOTES or plano in BP):
                r["causa"] = "FORA_DO_AGRUPAMENTO_PLANO"
                r["detalhe"] = f"plano {plano} no mês do dia 15 ({comp_add(c, 1)}); até 22/10/2026 só EXPERT_ESSENCIAL ia para o agrupamento"
                if plano in BP and regime != "LUCRO_PRESUMIDO":
                    r["detalhe"] += "; BP no Simples não tem notificação nem hoje"
            elif not guias and d["id_empresa"]:
                r["causa"] = "SEM_GUIA"
                r["detalhe"] = "sem grupo e sem guia no controle_guias"
            else:
                r["causa"] = "SEM_GATILHO"
                r["detalhe"] = f"{len(guias)} guia(s) no microsserviço, nenhum grupo nem histórico" + ("" if d["planos"] else " (plano não conferido: sem BigQuery)")
        elif st == "SUCESSO_AGRUPAMENTO":
            ok = [k for k, v in r["canais"].items() if v.startswith("SUCESSO")]
            falha = [k for k, v in r["canais"].items() if not v.startswith(("SUCESSO", "AGUARDANDO"))]
            if falha:
                r["causa"] = "FALHA_NOTIFICACAO"
            elif len(ok) == 2:
                r["causa"] = "ENVIADO"
            elif ok:
                r["causa"] = "ENVIADO_PARCIAL"
            elif (plano not in EXPERTS and plano not in BP) or (plano in BP and regime != "LUCRO_PRESUMIDO"):
                r["causa"] = "SEGMENTO_SEM_NOTIFICACAO"
            else:
                r["causa"] = "ELEGIVEL_NAO_NOTIFICADO"
        elif st == "AGRUPAMENTO_SEM_GUIA":
            r["causa"] = "SEM_GUIA"
            r["detalhe"] = f"{len(guias)} guia(s) da competência no microsserviço (TFE/ISS não agrupáveis contam aqui)"
        elif st in ("GUIAS_AGUARDANDO_GERACAO", "GUIAS_COM_ERRO"):
            trav = [i for i in itens if i["controle_guia_id"] and (not i["tem_arquivo"] or i["status"] != "REGISTRADO")]
            r["travando"] = [f"{i['imposto']} controle_guia {i['controle_guia_id']} id_guia {i['id_guia']} {i['status']} "
                             f"{'sem PDF' if not i['tem_arquivo'] else 'com PDF'} venc {i['venc']} atualizado {str(i['updated_at'])[:10]}" for i in trav]
            impostos = [i["imposto"] for i in itens if i["imposto"]]
            dup = sorted({x for x in impostos if impostos.count(x) > 1})
            if st == "GUIAS_COM_ERRO":
                r["causa"] = "GUIAS_COM_ERRO"
            elif r["tem_pdf"] or dup:
                r["causa"] = "GUIA_TRAVANDO"
                r["detalhe"] = (f"imposto duplicado no grupo: {', '.join(dup)}; " if dup else "") + "o grupo tem PDF, mas uma guia segue sem arquivo"
            else:
                r["causa"] = "AGUARDANDO_GERACAO"
        elif st and (st.startswith("ERRO_GUIA_ALTERADA") or st == "ERRO_NOVA_GUIA"):
            if any(v.startswith("SUCESSO") for v in r["canais"].values()):
                r["causa"] = "ENVIADO" if len(r["canais"]) == 2 else "ENVIADO_PARCIAL"
                r["detalhe"] = f"notificado antes; depois o grupo foi para {st} e as guias novas não foram renotificadas"
            else:
                r["causa"] = "ERRO_GUIA_ALTERADA"
        elif st in ("ERRO_SISTEMA", "ERRO_GERACAO_PDF_AGRUPAMENTO"):
            r["causa"] = "ERRO_PROCESSAMENTO"
        else:
            r["causa"] = "OUTRO"
        # avulsas cujas guias são desta competência
        ids = {str(x["id_guia"]) for x in guias}
        av = [a for a in d["avulsas"] if a["event_source_id"] in ids]
        r["avulsas"] = [f"{a['canal']} {str(a['created_at'])[:10]} guia {guias_por_id[a['event_source_id']]['imposto']} "
                        f"{'enviada' if a['is_sent'] else 'não enviada'}" for a in av]
        if r["causa"] not in ("ENVIADO", "ENVIADO_PARCIAL") and not av:
            if plano and plano not in EXPERTS:
                r["avulsa_motivo"] = "experts-service só notifica avulsa de plano Experts"
            elif guias:
                r["avulsa_motivo"] = ("guias agrupáveis da competência atual ficam seguradas pelo experts-service (dia < 15, ou dia ≥ 15 sem WhatsApp "
                                      "do grupo com SUCESSO): buraco de silêncio")
        por_comp.append(r)
    # avulsas que não são de guia do agrupamento (ISS, TFE etc.)
    ids_todas = {str(x["id_guia"]) for x in d["guias"]}
    outras = [a for a in d["avulsas"] if a["event_source_id"] not in ids_todas]
    return por_comp, outras


def resumo(d, por_comp, outras):
    L = [f"# Notificações de guias · CNPJ {d['cnpj']}", "",
         f"Competências {d['desde']} a {d['ate']} · id_empresa {', '.join(map(str, d['id_empresa'])) or '—'} · gerado {dt.datetime.now(TZ):%Y-%m-%d %H:%M}", ""]
    for a in d["avisos"]:
        L.append(f"> ⚠️ {a}")
    L += ["", "| Comp. | Envio (dia 15) | Plano | Grupo | E-mail | WhatsApp | Causa |", "| --- | --- | --- | --- | --- | --- | --- |"]
    for r in por_comp:
        pl = (r["plano"] or "—") + ("*" if r["plano_fonte"] == "bq" else "")
        L.append(f"| {r['comp']} | {r['dia_15'][:7]} | {pl} | {r['status_grupo'] or 'sem grupo'} | "
                 f"{r['canais'].get('EMAIL', '—')} | {r['canais'].get('WHATSAPP', '—')} | **{r['causa']}** |")
    L += ["", "\\* plano do snapshot mensal do BigQuery (fim do mês do dia 15, aproximado): o grupo não guardava o plano antes de 2026-10. Troca de plano no meio do mês pode aparecer só no mês seguinte.",
          "", "## Detalhe das competências não enviadas", ""]
    for r in por_comp:
        if r["causa"] == "ENVIADO" and not r["detalhe"]:
            continue
        L.append(f"### {r['comp']} (envio de {r['dia_15'][:7]}): {r['causa']}")
        L.append(f"- {CAUSAS[r['causa']]}" + (f" ({r['detalhe']})" if r["detalhe"] else ""))
        if r["plano_snapshot_mes_comp"] or r["plano_snapshot_mes_dia15"]:
            L.append(f"- Plano no BigQuery: {r['plano_snapshot_mes_comp'] or '—'} em {r['comp']}, {r['plano_snapshot_mes_dia15'] or '—'} em {comp_add(r['comp'], 1)}")
        if r["guias"]:
            L.append(f"- Guias no microsserviço: {'; '.join(r['guias'])}")
        for t in r["travando"]:
            L.append(f"- Travando o grupo {r['grupo_id']}: {t}")
        if r["eventos_reprocessamento"]:
            dias = sorted({str(h["created_at"])[:10] for h in d["historico"] if h["comp"] == r["comp"]})[1:]
            L.append(f"- Eventos de reprocessamento depois da montagem: {r['eventos_reprocessamento']} ({', '.join(dias)}), status final {r['status_grupo']}")
        L.append(f"- Avulsa: {'; '.join(r['avulsas']) if r['avulsas'] else 'nenhuma' + (' — ' + r['avulsa_motivo'] if r.get('avulsa_motivo') else '')}")
        if r["causa"] in ACAO:
            L.append(f"- O que fazer: {ACAO[r['causa']]}")
        L.append("")
    if outras:
        L += ["## Avulsas de guias fora do agrupamento (ISS, TFE etc.)", ""]
        L += [f"- {a['canal']} {str(a['created_at'])[:10]} guia {a['event_source_id']} {'enviada' if a['is_sent'] else 'não enviada'}" for a in outras]
        L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cnpj")
    ap.add_argument("--desde", type=int)
    ap.add_argument("--ate", type=int)
    ap.add_argument("--saida")
    ap.add_argument("--sem-bq", action="store_true")
    ap.add_argument("--sem-wpp", action="store_true")
    a = ap.parse_args()
    cnpj = re.sub(r"[^0-9A-Za-z]", "", a.cnpj).upper()
    if len(cnpj) != 14:
        sys.exit("CNPJ inválido (14 caracteres, numérico ou alfanumérico)")
    hoje = dt.datetime.now(TZ).date()
    ate = a.ate or comp_add(hoje.year * 100 + hoje.month, -1)
    desde = a.desde or comp_add(ate, -11)
    d = coletar(cnpj, desde, ate, not a.sem_bq, not a.sem_wpp)
    por_comp, outras = classificar(d)
    saida = a.saida or os.path.expanduser(f"~/Downloads/investigacoes/notificacoes-guias/{cnpj}/{dt.datetime.now(TZ):%Y-%m-%d_%H%M}")
    os.makedirs(saida, exist_ok=True)
    md = resumo(d, por_comp, outras)
    with open(os.path.join(saida, "resumo.md"), "w") as f:
        f.write(md + "\n")
    with open(os.path.join(saida, "dados.json"), "w") as f:
        json.dump({"coleta": d, "competencias": por_comp, "avulsas_fora_agrupamento": outras}, f, ensure_ascii=False, indent=1, default=str)
    print(md)
    print(f"\n→ {saida}")


if __name__ == "__main__":
    main()
