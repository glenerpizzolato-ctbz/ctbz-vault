#!/usr/bin/env python3
"""Explain, per Zendesk ticket, why the CSAT Transbordo did (or did not) hold the CSAT survey.

Two engines decide the CSAT of a human ticket (trigger -> Pub/Sub `zendesk-trigger.p2p.csat-survey`):

- experts-service (legacy, until the cutover on ~2026-11-12): RunSurveyCsatEngineConsumer ->
  FetchTranbordoUseCase -> ProcessExpertsTransbordoStrategy / ProcessBpmpTransbordoStrategy. It logs
  every rule (flow `csat-engine`), so the checklist comes straight from the logs.
- survey-service (current): CsatSurveyConsumer -> job `csat.request` -> prepareRequest -> business
  hours window -> TransbordoHold.prepare -> DispatchEngine. It logs only the outcome (`CSAT
  DISPATCHED|HELD|SKIPPED`, `CSAT ignorado: ...`, `CSAT agendado/descartado`), so the transbordo
  rules are re-evaluated here with the data of the databases.

Sources (all read-only, prod; never the Zendesk prod API):
1. Cloud Logging, project contabilizei-prod-01: experts-service (namespace experts-prd), survey-service
   (namespace atendimento-canais-prd) and zendesk-agents (namespace crm-prd, "is closed or solved",
   used as the solve time to infer the 10-minute delay, i.e. enable_transbordo, on the survey-service).
2. psql prd_issue_ticketing (ticket_jira): the Jira tickets of the CNPJ (current state).
3. psql prd_experts_experts_service: survey_csat_sent and ticket_transbordo (the survey-service rows are
   mirrored there, with survey_service_id).
4. psql prd_crm_atendimento_zendesk (tickets): parent ticket and the CNPJ tickets opened after it.

Usage:
  analisar_csat_transbordo.py 30257371 30260000 ... [--file ids.txt] [--freshness 30d]
                              [--out ~/Downloads/csat-transbordo-<date>.csv] [--no-db]

Outputs <out>.csv (one row per ticket) and <out>.md (per-ticket checklist of rules passed / blocked).
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

LOG_PROJECT = "contabilizei-prod-01"
ENGINE_LOG_FILTER = (
    'resource.type="k8s_container" AND ('
    '(resource.labels.namespace_name="experts-prd" AND resource.labels.container_name="experts-service") OR '
    '(resource.labels.namespace_name="atendimento-canais-prd" AND resource.labels.container_name="survey-service"))'
)
SOLVE_LOG_FILTER = (
    'resource.type="k8s_container" AND resource.labels.namespace_name="crm-prd" '
    'AND resource.labels.container_name="zendesk-agents" AND "is closed or solved"'
)
DB_EXPERTS = "prd_experts_experts_service"
DB_TICKETING = "prd_issue_ticketing"
DB_ZENDESK = "prd_crm_atendimento_zendesk"
ZD_LINK = "https://contabilizei.zendesk.com/agent/tickets/{}"

# Mirrors experts-service src/domain/ticket-transbordo/constants/jira-projects.ts and survey-service
# src/modules/csat/transbordo-hold.ts (isJiraEligible).
JIRA_PROJECTS = [
    "NFEXP", "EXPBKO", "VAL", "SDC", "PREV", "RHC", "C20", "SST", "OBA", "ATE", "RTRAB", "OPFIS",
    "REG", "ER", "INV", "ENQEXP", "PROA",
]
SLA_48H_PROJECTS = ["EXPBKO"]
DUE_DATE_IGNORED_PROJECTS = ["NFEXP"]
SLA_LIMIT_HOURS = 48
TRANSBORDO_KIND = {"HUMAN_EXPERTS": "JIRA", "HUMAN_BPMP": "PARALLEL_CONVERSATION"}
BPMP_VIA = "Conversa paralela"
DELAY_MIN = 10

# Cause code -> (cause found?, text). found=False: the data does not close the case.
CAUSES = {
    "TICKET_DE_RESPOSTA_CSAT": (True, "O ticket {ticket} é a resposta do cliente a uma pesquisa (via '{via}', grupo '{grupo}'), não o atendimento: a pesquisa veio do ticket {pai}. Analise o {pai}."),
    "TICKET_OFF_DO_TRANSBORDO": (True, "O ticket {ticket} é o ticket off de acompanhamento (via '{via}', grupo '{grupo}'{jiras}), não o atendimento: ele não passa pelo motor que decide a pesquisa. {fup} Analise o atendimento {pai}."),
    "SEM_LOG_DO_MOTOR": (False, "Nenhum log de decisão do CSAT para o ticket no período (experts-service nem survey-service): o gatilho do Zendesk não disparou, o ticket não foi resolvido ou os logs já saíram da retenção."),
    "CSAT_POR_OUTRO_FLUXO": (True, "Não há decisão do motor para o ticket, mas há pesquisa enviada por outro fluxo ({detail}): o transbordo só existe no motor do ticket humano."),
    "ORIGEM_FORA_DO_TRANSBORDO": (True, "Origem {source}: o transbordo só vale para HUMAN_EXPERTS (Jira) e HUMAN_BPMP (conversa paralela)."),
    "FLAG_ENABLE_TRANSBORDO_DESLIGADA": (True, "O gatilho do Zendesk mandou enable_transbordo=false{inferido}: a checagem de transbordo foi pulada."),
    "CSAT_NAO_ELEGIVEL": (True, "A pesquisa não saiu por regra do CSAT, antes do transbordo ({detail}): não houve vazamento."),
    "CSAT_AGENDADO_EXPEDIENTE": (False, "O pedido foi agendado para a abertura do expediente ({detail}) e ainda não há decisão final no período."),
    "TRANSBORDO_SEGUROU": (True, "O transbordo segurou a pesquisa ({detail})."),
    "ERRO_NO_MOTOR": (True, "O motor falhou ao processar o ticket ({detail})."),
    "JIRA_CRIADO_APOS_MOTOR": (True, "O Jira {jira} foi criado {minutos} min depois de o motor decidir ({engine}): quando o motor buscou, ainda não havia Jira elegível para o CNPJ."),
    "JIRA_ANTERIOR_AO_ATENDIMENTO": (True, "O Jira {jira} foi criado antes do ticket do atendimento ({criado} < {pai}): o motor só considera Jiras abertos depois do ticket pai."),
    "JIRA_PROJETO_NAO_ELEGIVEL": (True, "O Jira {jira} é do projeto {projeto}: só EXPBKO (due_date <= 48h) e NFEXP geram transbordo."),
    "DUE_DATE_PREENCHIDO_APOS_MOTOR": (True, "O Jira {jira} estava sem due_date quando o motor decidiu ({engine}); o due_date ({due}) só foi preenchido depois (automação de SLA do Jira). Com ele, o Jira {teria}."),
    "JIRA_SEM_DUE_DATE": (True, "O Jira {jira} (EXPBKO) está sem due_date, então não passa na regra de SLA de 48h{prov}."),
    "DUE_DATE_ACIMA_48H": (True, "O due_date do Jira {jira} ({due}) estava a {horas}h do momento do motor, acima do limite de 48h."),
    "DEMANDA_PREVENTIVA_VAZIA": (True, "O campo 'Demanda preventiva' do Jira {jira} estava vazio: sem ele o Jira é descartado{prov}."),
    "DEMANDA_PREVENTIVA": (True, "O Jira {jira} é demanda preventiva (campo = Sim), que não gera transbordo."),
    "JIRA_JA_RESOLVIDO": (True, "O Jira {jira} já estava fechado quando o motor decidiu."),
    "JIRA_ESTADO_MUDOU": (False, "Hoje o Jira {jira} passaria nas regras, mas ele mudou depois do motor ({mudou}); confirmar no changelog do Jira qual campo (due_date, status, Demanda preventiva) estava diferente às {engine}."),
    "SEM_JIRA_PARA_O_CNPJ": (False, "Nenhum Jira do CNPJ {cnpj} no ticketing depois do atendimento: o ticket off pode não ter Jira, ou o Jira foi aberto com outro CNPJ / sem CNPJ.{extra}"),
    "BPMP_TICKET_OFF_VIA_DIFERENTE": (True, "Nenhum ticket via 'Conversa paralela' do CNPJ depois do atendimento; o ticket aberto depois foi o {ticket} (via '{via}'): se ele é o ticket off, não foi aberto pela conversa paralela, a única via que o BPMP reconhece."),
    "BPMP_TICKET_OFF_APOS_MOTOR": (True, "O ticket off {ticket} foi criado {minutos} min depois de o motor decidir ({engine}); o HUMAN_BPMP não tem o atraso de 10 min."),
    "BPMP_SEM_TICKET_OFF": (False, "Nenhum ticket do CNPJ {cnpj} aberto depois do atendimento: não houve ticket off (ou foi aberto em outra organização)."),
    "INDETERMINADO": (False, "O motor liberou a pesquisa, mas os dados não fecham a causa ({detail})."),
}

# experts-service (legacy) log messages. Keep in sync with the code when the messages change.
P = {
    "received": re.compile(r"received message from ticket id (\d+) and source (\w+)"),
    "scheduled": re.compile(r"scheduling survey csat engine for HUMAN_EXPERTS with transbordo, ticket id (\d+)"),
    "running": re.compile(r"running survey csat engine for ticket id (\d+) and source (\w+)"),
    "invalid": re.compile(r"ticket id (\d+): (.+ skipping survey)$"),
    "fup_source": re.compile(r"ticket id (\d+) has source (\w+), handled by the FUP flow"),
    "generic": re.compile(r"ticket id (\d+): assignee (\S+) is a generic account"),
    "blocked": re.compile(r"ticket id (\d+): (\w+) (\S+) is blocked, skipping survey"),
    "microtema": re.compile(r"ticket id (\d+): micro tema (\S+) is not eligible"),
    "context": re.compile(r"ticket id (\d+): context resolved for (\w+) (\S+) with template (\S+) and micro tema (\S+)"),
    "limit_reached": re.compile(r"ticket id (\d+): cnpj (\S+) has reached the conventional survey limit of (\S+) responses in the last (\S+) days \((\S+) current"),
    "limit_ok": re.compile(r"ticket id (\d+): cnpj (\S+) is under the conventional survey limit \((\S+) of (\S+) responses in the last (\S+) days\)"),
    "no_quarantine": re.compile(r"ticket id (\d+): source (\w+) has no quarantine"),
    "matched": re.compile(r"ticket id (\d+) matched requirement (\w+), checking transbordo"),
    "src_not_eligible": re.compile(r"source (\w+) is not eligible for transbordo, skipping transbordo check for ticket id (\d+)"),
    "flag_off": re.compile(r"enable_transbordo is false, skipping transbordo check for ticket id (\d+)"),
    "created_at": re.compile(r"fetched ticket timestamp data from Zendesk for ticket id (\d+), created_at: (\S+)"),
    "jira_found": re.compile(r"found (\d+) Jira tickets for ticket id (\d+), (\d+) eligible for transbordo"),
    "jira_skip": re.compile(r"skipping transbordo record creation for parent_ticket_id (\d+) with issue_key (\S+) from instance (\S+) (.+)$"),
    "jira_saved": re.compile(r"saved transbordo record for parent_ticket_id (\d+) with issue_key (\S+)"),
    "bpmp_found": re.compile(r"found (\d+) parallel conversation transbordos for ticket id (\d+)"),
    "pending": re.compile(r"finished fetching tickets transbordo for source (\w+) and ticket id (\d+), found (\d+) records"),
    "block_jira": re.compile(r"blocking CSAT survey for ticket_id (\d+): eligible Jira tickets found"),
    "released": re.compile(r"no pending transbordo found for cnpj (\S+) and ticket id (\d+), survey csat is released"),
    "held": re.compile(r"ticket id (\d+) has transbordo in progress, holding survey csat"),
    "sending": re.compile(r"ticket id (\d+): sending survey csat for cnpj (\S+) by rule (\w+) with template (\S+)"),
    "dispatched": re.compile(r"ticket id (\d+) had survey csat dispatched by (\w+)"),
    "no_requirement": re.compile(r"ticket id (\d+) hasnt match any requirement"),
    "error": re.compile(r"error processing survey csat engine message for ticket id (\d+)"),
}
LEGACY_DECISIONS = ("dispatched", "held", "invalid", "fup_source", "generic", "blocked", "microtema", "no_requirement", "error")

SKIP_REASONS = [  # legacy jira_skip tail -> cause
    (re.compile(r"created at (\S+), before the parent ticket"), "JIRA_ANTERIOR_AO_ATENDIMENTO"),
    (re.compile(r"the ticket is resolved"), "JIRA_JA_RESOLVIDO"),
    (re.compile(r"project (\S+) is not eligible for transbordo"), "JIRA_PROJETO_NAO_ELEGIVEL"),
    (re.compile(r"due_date is null"), "JIRA_SEM_DUE_DATE"),
    (re.compile(r"due_date (\S+) is (-?\d+) hours away"), "DUE_DATE_ACIMA_48H"),
    (re.compile(r"field demanda_preventiva is empty"), "DEMANDA_PREVENTIVA_VAZIA"),
    (re.compile(r"as preventive demand"), "DEMANDA_PREVENTIVA"),
]
JIRA_RULE = {  # cause -> (rule code, rule text)
    "JIRA_ANTERIOR_AO_ATENDIMENTO": ("R12", "Jira criado depois do ticket pai"),
    "JIRA_JA_RESOLVIDO": ("R13", "Jira não está fechado"),
    "JIRA_PROJETO_NAO_ELEGIVEL": ("R14", "Projeto elegível (EXPBKO com SLA ou NFEXP)"),
    "JIRA_SEM_DUE_DATE": ("R14", "EXPBKO com due_date <= 48h"),
    "DUE_DATE_ACIMA_48H": ("R14", "EXPBKO com due_date <= 48h"),
    "DEMANDA_PREVENTIVA_VAZIA": ("R15", "Demanda preventiva preenchida e = Não"),
    "DEMANDA_PREVENTIVA": ("R15", "Demanda preventiva preenchida e = Não"),
}


def parse_ts(value):
    if value is None or value == "":
        return None
    if isinstance(value, dt.datetime):
        return value if value.tzinfo else value.replace(tzinfo=dt.timezone.utc)
    s = str(value).strip().replace(" ", "T", 1)
    s = re.sub(r"Z$", "+00:00", s)
    s = re.sub(r"([+-]\d\d)$", r"\1:00", s)
    m = re.match(r"^(.*?\.\d{1,6})\d*(.*)$", s)
    if m:
        s = m.group(1) + m.group(2)
    try:
        d = dt.datetime.fromisoformat(s)
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=dt.timezone.utc)


def brt(d):
    return (d - dt.timedelta(hours=3)).strftime("%d/%m/%Y %H:%M:%S") + " BRT" if d else ""


def minutes(a, b):
    return round((a - b).total_seconds() / 60)


def valid_cnpj(c):
    return bool(c) and re.fullmatch(r"[0-9A-Z]{14}", c) is not None


# ---------------------------------------------------------------------------------------------
# Data sources


def gcloud_read(flt, freshness):
    cmd = ["gcloud", "logging", "read", flt, "--project", LOG_PROJECT, f"--freshness={freshness}", "--format=json", "--limit=20000"]
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    if res.returncode != 0:
        sys.exit(f"gcloud logging read falhou: {res.stderr.strip()[:500]}")
    return json.loads(res.stdout or "[]")


def read_logs(ticket_ids, freshness, base_filter, batch_size=15):
    out = {t: [] for t in ticket_ids}
    for i in range(0, len(ticket_ids), batch_size):
        batch = ticket_ids[i:i + batch_size]
        text = " OR ".join(f'"{t}"' for t in batch)
        for e in gcloud_read(f"{base_filter} AND ({text})", freshness):
            p = e.get("jsonPayload") or {}
            msg = p.get("message") or p.get("msg") or e.get("textPayload") or ""
            item = {"ts": parse_ts(e.get("timestamp")), "msg": msg, "p": p, "svc": (e.get("resource") or {}).get("labels", {}).get("container_name")}
            for t in batch:
                if str(p.get("ticketId")) == str(t) or re.search(rf"\b{t}\b", msg):
                    out[t].append(item)
    for t in out:
        out[t].sort(key=lambda x: x["ts"])
    return out


def psql_json(service, sql):
    wrapped = f"select coalesce(json_agg(t), '[]'::json) from ({sql}) t"
    env = {**os.environ, "PGCONNECT_TIMEOUT": "15", "PGOPTIONS": "-c statement_timeout=90000"}
    try:
        res = subprocess.run(["psql", "-w", f"service={service}", "-At", "-v", "ON_ERROR_STOP=1", "-c", wrapped], capture_output=True, text=True, timeout=120, env=env)
    except subprocess.TimeoutExpired:
        print(f"[aviso] {service}: consulta passou de 120 s (proxy travado?)", file=sys.stderr)
        return None
    if res.returncode != 0:
        err = res.stderr.strip().splitlines()
        print(f"[aviso] {service}: {err[0] if err else 'erro'}", file=sys.stderr)
        return None
    return json.loads(res.stdout.strip() or "[]")


class Db:
    def __init__(self, enabled):
        self.enabled = enabled
        self.down = set()

    def q(self, service, sql):
        if not self.enabled or service in self.down:
            return None
        rows = psql_json(service, sql)
        if rows is None:
            self.down.add(service)
        return rows

    def ok(self, service):
        return self.enabled and service not in self.down


# ---------------------------------------------------------------------------------------------
# Report helpers


def new_report(tid):
    return {
        "ticket_id": tid, "engine": "", "cnpj": "", "source": "", "enable_transbordo": "",
        "ticket_created_at": None, "solved_at": None, "received_at": None, "engine_at": None, "runs": 0,
        "csat_sent": "", "regra_envio": "", "transbordo_segurou": "", "found": False, "cause_code": "",
        "cause": "", "checks": [], "jiras": [], "jiras_detail": [], "ticket_off": [], "transbordo_rows": [],
        "survey_rows": [], "notes": [], "_offs": None, "_tj": None,
    }


def check(r, code, rule, status, detail=""):
    r["checks"].append({"code": code, "rule": rule, "status": status, "detail": detail})


def fmt(code, kw):
    try:
        return CAUSES[code][1].format(**kw)
    except KeyError:
        return CAUSES[code][1]


def set_cause(r, code, force=False, **kw):
    if r["cause_code"] and not force:
        r["notes"].append(f"[{code}] {fmt(code, kw)}")
        return
    r["cause_code"], r["found"], r["cause"] = code, CAUSES[code][0], fmt(code, kw)


def load_base(r, db):
    tid = r["ticket_id"]
    zd = (db.q(DB_ZENDESK, f"select id, status, via, created_at, organization_external_id, organization_cnpj, group_name, assignee_email from tickets where id = {tid}") or [None])[0]
    r["_zd"] = zd
    if zd:
        r["cnpj"] = re.sub(r"[^0-9A-Za-z]", "", zd.get("organization_external_id") or zd.get("organization_cnpj") or "").upper()
        r["ticket_created_at"] = parse_ts(zd.get("created_at"))
    r["survey_rows"] = db.q(DB_EXPERTS, f"select id, status, regra, template, csat_kind, source, created_at, survey_service_id from survey_csat_sent where id_ticket = {tid} order by id") or []
    r["transbordo_rows"] = db.q(DB_EXPERTS, f"select id, parent_ticket_id, fup_ticket_id, status, jira_ticket_id, created_at, survey_service_id from ticket_transbordo where parent_ticket_id = {tid} order by id") or []


def jiras_of_cnpj(r, db):
    if r["_tj"] is not None:
        return r["_tj"]
    rows = []
    if valid_cnpj(r["cnpj"]) and (r["ticket_created_at"] or r["engine_at"]):
        start = (r["ticket_created_at"] or r["engine_at"]) - dt.timedelta(days=15)
        end = (r["engine_at"] or dt.datetime.now(dt.timezone.utc)) + dt.timedelta(days=3)
        rows = db.q(DB_TICKETING, f"select issue_key, project_key, status, status_name, created_at, updated_at, due_date, instance_name, metadata from ticket_jira where cnpj = '{r['cnpj']}' and created_at between '{start.isoformat()}' and '{end.isoformat()}' order by created_at") or []
    r["_tj"] = rows
    return rows


def jira_eval(j, engine_at, parent_created):
    """Re-evaluate a ticket_jira row (current state) with isJiraEligible at the engine time.

    Returns (cause or None, info dict)."""
    created = parse_ts(j.get("created_at"))
    due = parse_ts(j.get("due_date"))
    updated = parse_ts(j.get("updated_at"))
    meta = j.get("metadata") or {}
    dp = meta.get("demanda_preventiva")
    dp = dp.get("value") if isinstance(dp, dict) else dp
    info = {"created": created, "due": due, "updated": updated, "dp": dp, "changed_after": bool(engine_at and updated and updated > engine_at)}
    if engine_at and created and created > engine_at:
        return "JIRA_CRIADO_APOS_MOTOR", info
    if parent_created and created and created < parent_created:
        return "JIRA_ANTERIOR_AO_ATENDIMENTO", info
    if j.get("status") == "closed" and not info["changed_after"]:
        return "JIRA_JA_RESOLVIDO", info
    if j["project_key"] not in DUE_DATE_IGNORED_PROJECTS:
        if j["project_key"] not in SLA_48H_PROJECTS:
            return "JIRA_PROJETO_NAO_ELEGIVEL", info
        if not due:
            return "JIRA_SEM_DUE_DATE", info
        if engine_at:
            hours = int((due - engine_at).total_seconds() / 3600)
            info["hours"] = hours
            if hours > SLA_LIMIT_HOURS:
                return "DUE_DATE_ACIMA_48H", info
    if dp is None:
        return "DEMANDA_PREVENTIVA_VAZIA", info
    if dp == "Sim":
        return "DEMANDA_PREVENTIVA", info
    return None, info


def jira_line(j, cause, info):
    return f"{j['issue_key']} ({j['project_key']}): criado {brt(info['created'])}, {j['status_name']}, due {brt(info['due']) or 'vazio'}, preventiva {info['dp']}, atualizado {brt(info['updated'])} → {cause or 'passaria hoje'}"


def explain_release_jira(r, db, from_logs_found=None):
    """Explain a released JIRA-kind ticket by re-evaluating the CNPJ's Jira tickets."""
    if not db.ok(DB_TICKETING):
        set_cause(r, "INDETERMINADO", detail="banco do ticketing indisponível para reavaliar os Jiras")
        return
    engine_at, parent = r["engine_at"], r["ticket_created_at"]
    rows = jiras_of_cnpj(r, db)
    relevant = [j for j in rows if not parent or parse_ts(j["created_at"]) >= parent - dt.timedelta(days=1)]
    evals = []
    for j in relevant:
        cause, info = jira_eval(j, engine_at, parent)
        evals.append((j, cause, info))
        r["jiras_detail"].append(jira_line(j, cause, info))
    if not relevant:
        set_cause(r, "SEM_JIRA_PARA_O_CNPJ", cnpj=r["cnpj"], extra=ticket_off_hint(r, db))
        return
    # Priority: Jira that would pass today but changed (state at engine time unknown), late Jira, the rest.
    in_window = [x for x in evals if x[1] != "JIRA_ANTERIOR_AO_ATENDIMENTO"] or evals
    for j, cause, info in in_window:
        code, text = JIRA_RULE.get(cause, ("R12", "Jira criado antes do motor decidir")) if cause else ("R12-R15", "Jira elegível")
        check(r, code, f"[{j['issue_key']}] {text}", "BLOQUEOU" if cause else "PASSARIA HOJE", jira_line(j, cause, info))
    passing = [x for x in in_window if x[1] is None]
    if passing:
        j, _, info = passing[0]
        if info["changed_after"]:
            set_cause(r, "JIRA_ESTADO_MUDOU", jira=j["issue_key"], mudou=f"atualizado {brt(info['updated'])}", engine=brt(engine_at))
        else:
            set_cause(r, "INDETERMINADO", detail=f"o Jira {j['issue_key']} passaria nas regras e não mudou depois do motor; conferir o ticketing (CNPJ do Jira) e o enable_transbordo")
        return
    j, cause, info = in_window[0]
    kw = {"jira": j["issue_key"], "engine": brt(engine_at), "projeto": j["project_key"], "criado": brt(info["created"]), "pai": brt(parent), "due": brt(info["due"]), "horas": info.get("hours", "?"), "prov": ""}
    if cause == "JIRA_CRIADO_APOS_MOTOR":
        kw["minutos"] = minutes(info["created"], engine_at)
    if cause in ("JIRA_SEM_DUE_DATE", "DEMANDA_PREVENTIVA_VAZIA") and info["changed_after"]:
        kw["prov"] = " (o Jira mudou depois do motor: conferir o changelog)"
    set_cause(r, cause, **kw)


def ticket_off_candidates(r, db):
    if r["_offs"] is not None:
        return r["_offs"]
    rows = []
    parent = r["ticket_created_at"]
    if valid_cnpj(r["cnpj"]) and parent:
        rows = db.q(DB_ZENDESK, f"select id, status, via, created_at, updated_at, group_name, tags from tickets where organization_external_id = '{r['cnpj']}' and created_at >= '{parent.isoformat()}' and created_at <= '{(parent + dt.timedelta(days=7)).isoformat()}' and id <> {r['ticket_id']} order by created_at") or []
    # Follow-ups and the answers to the survey itself (group "... CSAT - Respostas") are not ticket off.
    rows = [x for x in rows if x.get("via") != "Ticket fechado" and "CSAT" not in (x.get("group_name") or "")]
    r["_offs"] = rows
    r["ticket_off"] = [f"{x['id']} via {x['via']} ({x['status']}) {brt(parse_ts(x['created_at']))} [{x.get('group_name') or ''}]{' jira_escalated' if 'jira_escalated' in (x.get('tags') or []) else ''}" for x in rows]
    return rows


def ticket_off_hint(r, db):
    offs = ticket_off_candidates(r, db)
    return (" Tickets do CNPJ abertos depois do atendimento: " + "; ".join(r["ticket_off"][:5]) + ".") if offs else ""


def explain_release_bpmp(r, db):
    if not db.ok(DB_ZENDESK):
        set_cause(r, "INDETERMINADO", detail="banco do atendimento-zendesk indisponível para reavaliar os tickets off")
        return
    offs = ticket_off_candidates(r, db)
    engine_at = r["engine_at"]
    parallel = [x for x in offs if x["via"] == BPMP_VIA]
    late = [x for x in parallel if engine_at and parse_ts(x["created_at"]) > engine_at]
    if late:
        x = late[0]
        set_cause(r, "BPMP_TICKET_OFF_APOS_MOTOR", ticket=x["id"], minutos=minutes(parse_ts(x["created_at"]), engine_at), engine=brt(engine_at))
    elif parallel:
        x = parallel[0]
        set_cause(r, "INDETERMINADO", detail=f"o ticket {x['id']} via Conversa paralela existia antes do motor; pode ter sido resolvido antes (status hoje {x['status']})")
    elif offs:
        x = offs[0]
        set_cause(r, "BPMP_TICKET_OFF_VIA_DIFERENTE", ticket=x["id"], via=x["via"])
    else:
        set_cause(r, "BPMP_SEM_TICKET_OFF", cnpj=r["cnpj"])


def pending_note(r, db):
    if valid_cnpj(r["cnpj"]) and r["engine_at"]:
        rows = db.q(DB_EXPERTS, f"select id, parent_ticket_id, status, jira_ticket_id, fup_ticket_id, created_at from ticket_transbordo where organization_cnpj = '{r['cnpj']}' and created_at between '{(r['engine_at'] - dt.timedelta(days=30)).isoformat()}' and '{(r['engine_at'] + dt.timedelta(days=7)).isoformat()}' order by id")
        if rows:
            r["notes"].append("ticket_transbordo do CNPJ (±30d): " + "; ".join(f"{p['id']} pai {p['parent_ticket_id']} {p['status']} {p.get('jira_ticket_id') or p.get('fup_ticket_id') or ''} {brt(parse_ts(p['created_at']))}" for p in rows))


# ---------------------------------------------------------------------------------------------
# Legacy engine (experts-service)


def legacy_last_run(entries):
    runs, cur = [], None
    for e in entries:
        if P["received"].search(e["msg"]):
            cur = {"received": e, "items": [e]}
            runs.append(cur)
        elif cur is not None:
            cur["items"].append(e)
        elif P["running"].search(e["msg"]):
            cur = {"received": None, "items": [e]}
            runs.append(cur)
    if not runs:
        return 0, None
    decided = [x for x in runs if any(P[k].search(i["msg"]) for i in x["items"] for k in LEGACY_DECISIONS)]
    return len(runs), (decided or runs)[-1]


def analyze_legacy(r, run, db):
    items = run["items"]

    def first(key):
        for e in items:
            m = P[key].search(e["msg"])
            if m:
                return e, m
        return None, None

    def all_of(key):
        return [(e, P[key].search(e["msg"])) for e in items if P[key].search(e["msg"])]

    rec = run["received"]
    if rec:
        p = rec["p"]
        r["received_at"] = rec["ts"]
        r["source"] = P["received"].search(rec["msg"]).group(2)
        r["enable_transbordo"] = str(p.get("enable_transbordo")).lower() if "enable_transbordo" in p else "?"
        r["cnpj"] = re.sub(r"[^0-9A-Za-z]", "", str(p.get("organization_cnpj") or "")).upper() or r["cnpj"]
        check(r, "R01", "Motor CSAT acionado pelo gatilho do Zendesk", "OK", f"{brt(rec['ts'])}, source {r['source']}, group {p.get('group_id')}")
    else:
        e, m = first("running")
        r["source"] = m.group(2) if m else ""
        r["enable_transbordo"] = "?"
        check(r, "R01", "Motor CSAT acionado pelo gatilho do Zendesk", "?", "a linha 'received' ficou fora da janela de logs")

    src_ok = r["source"] in TRANSBORDO_KIND
    flag = r["enable_transbordo"]
    check(r, "R02", "Origem com transbordo (HUMAN_EXPERTS/HUMAN_BPMP)", "OK" if src_ok else "BLOQUEOU", r["source"])
    check(r, "R03", "enable_transbordo=true no payload do gatilho", {"true": "OK", "?": "?"}.get(flag, "BLOQUEOU"), flag)
    e_sched, _ = first("scheduled")
    e_run, _ = first("running")
    r["engine_at"] = e_run["ts"] if e_run else None
    if r["source"] == "HUMAN_EXPERTS" and flag == "true":
        check(r, "R04", f"Atraso de {DELAY_MIN} min antes do motor (só HUMAN_EXPERTS)", "OK" if e_sched and e_run else "?", f"agendado {brt(e_sched['ts']) if e_sched else '?'} → executado {brt(e_run['ts']) if e_run else '?'}")
    elif r["source"] == "HUMAN_BPMP":
        check(r, "R04", f"Atraso de {DELAY_MIN} min antes do motor (só HUMAN_EXPERTS)", "N/A", "HUMAN_BPMP roda na hora")

    pre_block = None
    for key, code, rule in [
        ("invalid", "R05", "Payload válido (CNPJ, assignee, telefone, custom fields)"),
        ("fup_source", "R05", "Origem não é o próprio FUP (CSAT_FUP_TRANSBORDO)"),
        ("generic", "R06", "Atendente não é conta genérica"),
        ("blocked", "R07", "CNPJ fora da blocklist de pesquisa"),
        ("microtema", "R08", "Micro tema elegível"),
    ]:
        e, m = first(key)
        if m:
            check(r, code, rule, "BLOQUEOU", m.group(0)[:200])
            pre_block = pre_block or m.group(0)[:200]
    if not pre_block:
        e, m = first("context")
        check(r, "R05-R08", "Payload, conta genérica, blocklist e micro tema", "OK" if m else "?", f"template {m.group(4)}" if m else "")

    for key, st in (("limit_reached", "NÃO"), ("limit_ok", "OK"), ("no_quarantine", "OK")):
        e, m = first(key)
        if m:
            check(r, "R09a", "Limite convencional de pesquisas (quarentena)", st, m.group(0)[:160])
    e, m_match = first("matched")
    e, m_noreq = first("no_requirement")
    if m_match:
        check(r, "R09", "Regra de envio do CSAT casou (limite/prioridade)", "OK", m_match.group(2))
    elif m_noreq:
        check(r, "R09", "Regra de envio do CSAT casou (limite/prioridade)", "NÃO", "limite atingido e sem prioridade")
        pre_block = pre_block or "nenhuma regra de envio casou (limite atingido e sem prioridade de micro tema/assessor)"

    e_err, m_err = first("error")
    if m_err and not first("dispatched")[1] and not first("held")[1]:
        r["csat_sent"] = "não"
        set_cause(r, "ERRO_NO_MOTOR", detail=f"{brt(e_err['ts'])}; ver o stack no Cloud Logging")
        return
    if pre_block:
        r["csat_sent"], r["transbordo_segurou"] = "não", "N/A"
        set_cause(r, "CSAT_NAO_ELEGIVEL", detail=pre_block)
        return

    if first("src_not_eligible")[1] or not src_ok:
        set_cause(r, "ORIGEM_FORA_DO_TRANSBORDO", source=r["source"])
    elif first("flag_off")[1] or flag == "false":
        set_cause(r, "FLAG_ENABLE_TRANSBORDO_DESLIGADA", inferido="")

    e, m = first("created_at")
    if m:
        r["ticket_created_at"] = parse_ts(m.group(2))
        check(r, "R10", "Data de criação do ticket pai (Zendesk)", "OK", brt(r["ticket_created_at"]))

    if r["source"] == "HUMAN_EXPERTS" and flag == "true":
        e, m = first("jira_found")
        found = int(m.group(1)) if m else None
        eligible = int(m.group(3)) if m else None
        r["jiras"] = (e["p"].get("jira_issue_keys") if e else None) or []
        check(r, "R11", "Jiras do CNPJ no ticketing (projetos monitorados, criados depois do pai)", "OK" if found else ("NÃO" if found == 0 else "?"), f"{found} encontrado(s): {', '.join(r['jiras'])}" if found is not None else "")
        tj = {j["issue_key"]: j for j in jiras_of_cnpj(r, db)}
        for e, m in all_of("jira_skip"):
            key, tail = m.group(2), m.group(4)
            cause = next((c for rx, c in SKIP_REASONS if rx.search(tail)), None)
            row = tj.get(key)
            now_cause, info = jira_eval(row, r["engine_at"], r["ticket_created_at"]) if row else (None, None)
            code, text = JIRA_RULE.get(cause, ("R12-R15", "Regra do Jira"))
            check(r, code, f"[{key}] {text}", "BLOQUEOU", tail)
            if row:
                r["jiras_detail"].append(f"{key}: descartado pelo motor ({tail}); hoje: {jira_line(row, now_cause, info)}")
            kw = {"jira": key, "engine": brt(r["engine_at"]), "prov": ""}
            if cause == "JIRA_SEM_DUE_DATE" and info and info["due"]:
                again, _ = jira_eval({**row, "status": "open"}, r["engine_at"], r["ticket_created_at"])
                kw.update(due=brt(info["due"]), teria="teria segurado a pesquisa" if again is None else f"ainda seria descartado ({again})")
                set_cause(r, "DUE_DATE_PREENCHIDO_APOS_MOTOR", **kw)
            elif cause == "JIRA_ANTERIOR_AO_ATENDIMENTO":
                set_cause(r, cause, criado=brt(info["created"]) if info else "?", pai=brt(r["ticket_created_at"]), **kw)
            elif cause == "JIRA_PROJETO_NAO_ELEGIVEL":
                mm = re.search(r"project (\S+)", tail)
                set_cause(r, cause, projeto=mm.group(1) if mm else "?", **kw)
            elif cause == "DUE_DATE_ACIMA_48H":
                mm = re.search(r"due_date (\S+) is (-?\d+) hours", tail)
                set_cause(r, cause, due=mm.group(1) if mm else "?", horas=mm.group(2) if mm else "?", **kw)
            elif cause:
                set_cause(r, cause, **kw)
        for e, m in all_of("jira_saved"):
            check(r, "R12-R15", f"[{m.group(2)}] Jira elegível → grava ticket_transbordo PENDING", "SEGUROU")
        if eligible is not None:
            check(r, "R16", "Algum Jira elegível → segura", "SEGUROU" if eligible else "NÃO", f"{eligible} elegível(is)")
        if found == 0:
            explain_release_jira(r, db)
    elif r["source"] == "HUMAN_BPMP" and flag == "true":
        e, m = first("bpmp_found")
        n = int(m.group(1)) if m else None
        ids = (e["p"].get("transbordo_ticket_ids") if e else None) or []
        check(r, "R11b", f"Tickets '{BPMP_VIA}' abertos do CNPJ, criados depois do pai", "OK" if n else ("NÃO" if n == 0 else "?"), f"{n} encontrado(s) {ids}" if n is not None else "")
        if n == 0:
            explain_release_bpmp(r, db)

    e, m = first("pending")
    if m:
        check(r, "R17", "Há transbordo PENDING para o CNPJ (qualquer ticket) → segura", "SEGUROU", f"{m.group(3)} registro(s): {e['p'].get('pending_transbordo_ids')}")
    elif first("released")[1]:
        check(r, "R17", "Há transbordo PENDING para o CNPJ (qualquer ticket) → segura", "NÃO", "nenhum PENDING")

    e_held, m_held = first("held")
    e_disp, m_disp = first("dispatched")
    e_send, m_send = first("sending")
    if m_held:
        r["transbordo_segurou"], r["csat_sent"] = "sim", "não (segurado)"
        det = [x for x, k in (("PENDING do CNPJ", "pending"), ("Jira elegível", "block_jira")) if first(k)[1]]
        set_cause(r, "TRANSBORDO_SEGUROU", force=True, detail=", ".join(det) or "ver logs")
        check(r, "DEC", "Decisão do motor", "SEGUROU", brt(e_held["ts"]))
    elif m_disp or m_send:
        r["transbordo_segurou"], r["csat_sent"] = "não", "sim"
        r["regra_envio"] = m_send.group(3) if m_send else m_disp.group(2)
        check(r, "DEC", "Decisão do motor", "LIBEROU", f"pesquisa enviada {brt((e_send or e_disp)['ts'])} pela regra {r['regra_envio']}")
        if not r["cause_code"]:
            set_cause(r, "INDETERMINADO", detail="ver o checklist e os Jiras/tickets do CNPJ")


# ---------------------------------------------------------------------------------------------
# Current engine (survey-service)

SS_OUTCOME = re.compile(r"^CSAT (DISPATCHED|HELD|SKIPPED)$")
SS_IGNORED = re.compile(r"^CSAT ignorado: (.+)$")
SS_SCHEDULED = re.compile(r"^CSAT agendado para a abertura do expediente")
SS_DISCARDED = re.compile(r"^CSAT descartado: (.+)$")


def solve_time_before(solves, decision_at):
    """Start of the last burst of 'closed or solved' logs before the decision (the solve moment)."""
    prior = [s for s in solves if decision_at is None or s <= decision_at]
    if not prior:
        return None
    start = prior[-1]
    for s in reversed(prior[:-1]):
        if (start - s).total_seconds() <= 120:
            start = s
        else:
            break
    return start


def analyze_survey_service(r, entries, solves, db):
    decisions = [e for e in entries if SS_OUTCOME.match(e["msg"]) or SS_IGNORED.match(e["msg"]) or SS_DISCARDED.match(e["msg"])]
    sched = [e for e in entries if SS_SCHEDULED.match(e["msg"])]
    r["runs"] = len(decisions)
    if len(decisions) > 1:
        r["notes"].append(f"O survey-service decidiu {len(decisions)} vezes para o ticket (reabertura/novo solved); o relatório usa a última.")
    last = decisions[-1] if decisions else None
    if not last:
        if sched:
            e = sched[-1]
            check(r, "R01", "Motor CSAT (survey-service) acionado", "OK", brt(e["ts"]))
            check(r, "RJ", "Janela de expediente", "AGENDADO", f"para {e['p'].get('scheduledFor')} ({e['p'].get('reason')})")
            set_cause(r, "CSAT_AGENDADO_EXPEDIENTE", detail=f"{e['p'].get('reason')}, para {e['p'].get('scheduledFor')}")
        return
    p = last["p"]
    r["engine_at"] = last["ts"]
    r["source"] = p.get("source") or ((p.get("outcome") or {}).get("dispatch") or {}).get("source") or r["source"]
    kind = TRANSBORDO_KIND.get(r["source"])
    check(r, "R01", "Motor CSAT (survey-service, job csat.request) acionado", "OK", f"decisão {brt(last['ts'])}, source {r['source']}")
    check(r, "R02", "Origem com transbordo (HUMAN_EXPERTS → Jira, HUMAN_BPMP → conversa paralela)", "OK" if kind else "BLOQUEOU", r["source"])
    if sched:
        check(r, "RJ", "Janela de expediente", "AGENDADO", f"agendado {brt(sched[-1]['ts'])} para {sched[-1]['p'].get('scheduledFor')}; decidiu na abertura")

    m = SS_IGNORED.match(last["msg"])
    if m:
        check(r, "R05", "prepareRequest (assignee, identificador, telefone, conta genérica)", "BLOQUEOU", m.group(1))
        r["csat_sent"], r["transbordo_segurou"] = "não", "N/A"
        set_cause(r, "CSAT_NAO_ELEGIVEL", detail=m.group(1))
        return
    m = SS_DISCARDED.match(last["msg"])
    if m:
        check(r, "RJ", "Janela de expediente", "DESCARTOU", m.group(1))
        r["csat_sent"], r["transbordo_segurou"] = "não", "N/A"
        set_cause(r, "CSAT_NAO_ELEGIVEL", detail=f"janela de expediente: {m.group(1)}")
        return

    outcome = (p.get("outcome") or {}).get("outcome") or SS_OUTCOME.match(last["msg"]).group(1)
    r["solved_at"] = solve_time_before(solves, r["engine_at"])
    gap = minutes(r["engine_at"], r["solved_at"]) if r["solved_at"] else None
    if outcome == "HELD" or r["transbordo_rows"]:
        r["enable_transbordo"] = "true"
        flag_detail = "inferido: o transbordo foi avaliado"
    elif kind == "JIRA" and gap is not None:
        r["enable_transbordo"] = "true (inferido)" if gap >= DELAY_MIN - 1 else "false (inferido)"
        flag_detail = f"inferido pelo atraso solved → decisão de {gap} min (com a flag o job espera {DELAY_MIN} min)"
    else:
        r["enable_transbordo"] = "?"
        flag_detail = "o survey-service não loga a flag; sem atraso para inferir" if kind == "PARALLEL_CONVERSATION" else "sem horário do solved para inferir"
    flag_true = r["enable_transbordo"].startswith("true")
    if kind:
        check(r, "R03", "enable_transbordo=true no payload do gatilho", "OK" if flag_true else ("?" if r["enable_transbordo"] == "?" else "BLOQUEOU"), flag_detail)
    if kind == "JIRA":
        check(r, "R04", f"Atraso de {DELAY_MIN} min antes da decisão (só transbordo JIRA)", "OK" if gap is not None and gap >= DELAY_MIN - 1 else ("?" if gap is None else "NÃO"), f"solved {brt(r['solved_at'])} → decisão {brt(r['engine_at'])}" if r["solved_at"] else "solved não encontrado nos logs do zendesk-agents")
    elif kind:
        check(r, "R04", f"Atraso de {DELAY_MIN} min (só transbordo JIRA)", "N/A", "HUMAN_BPMP decide na hora")
    check(r, "R10", "Data de criação do ticket pai (atendimento-zendesk)", "OK" if r["ticket_created_at"] else "?", brt(r["ticket_created_at"]))

    if outcome == "SKIPPED":
        verdicts = (p.get("outcome") or {}).get("verdicts")
        check(r, "R09", "Regra de envio (LIMITE_NAO_ATINGIDO → ASSESSOR_PRIORITARIO)", "NÃO", json.dumps(verdicts, ensure_ascii=False)[:300])
        r["csat_sent"], r["transbordo_segurou"] = "não", "N/A"
        set_cause(r, "CSAT_NAO_ELEGIVEL", detail=f"nenhuma regra de envio casou: {json.dumps(verdicts, ensure_ascii=False)[:200]}")
        return
    rule = (p.get("outcome") or {}).get("rule") or ((p.get("outcome") or {}).get("dispatch") or {}).get("rule")
    check(r, "R09", "Regra de envio (LIMITE_NAO_ATINGIDO → ASSESSOR_PRIORITARIO)", "OK", rule or "")

    if outcome == "HELD":
        r["transbordo_segurou"], r["csat_sent"] = "sim", "não (segurado)"
        mine = ", ".join(f"{t['id']} {t['status']} {t.get('jira_ticket_id') or t.get('fup_ticket_id') or ''}".strip() for t in r["transbordo_rows"])
        check(r, "DEC", "Decisão do motor", "SEGUROU", brt(r["engine_at"]))
        set_cause(r, "TRANSBORDO_SEGUROU", force=True, detail=f"ticket_transbordo do ticket: {mine}" if mine else "PENDING de outro ticket do mesmo CNPJ")
        return

    r["transbordo_segurou"], r["csat_sent"], r["regra_envio"] = "não", "sim", rule or ""
    if not kind:
        set_cause(r, "ORIGEM_FORA_DO_TRANSBORDO", source=r["source"])
    elif r["enable_transbordo"].startswith("false"):
        set_cause(r, "FLAG_ENABLE_TRANSBORDO_DESLIGADA", inferido=f" ({flag_detail})")
    elif kind == "JIRA":
        explain_release_jira(r, db)
    else:
        explain_release_bpmp(r, db)
    check(r, "DEC", "Decisão do motor", "LIBEROU", f"pesquisa enviada {brt(r['engine_at'])} pela regra {rule}")
    if r["enable_transbordo"] == "?" and r["cause_code"] in ("BPMP_SEM_TICKET_OFF", "SEM_JIRA_PARA_O_CNPJ", "INDETERMINADO"):
        r["notes"].append("enable_transbordo não pôde ser confirmado: se a flag estava desligada, essa é a causa.")


def ticket_off_role(r, tid, entries, db):
    """Detect when the given ticket is the follow-up (ticket off) of a transbordo, not the attendance.

    Evidence: the legacy ticket-off webhook logs ("fetching transbordo for ticket_id X by jira issues [...]"),
    a ticket_transbordo row with fup_ticket_id = X, or the jira_escalated tag. Returns the cause kwargs or None."""
    zd = r.get("_zd") or {}
    jiras, solved_at, not_found = [], None, False
    for e in entries:
        m = re.search(rf"fetching transbordo for ticket_id {tid} by jira issues \[(.*?)\]", e["msg"])
        if m:
            jiras = re.findall(r"[A-Z][A-Z0-9]+-\d+", m.group(1)) or jiras
            solved_at = e["ts"]
        if re.search(rf"parent ticket not found for ticket id {tid}\b", e["msg"]):
            not_found = True
    tt = db.q(DB_EXPERTS, f"select id, parent_ticket_id, status, jira_ticket_id, created_at from ticket_transbordo where fup_ticket_id = {tid}" + (" or jira_ticket_id in (" + ",".join(f"'{j}'" for j in jiras) + ")" if jiras else "") + " order by id") or []
    tags = db.q(DB_ZENDESK, f"select tags::text as tags from tickets where id = {tid}") or []
    escalated = bool(tags) and "jira_escalated" in (tags[0].get("tags") or "")
    if not (solved_at or tt or escalated):
        return None
    pai = tt[0]["parent_ticket_id"] if tt else None
    if not pai and valid_cnpj(r["cnpj"]) and zd.get("created_at"):
        # The attendance is the human ticket that went through the CSAT engine; WhatsApp ticket as fallback.
        prev = db.q(DB_EXPERTS, f"select id_ticket as id from survey_csat_sent where cnpj = '{r['cnpj']}' and source in ('HUMAN_EXPERTS', 'HUMAN_BPMP') and id_ticket < {tid} and created_at between timestamptz '{zd['created_at']}' - interval '2 days' and timestamptz '{zd['created_at']}' + interval '2 days' order by id_ticket desc limit 1") or []
        if not prev:
            prev = db.q(DB_ZENDESK, f"select id from tickets where organization_external_id = '{r['cnpj']}' and id <> {tid} and via in ('WhatsApp', 'Conversa paralela') and group_name not like '%CSAT%' and created_at <= '{zd['created_at']}' and created_at >= timestamptz '{zd['created_at']}' - interval '2 days' order by created_at desc limit 1") or []
        pai = prev[0]["id"] if prev else "?"
    check(r, "OFF", "Ticket off do transbordo", "SIM", ", ".join(x for x in (f"Jira {', '.join(jiras)}" if jiras else "", "tag jira_escalated" if escalated else "", f"ticket_transbordo {[x['id'] for x in tt]}" if tt else "") if x))
    if tt:
        fup = "Transbordo(s) dele: " + "; ".join(f"{x['id']} (pai {x['parent_ticket_id']}, {x['status']})" for x in tt) + "."
    elif solved_at:
        fup = f"Quando foi resolvido ({brt(solved_at)}), o fluxo do FUP procurou o transbordo" + (f" pelo Jira {', '.join(jiras)}" if jiras else "") + (" e não achou (parent ticket not found)" if not_found else "") + ": o atendimento não tinha sido segurado, então não havia transbordo e o FUP não saiu."
        check(r, "FUP", "FUP do ticket off resolvido", "NÃO", "nenhum ticket_transbordo para o Jira/ticket off")
    else:
        fup = "Não há ticket_transbordo apontando para ele: o atendimento não foi segurado."
    r["csat_sent"], r["transbordo_segurou"] = "-", "não" if not tt else "sim"
    set_cause(r, "TICKET_OFF_DO_TRANSBORDO", ticket=tid, via=zd.get("via"), grupo=zd.get("group_name"), jiras=f", Jira {', '.join(jiras)}" if jiras else "", fup=fup, pai=pai)
    return r


# ---------------------------------------------------------------------------------------------


def analyze(tid, entries, solves, db):
    r = new_report(tid)
    load_base(r, db)
    legacy = [e for e in entries if e["svc"] == "experts-service" and (e["p"].get("flow") == "csat-engine" or P["sending"].search(e["msg"]) or P["error"].search(e["msg"]) or e["p"].get("name", "").startswith("RunSurveyCsat"))]
    current = [e for e in entries if e["svc"] == "survey-service" and str(e["p"].get("ticketId")) == str(tid) and (SS_OUTCOME.match(e["msg"]) or SS_IGNORED.match(e["msg"]) or SS_DISCARDED.match(e["msg"]) or SS_SCHEDULED.match(e["msg"]))]
    n_runs, run = legacy_last_run(legacy)
    legacy_at = max((e["ts"] for e in run["items"]), default=None) if run else None
    current_at = current[-1]["ts"] if current else None

    if current_at and (not legacy_at or current_at > legacy_at):
        r["engine"] = "survey-service"
        analyze_survey_service(r, current, solves, db)
    elif run:
        r["engine"] = "experts-service"
        r["runs"] = n_runs
        if n_runs > 1:
            r["notes"].append(f"O motor rodou {n_runs} vezes para o ticket; o relatório usa a última execução com decisão.")
        analyze_legacy(r, run, db)
        r["solved_at"] = solve_time_before(solves, r["received_at"] or r["engine_at"])
    else:
        check(r, "R01", "Motor CSAT acionado pelo gatilho do Zendesk", "NÃO", "sem log de decisão no experts-service nem no survey-service")
        zd = r.get("_zd") or {}
        if zd and (zd.get("via") == "Ticket fechado" or "CSAT" in (zd.get("group_name") or "")) and valid_cnpj(r["cnpj"]):
            prev = db.q(DB_EXPERTS, f"select id_ticket, created_at, regra, source from survey_csat_sent where cnpj = '{r['cnpj']}' and created_at <= '{zd['created_at']}' order by created_at desc limit 1") or []
            if prev:
                r["csat_sent"] = "-"
                set_cause(r, "TICKET_DE_RESPOSTA_CSAT", ticket=tid, via=zd.get("via"), grupo=zd.get("group_name"), pai=prev[0]["id_ticket"])
                return r
        if not r["survey_rows"] and ticket_off_role(r, tid, entries, db):
            return r
        if r["survey_rows"]:
            s = r["survey_rows"][-1]
            r["csat_sent"], r["regra_envio"] = "sim", s.get("regra") or ""
            set_cause(r, "CSAT_POR_OUTRO_FLUXO", detail=f"survey_csat_sent {s['id']}, regra {s.get('regra')}, source {s.get('source')}, kind {s.get('csat_kind')}")
        else:
            r["csat_sent"] = "não" if db.ok(DB_EXPERTS) else "?"
            set_cause(r, "SEM_LOG_DO_MOTOR")
        return r

    if r["transbordo_segurou"] == "não":
        ticket_off_candidates(r, db)
        pending_note(r, db)
    return r


CSV_COLUMNS = [
    "ticket_id", "link_zendesk", "motor", "cnpj", "source", "enable_transbordo", "ticket_criado_em", "solved_em",
    "motor_decidiu_em", "execucoes_motor", "csat_enviado", "regra_envio", "transbordo_segurou", "causa_descoberta",
    "codigo_causa", "causa", "detalhe_jiras", "tickets_off_candidatos", "ticket_transbordo_do_ticket",
    "survey_csat_sent", "checklist", "observacoes",
]


def to_row(r):
    return {
        "ticket_id": r["ticket_id"], "link_zendesk": ZD_LINK.format(r["ticket_id"]), "motor": r["engine"],
        "cnpj": r["cnpj"], "source": r["source"], "enable_transbordo": r["enable_transbordo"],
        "ticket_criado_em": brt(r["ticket_created_at"]), "solved_em": brt(r["solved_at"]),
        "motor_decidiu_em": brt(r["engine_at"]), "execucoes_motor": r["runs"], "csat_enviado": r["csat_sent"],
        "regra_envio": r["regra_envio"], "transbordo_segurou": r["transbordo_segurou"],
        "causa_descoberta": "sim" if r["found"] else "não", "codigo_causa": r["cause_code"], "causa": r["cause"],
        "detalhe_jiras": " | ".join(r["jiras_detail"]), "tickets_off_candidatos": " | ".join(r["ticket_off"]),
        "ticket_transbordo_do_ticket": " | ".join(f"{t['id']} {t['status']} {t.get('jira_ticket_id') or t.get('fup_ticket_id') or ''}".strip() for t in r["transbordo_rows"]),
        "survey_csat_sent": " | ".join(f"{s['id']} {s['status']} {s['regra']} {s['template']}" for s in r["survey_rows"]),
        "checklist": " ; ".join(f"{c['code']} {c['status']}" for c in r["checks"]),
        "observacoes": " | ".join(r["notes"]),
    }


def to_md(reports, args):
    lines = [f"# CSAT Transbordo — análise de {len(reports)} ticket(s)", "", f"Gerado em {brt(dt.datetime.now(dt.timezone.utc))}, logs dos últimos {args.freshness}.", ""]
    lines += ["| Ticket | Motor | Origem | CSAT enviado | Transbordo segurou | Causa descoberta | Código |", "|---|---|---|---|---|---|---|"]
    for r in reports:
        lines.append(f"| [{r['ticket_id']}]({ZD_LINK.format(r['ticket_id'])}) | {r['engine'] or '-'} | {r['source'] or '?'} | {r['csat_sent']} | {r['transbordo_segurou']} | {'sim' if r['found'] else 'não'} | `{r['cause_code']}` |")
    for r in reports:
        lines += ["", f"## Ticket {r['ticket_id']}", ""]
        lines.append(f"- **Motor:** {r['engine'] or '-'} · **CNPJ:** {r['cnpj'] or '?'} · **Origem:** {r['source'] or '?'} · **enable_transbordo:** {r['enable_transbordo'] or '?'}")
        lines.append(f"- **Ticket criado:** {brt(r['ticket_created_at'])} · **Solved:** {brt(r['solved_at']) or '-'} · **Motor decidiu:** {brt(r['engine_at'])}")
        lines.append(f"- **Causa ({r['cause_code']}):** {r['cause']}")
        lines += ["", "| Regra | Descrição | Resultado | Detalhe |", "|---|---|---|---|"]
        for c in r["checks"]:
            lines.append(f"| {c['code']} | {c['rule']} | {c['status']} | {str(c['detail']).replace('|', '/')} |")
        for label, items in (("Jiras", r["jiras_detail"]), ("Tickets off candidatos", r["ticket_off"]), ("Observações", r["notes"])):
            if items:
                lines += ["", f"**{label}:**", ""] + [f"- {x}" for x in items]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tickets", nargs="*", help="ids (ou links) de tickets do Zendesk")
    ap.add_argument("--file", help="arquivo com ids/links (um por linha, ou separados por vírgula/espaço)")
    ap.add_argument("--freshness", default="30d", help="janela de logs (padrão 30d, a retenção do _Default)")
    ap.add_argument("--out", help="caminho do CSV (o .md sai ao lado)")
    ap.add_argument("--no-db", action="store_true", help="só logs, sem consultar os bancos")
    args = ap.parse_args()

    raw = " ".join(args.tickets) + (" " + Path(args.file).expanduser().read_text() if args.file else "")
    ids = []
    for tok in re.findall(r"(?:tickets/)?(\d{6,})", raw):
        if int(tok) not in ids:
            ids.append(int(tok))
    if not ids:
        sys.exit("informe ao menos um id de ticket")

    out = Path(args.out).expanduser() if args.out else Path.home() / "Downloads" / f"csat-transbordo-{dt.date.today().isoformat()}.csv"
    out.parent.mkdir(parents=True, exist_ok=True)

    print(f"Lendo logs de {len(ids)} ticket(s) ({args.freshness})...", file=sys.stderr)
    logs = read_logs(ids, args.freshness, ENGINE_LOG_FILTER)
    solves = {t: [e["ts"] for e in v] for t, v in read_logs(ids, args.freshness, SOLVE_LOG_FILTER, batch_size=20).items()}
    db = Db(not args.no_db)
    reports = [analyze(t, logs[t], solves[t], db) for t in ids]
    if db.down:
        print(f"[aviso] bancos indisponíveis (proxy fora?): {', '.join(sorted(db.down))}", file=sys.stderr)

    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        w.writeheader()
        for r in reports:
            w.writerow(to_row(r))
    md = out.with_suffix(".md")
    md.write_text(to_md(reports, args), encoding="utf-8")

    found = sum(1 for r in reports if r["found"])
    print(f"\n{len(reports)} ticket(s), causa descoberta em {found}.")
    for r in reports:
        print(f"- {r['ticket_id']} [{r['engine'] or '-'} {r['source'] or '?'}] csat={r['csat_sent'] or '?'} segurou={r['transbordo_segurou'] or '?'} → {r['cause_code']}: {r['cause']}")
    print(f"\nPlanilha: {out}\nRelatório: {md}")


if __name__ == "__main__":
    main()
