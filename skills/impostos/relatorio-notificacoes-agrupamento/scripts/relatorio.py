#!/usr/bin/env python3
"""
Relatório das notificações do agrupamento de guias (dia 15) em PRODUÇÃO, somente leitura.

Cruza o banco do agrupamento (grupo_guia + controle_notificacao) com o WhatsApp ativo do atendimento-zendesk (mensagem_ativa + mensagem_ativa_status, ligados por controle_notificacao.external_id = mensagem_ativa.id_message_broker) e mostra, por segmento (Experts SN, Experts LP, BP LP) e canal (e-mail, WhatsApp): quantos deveriam receber, quantos receberam, o que está em trânsito, o que falta enviar, as falhas e a próxima rodada das crons.

Uso:
  relatorio.py gerar [--competencia AAAAMM | --data AAAA-MM-DD] [--publico exp,bp] [--regime simples,lp] [--canal email,wpp]
                     [--plano EXPERT_PRO,...] [--saida DIR] [--pdf] [--autor A]
      coleta, grava dados.json, resumo.md, pendentes.csv, problemas.csv e relatorio.html em DIR (e relatorio.pdf com --pdf)
  relatorio.py resumo --dados DIR/dados.json
      reimprime o resumo de texto de uma coleta

Filtros (opcionais, combináveis, listas separadas por vírgula): --publico exp|bp, --regime simples|lp, --canal email|wpp e --plano
(BASICO, AVANCADO, PREMIUM, MULTIBENEFICIOS, EXPERT_ESSENCIAL, EXPERT_PRO). BP Simples não tem notificação. --data é o dia da rodada
(ex: 2026-10-15) e vira a competência do mês anterior (202609). Competência passada mostra o estado atual dela, não uma foto daquela data.

Padrões: competência = mês anterior ao de hoje (America/Sao_Paulo); DIR = ~/Downloads/relatorios/notificacoes-agrupamento/<competencia>/<AAAA-MM-DD_HHMM>.
Precisa dos proxies de prd de pé: sql_atendimento_prd (5443) e sql_crm_prd (5444). Os serviços abrem em modo só leitura; o script só faz SELECT.
Nunca grava e-mail nem telefone de cliente nas saídas: só id do agrupamento, CNPJ, segmento, plano e status.
"""
import argparse
import csv
import datetime as dt
import html
import json
import os
import shutil
import subprocess
import sys
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Sao_Paulo")
SVC_AGRUP = "prd_atendimento_canais_ms_agrupamento_guias"
SVC_CRM = "prd_crm_atendimento_zendesk"
AUTOR_PADRAO = "microsservico-agrupamento-guias"  # quando o agrupamento-guias-service assumir: "agrupamento-guias-service"

SEGMENTOS = {
    "EXP_SN": "Experts Simples",
    "EXP_LP": "Experts Lucro Presumido",
    "BP_LP": "BP Lucro Presumido",
}
CANAIS = {"EMAIL": "E-mail", "WHATSAPP": "WhatsApp"}
SEGMENTOS_TODOS, CANAIS_TODOS = dict(SEGMENTOS), dict(CANAIS)  # rótulos, mesmo com filtro (o resumo também lê dados.json antigos)
PLANOS = {"exp": ["EXPERT_ESSENCIAL", "EXPERT_PRO"], "bp": ["BASICO", "AVANCADO", "PREMIUM", "MULTIBENEFICIOS"]}
SEG_PARTES = {"EXP_SN": ("exp", "simples"), "EXP_LP": ("exp", "lp"), "BP_LP": ("bp", "lp")}
CANAL_ARG = {"email": "EMAIL", "wpp": "WHATSAPP", "whatsapp": "WHATSAPP"}
FILTRO_SQL = ""  # condição extra sobre o grupo (segmento e plano), montada em aplicar_filtros

# Segmento do grupo, igual às queries buscarGruposGuiaElegiveisNotificacao* do GrupoGuiaRepository.
SEG_SQL = """
CASE
  WHEN g.plano_pagamento_empresa IN ('EXPERT_ESSENCIAL','EXPERT_PRO') AND g.regime_tributario = 'LUCRO_PRESUMIDO' THEN 'EXP_LP'
  WHEN g.plano_pagamento_empresa IN ('EXPERT_ESSENCIAL','EXPERT_PRO') THEN 'EXP_SN'
  WHEN g.plano_pagamento_empresa IN ('BASICO','AVANCADO','PREMIUM','MULTIBENEFICIOS') AND g.regime_tributario = 'LUCRO_PRESUMIDO' THEN 'BP_LP'
  WHEN g.plano_pagamento_empresa IN ('BASICO','AVANCADO','PREMIUM','MULTIBENEFICIOS') THEN 'BP_SN'
  ELSE 'SEM_PLANO'
END
"""
# Elegível ao canal: só SUCESSO_AGRUPAMENTO; WhatsApp BP LP deixa o BASICO de fora.
ELEG_SQL = {
    "EMAIL": "g.status = 'SUCESSO_AGRUPAMENTO' AND seg IN ('EXP_SN','EXP_LP','BP_LP')",
    "WHATSAPP": "g.status = 'SUCESSO_AGRUPAMENTO' AND seg IN ('EXP_SN','EXP_LP','BP_LP') AND NOT (seg = 'BP_LP' AND g.plano_pagamento_empresa = 'BASICO')",
}

# Crons de prd (Cloud Scheduler, America/Sao_Paulo), dias 15 a 19. Conferir em ~/ctbz-vault/obsidian/infra/schedulers.md.
CRONS = {
    ("EXP_SN", "EMAIL"): [3, 12], ("EXP_LP", "EMAIL"): [5, 14], ("BP_LP", "EMAIL"): [4, 13],
    ("EXP_SN", "WHATSAPP"): [9, 15], ("EXP_LP", "WHATSAPP"): [9, 15], ("BP_LP", "WHATSAPP"): [10],
}
DIAS_CRON = range(15, 20)

STATUS_AGRUP = {
    "SUCESSO_AGRUPAMENTO": "Agrupado: entra na notificação",
    "SUCESSO_AGRUPAMENTO_SEM_ARQUIVO_GUIA_AVULSA": "Agrupado sem arquivo de guia avulsa: as crons não pegam",
    "AGRUPAMENTO_SEM_GUIA": "Sem guia para agrupar: nada a notificar",
    "GUIAS_AGUARDANDO_GERACAO": "Guias ainda não geradas: nunca é reprocessado",
    "GUIAS_COM_ERRO": "Guia com erro",
    "ERRO_GERACAO_PDF_AGRUPAMENTO": "Erro ao gerar o PDF agrupado",
    "ERRO_NOVA_GUIA": "Nova guia depois do agrupamento",
    "ERRO_GUIA_ALTERADA": "Guia alterada depois do agrupamento",
    "ERRO_GUIA_ALTERADA_RECORRENTE": "Guia alterada de forma recorrente",
    "ERRO_GUIA_ARQUIVO_ALTERADO": "Arquivo da guia alterado",
}
ATIVO_ORDEM = ["PROCESSANDO", "SOLICITADA", "ENVIADA", "ENTREGUE", "RESPONDIDA", "BLOQUEADA_OPTOUT", "ERRO", "SEM_ATIVO"]
ATIVO_ROTULO = {
    "PROCESSANDO": "Na fila (aguardando horário comercial)", "SOLICITADA": "Solicitada à Meta", "ENVIADA": "Enviada",
    "ENTREGUE": "Entregue", "RESPONDIDA": "Respondida", "BLOQUEADA_OPTOUT": "Opt-out", "ERRO": "Erro", "SEM_ATIVO": "Sem registro no ativo",
}


def psql_json(service, sql):
    q = f"select coalesce(json_agg(t), '[]'::json) from ({sql}) t"
    r = subprocess.run(["psql", "-w", f"service={service}", "-X", "-q", "-At", "-v", "ON_ERROR_STOP=1", "-c", q], capture_output=True, text=True)
    if r.returncode != 0:
        msg = r.stderr.strip()
        if "Connection refused" in msg:
            msg += f"\n→ proxy de pé? (sql_atendimento_prd para {SVC_AGRUP}, sql_crm_prd para {SVC_CRM})"
        sys.exit(f"erro no psql ({service}): {msg}")
    return json.loads(r.stdout or "[]")


def competencia_padrao(agora):
    primeiro = agora.date().replace(day=1)
    anterior = primeiro - dt.timedelta(days=1)
    return anterior.year * 100 + anterior.month


def comp_anterior(c):
    a, m = divmod(c, 100)
    return (a - 1) * 100 + 12 if m == 1 else a * 100 + m - 1


def dia_15(c):
    a, m = divmod(c, 100)
    a, m = (a + 1, 1) if m == 12 else (a, m + 1)
    return dt.datetime(a, m, 15, tzinfo=TZ)


def proxima_cron(seg, canal, c, agora):
    d15 = dia_15(c)
    for dia in DIAS_CRON:
        for h in CRONS.get((seg, canal), []):
            t = d15.replace(day=dia, hour=h)
            if t > agora:
                return t
    return None


def coletar(c, autor):
    base = f"select * from (select g.*, {SEG_SQL} as seg from grupo_guia g where g.periodo_apuracao = {{c}}) g where true {FILTRO_SQL}"
    ultimo = """select distinct on (cn.grupo_guia_id, cn.tipo_notificacao) cn.grupo_guia_id, cn.tipo_notificacao, cn.status, cn.motivo,
                       cn.external_id, cn.diagnostico_aumento_imposto_id, cn.created_at
                from controle_notificacao cn join grupo_guia g on g.id = cn.grupo_guia_id
                where g.periodo_apuracao = {c}
                order by cn.grupo_guia_id, cn.tipo_notificacao, cn.created_at desc, cn.id desc"""
    out = {}
    out["universo"] = psql_json(SVC_AGRUP, f"""
        with g as ({base.format(c=c)})
        select seg, coalesce(plano_pagamento_empresa,'(nulo)') plano, coalesce(regime_tributario,'(nulo)') regime, status, count(*)::int n
        from g group by 1,2,3,4""")
    out["universo_anterior"] = psql_json(SVC_AGRUP, f"""
        with g as ({base.format(c=comp_anterior(c))}) select seg, status, count(*)::int n from g group by 1,2""")
    out["matriz"] = []
    out["pendentes"] = []
    for canal, eleg in ((k, v) for k, v in ELEG_SQL.items() if k in CANAIS):
        out["matriz"] += [dict(r, canal=canal) for r in psql_json(SVC_AGRUP, f"""
            with g as ({base.format(c=c)}), u as ({ultimo.format(c=c)})
            select g.seg, ({eleg}) elegivel, coalesce(u.status,'SEM_NOTIFICACAO') status, u.motivo,
                   (u.diagnostico_aumento_imposto_id is not null) diagnostico, count(*)::int n
            from g left join u on u.grupo_guia_id = g.id and u.tipo_notificacao = '{canal}'
            group by 1,2,3,4,5""")]
        out["pendentes"] += [dict(r, canal=canal) for r in psql_json(SVC_AGRUP, f"""
            with g as ({base.format(c=c)})
            select g.id, g.cnpj, g.seg, g.plano_pagamento_empresa plano, g.updated_at
            from g where {eleg} and not exists (select 1 from controle_notificacao cn where cn.grupo_guia_id = g.id and cn.tipo_notificacao = '{canal}')
            order by g.updated_at""")]
    out["problemas"] = psql_json(SVC_AGRUP, f"""
        with g as ({base.format(c=c)}), u as ({ultimo.format(c=c)})
        select g.id, g.cnpj, g.seg, g.plano_pagamento_empresa plano, u.tipo_notificacao canal, u.status, u.motivo, u.created_at
        from g join u on u.grupo_guia_id = g.id
        where u.status in ('FALHA','DADOS_INCOMPLETO') and u.tipo_notificacao in ({",".join(f"'{k}'" for k in CANAIS)}) order by u.tipo_notificacao, u.motivo, g.id""")
    out["timeline"] = psql_json(SVC_AGRUP, f"""
        select to_char(date_trunc('hour', (cn.created_at at time zone 'UTC') at time zone 'America/Sao_Paulo'), 'YYYY-MM-DD"T"HH24') hora,
               cn.tipo_notificacao canal, count(*)::int n
        from controle_notificacao cn join ({base.format(c=c)}) g on g.id = cn.grupo_guia_id
        where cn.tipo_notificacao in ({",".join(f"'{k}'" for k in CANAIS)}) group by 1,2 order by 1""")
    out["controle_anterior"] = psql_json(SVC_AGRUP, f"""
        select cn.tipo_notificacao canal, cn.status, count(*)::int n
        from controle_notificacao cn join ({base.format(c=comp_anterior(c))}) g on g.id = cn.grupo_guia_id
        where cn.tipo_notificacao in ({",".join(f"'{k}'" for k in CANAIS)}) group by 1,2""")
    if "WHATSAPP" not in CANAIS:
        out.update(whatsapp_ativo=[], ativos_total=0, ativos_sem_controle=0, retentativas_max=0)
        return out
    wpp = psql_json(SVC_AGRUP, f"""
        with g as ({base.format(c=c)}), u as ({ultimo.format(c=c)})
        select g.id, g.seg, u.status, u.motivo, u.external_id, u.created_at, ({ELEG_SQL['WHATSAPP']}) elegivel
        from g left join u on u.grupo_guia_id = g.id and u.tipo_notificacao = 'WHATSAPP'
        where ({ELEG_SQL['WHATSAPP']}) or u.grupo_guia_id is not null""")
    inicios = [w["created_at"] for w in wpp if w["created_at"]]
    desde = min(inicios) if inicios else (dia_15(c) - dt.timedelta(days=2)).isoformat()
    desde = f"{str(desde)[:19]}+00" if inicios else desde  # controle_notificacao grava UTC sem fuso
    ativos = psql_json(SVC_CRM, f"""
        with m as (select id, id_message_broker, template, retentativas, criado_em from mensagem_ativa
                   where autor = '{autor}' and criado_em >= '{desde}'),
             s as (select distinct on (st.id_mensagem) st.id_mensagem, st.status::text status, st.erro, st.created_at
                   from mensagem_ativa_status st join m on m.id = st.id_mensagem order by st.id_mensagem, st.created_at desc, st.id desc)
        select m.id_message_broker, m.template, m.retentativas, coalesce(s.status,'PROCESSANDO') status, left(s.erro, 160) erro, s.created_at status_em
        from m left join s on s.id_mensagem = m.id""")
    por_broker = {a["id_message_broker"]: a for a in ativos}
    cruz = {}
    # O cartão do WhatsApp sai inteiro desta consulta (uma foto só): os callbacks mudam o controle enquanto o ativo envia.
    # Cada elegível cai numa categoria só: sem notificação, sem contato, opt-out/falha antes do ativo ou o status do ativo.
    for w in wpp:
        if not w["elegivel"]:
            continue
        a = por_broker.get(w["external_id"]) if w["external_id"] else None
        if w["status"] is None:
            st = "SEM_NOTIFICACAO"
        elif w["status"] == "DADOS_INCOMPLETO" or w["motivo"] == "DADOS_INCOMPLETO":
            st = "INCOMPLETO"
        elif w["external_id"]:
            st = a["status"] if a else "SEM_ATIVO"
        else:
            st = "BLOQUEADA_OPTOUT" if w["status"] == "BLOQUEADA_OPTOUT" else "FALHA_PUBLICACAO"
        k = (w["seg"], w["status"], st, a["template"] if a else None, (a or {}).get("erro"))
        cruz[k] = cruz.get(k, 0) + 1
    out["whatsapp_ativo"] = [dict(seg=k[0], controle=k[1], ativo=k[2], template=k[3], erro=k[4], n=n) for k, n in cruz.items()]
    out["ativos_total"] = len(ativos)
    # com filtro de segmento/plano os ativos dos outros segmentos apareceriam como "sem controle"
    out["ativos_sem_controle"] = 0 if FILTRO_SQL else len(set(por_broker) - {w["external_id"] for w in wpp if w["external_id"]})
    out["retentativas_max"] = max((a["retentativas"] or 0 for a in ativos), default=0)
    return out


def analisar(d, c, agora):
    cel = {}
    for seg in SEGMENTOS:
        for canal in CANAIS:
            rows = [r for r in d["matriz"] if r["seg"] == seg and r["canal"] == canal]
            el = [r for r in rows if r["elegivel"]]
            cnt = lambda st, rs=el: sum(r["n"] for r in rs if r["status"] == st)
            inc_falha = sum(r["n"] for r in el if r["status"] == "FALHA" and r["motivo"] == "DADOS_INCOMPLETO")
            x = dict(seg=seg, canal=canal, elegiveis=sum(r["n"] for r in el), sem_notificacao=cnt("SEM_NOTIFICACAO"),
                     sucesso=cnt("SUCESSO"), aguardando=cnt("AGUARDANDO_NOTIFICACAO"), falha=cnt("FALHA") - inc_falha,
                     incompleto=cnt("DADOS_INCOMPLETO") + inc_falha, optout=cnt("BLOQUEADA_OPTOUT"),
                     diagnostico=sum(r["n"] for r in el if r["diagnostico"]),
                     fora_elegiveis=sum(r["n"] for r in rows if not r["elegivel"] and r["status"] != "SEM_NOTIFICACAO"))
            if canal == "WHATSAPP":
                at = [w for w in d["whatsapp_ativo"] if w["seg"] == seg]
                b = lambda st: sum(w["n"] for w in at if w["ativo"] == st)
                x.update(elegiveis=sum(w["n"] for w in at), sem_notificacao=b("SEM_NOTIFICACAO"), incompleto=b("INCOMPLETO"),
                         falha=b("FALHA_PUBLICACAO"), optout=b("BLOQUEADA_OPTOUT"))
                x["ativo"] = {st: b(st) for st in ATIVO_ORDEM}
                x["templates"] = {}
                for w in at:
                    if w["template"]:
                        x["templates"][w["template"]] = x["templates"].get(w["template"], 0) + w["n"]
                transito = x["ativo"]["PROCESSANDO"] + x["ativo"]["SOLICITADA"]
                x["entregue"] = x["ativo"]["ENTREGUE"] + x["ativo"]["RESPONDIDA"]
                x["erro_ativo"] = x["ativo"]["ERRO"]
                x["sem_ativo"] = x["ativo"]["SEM_ATIVO"]
            else:
                transito = x["aguardando"]
                x["erro_ativo"] = x["sem_ativo"] = 0
            x["transito"] = transito
            prox = proxima_cron(seg, canal, c, agora)
            x["proxima_cron"] = prox.isoformat() if prox else None
            base = max(x["elegiveis"], 1)
            falhas = x["falha"] + x["erro_ativo"]
            if (x["sem_notificacao"] and not prox) or falhas / base > 0.02 or x["sem_ativo"] / base > 0.005:
                x["veredito"] = "critico"
            elif x["sem_notificacao"] or transito or falhas or x["incompleto"]:
                x["veredito"] = "andamento" if (x["sem_notificacao"] or transito) else "atencao"
            else:
                x["veredito"] = "ok"
            cel[f"{seg}.{canal}"] = x
    return cel


def fmt(n):
    return f"{n:,}".replace(",", ".")


def pct(a, b):
    return f"{(100 * a / b):.1f}%".replace(".", ",") if b else "–"


VEREDITO = {"ok": ("Concluído", "ok"), "andamento": ("Em andamento", "info"), "atencao": ("Concluído com perdas", "warn"), "critico": ("Precisa de ação", "crit")}


def texto_resumo(rel):
    c, cel = rel["competencia"], rel["celulas"]
    linhas = [f"*Notificações do agrupamento de guias · competência {c % 100:02d}/{c // 100}* (foto de {rel['gerado_em_fmt']})" + (f" · filtro: {rel['filtros']}" if rel.get("filtros") else ""), ""]
    for k, x in cel.items():
        seg, canal = k.split(".")
        nome, cn = SEGMENTOS_TODOS[seg], CANAIS_TODOS[canal]
        ok = x["entregue"] if canal == "WHATSAPP" else x["sucesso"]
        extra = f", {fmt(x['transito'])} em trânsito" if x["transito"] else ""
        pend = f", {fmt(x['sem_notificacao'])} ainda não enviados" if x["sem_notificacao"] else ""
        fal = x["falha"] + x["erro_ativo"]
        linhas.append(f"- {nome} · {cn}: {VEREDITO[x['veredito']][0]} — {fmt(ok)}/{fmt(x['elegiveis'])} {'entregues' if canal == 'WHATSAPP' else 'enviados'} ({pct(ok, x['elegiveis'])}){extra}{pend}, {fmt(fal)} falhas, {fmt(x['incompleto'])} sem contato")
    linhas += ["", f"Não notificáveis (erro ou sem guia no agrupamento): {fmt(rel['nao_notificaveis'])} grupos."]
    return "\n".join(linhas)


def gerar_html(rel):
    c, cel, d = rel["competencia"], rel["celulas"], rel["dados"]
    e = html.escape
    comp = f"{c % 100:02d}/{c // 100}"

    def pill(v):
        t, k = VEREDITO[v]
        return f'<span class="pill {k}">{t}</span>'

    def barra(partes, total):
        if not total:
            return '<div class="bar"></div>'
        segs = "".join(f'<span class="{k}" style="width:{100 * n / total:.2f}%" title="{e(r)}: {fmt(n)}"></span>' for k, n, r in partes if n)
        return f'<div class="bar">{segs}</div>'

    # Cartões por segmento x canal
    cards = []
    for seg, nome in SEGMENTOS.items():
        for canal, cn in CANAIS.items():
            x = cel[f"{seg}.{canal}"]
            el = x["elegiveis"]
            if canal == "WHATSAPP":
                a = x["ativo"]
                partes = [("s-ok", a["ENTREGUE"] + a["RESPONDIDA"], "Entregue/respondida"), ("s-ok2", a["ENVIADA"], "Enviada"),
                          ("s-info", a["PROCESSANDO"] + a["SOLICITADA"], "Em trânsito"), ("s-pend", x["sem_notificacao"], "Ainda não enviada"),
                          ("s-warn", x["incompleto"] + x["optout"], "Sem contato/opt-out"), ("s-crit", a["ERRO"] + x["sem_ativo"] + x["falha"], "Erro")]
                kv = [("Entregues", x["entregue"]), ("Respondidas", a["RESPONDIDA"]), ("Em trânsito", x["transito"]), ("Ainda não enviadas", x["sem_notificacao"]),
                      ("Erro no ativo", a["ERRO"]), ("Falha antes do ativo", x["falha"]), ("Sem contato", x["incompleto"]), ("Opt-out", x["optout"]), ("Sem registro no ativo", x["sem_ativo"])]
                ok = x["entregue"]
            else:
                partes = [("s-ok", x["sucesso"], "Enviado"), ("s-info", x["aguardando"], "Aguardando callback"), ("s-pend", x["sem_notificacao"], "Ainda não enviado"),
                          ("s-warn", x["incompleto"] + x["optout"], "Sem contato/opt-out"), ("s-crit", x["falha"], "Falha")]
                kv = [("Enviados", x["sucesso"]), ("Aguardando callback", x["aguardando"]), ("Ainda não enviados", x["sem_notificacao"]),
                      ("Falhas", x["falha"]), ("Sem contato", x["incompleto"]), ("Opt-out", x["optout"])]
                ok = x["sucesso"]
            if x["diagnostico"]:
                kv.append(("Com diagnóstico", x["diagnostico"]))
            prox = x["proxima_cron"]
            prox_txt = dt.datetime.fromisoformat(prox).strftime("%d/%m às %Hh") if prox else "sem rodadas restantes"
            kvh = "".join(f'<div><dt>{k}</dt><dd>{fmt(v)}</dd></div>' for k, v in kv if v or k in ("Enviados", "Entregues"))
            cards.append(f"""
<article class="card v-{VEREDITO[x['veredito']][1]}">
  <header><div><p class="eyebrow">{cn}</p><h3>{nome}</h3></div>{pill(x['veredito'])}</header>
  <p class="big"><strong>{pct(ok, el)}</strong> <span>{fmt(ok)} de {fmt(el)} {'entregues' if canal == 'WHATSAPP' else 'enviados'}</span></p>
  {barra(partes, el)}
  <dl>{kvh}</dl>
  <p class="foot">Próxima rodada da cron: {prox_txt}</p>
</article>""")

    # Universo
    uni = {}
    for r in d["universo"]:
        uni[r["status"]] = uni.get(r["status"], 0) + r["n"]
    ant = {}
    for r in d["universo_anterior"]:
        ant[r["status"]] = ant.get(r["status"], 0) + r["n"]
    tot = sum(uni.values())
    uni_rows = "".join(
        f'<tr class="{"hl" if s == "SUCESSO_AGRUPAMENTO" else ""}"><td><code>{e(s)}</code><br><small>{e(STATUS_AGRUP.get(s, ""))}</small></td><td class="n">{fmt(n)}</td><td class="n">{pct(n, tot)}</td><td class="n muted">{fmt(ant.get(s, 0))}</td></tr>'
        for s, n in sorted(uni.items(), key=lambda kv: -kv[1]))
    planos = {}
    for r in d["universo"]:
        k = (r["seg"], r["plano"], r["regime"])
        planos[k] = planos.get(k, 0) + r["n"]
    plano_rows = "".join(f'<tr><td>{e(SEGMENTOS.get(k[0], k[0]))}</td><td><code>{e(k[1])}</code></td><td><code>{e(k[2])}</code></td><td class="n">{fmt(n)}</td></tr>'
                         for k, n in sorted(planos.items(), key=lambda kv: -kv[1]))

    # Timeline (barras por hora)
    tl = {}
    for r in d["timeline"]:
        tl.setdefault(r["hora"], {})[r["canal"]] = r["n"]
    horas = sorted(h for h in tl if h >= dia_15(c).strftime("%Y-%m-%dT00"))
    mx = max((sum(v.values()) for h, v in tl.items() if h in horas), default=1)
    W, H, bw = 720, 160, max(4, min(24, 680 // max(len(horas), 1)))
    bars = []
    for i, h in enumerate(horas):
        x0 = 30 + i * (bw + 4)
        y = H - 20
        for canal, cls in (("EMAIL", "c-email"), ("WHATSAPP", "c-wpp")):
            n = tl[h].get(canal, 0)
            hh = (H - 40) * n / mx
            if n:
                bars.append(f'<rect class="{cls}" x="{x0}" y="{y - hh:.1f}" width="{bw}" height="{hh:.1f}"><title>{h[8:10]}/{h[5:7]} {h[11:]}h · {CANAIS_TODOS[canal]}: {fmt(n)}</title></rect>')
            y -= hh
        bars.append(f'<text x="{x0 + bw / 2}" y="{H - 5}" text-anchor="middle">{h[8:10]}·{h[11:]}h</text>')
    svg_w = max(W, 40 + len(horas) * (bw + 4))
    timeline = f'<svg viewBox="0 0 {svg_w} {H}" width="{svg_w}" height="{H}" role="img" aria-label="Notificações criadas por hora"><line class="axis" x1="26" y1="{H - 20}" x2="{svg_w - 4}" y2="{H - 20}"/><text x="2" y="24">{fmt(mx)}</text>{"".join(bars)}</svg>'

    # Erros do WhatsApp ativo
    errs = {}
    for w in d["whatsapp_ativo"]:
        if w["ativo"] == "ERRO":
            errs[w["erro"] or "(sem mensagem)"] = errs.get(w["erro"] or "(sem mensagem)", 0) + w["n"]
    err_rows = "".join(f'<tr><td>{e(k)}</td><td class="n">{fmt(n)}</td></tr>' for k, n in sorted(errs.items(), key=lambda kv: -kv[1])[:12]) or '<tr><td colspan="2" class="muted">Nenhum erro registrado no ativo.</td></tr>'
    tpls = {}
    for w in d["whatsapp_ativo"]:
        if w["template"]:
            tpls[(w["template"], w["ativo"])] = tpls.get((w["template"], w["ativo"]), 0) + w["n"]
    tpl_names = sorted({k[0] for k in tpls})
    tpl_rows = "".join("<tr><td><code>" + e(t) + "</code></td>" + "".join(f'<td class="n">{fmt(tpls.get((t, s), 0))}</td>' for s in ATIVO_ORDEM[:-1]) + "</tr>" for t in tpl_names)
    tpl_head = "".join(f"<th>{e(ATIVO_ROTULO[s])}</th>" for s in ATIVO_ORDEM[:-1])

    # Problemas e pendentes (amostra; lista completa nos CSVs)
    prob = {}
    for p in d["problemas"]:
        k = (CANAIS_TODOS[p["canal"]], p["status"], p["motivo"] or "")
        prob[k] = prob.get(k, 0) + 1
    prob_rows = "".join(f'<tr><td>{e(k[0])}</td><td><code>{e(k[1])}</code></td><td><code>{e(k[2])}</code></td><td class="n">{fmt(n)}</td></tr>' for k, n in sorted(prob.items(), key=lambda kv: -kv[1])) or '<tr><td colspan="4" class="muted">Nenhuma falha ou contato incompleto.</td></tr>'
    pend = d["pendentes"]
    pend_rows = "".join(f'<tr><td>{p["id"]}</td><td>{e(p["cnpj"])}</td><td>{e(SEGMENTOS.get(p["seg"], p["seg"]))}</td><td>{e(CANAIS_TODOS[p["canal"]])}</td><td><code>{e(p["plano"] or "")}</code></td></tr>' for p in pend[:40]) or '<tr><td colspan="5" class="muted">Nenhum grupo elegível sem notificação.</td></tr>'
    pend_more = f'<p class="muted">Mostrando 40 de {fmt(len(pend))}. A lista completa está no pendentes.csv da coleta.</p>' if len(pend) > 40 else ""

    alertas = "".join(f"<li>{e(a)}</li>" for a in rel["alertas"]) or "<li>Nenhum alerta.</li>"
    ca = {}
    for r in d["controle_anterior"]:
        ca.setdefault(r["canal"], {})[r["status"]] = r["n"]
    ant_txt = " · ".join(f"{CANAIS_TODOS[k]}: " + ", ".join(f"{s.lower()} {fmt(n)}" for s, n in sorted(v.items(), key=lambda kv: -kv[1])) for k, v in ca.items())

    return f"""<title>Agrupamento {comp} · Notificações</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Sans+Condensed:wght@600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: painel de leitura rápida — veredito no topo, grade segmento × canal, detalhe abaixo. */
:root {{
  --bg:#f5f7f6; --surface:#ffffff; --fg:#17201d; --muted:#5d6b66; --line:#d9e0dd; --accent:#0f6b5c;
  --ok:#1f8a4c; --ok2:#7cc49a; --info:#2f6fb5; --pend:#b9c3bf; --warn:#c98a12; --crit:#c2402f;
  --email:#0f6b5c; --wpp:#6aa892;
  --display:"IBM Plex Sans Condensed","Arial Narrow",system-ui,sans-serif; --body:"IBM Plex Sans",system-ui,sans-serif; --mono:"IBM Plex Mono",ui-monospace,monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg:#0f1513; --surface:#18201d; --fg:#e4ebe8; --muted:#94a39d; --line:#2b3633; --accent:#5cc2ad;
  --ok:#4cc27c; --ok2:#2e7a52; --info:#6ea6e6; --pend:#4a5551; --warn:#e3a93a; --crit:#ec6a57; --email:#5cc2ad; --wpp:#2f7d69; color-scheme:dark }} }}
:root[data-theme="dark"] {{
  --bg:#0f1513; --surface:#18201d; --fg:#e4ebe8; --muted:#94a39d; --line:#2b3633; --accent:#5cc2ad;
  --ok:#4cc27c; --ok2:#2e7a52; --info:#6ea6e6; --pend:#4a5551; --warn:#e3a93a; --crit:#ec6a57; --email:#5cc2ad; --wpp:#2f7d69; color-scheme:dark }}
body {{ background:var(--bg); color:var(--fg); font-family:var(--body); font-size:15px; line-height:1.5 }}
main {{ max-width:1180px; margin:0 auto; padding-block:28px 56px; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); display:grid; gap:32px }}
h1,h2,h3 {{ font-family:var(--display); text-wrap:balance; margin:0 }}
h1 {{ font-size:2rem; letter-spacing:-.01em }} h2 {{ font-size:1.3rem }} h3 {{ font-size:1.1rem }}
.eyebrow {{ margin:0; font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); font-weight:600 }}
.muted {{ color:var(--muted) }} .filtro {{ color:var(--accent) !important; font-weight:600 }} code {{ font-family:var(--mono); font-size:.82em }}
.head {{ display:grid; gap:8px }} .head p {{ margin:0; color:var(--muted); max-width:70ch }}
.alertas {{ background:var(--surface); border:1px solid var(--line); border-left:4px solid var(--warn); padding:12px 16px; border-radius:6px }}
.alertas ul {{ margin:6px 0 0; padding-left:20px }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:16px }}
.card {{ background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:16px; display:grid; gap:12px; border-top:4px solid var(--pend) }}
.card.v-ok {{ border-top-color:var(--ok) }} .card.v-info {{ border-top-color:var(--info) }} .card.v-warn {{ border-top-color:var(--warn) }} .card.v-crit {{ border-top-color:var(--crit) }}
.card header {{ display:flex; justify-content:space-between; align-items:flex-start; gap:8px }}
.pill {{ font-size:.75rem; font-weight:600; padding:2px 10px; border-radius:999px; white-space:nowrap; border:1px solid currentColor }}
.pill.ok {{ color:var(--ok) }} .pill.info {{ color:var(--info) }} .pill.warn {{ color:var(--warn) }} .pill.crit {{ color:var(--crit) }}
.big {{ margin:0; display:flex; align-items:baseline; gap:10px; flex-wrap:wrap }} .big strong {{ font-family:var(--display); font-size:2.2rem; line-height:1 }} .big span {{ color:var(--muted) }}
.bar {{ display:flex; height:10px; border-radius:5px; overflow:hidden; background:var(--line) }} .bar span {{ display:block; height:100% }}
.s-ok {{ background:var(--ok) }} .s-ok2 {{ background:var(--ok2) }} .s-info {{ background:var(--info) }} .s-pend {{ background:var(--pend) }} .s-warn {{ background:var(--warn) }} .s-crit {{ background:var(--crit) }}
dl {{ margin:0; display:grid; grid-template-columns:1fr 1fr; gap:4px 16px }} dl div {{ display:flex; justify-content:space-between; gap:8px; border-bottom:1px dashed var(--line) }}
dt {{ color:var(--muted); font-size:.85rem }} dd {{ margin:0; font-variant-numeric:tabular-nums; font-weight:500 }}
.foot {{ margin:0; font-size:.8rem; color:var(--muted) }}
.legend {{ display:flex; flex-wrap:wrap; gap:12px; font-size:.8rem; color:var(--muted) }} .legend i {{ display:inline-block; width:10px; height:10px; border-radius:2px; margin-right:4px; vertical-align:middle }}
section {{ display:grid; gap:12px; min-width:0 }}
.two {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(340px, 1fr)); gap:24px }} .two > * {{ min-width:0 }}
.scroll {{ overflow-x:auto; background:var(--surface); border:1px solid var(--line); border-radius:8px }}
table {{ border-collapse:collapse; width:100%; font-size:.88rem }} th,td {{ padding:7px 10px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top }}
th {{ font-size:.72rem; text-transform:uppercase; letter-spacing:.06em; color:var(--muted); font-weight:600 }}
td.n {{ text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap }} tr.hl td {{ background:color-mix(in srgb, var(--accent) 8%, transparent) }}
svg text {{ fill:var(--muted); font-size:10px; font-family:var(--mono) }} svg .axis {{ stroke:var(--line) }} .c-email {{ fill:var(--email) }} .c-wpp {{ fill:var(--wpp) }}
footer {{ font-size:.8rem; color:var(--muted) }}
</style>
<main>
  <div class="head">
    <p class="eyebrow">Agrupamento de guias · notificações do dia 15</p>
    <h1>Competência {comp}</h1>{f'<p class="filtro">Filtro: {e(rel["filtros"])}</p>' if rel.get("filtros") else ""}
    <p>Foto de {e(rel['gerado_em_fmt'])} (horário de Brasília). Elegível é o grupo com status <code>SUCESSO_AGRUPAMENTO</code> no segmento (mesma regra das crons). No WhatsApp, entregue vem do status real do ativo no atendimento-zendesk, não só do controle do agrupamento.</p>
  </div>
  <div class="alertas"><p class="eyebrow">O que pede atenção</p><ul>{alertas}</ul></div>
  <section>
    <h2>Por segmento e canal</h2>
    <div class="legend"><span><i class="s-ok"></i>Enviado/entregue</span><span><i class="s-ok2"></i>Enviado (sem confirmação de entrega)</span><span><i class="s-info"></i>Em trânsito</span><span><i class="s-pend"></i>Ainda não enviado</span><span><i class="s-warn"></i>Sem contato/opt-out</span><span><i class="s-crit"></i>Falha</span></div>
    <div class="grid">{''.join(cards)}</div>
  </section>
  <section>
    <h2>Envios ao longo das rodadas</h2>
    <div class="legend"><span><i class="c-email" style="background:var(--email)"></i>E-mail</span><span><i style="background:var(--wpp)"></i>WhatsApp</span></div>
    <div class="scroll" style="padding:8px">{timeline}</div>
    <p class="muted">Notificações criadas por hora. O WhatsApp criado em fim de semana ou fora das 9h–19h fica na fila do ativo e sai no próximo horário comercial.</p>
  </section>
  <div class="two">
    <section><h2>WhatsApp por template</h2><div class="scroll"><table><thead><tr><th>Template</th>{tpl_head}</tr></thead><tbody>{tpl_rows}</tbody></table></div></section>
    <section><h2>Erros do WhatsApp ativo</h2><div class="scroll"><table><thead><tr><th>Erro</th><th>Qtd.</th></tr></thead><tbody>{err_rows}</tbody></table></div></section>
  </div>
  <div class="two">
    <section><h2>Falhas e contato incompleto</h2><div class="scroll"><table><thead><tr><th>Canal</th><th>Status</th><th>Motivo</th><th>Qtd.</th></tr></thead><tbody>{prob_rows}</tbody></table></div></section>
    <section><h2>Elegíveis ainda não notificados</h2><div class="scroll"><table><thead><tr><th>Grupo</th><th>CNPJ</th><th>Segmento</th><th>Canal</th><th>Plano</th></tr></thead><tbody>{pend_rows}</tbody></table></div>{pend_more}</section>
  </div>
  <div class="two">
    <section><h2>Resultado do agrupamento</h2><div class="scroll"><table><thead><tr><th>Status</th><th>Grupos</th><th>%</th><th>Comp. anterior</th></tr></thead><tbody>{uni_rows}</tbody></table></div></section>
    <section><h2>Grupos por plano e regime</h2><div class="scroll"><table><thead><tr><th>Segmento</th><th>Plano</th><th>Regime</th><th>Grupos</th></tr></thead><tbody>{plano_rows}</tbody></table></div></section>
  </div>
  <footer>Competência anterior, status final do controle: {e(ant_txt)}. Fontes: banco ms_agrupamento_guias (grupo_guia, controle_notificacao) e atendimento-zendesk (mensagem_ativa, autor {e(rel['autor'])}), lidos em modo somente leitura. Gerado pela skill relatorio-notificacoes-agrupamento.</footer>
</main>
"""


def alertas(rel):
    d, cel, out = rel["dados"], rel["celulas"], []
    for k, x in cel.items():
        seg, canal = k.split(".")
        nome = f"{SEGMENTOS_TODOS[seg]} · {CANAIS_TODOS[canal]}"
        if x["sem_notificacao"]:
            quando = dt.datetime.fromisoformat(x["proxima_cron"]).strftime("%d/%m às %Hh") if x["proxima_cron"] else None
            out.append(f"{nome}: {fmt(x['sem_notificacao'])} elegíveis ainda sem notificação" + (f" (próxima rodada {quando})." if quando else ", e não há mais rodadas da cron: precisa de disparo manual."))
        if x.get("sem_ativo"):
            out.append(f"{nome}: {fmt(x['sem_ativo'])} WhatsApps com controle no agrupamento e sem registro no ativo (mensagem perdida na publicação?).")
        if x["falha"] + x["erro_ativo"]:
            out.append(f"{nome}: {fmt(x['falha'] + x['erro_ativo'])} falhas ({pct(x['falha'] + x['erro_ativo'], x['elegiveis'])}).")
        if canal == "WHATSAPP" and x["ativo"]["PROCESSANDO"]:
            out.append(f"{nome}: {fmt(x['ativo']['PROCESSANDO'])} na fila do ativo (só sai em dia útil, das 9h às 19h, e é liberado aos poucos).")
    avulsa = sum(r["n"] for r in d["universo"] if r["status"] == "SUCESSO_AGRUPAMENTO_SEM_ARQUIVO_GUIA_AVULSA")
    if avulsa:
        out.append(f"{fmt(avulsa)} grupos com SUCESSO_AGRUPAMENTO_SEM_ARQUIVO_GUIA_AVULSA: as crons não os consideram elegíveis.")
    aguard = sum(r["n"] for r in d["universo"] if r["status"] == "GUIAS_AGUARDANDO_GERACAO")
    if aguard:
        out.append(f"{fmt(aguard)} grupos em GUIAS_AGUARDANDO_GERACAO: não são reprocessados e não serão notificados.")
    sem_plano = sum(r["n"] for r in d["universo"] if r["seg"] in ("SEM_PLANO", "BP_SN") and r["status"] == "SUCESSO_AGRUPAMENTO")
    if sem_plano:
        out.append(f"{fmt(sem_plano)} grupos agrupados sem segmento com notificação (plano nulo ou BP no Simples).")
    if d["ativos_sem_controle"]:
        out.append(f"{fmt(d['ativos_sem_controle'])} ativos do autor no período sem controle correspondente nesta competência (reenvios ou outra competência).")
    return out


def lista(v):
    return [x.strip().lower() for x in v.split(",") if x.strip()] if v else []


def aplicar_filtros(args):
    """Restringe SEGMENTOS, CANAIS e o SQL do grupo conforme os filtros e devolve a descrição deles."""
    global FILTRO_SQL
    publicos, regimes, canais = lista(args.publico), lista(args.regime), lista(args.canal)
    planos = [x.upper() for x in lista(args.plano)]
    for v, ok, nome in ((publicos, PLANOS, "--publico"), (regimes, ("simples", "lp"), "--regime"), (canais, CANAL_ARG, "--canal")):
        ruim = [x for x in v if x not in ok]
        if ruim:
            sys.exit(f"{nome}: valor inválido {ruim} (aceitos: {', '.join(ok)})")
    todos = PLANOS["exp"] + PLANOS["bp"]
    if [x for x in planos if x not in todos]:
        sys.exit(f"--plano: valor inválido (aceitos: {', '.join(todos)})")
    segs = [k for k, (pub, reg) in SEG_PARTES.items()
            if (not publicos or pub in publicos) and (not regimes or reg in regimes) and (not planos or set(planos) & set(PLANOS[pub]))]
    if not segs:
        sys.exit("nenhum segmento com notificação para esses filtros (BP Simples não tem notificação; confira se o plano bate com o público)")
    for k in list(SEGMENTOS):
        if k not in segs:
            del SEGMENTOS[k]
    if canais:
        for k in list(CANAIS):
            if k not in {CANAL_ARG[x] for x in canais}:
                del CANAIS[k]
    conds = []
    if len(segs) < len(SEG_PARTES):
        conds.append("seg in (" + ",".join(f"'{x}'" for x in segs) + ")")
    if planos:
        conds.append("plano_pagamento_empresa in (" + ",".join(f"'{x}'" for x in planos) + ")")
    FILTRO_SQL = "".join(f" and {x}" for x in conds)
    desc = []
    if len(segs) < len(SEG_PARTES):
        desc.append(" + ".join(SEGMENTOS.values()))
    if planos:
        desc.append("planos " + ", ".join(planos))
    if canais:
        desc.append(" + ".join(CANAIS.values()))
    return " · ".join(desc)


def gerar(args):
    agora = dt.datetime.now(TZ)
    if args.data:
        if args.competencia:
            sys.exit("use --competencia ou --data, não os dois")
        c = competencia_padrao(dt.datetime.fromisoformat(args.data).replace(tzinfo=TZ))
    else:
        c = args.competencia or competencia_padrao(agora)
    filtros = aplicar_filtros(args)
    sufixo = "_" + "-".join(x for x in (args.publico, args.regime, args.canal, args.plano) if x).replace(",", "+").lower() if filtros else ""
    saida = os.path.expanduser(args.saida or f"~/Downloads/relatorios/notificacoes-agrupamento/{c}/{agora:%Y-%m-%d_%H%M}{sufixo}")
    os.makedirs(saida, exist_ok=True)
    print(f"coletando competência {c} (autor {args.autor}){' · ' + filtros if filtros else ''}…", file=sys.stderr)
    d = coletar(c, args.autor)
    rel = dict(competencia=c, autor=args.autor, gerado_em=agora.isoformat(), gerado_em_fmt=agora.strftime("%d/%m/%Y %H:%M"), filtros=filtros, dados=d)
    rel["celulas"] = analisar(d, c, agora)
    rel["nao_notificaveis"] = sum(r["n"] for r in d["universo"] if r["status"] != "SUCESSO_AGRUPAMENTO")
    rel["alertas"] = alertas(rel)
    with open(f"{saida}/dados.json", "w") as f:
        json.dump(rel, f, ensure_ascii=False, indent=1, default=str)
    for nome, rows in (("pendentes", d["pendentes"]), ("problemas", d["problemas"])):
        with open(f"{saida}/{nome}.csv", "w", newline="") as f:
            if rows:
                w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
    resumo = texto_resumo(rel) + "\n\nAlertas:\n" + "\n".join(f"- {a}" for a in rel["alertas"])
    with open(f"{saida}/resumo.md", "w") as f:
        f.write(resumo + "\n")
    with open(f"{saida}/relatorio.html", "w") as f:
        f.write(gerar_html(rel))
    if args.pdf:
        chrome = shutil.which("google-chrome") or shutil.which("chromium")
        if not chrome:
            print("aviso: Chrome não encontrado, PDF não gerado", file=sys.stderr)
        else:
            doc = f"{saida}/_pdf.html"
            with open(doc, "w") as f:
                f.write('<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"></head><body>' + gerar_html(rel) + "</body></html>")
            subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=4000",
                            f"--print-to-pdf={saida}/relatorio.pdf", f"file://{doc}"], capture_output=True)
            os.remove(doc)
    print(resumo)
    print(f"\narquivos em {saida}", file=sys.stderr)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gerar")
    g.add_argument("--competencia", type=int)
    g.add_argument("--data", help="dia da rodada (AAAA-MM-DD); a competência é o mês anterior")
    g.add_argument("--publico", help="exp, bp")
    g.add_argument("--regime", help="simples, lp")
    g.add_argument("--canal", help="email, wpp")
    g.add_argument("--plano", help="BASICO, AVANCADO, PREMIUM, MULTIBENEFICIOS, EXPERT_ESSENCIAL, EXPERT_PRO")
    g.add_argument("--saida")
    g.add_argument("--pdf", action="store_true")
    g.add_argument("--autor", default=AUTOR_PADRAO)
    r = sub.add_parser("resumo")
    r.add_argument("--dados", required=True)
    a = p.parse_args()
    if a.cmd == "gerar":
        gerar(a)
    else:
        with open(a.dados) as f:
            rel = json.load(f)
        print(texto_resumo(rel) + "\n\nAlertas:\n" + "\n".join(f"- {x}" for x in rel["alertas"]))


if __name__ == "__main__":
    main()
