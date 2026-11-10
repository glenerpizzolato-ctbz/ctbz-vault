#!/usr/bin/env python3
"""
Regressão das notificações do microsservico-agrupamento-guias (e-mail, WhatsApp e diagnóstico BP) em DEV.

Massa sintética marcada por id_empresa na faixa 99000000000001..99000000000999 (e sistema_origem = 'regressao-notificacoes'), um grupo por cenário. O playbook completo (fluxo, regras, cenários, como ler o resultado) fica no vault CTBZ: obsidian/repositories/microsservico-agrupamento-guias/notifications-regression-tests.md.

Uso:
  regressao.py cenarios                                   lista os cenários e o esperado de cada um
  regressao.py massa [--periodo AAAAMM] [--service S] [--aplicar]
                                                          gera (e com --aplicar, grava) a massa; sem --aplicar só imprime o SQL
  regressao.py limpar [--service S] [--aplicar]           apaga toda a massa sintética (grupos, itens, guias, parcelas, diagnósticos e controles)
  regressao.py checar [--periodo AAAAMM] [--service S]  mostra tudo o que cada rota de lote alcançaria e falha se houver contato fora do CONTATO_TESTE
  regressao.py disparar --token-env VAR [--rotas email,whatsapp,diagnostico-bp] [--periodo AAAAMM] [--service S]
                                                          roda o checar e, só se passar, chama as rotas de lote do pod de DEV (api-dev)
  regressao.py verificar --desde 2026-11-10T18:00:00Z [--service S] [--projeto-logs P]
                                                          compara banco (controle_notificacao) e logs do pod com o esperado

REGRA: o contato da massa é fixo (CONTATO_TESTE) e o disparar se recusa a rodar se qualquer grupo ou diagnóstico elegível tiver outro e-mail ou telefone. Nunca relaxar essa checagem.

O --periodo padrão é a competência atual do serviço (mês anterior ao de hoje). Precisa do proxy de dev de pé (serviço do ~/.pg_service.conf) e do gcloud autenticado para os logs.
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
import urllib.request

SERVICE = "dev_atendimento_canais_ms_agrupamento_guias"
PROJETO_LOGS = "contabilizei-dev-01"
CONTAINER = "microsservico-agrupamento-guias"
BASE_DEV = "https://api-dev.contabilizei.com.br/agrupamento-guias"
EMP_BASE = 99000000000000
ORIGEM = "regressao-notificacoes"

# REGRA: toda notificação de teste vai SÓ para este contato. Nunca disparar para outro e-mail ou telefone.
CONTATO_TESTE = {"nome": "NOME TESTE", "email": "glener.pizzolato@contabilizei.com.br", "telefone": "55996981032"}

# Templates de e-mail de DEV (application-dev.yml). Experts LP usa o mesmo de Experts SN em DEV.
TPL = {"EXP_SN": "8d278fab", "EXP_LP": "8d278fab", "BP_LP": "c9085510", "DIAG_FAT": "7c837342"}
BUG_WPP_PARCELA = "PRD-176440"

SN, LP = "SIMPLES", "LUCRO_PRESUMIDO"

# Cada cenário: grupo sintético + esperado no e-mail e no WhatsApp.
# email: ("ENVIA", nomeGuia, template) | ("NAO_ELEGIVEL",) | ("STATUS", status, motivo)
# wpp:   ("ENVIA", template_whatsapp) | ("NAO_ELEGIVEL",)
CENARIOS = [
    dict(id="SN-01", desc="Experts SN · só 1 guia", regime=SN, plano="EXPERT_PRO",
         guias=[("SIMPLES", "PENDENTE")],
         email=("ENVIA", "DAS SIMPLES", "EXP_SN"), wpp=("ENVIA", "experts_empacotamento_guias_impostosb")),
    dict(id="SN-02", desc="Experts SN · várias guias, duas com descrição INSS", regime=SN, plano="EXPERT_ESSENCIAL",
         guias=[("SIMPLES", "PENDENTE"), ("ISS", "PENDENTE"), ("INSS_EMPRESA", "PENDENTE"), ("INSS_PRO_LABORE", "REGISTRADO")],
         email=("ENVIA", "DAM ISS<br>DAS SIMPLES<br>INSS<br>INSS", "EXP_SN"), wpp=("ENVIA", "experts_empacotamento_guias_impostosb")),
    dict(id="SN-03", desc="Experts SN · só 1 parcela", regime=SN, plano="EXPERT_PRO",
         parcelas=[("SIMPLES", "SIMPLES", "003/060")],
         email=("ENVIA", "Parcelamento DAS - parcela 3 de 60", "EXP_SN"), wpp=("ENVIA", "experts_empacotamento_guias_impostosb")),
    dict(id="SN-04", desc="Experts SN · várias parcelas, todos os formatos de nr_prestacao e tipo", regime=SN, plano="EXPERT_PRO",
         parcelas=[(None, "PGFN_SIMPLES", "22"), ("SIMPLES", "SIMPLES", "012/060"), ("SIMPLES", "SIMPLES", "001/060"),
                   ("INSS", "PREVIDENCIARIO_INSS", None), (None, None, "5/10")],
         email=("ENVIA", "Parcelamento - parcela 5 de 10<br>Parcelamento DAS - parcela 1 de 60<br>Parcelamento DAS - parcela 12 de 60"
                         "<br>Parcelamento PGFN DAS - parcela 22<br>Parcelamento Previdenciário", "EXP_SN"),
         wpp=("ENVIA", "experts_empacotamento_guias_impostosb")),
    dict(id="SN-05", desc="Experts SN · misto + guia avulsa (EMISSAO_PENDENTE)", regime=SN, plano="EXPERT_PRO",
         guias=[("SIMPLES", "PENDENTE"), ("ISS", "EMISSAO_PENDENTE")], parcelas=[("SIMPLES", "SIMPLES", "005/060")],
         email=("ENVIA", "DAS SIMPLES<br>Parcelamento DAS - parcela 5 de 60", "EXP_SN"), wpp=("ENVIA", "experts_empacotamento_guias_impostosb")),
    dict(id="SN-06", desc="Experts SN · diagnóstico AUMENTO_FATURAMENTO", regime=SN, plano="EXPERT_PRO",
         guias=[("SIMPLES", "PENDENTE")], parcelas=[("SIMPLES", "SIMPLES", "002/060")], diag=("AUMENTO_FATURAMENTO", "EXPERTS"),
         email=("ENVIA", None, "DIAG_FAT"), wpp=("ENVIA", "exp_guias_diag_fatur_01")),
    dict(id="SN-07", desc="Experts SN · só guia avulsa (nenhum documento no PDF)", regime=SN, plano="EXPERT_PRO",
         guias=[("ISS", "EMISSAO_FUTURA")],
         email=("STATUS", "FALHA", "ERRO_ENVIO_EMAIL"), wpp=("ENVIA", "experts_empacotamento_guias_impostosb")),
    dict(id="SN-08", desc="Experts SN · regime nulo (legado)", regime=None, plano="EXPERT_PRO",
         guias=[("SIMPLES", "PENDENTE")],
         email=("ENVIA", "DAS SIMPLES", "EXP_SN"), wpp=("ENVIA", "experts_empacotamento_guias_impostosb")),
    dict(id="SN-09", desc="Experts · plano nulo (legado) não entra em nenhuma busca", regime=SN, plano=None,
         guias=[("SIMPLES", "PENDENTE")], email=("NAO_ELEGIVEL",), wpp=("NAO_ELEGIVEL",)),
    dict(id="SN-10", desc="Experts SN · diagnóstico de motivo não habilitado (DESENQUADRAMENTO_FATOR_R) usa o template padrão", regime=SN, plano="EXPERT_PRO",
         guias=[("SIMPLES", "PENDENTE")], diag=("DESENQUADRAMENTO_FATOR_R", "EXPERTS"),
         email=("ENVIA", "DAS SIMPLES", "EXP_SN"), wpp=("ENVIA", "experts_empacotamento_guias_impostosb")),
    dict(id="SN-11", desc="Experts SN · contato sem e-mail", regime=SN, plano="EXPERT_PRO", sem_email=True,
         guias=[("SIMPLES", "PENDENTE")],
         email=("STATUS", "DADOS_INCOMPLETO", "DADOS_INCOMPLETO"), wpp=("ENVIA", "experts_empacotamento_guias_impostosb")),
    dict(id="SN-12", desc="Experts SN · competência anterior não entra na busca", regime=SN, plano="EXPERT_PRO", periodo_anterior=True,
         guias=[("SIMPLES", "PENDENTE")], email=("NAO_ELEGIVEL",), wpp=("NAO_ELEGIVEL",)),
    dict(id="SN-13", desc="Experts SN · grupo com status GUIAS_COM_ERRO não entra na busca", regime=SN, plano="EXPERT_PRO", status="GUIAS_COM_ERRO",
         guias=[("SIMPLES", "PENDENTE")], email=("NAO_ELEGIVEL",), wpp=("NAO_ELEGIVEL",)),
    dict(id="SN-14", desc="Experts SN · e-mail já notificado com sucesso não é reenviado (WhatsApp sim)", regime=SN, plano="EXPERT_PRO", ja_notificado_email=True,
         guias=[("SIMPLES", "PENDENTE")], email=("NAO_ELEGIVEL",), wpp=("ENVIA", "experts_empacotamento_guias_impostosb")),
    dict(id="LP-01", desc="Experts LP · só guias", regime=LP, plano="EXPERT_PRO",
         guias=[("CSLL", "PENDENTE"), ("IRPJ_16", "PENDENTE"), ("PIS", "PENDENTE"), ("COFINS", "PENDENTE"), ("ISS", "PENDENTE")],
         email=("ENVIA", "DAM ISS<br>DARF COFINS<br>DARF CSLL<br>DARF_IRPJ<br>PIS", "EXP_LP"), wpp=("ENVIA", "experts_empacotamento_guias_impostosb")),
    dict(id="LP-02", desc="Experts LP · só parcelas", regime=LP, plano="EXPERT_ESSENCIAL",
         parcelas=[("IRPJ", "DARF_UNIFICADO", "004/024"), ("CSLL", "PGFN_DEMAIS_DEBITOS", "004/024")],
         email=("ENVIA", "Parcelamento DARF Unificado - parcela 4 de 24<br>Parcelamento PGFN Demais Débitos - parcela 4 de 24", "EXP_LP"),
         wpp=("ENVIA", "experts_empacotamento_guias_impostosb")),
    dict(id="LP-03", desc="Experts LP · misto", regime=LP, plano="EXPERT_PRO",
         guias=[("CSLL", "PENDENTE"), ("PIS", "PENDENTE")], parcelas=[("INSS", "PREVIDENCIARIO_INSS", "010/060")],
         email=("ENVIA", "DARF CSLL<br>PIS<br>Parcelamento Previdenciário - parcela 10 de 60", "EXP_LP"),
         wpp=("ENVIA", "experts_empacotamento_guias_impostosb")),
    dict(id="BP-01", desc="BP LP BASICO · só guias (BASICO não recebe WhatsApp)", regime=LP, plano="BASICO",
         guias=[("CSLL", "PENDENTE"), ("IRPJ_16", "PENDENTE"), ("COFINS", "PENDENTE")],
         email=("ENVIA", "DARF COFINS<br>DARF CSLL<br>DARF_IRPJ", "BP_LP"), wpp=("NAO_ELEGIVEL",)),
    dict(id="BP-02", desc="BP LP AVANCADO · só parcela", regime=LP, plano="AVANCADO",
         parcelas=[("INSS", "PGFN_PREVIDENCIARIO_INSS", "007/030")],
         email=("ENVIA", "Parcelamento PGFN Previdenciário - parcela 7 de 30", "BP_LP"), wpp=("ENVIA", "bpm_empacotamento_guias_impostos")),
    dict(id="BP-03", desc="BP LP MULTIBENEFICIOS · misto", regime=LP, plano="MULTIBENEFICIOS",
         guias=[("PIS", "PENDENTE"), ("COFINS", "PENDENTE")], parcelas=[(None, "PGFN_SIMPLES", "15"), ("CSLL", "DIVIDA_ATIVA", "002/012")],
         email=("ENVIA", "DARF COFINS<br>PIS<br>Parcelamento Dívida Ativa - parcela 2 de 12<br>Parcelamento PGFN DAS - parcela 15", "BP_LP"),
         wpp=("ENVIA", "bpm_empacotamento_guias_impostos")),
    dict(id="BP-04", desc="BP LP PREMIUM · só guia", regime=LP, plano="PREMIUM",
         guias=[("PIS", "PENDENTE")], email=("ENVIA", "PIS", "BP_LP"), wpp=("ENVIA", "bpm_empacotamento_guias_impostos")),
    dict(id="BP-05", desc="BP no Simples não é notificado pelo agrupamento", regime=SN, plano="BASICO",
         guias=[("SIMPLES", "PENDENTE")], email=("NAO_ELEGIVEL",), wpp=("NAO_ELEGIVEL",)),
]

# Diagnóstico BP (rota diagnostico/envia-lote/bp): só diagnóstico, sem grupo. diag_bp: esperado ("ENVIA", template) | ("IGNORADO",)
CENARIOS_DIAG_BP = [
    dict(id="DBP-01", desc="Diagnóstico BP AUMENTO_FATURAMENTO", motivo="AUMENTO_FATURAMENTO", plano="BASICO", diag_bp=("ENVIA", "bp_diag_fatur_02")),
    dict(id="DBP-02", desc="Diagnóstico BP de motivo não habilitado (PROPORCAO_ANEXOS)", motivo="PROPORCAO_ANEXOS", plano="AVANCADO", diag_bp=("IGNORADO",)),
]

RESULTADO_DIAG = {
    "AUMENTO_FATURAMENTO": {"faturamentoAtual": 3110, "diagnosticoPositivo": True, "faturamentoAnterior": 2310, "porcentagemAumento": 34.63},
    "DESENQUADRAMENTO_FATOR_R": {"diagnosticoPositivo": True, "fatorRAtual": 0.21, "fatorRAnterior": 0.30},
    "PROPORCAO_ANEXOS": {"diagnosticoPositivo": True},
}


def todos():
    return CENARIOS + CENARIOS_DIAG_BP


def idx(cid):
    return [c["id"] for c in todos()].index(cid) + 1


def cnpj(i):
    base = "99%08d01" % i

    def dv(n):
        w = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2] if len(n) == 12 else [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        r = sum(int(a) * b for a, b in zip(n, w)) % 11
        return "0" if r < 2 else str(11 - r)

    base += dv(base)
    return base + dv(base)


def periodo_atual():
    hoje = dt.date.today().replace(day=1) - dt.timedelta(days=1)
    return hoje.year * 100 + hoje.month


def soma_mes(p, n):
    a, m = divmod(p, 100)
    m += n
    while m > 12:
        a, m = a + 1, m - 12
    while m < 1:
        a, m = a - 1, m + 12
    return a * 100 + m


def q(v):
    return "null" if v is None else "'" + str(v).replace("'", "''") + "'"


def sql_massa(a):
    p = a.periodo
    out = ["begin;",
           # arquivos reais de dev para o PDF do grupo, da guia e da parcela (o conteúdo não importa, só precisa existir no storage)
           "create temp table arq as select "
           "(select path from grupo_guia where path is not null and id_empresa not between 99000000000000 and 99000000000999 order by id desc limit 1) gpath, "
           "(select id_arquivo from controle_guias where bucket_name is not null and id_empresa not between 99000000000000 and 99000000000999 order by id desc limit 1) garq, "
           "(select bucket_name from controle_guias where bucket_name is not null and id_empresa not between 99000000000000 and 99000000000999 order by id desc limit 1) gbucket, "
           "(select id_arquivo from controle_parcelas where bucket_name is not null and id_empresa not between 99000000000000 and 99000000000999 order by id desc limit 1) parq, "
           "(select bucket_name from controle_parcelas where bucket_name is not null and id_empresa not between 99000000000000 and 99000000000999 order by id desc limit 1) pbucket;"]
    for c in CENARIOS:
        i = idx(c["id"])
        emp, cn = EMP_BASE + i, cnpj(i)
        contato = dict(CONTATO_TESTE)
        if c.get("sem_email"):
            contato.pop("email")
        per = soma_mes(p, -1) if c.get("periodo_anterior") else p
        out.append(
            f"insert into grupo_guia(id_empresa,periodo_apuracao,status,path,created_at,updated_at,cnpj,contato,regime_tributario,plano_pagamento_empresa) "
            f"select {emp},{per},{q(c.get('status', 'SUCESSO_AGRUPAMENTO'))},gpath,now(),now(),'{cn}',{q(json.dumps(contato, ensure_ascii=False))}::jsonb,{q(c['regime'])},{q(c['plano'])} from arq;")
        g = f"(select id from grupo_guia where id_empresa={emp})"
        for k, (imp, st) in enumerate(c.get("guias", []), 1):
            idg = emp * 100 + k
            out.append(
                f"insert into controle_guias(id_empresa,id_guia,periodo_apuracao,imposto,valor_principal,data_para_pagamento,data_criacao,data_atualizacao,status,id_arquivo,created_at,updated_at,sistema_origem,bucket_name,cnpj) "
                f"select {emp},{idg},{per},'{imp}',100,now()+interval '10 days',now(),now(),'{st}',garq,now(),now(),'{ORIGEM}',gbucket,'{cn}' from arq;")
            out.append(f"insert into item_grupo_guia(grupo_guia_id,controle_guia_id,created_at,updated_at) select {g},(select id from controle_guias where id_guia={idg}),now(),now();")
        pp = soma_mes(per, 1)
        for k, (imp, tipo, nr) in enumerate(c.get("parcelas", []), 1):
            idp = emp * 100 + 50 + k
            out.append(
                f"insert into controle_parcelas(id_parcela,id_empresa,cnpj,id_parcelamento,nr_prestacao,periodo_apuracao,periodo_apuracao_ano,periodo_apuracao_mes,vencimento,status,tipo_parcelamento,dia_vencimento,valor,valor_principal,imposto,imposto_list,id_arquivo,bucket_name,geracao_automatica,cobranca_gerada,cobrar_recalculo,sistema_origem,clock,created_at,updated_at) "
                f"select {idp},{emp},'{cn}',{idp + 1000},{q(nr)},{pp},{pp // 100},{pp % 100},now()+interval '10 days','PENDENTE',{q(tipo)},20,99.9,99.9,{q(imp)},'{{{imp or 'SIMPLES'}}}',parq,pbucket,false,false,false,'{ORIGEM}',now(),now(),now() from arq;")
            out.append(f"insert into item_grupo_guia(grupo_guia_id,controle_parcela_id,created_at,updated_at) select {g},(select id from controle_parcelas where id_parcela={idp}),now(),now();")
        if c.get("diag"):
            motivo, plano = c["diag"]
            out.append(
                f"insert into diagnostico_aumento_imposto(motivo,resultado,id_guia,id_guia_referencia,created_at,id_empresa,cnpj,plano,contato) "
                f"values ('{motivo}',{q(json.dumps(RESULTADO_DIAG[motivo]))}::jsonb,{emp * 100 + 1},{emp * 100 + 1},now(),{emp},'{cn}','{plano}',{q(json.dumps(contato, ensure_ascii=False))}::jsonb);")
        if c.get("ja_notificado_email"):
            out.append(f"insert into controle_notificacao(tipo_notificacao,status,email,data_envio_notificacao,grupo_guia_id,created_at,updated_at,cnpj) "
                       f"values ('EMAIL','SUCESSO',{q(CONTATO_TESTE['email'])},now(),{g},now(),now(),'{cn}');")
    for c in CENARIOS_DIAG_BP:
        i = idx(c["id"])
        emp, cn = EMP_BASE + i, cnpj(i)
        contato = dict(CONTATO_TESTE)
        idg = emp * 100 + 1
        out.append(
            f"insert into controle_guias(id_empresa,id_guia,periodo_apuracao,imposto,valor_principal,data_para_pagamento,data_criacao,data_atualizacao,status,id_arquivo,created_at,updated_at,sistema_origem,bucket_name,cnpj) "
            f"select {emp},{idg},{p},'SIMPLES',100,now()+interval '10 days',now(),now(),'PENDENTE',garq,now(),now(),'{ORIGEM}',gbucket,'{cn}' from arq;")
        out.append(
            f"insert into diagnostico_aumento_imposto(motivo,resultado,id_guia,id_guia_referencia,created_at,id_empresa,cnpj,plano,contato) "
            f"values ('{c['motivo']}',{q(json.dumps(RESULTADO_DIAG[c['motivo']]))}::jsonb,{idg},{idg},now(),{emp},'{cn}','{c['plano']}',{q(json.dumps(contato, ensure_ascii=False))}::jsonb);")
    out.append("commit;")
    out.append("select g.id grupo, g.id_empresa - 99000000000000 n, g.cnpj, g.regime_tributario, g.plano_pagamento_empresa, g.status, g.periodo_apuracao, count(i.*) itens "
               "from grupo_guia g left join item_grupo_guia i on i.grupo_guia_id=g.id where g.id_empresa between 99000000000000 and 99000000000999 group by 1,2,3,4,5,6,7 order by 2;")
    return "\n".join(out)


def sql_limpar():
    faixa = "between 99000000000000 and 99000000000999"
    return "\n".join([
        "begin;",
        f"delete from controle_notificacao where grupo_guia_id in (select id from grupo_guia where id_empresa {faixa}) or diagnostico_aumento_imposto_id in (select id from diagnostico_aumento_imposto where id_empresa {faixa});",
        f"delete from item_grupo_guia where grupo_guia_id in (select id from grupo_guia where id_empresa {faixa});",
        f"delete from grupo_guia where id_empresa {faixa};",
        f"delete from controle_parcelas where id_empresa {faixa};",
        f"delete from diagnostico_aumento_imposto where id_empresa {faixa};",
        f"delete from controle_guias where id_empresa {faixa};",
        "commit;",
    ])


def psql(service, sql, json_out=False):
    args = ["psql", "-w", f"service={service}", "-v", "ON_ERROR_STOP=1"]
    if json_out:
        args += ["-At"]
    r = subprocess.run(args, input=sql, text=True, capture_output=True)
    if r.returncode != 0:
        sys.exit(r.stderr)
    return r.stdout


def cmd_cenarios(_):
    for c in todos():
        print(f"{c['id']:7} {c['desc']}")
        if "email" in c:
            print(f"        e-mail:   {c['email']}")
            wpp = c["wpp"]
            bug = " (bug conhecido " + BUG_WPP_PARCELA + ": falha enquanto não corrigido)" if c.get("parcelas") and wpp[0] == "ENVIA" else ""
            print(f"        whatsapp: {wpp}{bug}")
        else:
            print(f"        diagnóstico BP: {c['diag_bp']}")


def cmd_massa(a):
    s = sql_massa(a)
    if not a.aplicar:
        print(s)
        return
    print(psql(a.service, s))


def cmd_limpar(a):
    s = sql_limpar()
    if not a.aplicar:
        print(s)
        return
    print(psql(a.service, s))


ELEGIVEIS_SQL = """
with g as (select gg.* from grupo_guia gg where gg.periodo_apuracao = {p} and gg.status = 'SUCESSO_AGRUPAMENTO'),
r as (
  select 'exp-sn/EMAIL' rota, g.id, g.contato from g where (g.regime_tributario is null or g.regime_tributario <> 'LUCRO_PRESUMIDO') and g.plano_pagamento_empresa in ('EXPERT_ESSENCIAL','EXPERT_PRO') and not exists (select 1 from controle_notificacao cn where cn.grupo_guia_id = g.id and cn.tipo_notificacao = 'EMAIL')
  union all select 'exp-sn/WHATSAPP', g.id, g.contato from g where (g.regime_tributario is null or g.regime_tributario <> 'LUCRO_PRESUMIDO') and g.plano_pagamento_empresa in ('EXPERT_ESSENCIAL','EXPERT_PRO') and not exists (select 1 from controle_notificacao cn where cn.grupo_guia_id = g.id and cn.tipo_notificacao = 'WHATSAPP')
  union all select 'exp-lp/EMAIL', g.id, g.contato from g where g.regime_tributario = 'LUCRO_PRESUMIDO' and g.plano_pagamento_empresa in ('EXPERT_ESSENCIAL','EXPERT_PRO') and not exists (select 1 from controle_notificacao cn where cn.grupo_guia_id = g.id and cn.tipo_notificacao = 'EMAIL')
  union all select 'exp-lp/WHATSAPP', g.id, g.contato from g where g.regime_tributario = 'LUCRO_PRESUMIDO' and g.plano_pagamento_empresa in ('EXPERT_ESSENCIAL','EXPERT_PRO') and not exists (select 1 from controle_notificacao cn where cn.grupo_guia_id = g.id and cn.tipo_notificacao = 'WHATSAPP')
  union all select 'bp-lp/EMAIL', g.id, g.contato from g where g.regime_tributario = 'LUCRO_PRESUMIDO' and g.plano_pagamento_empresa in ('BASICO','AVANCADO','PREMIUM','MULTIBENEFICIOS') and not exists (select 1 from controle_notificacao cn where cn.grupo_guia_id = g.id and cn.tipo_notificacao = 'EMAIL')
  union all select 'bp-lp/WHATSAPP', g.id, g.contato from g where g.regime_tributario = 'LUCRO_PRESUMIDO' and g.plano_pagamento_empresa in ('AVANCADO','PREMIUM','MULTIBENEFICIOS') and not exists (select 1 from controle_notificacao cn where cn.grupo_guia_id = g.id and cn.tipo_notificacao = 'WHATSAPP')
  union all select distinct on (d.cnpj) 'diagnostico/envia-lote/bp', d.id, d.contato from diagnostico_aumento_imposto d join controle_guias cg on cg.id_guia = d.id_guia
    where d.plano not like 'EXPERT%' and cg.periodo_apuracao = {p} and not exists (select 1 from controle_notificacao cn where cn.cnpj = d.cnpj and cn.created_at >= date_trunc('month', current_date))
)
select coalesce(json_agg(r), '[]') from r;
"""

# Rotas de cada grupo do disparar (o que a checagem cobre)
ROTAS = {
    "email": ["exp-sn/EMAIL", "exp-lp/EMAIL", "bp-lp/EMAIL"],
    "whatsapp": ["exp-sn/WHATSAPP", "exp-lp/WHATSAPP", "bp-lp/WHATSAPP"],
    "diagnostico-bp": ["diagnostico/envia-lote/bp"],
}


def checar(a, rotas):
    """Lista o que cada rota alcançaria e devolve as violações da regra do contato fixo."""
    itens = json.loads(psql(a.service, ELEGIVEIS_SQL.format(p=a.periodo), json_out=True))
    violacoes = []
    for i in itens:
        if i["rota"] not in rotas:
            continue
        c = i["contato"] or {}
        email_ok = c.get("email") in (None, CONTATO_TESTE["email"])
        tel = re.sub(r"\D", "", c.get("telefone") or "")
        tel_ok = tel in ("", CONTATO_TESTE["telefone"])
        marca = "ok" if email_ok and tel_ok else "BLOQUEIA"
        print(f"{marca:8} {i['rota']:28} id={i['id']} email={c.get('email')} telefone={c.get('telefone')}")
        if marca != "ok":
            violacoes.append(i)
    return violacoes


def cmd_checar(a):
    v = checar(a, [r for rs in ROTAS.values() for r in rs])
    if v:
        sys.exit(f"\n{len(v)} destino(s) fora do contato de teste: NÃO disparar. Ajuste ou isole esses registros antes.")
    print("\nok: todas as rotas só alcançam o contato de teste")


def cmd_disparar(a):
    token = os.environ.get(a.token_env)
    if not token:
        sys.exit(f"variável {a.token_env} vazia: exporte o token do api-gateway de dev (ver obsidian/apis/)")
    grupos = a.rotas.split(",")
    v = checar(a, [r for g in grupos for r in ROTAS[g]])
    if v:
        sys.exit(f"{len(v)} destino(s) fora do contato de teste ({CONTATO_TESTE['email']} / {CONTATO_TESTE['telefone']}): disparo CANCELADO.")
    print("início:", dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"))
    for grupo in grupos:
        for r in ROTAS[grupo]:
            u = f"{BASE_DEV}/notificacao/{r}" if r.startswith("diagnostico") else f"{BASE_DEV}/notificacao/envia-lote/grupo-guia/{r}"
            req = urllib.request.Request(u, headers={"x-ctbz-api-gateway-token": token})
            try:
                with urllib.request.urlopen(req, timeout=120) as resp:
                    print(resp.status, u, resp.read()[:300].decode(errors="replace"))
            except Exception as e:
                print("ERRO", u, e)


def logs(desde, projeto):
    f = (f'resource.type="k8s_container" AND resource.labels.container_name="{CONTAINER}" AND timestamp>="{desde}" '
         f'AND (jsonPayload.message:"construção do DTO para envio de email" OR jsonPayload.message:"Template WhatsApp selecionado" '
         f'OR jsonPayload.message:"Notificacao BP" OR jsonPayload.message:"erro desconhecido")')
    r = subprocess.run(["gcloud", "logging", "read", f, "--project", projeto, "--limit", "5000", "--format", "value(jsonPayload.message)"],
                       text=True, capture_output=True)
    if r.returncode != 0:
        sys.exit(r.stderr)
    email, wpp = {}, {}
    for l in r.stdout.splitlines():
        m = re.search(r"Notificação (\d+) construção do DTO.*templateId=([0-9a-f-]+), variables=\{(.*?)\}, attach", l)
        if m:
            vs = m.group(3)
            ng = re.search(r"nomeGuia=(.*?)(?:, \w+=|$)", vs)
            email[int(m.group(1))] = (m.group(2)[:8], ng.group(1) if ng else None)
        m = re.search(r"Notificação (\d+) WhatsApp(?: BP LP)?, Template WhatsApp selecionado: (\w+)", l)
        if m:
            wpp[int(m.group(1))] = m.group(2)
        m = re.search(r"Notificacao BP (\d+) construida e enviada.*template=(\w+)", l)
        if m:
            wpp[int(m.group(1))] = m.group(2)
    return email, wpp


TEMPLATE_WPP = {  # nome do enum (log) -> nome do template no WhatsApp
    "GRUPO_GUIA_IMPOSTOS_EXPERT": "experts_empacotamento_guias_impostosb", "AUMENTO_FATURAMENTO": None,
    "GRUPO_GUIA_IMPOSTOS_BP_LP": "bpm_empacotamento_guias_impostos",
}


def cmd_verificar(a):
    rows = psql(a.service, (
        "select coalesce(json_agg(t),'[]') from (select g.id_empresa - 99000000000000 n, cn.id, cn.tipo_notificacao tipo, cn.status, cn.motivo, cn.external_id "
        "from grupo_guia g join controle_notificacao cn on cn.grupo_guia_id = g.id "
        f"where g.id_empresa between 99000000000000 and 99000000000999 and cn.created_at >= '{a.desde}' "
        "union all select d.id_empresa - 99000000000000, cn.id, 'DIAG_BP', cn.status, cn.motivo, cn.external_id "
        "from diagnostico_aumento_imposto d join controle_notificacao cn on cn.diagnostico_aumento_imposto_id = d.id "
        f"where d.id_empresa between 99000000000000 and 99000000000999 and cn.created_at >= '{a.desde}' order by 1, 2) t;"), json_out=True)
    por = {}
    for r in json.loads(rows):
        por.setdefault((r["n"], r["tipo"]), []).append(r)
    email_log, wpp_log = logs(a.desde, a.projeto_logs)
    falhas = 0

    def linha(cid, canal, ok, detalhe):
        nonlocal falhas
        falhas += 0 if ok in ("OK", "BUG") else 1
        print(f"{ok:5} {cid:7} {canal:9} {detalhe}")

    for c in CENARIOS:
        n = idx(c["id"])
        # e-mail
        regs = por.get((n, "EMAIL"), [])
        if c.get("ja_notificado_email"):
            regs = regs  # o SUCESSO semeado é anterior ao --desde, então não aparece
        e = c["email"]
        if e[0] == "NAO_ELEGIVEL":
            linha(c["id"], "e-mail", "OK" if not regs else "FALHA", "não elegível" if not regs else f"notificou: {regs}")
        elif e[0] == "STATUS":
            r = regs[-1] if regs else None
            ok = r and r["status"] == e[1] and r["motivo"] == e[2]
            linha(c["id"], "e-mail", "OK" if ok else "FALHA", f"esperado {e[1]}/{e[2]}, obtido {r and (r['status'], r['motivo'])}")
        else:
            r = regs[-1] if regs else None
            got = email_log.get(r["id"]) if r else None
            ok = bool(r and r["external_id"] and got and got[0] == TPL[e[2]] and got[1] == e[1])
            linha(c["id"], "e-mail", "OK" if ok else "FALHA",
                  f"template {got and got[0]} (esperado {TPL[e[2]]}) · nomeGuia {got and got[1]!r}" + ("" if ok else f" · esperado {e[1]!r} · registro {r}"))
        # whatsapp
        regs = por.get((n, "WHATSAPP"), [])
        w = c["wpp"]
        if w[0] == "NAO_ELEGIVEL":
            linha(c["id"], "whatsapp", "OK" if not regs else "FALHA", "não elegível" if not regs else f"notificou: {regs}")
        else:
            r = regs[-1] if regs else None
            tpl = wpp_log.get(r["id"]) if r else None
            tpl_nome = TEMPLATE_WPP.get(tpl, tpl)
            esperado_tpl = w[1]
            ok = bool(r and r["status"] in ("SUCESSO", "AGUARDANDO_NOTIFICACAO") and r["motivo"] is None)
            if not ok and c.get("parcelas") and r and r["motivo"] == "ERRO_DESCONHECIDO":
                linha(c["id"], "whatsapp", "BUG", f"FALHA/ERRO_DESCONHECIDO com parcela: bug conhecido {BUG_WPP_PARCELA}")
                continue
            linha(c["id"], "whatsapp", "OK" if ok else "FALHA", f"{r and (r['status'], r['motivo'])} · template {tpl} (esperado {esperado_tpl})")
    for c in CENARIOS_DIAG_BP:
        n = idx(c["id"])
        regs = por.get((n, "DIAG_BP"), [])
        e = c["diag_bp"]
        if e[0] == "IGNORADO":
            linha(c["id"], "diag BP", "OK" if not regs else "FALHA", "ignorado" if not regs else f"notificou: {regs}")
        else:
            r = regs[-1] if regs else None
            tpl = wpp_log.get(r["id"]) if r else None
            ok = bool(r and r["status"] in ("SUCESSO", "AGUARDANDO_NOTIFICACAO") and r["motivo"] is None)
            linha(c["id"], "diag BP", "OK" if ok else "FALHA", f"{r and (r['status'], r['motivo'])} · template {tpl} (esperado {e[1]})")
    print(f"\n{falhas} falha(s) fora dos bugs conhecidos")
    sys.exit(1 if falhas else 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    sp.add_parser("cenarios").set_defaults(f=cmd_cenarios)
    m = sp.add_parser("massa")
    m.add_argument("--periodo", type=int, default=periodo_atual())
    m.add_argument("--service", default=SERVICE)
    m.add_argument("--aplicar", action="store_true")
    m.set_defaults(f=cmd_massa)
    l = sp.add_parser("limpar")
    l.add_argument("--service", default=SERVICE)
    l.add_argument("--aplicar", action="store_true")
    l.set_defaults(f=cmd_limpar)
    c = sp.add_parser("checar")
    c.add_argument("--periodo", type=int, default=periodo_atual())
    c.add_argument("--service", default=SERVICE)
    c.set_defaults(f=cmd_checar)
    d = sp.add_parser("disparar")
    d.add_argument("--periodo", type=int, default=periodo_atual())
    d.add_argument("--service", default=SERVICE)
    d.add_argument("--token-env", required=True)
    d.add_argument("--rotas", default="email,whatsapp,diagnostico-bp")
    d.set_defaults(f=cmd_disparar)
    v = sp.add_parser("verificar")
    v.add_argument("--desde", required=True)
    v.add_argument("--service", default=SERVICE)
    v.add_argument("--projeto-logs", default=PROJETO_LOGS)
    v.set_defaults(f=cmd_verificar)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
