#!/usr/bin/env python3
"""
Collect the evidence to explain why a WhatsApp ticket from the Ultimate bot dropped into a given Zendesk group (N1 Ativação drops by SOCI status, AIDA rollout, ativo return, active company), without calling the Zendesk/Sunshine production API.

Sources (all read-only):
    ticket      prd_crm_atendimento_zendesk.tickets (psql service prd_crm_atendimento_zendesk, proxy sql_crm_prd on 5444; started and stopped here if it was down)
    trail       Cloud Logging, load balancer request logs of api.contabilizei.com.br (projects/contabilizei-prod-01/logs/requests): every GET the bot made with the phone, conversation id, process id or CNPJ in the URL
    state now   bot routes through the atendimento gateway (bots_api.py from the buscar-empresas-por-telefone skill): companies by phone, company by phone+CNPJ, process count and process data

Usage:
    validar_drop.py <ticket id | Zendesk link> [--status "<SOCI status at the time>"] [--processo ID] [--janela-min 180] [--sem-logs] [--json]

The report (Markdown) is printed and saved to ~/Downloads/validar-drop-<ticket>.md. --status overrides the SOCI status used for the expected group (use the status from the SOCI changelog at the conversation time).
"""

import argparse
import json
import re
import socket
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path.home() / ".claude/skills/buscar-empresas-por-telefone/scripts"))
import bots_api as b  # noqa: E402

CFG = json.loads((HERE / "roteamento.json").read_text())
GROUPS = CFG["grupos"]
PG_SERVICE = "prd_crm_atendimento_zendesk"
PROXY_ALIAS, PROXY_PORT = "sql_crm_prd", 5444
BRT = timezone(timedelta(hours=-3))
PROC_PATH = "/atendimento/zendesk/bots/whatsapp/fluxo/interacao/api/v1/bots/whatsapp/identificacao/processos"
LB_LOG = "projects/contabilizei-prod-01/logs/requests"

# URL fragment -> what the bot was doing (order matters: first match wins).
TRAIL_LABELS = [
    ("identificacao/processos/contagem", "contagem de processos de abertura pelo telefone"),
    ("identificacao/processos/dados", "dados do processo de abertura (statusJira, plano)"),
    ("mensagem/ativa", "checagem de mensagem ativa pendente (retorno de ativo)"),
    ("flags-empresas", "flags da empresa (bots-api)"),
    ("optouts", "opt-out (contato-service)"),
    ("tickets", "tickets do cliente/CNPJ"),
    ("autenticacao", "autenticação"),
    ("dados-cliente", "dados do cliente na plataforma"),
]


def group_name(gid) -> str:
    return GROUPS.get(str(gid), "?") if gid else "-"


def fmt_group(gid) -> str:
    return f"{group_name(gid)} (`{gid}`)" if gid else "-"


# ---------- database ----------

def port_open(port: int) -> bool:
    with socket.socket() as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


def start_proxy() -> bool:
    if port_open(PROXY_PORT):
        return False
    subprocess.Popen(["zsh", "-ic", f"_sql_proxy_start_alias {PROXY_ALIAS}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(40):
        if port_open(PROXY_PORT):
            return True
        time.sleep(1)
    sys.exit(f"proxy {PROXY_ALIAS} did not open port {PROXY_PORT}")


def stop_proxy() -> None:
    subprocess.run(["zsh", "-ic", f"_sql_proxy_kill_alias {PROXY_ALIAS}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def psql_json(sql: str) -> list[dict]:
    r = subprocess.run(["psql", "-w", f"service={PG_SERVICE}", "-At", "-c", f"select coalesce(json_agg(t), '[]') from ({sql}) t"], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr.strip())
    return json.loads(r.stdout.strip() or "[]")


def fetch_ticket(tid: int) -> dict | None:
    rows = psql_json(
        "select id, created_at, updated_at, status, via, group_id, group_name, organization_cnpj, organization_plano, requester_phone, requester_id, "
        f"sunshine_conversation_id, integration_id, tema_bot, tags, comments_formatted as transcript from tickets where id = {tid}"
    )
    return rows[0] if rows else None


def fetch_other_tickets(phone: str, created_at: str, tid: int) -> list[dict]:
    digits = re.sub(r"\D", "", phone)
    if not digits:
        return []
    return psql_json(
        "select id, created_at, status, via, group_id, group_name from tickets "
        f"where requester_phone in ('+{digits}', '{digits}') and id <> {tid} "
        f"and created_at between timestamptz '{created_at}' - interval '15 days' and timestamptz '{created_at}' + interval '1 day' "
        "order by created_at desc limit 15"
    )


def fetch_ativos(ids: list[str]) -> list[dict]:
    ids = [i for i in ids if i.isdigit()]
    if not ids:
        return []
    return psql_json(
        "select m.id, m.integracao, m.tipo, m.template, m.squad, m.autor, m.categoria, m.nome_grupo, m.agente_retorno, m.habilitado, m.criado_em, "
        "m.validade_em_minutos, m.doc_tipo, m.doc_valor, m.metadados ->> 'csat_source' as csat_source, "
        "(select json_agg(json_build_object('status', s.status, 'em', s.created_at) order by s.created_at) from mensagem_ativa_status s where s.id_mensagem = m.id) as status "
        f"from mensagem_ativa m where m.id in ({','.join(ids)})"
    )


# ---------- transcript ----------

BLOCK_RE = re.compile(r"Atualizado por: (?P<autor>[^\n]+?), (?P<data>\d{1,2} de [^,]+ de \d{4}), (?P<hora>\d{1,2}:\d{2})(?P<priv> \(privado\))?\n")
TRANSFER_RE = re.compile(r"Transferência de ticket via app \{grupo: (\d+) - ([^,]+), agente: ([^}]+)\} para \{grupo: (\d+) - ([^,]+), agente: ([^}]+)\}")


def parse_blocks(text: str | None) -> list[dict]:
    """comments_formatted lists the updates newest first; return them oldest first."""
    if not text:
        return []
    marks = list(BLOCK_RE.finditer(text))
    blocks = []
    for i, m in enumerate(marks):
        body = text[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(text)]
        body = body.replace("----------------------------------------------", "").strip()
        blocks.append({"autor": m["autor"], "hora": m["hora"], "privado": bool(m["priv"]), "texto": body})
    return list(reversed(blocks))


def transfers(blocks: list[dict]) -> list[dict]:
    out = []
    for blk in blocks:
        for m in TRANSFER_RE.finditer(blk["texto"]):
            out.append({"hora": blk["hora"], "autor": blk["autor"], "de": m[1], "de_nome": m[2].strip(), "para": m[4], "para_nome": m[5].strip(), "agente": m[6].strip()})
    return out


def csat_answers(blocks: list[dict]) -> dict:
    """Client answers to the CSAT return questions (Quero atendimento / mesmo tema x novo assunto)."""
    lines = "\n".join(blk["texto"] for blk in blocks if not blk["privado"]).splitlines()
    out = {"quero_atendimento": None, "tema": [], "linhas_bot": []}
    for ln in lines:
        m = re.match(r"\((\d{2}:\d{2}:\d{2})\) ([^:]+): (.*)", ln)
        if not m:
            continue
        hora, who, msg = m.groups()
        if who.strip() in ("Bot", "Bots API"):
            out["linhas_bot"].append(f"{hora} {msg}")
            continue
        low = msg.strip().lower()
        if low == "quero atendimento" and not out["quero_atendimento"]:
            out["quero_atendimento"] = hora
        if low in ("mesmo tema", "novo assunto"):
            out["tema"].append(f"{hora} {msg.strip()}")
    return out


# ---------- tags ----------

PREFIXED = ("processo_id", "processo", "conversationid", "businessphone", "telefone", "cnpj", "integrationid", "sys_template_ativo", "id_mensagem_ativa", "carteira")


def parse_tags(tags: list[str]) -> dict:
    out = {"flags": set(tags or []), "sys_grupo": [t for t in tags or [] if t.startswith("sys_grupo")]}
    for t in tags or []:
        if ":" in t:
            k, v = t.split(":", 1)
            if k in PREFIXED:
                out.setdefault(k, [])
                if v not in out[k]:
                    out[k].append(v)
    return out


# ---------- load balancer trail ----------

def phone_variants(phone: str) -> list[str]:
    d = re.sub(r"\D", "", phone)
    if not d:
        return []
    out = [d]
    if d.startswith("55") and len(d) == 13 and d[4] == "9":
        out.append(d[:4] + d[5:])
    elif d.startswith("55") and len(d) == 12:
        out.append(d[:4] + "9" + d[4:])
    return out


def trail_filter(needles: list[str], start: datetime, end: datetime) -> str:
    ors = " OR ".join(f'httpRequest.requestUrl:"{n}"' for n in needles)
    return f'logName="{LB_LOG}" AND timestamp>="{start.isoformat()}" AND timestamp<="{end.isoformat()}" AND ({ors})'


def read_trail(flt: str) -> list[dict]:
    r = subprocess.run(["gcloud", "logging", "read", flt, "--project", "contabilizei-prod-01", "--limit", "300", "--order", "asc", "--format", "json"], capture_output=True, text=True, timeout=300)
    if r.returncode:
        raise RuntimeError(r.stderr.strip()[:500])
    out = []
    for e in json.loads(r.stdout or "[]"):
        h = e.get("httpRequest", {})
        url = h.get("requestUrl", "")
        label = next((lbl for frag, lbl in TRAIL_LABELS if frag in url), "")
        out.append({"ts": e.get("timestamp"), "method": h.get("requestMethod"), "status": h.get("status"), "url": url.replace("https://api.contabilizei.com.br", ""), "label": label})
    return out


def logs_console_link(flt: str, start: datetime, end: datetime) -> str:
    q = urllib.parse.quote(flt, safe="")
    return f"https://console.cloud.google.com/logs/query;query={q};startTime={start.strftime('%Y-%m-%dT%H:%M:%SZ')};endTime={end.strftime('%Y-%m-%dT%H:%M:%SZ')}?project=contabilizei-prod-01"


def conversation_start(trail: list[dict], created: datetime) -> datetime | None:
    """The bot checks for a pending ativo (mensagem/ativa) right after loading the config, at the start of every session: use the last check before the ticket. Fallback: walk back while the gap between calls stays under 20 min."""
    marks = [parse_ts(t["ts"]) for t in trail if "mensagem/ativa" in t["url"] and parse_ts(t["ts"]) <= created + timedelta(minutes=1)]
    if marks and created - marks[-1] < timedelta(hours=2):
        first = marks[-1]
        for m in reversed(marks[:-1]):
            if first - m > timedelta(seconds=30):
                break
            first = m
        return first
    times = sorted(parse_ts(t["ts"]) for t in trail if t.get("ts") and parse_ts(t["ts"]) <= created + timedelta(minutes=1))
    if not times:
        return None
    start = times[-1]
    for t in reversed(times[:-1]):
        if start - t > timedelta(minutes=20):
            break
        start = t
    return start if created - start < timedelta(hours=3) else None


def parse_ts(s: str) -> datetime:
    s = s.replace("Z", "+00:00")
    s = re.sub(r"\.(\d{6})\d+", r".\1", s)
    return datetime.fromisoformat(s)


# ---------- bot routes (state now) ----------

def gw_get(path: str):
    url, tok = b.credentials("prd")
    s, r = b.http("GET", url + path, b.gateway_headers(tok))
    if s in (401, 403) and isinstance(r, dict):
        url, tok = b.credentials("prd", refresh=True)
        s, r = b.http("GET", url + path, b.gateway_headers(tok))
    return s, (r.get("data", r) if isinstance(r, dict) else r)


def gw_post(path: str, body: dict):
    s, r = b.call_gateway("prd", path, body)
    return s, (r.get("data", r) if isinstance(r, dict) else r)


def state_now(phone: str, extra_proc: list[str], extra_cnpj: list[str]) -> dict:
    st = {"empresas": None, "empresas_cnpj": {}, "contagem": None, "processos": {}, "erros": []}
    try:
        s, r = gw_post(f"{b.PLATAFORMA_PATH}/buscar-por-telefone", {"telefone": phone})
        st["empresas"] = r if s < 400 else None
        if s >= 400:
            st["erros"].append(f"buscar-por-telefone HTTP {s}")
    except Exception as e:  # noqa: BLE001
        st["erros"].append(f"buscar-por-telefone: {e}")
    cnpjs = list(dict.fromkeys(extra_cnpj + (((st["empresas"] or {}).get("empresasAtivasOuRascunho") or {}).get("listasCNPJs", {}).get("total") or [])))
    for c in cnpjs[:5]:
        try:
            s, r = gw_post(f"{b.PLATAFORMA_PATH}/buscar-por-telefone-e-cnpj", {"telefone": phone, "cnpj": re.sub(r"\D", "", c)})
            emp = (r or {}).get("empresaLogada") if isinstance(r, dict) else None
            st["empresas_cnpj"][c] = {"http": s, **({k: emp.get(k) for k in ("status", "categoriaPlano", "abertura", "jiraStatus", "jiraFinalizado", "idProcesso")} if isinstance(emp, dict) else {}),
                                      "assessor": bool(isinstance(emp, dict) and emp.get("assessor"))}
        except Exception as e:  # noqa: BLE001
            st["erros"].append(f"buscar-por-telefone-e-cnpj {c}: {e}")
    try:
        s, r = gw_get(f"{PROC_PATH}/contagem/{phone}")
        st["contagem"] = (r or {}).get("processosStatusPermitidos", r) if isinstance(r, dict) else r
        if s >= 400:
            st["erros"].append(f"contagem HTTP {s}")
    except Exception as e:  # noqa: BLE001
        st["erros"].append(f"contagem: {e}")
    ids = [str(x) for x in (((st["contagem"] or {}).get("listasIDs") or {}).get("total") or [])] if isinstance(st["contagem"], dict) else []
    for pid in list(dict.fromkeys(ids + extra_proc)):
        try:
            s, r = gw_get(f"{PROC_PATH}/dados/{pid}/telefone/{phone}")
            d = r if isinstance(r, dict) else {}
            st["processos"][pid] = {"http": s, "na_contagem": pid in ids, "idJira": d.get("idJira"), "statusJira": d.get("statusJira"), "plano": d.get("plano"),
                                    "statusPagto": d.get("statusPagto"), "cnpj": (d.get("empresa") or {}).get("cnpj"), "assessor": bool(d.get("nomeAssessor") or d.get("emailAssessor"))}
        except Exception as e:  # noqa: BLE001
            st["erros"].append(f"dados {pid}: {e}")
    return st


# ---------- routing ----------

AIDA_GROUPS = ("31714889423900", "29248769628572", "29248799750812")


def expected_drop(status: str | None, plano: str | None) -> tuple[str, str]:
    """Group of the Ativação Inbound drops for a SOCI status. The drops apply to Experts and BP (BP gets there after the AIDA hands off)."""
    experts = "EXPERT" in (plano or "").upper()
    if not status:
        return "", "sem statusJira: não dá para calcular o drop"
    s = status.strip().lower()
    if s == "finalizado":
        gid = CFG["finalizado_experts"] if experts else CFG["finalizado_bp"]
        return gid, "Finalizado → " + group_name(gid) + "; mas Finalizado some da contagem, então só chega aqui pelo ramo de empresa (consulta CNPJ)"
    for gid, statuses in CFG["drops_experts"].items():
        if s in (x.lower() for x in statuses):
            return gid, f"status `{status}` está no drop de {group_name(gid)}"
    tag = f", com tag `{CFG['else_tag_experts']}`" if experts else ""
    return CFG["else_experts"], f"status `{status}` fora do mapa → ELSE (Atendimento{tag})"


def ativo_kind(template: str | None) -> str:
    t = (template or "").lower()
    if t.startswith("csat_retorna_atendimento"):
        return "csat_retorno"
    if t.startswith(("follow_up_transbordo", "fup_csat")):
        return "fup_transbordo"
    return "ativo"


def hhmm(ts: str | None) -> str:
    return parse_ts(ts).astimezone(BRT).strftime("%H:%M:%S") if ts else "?"


def analyse(tk: dict, tags: dict, st: dict, trail: list[dict], start: datetime | None, status_override: str | None, proc_override: str | None, ctx: dict) -> dict:
    gid_now = str(tk.get("group_id") or "")
    trf = ctx["transfers"]
    # The bot's drop is the group before the first manual/app transfer.
    gid = trf[0]["de"] if trf else gid_now
    flags = tags["flags"]
    notes = []
    created = parse_ts(tk["created_at"])
    session = [t for t in trail if start and start - timedelta(seconds=5) <= parse_ts(t["ts"]) <= created + timedelta(minutes=1)]
    passou_processos = any("identificacao/processos" in t["url"] for t in session)

    ativo_tag = bool(tags.get("sys_template_ativo") or tags.get("id_mensagem_ativa") or "src_outbound" in flags)
    ativo = ativo_tag and not passou_processos
    at = (ctx["ativos"] or [{}])[0]
    kind = ativo_kind(at.get("template") or (tags.get("sys_template_ativo") or [None])[0])
    entrada = ""
    if ativo_tag:
        resp = next((x["em"] for x in (at.get("status") or []) if x["status"] == "RESPONDIDA"), None)
        notes.append(f"Ativo `{at.get('id', (tags.get('id_mensagem_ativa') or ['?'])[0])}`: integração `{at.get('integracao')}`, categoria `{at.get('categoria')}`, template `{at.get('template')}`, enviado por `{at.get('autor')}` às {hhmm(at.get('criado_em'))}, "
                     f"grupo do ativo `{at.get('nome_grupo')}`, csat_source `{at.get('csat_source')}`, documento `{at.get('doc_tipo')}`, respondido às {hhmm(resp)} (validade {at.get('validade_em_minutos')} min).")
        cs = ctx["csat"]
        if kind == "csat_retorno":
            com_cnpj = (at.get("doc_tipo") or "").lower() == "cnpj"
            entrada = (f"retorno da pesquisa CSAT (`{at.get('template')}`) → \"Quero atendimento\" às {cs['quero_atendimento'] or '?'} → "
                       + ("csat_source HUMAN_CP → ReRoute Ticket (IA)" if "HUMAN_CP" in (at.get("csat_source") or "") else
                          f"\"mesmo tema ou novo assunto?\" (respostas: {', '.join(cs['tema']) or '?'}; vale a primeira) → "
                          + ("com CNPJ: consulta CNPJ → Business Hours Outbound / acesso Experts" if com_cnpj else
                             "ativo sem CNPJ (documento `" + str(at.get('doc_tipo')) + "`) → Init session / reautenticação → nova identificação")))
        elif kind == "fup_transbordo":
            entrada = "follow-up de transbordo → \"Quero atendimento\" → Business Hours Outbound (CSAT_FUP_ESCALATE)"
        else:
            entrada = f"retorno de ativo `{at.get('integracao')}` → \"Responder mensagem\" → grupo do ativo (`{at.get('nome_grupo')}`)"
        if passou_processos:
            notes.append("Depois do ativo, a sessão fez contagem/dados de processo: o ativo já estava `RESPONDIDA` (desabilitado) e a conversa seguiu a identificação normal da Ativação, então valem o rollout da IA e o drop por status.")
    escalated_ai = "escalated_to_ai" in flags
    sec = start.astimezone(timezone.utc).second if start else None

    procs = st["processos"]
    total_ids = [str(x) for x in (((st["contagem"] or {}).get("listasIDs") or {}).get("total") or [])] if isinstance(st["contagem"], dict) else []
    tag_proc = (tags.get("processo_id") or []) + (tags.get("processo") or [])
    sess_proc = [re.search(r"/dados/(\d+)/", t["url"]).group(1) for t in session if re.search(r"/dados/(\d+)/", t["url"])]
    pid = proc_override or (sess_proc[0] if sess_proc else (tag_proc[0] if tag_proc else (total_ids[0] if total_ids else None)))
    proc = procs.get(pid, {}) if pid else {}
    status = status_override or proc.get("statusJira")
    plano = proc.get("plano") or tk.get("organization_plano")
    experts = "EXPERT" in (plano or "").upper()

    ativas = ((st["empresas"] or {}).get("empresasAtivasOuRascunho") or {}).get("quantidades", {}).get("total", 0) if st["empresas"] else None
    emp_abertura = [c for c, e in st["empresas_cnpj"].items() if e.get("abertura")]
    emp_final = [c for c, e in st["empresas_cnpj"].items() if e.get("jiraFinalizado")]

    if ativo:
        ramo = entrada + " (sem identificação de processo na sessão)"
        notes.append("A conversa não passou pela contagem de processos: o destino vem do fluxo do ativo, não dos drops do SOCI nem da IA de Ativação.")
    elif ativas and emp_final and not (emp_abertura and not emp_final):
        ramo = "empresa ativa com Jira finalizado → menu completo (ongoing/onboarding), não passa pelos drops de Ativação"
    elif ativas and not emp_abertura:
        ramo = "empresa ativa fora de abertura → menu completo (Falar com Assessor → Experts Grupo Padrão / fluxo BP), não passa pelos drops de Ativação"
    elif ativas:
        ramo = "empresa ativa ainda em abertura (jiraFinalizado=false) → " + ("Menu Inic sem Jira → Ativação Inbound (drops)" if experts else "Ativação Inbound BP (AIDA, depois drops)")
    elif total_ids or passou_processos:
        ramo = "sem empresa ativa, com processo de abertura na contagem → Ativação Inbound (drops por statusJira do primeiro processo)"
    else:
        ramo = "sem empresa ativa e sem processo na contagem → fluxo de não cliente / identificação falhou"

    exp_gid, exp_why = expected_drop(status, plano)
    ia_first = None
    if not ativo and "menu completo" not in ramo:
        if not experts:
            ia_first = CFG["ia_ativacao_bp"]
            notes.append("Plano BP: a Ativação Inbound manda primeiro para a AIDA Ativação BP (`flagRolloutAtivacaoInboundBP` = 100%); o drop por status só vale quando a IA transfere para humano.")
        elif sec is not None and sec <= CFG["rollout_ia_experts_segundo_max"]:
            ia_first = CFG["ia_ativacao_experts"]
            notes.append(f"Início estimado da conversa no segundo :{sec:02d} (≤ {CFG['rollout_ia_experts_segundo_max']}): rollout da IA de Ativação Experts (`flagRolloutIAAtivExp`), então vai primeiro para a AIDA Ativação Experts; o drop por status só vale se a IA transferir.")
    if escalated_ai and gid not in AIDA_GROUPS:
        notes.append("O ticket tem `escalated_to_ai`: a IA atendeu primeiro e o grupo atual é o da transferência feita depois (pela IA ou por um agente). Conferir o histórico de grupo (BigQuery `raw_tb_ticket_events`, D-1) ou o log da Ultimate.")

    for p in tag_proc:
        if p not in total_ids:
            info = procs.get(p, {})
            why = "status FINALIZADO (a contagem descarta)" if (info.get("statusJira") or "").upper() == "FINALIZADO" else "telefone do sócio na Abertura diferente do telefone da conversa (ver histórico de `[SOCI] Telefone`)"
            notes.append(f"O processo `{p}` está nas tags do ticket mas **não** aparece hoje na contagem do telefone: provável {why}.")
    if len(total_ids) > 1:
        notes.append(f"O telefone tem {len(total_ids)} processos na contagem; o bot usa o primeiro (`{total_ids[0]}`).")
    if ativas and total_ids:
        notes.append("O telefone tem empresa ativa **e** processo em andamento: o ramo da empresa (consulta CNPJ) é avaliado antes do de processos.")
    if pid and not status_override:
        notes.append("O status usado é o de **hoje**: confirmar no changelog do SOCI qual era o status no horário da conversa e, se for outro, rodar de novo com `--status`.")

    if ativo_tag and not ativo:
        ramo = entrada + " → " + ramo
    sem_ia = None
    if gid not in AIDA_GROUPS and not escalated_ai:
        if ativo:
            sem_ia = "o fluxo do ativo escala direto para humano/grupo do ativo, sem passar pela Ativação Inbound (onde fica a IA)"
        elif "menu completo" in ramo:
            sem_ia = "cliente com empresa ativa fora da abertura vai para o menu completo; a IA de Ativação não se aplica"
        elif experts and sec is not None and sec > CFG["rollout_ia_experts_segundo_max"]:
            sem_ia = f"sorteio do rollout da IA Experts: a sessão começou no segundo :{sec:02d} (> {CFG['rollout_ia_experts_segundo_max']}), então `flagRolloutIAAtivExp` = false e o bot foi direto ao drop por status"
        elif not experts and plano:
            sem_ia = "plano BP deveria ir para a AIDA Ativação BP (rollout 100%): sem IA aqui é inesperado"
        if sem_ia:
            notes.append("Sem IA: " + sem_ia + ".")
    if trf:
        txt = f"O drop do bot foi para {fmt_group(gid)}; depois houve {len(trf)} transferência(s) por app/agente (a última para {trf[-1]['para_nome']}, às {trf[-1]['hora']})"
        if gid_now == gid:
            back = sum(1 for x in trf if x["de"] == gid)
            txt += f", mas o ticket está de novo em {group_name(gid)}" + (f" ({back} transferências saíram dele: algo o devolveu, provável gatilho do Zendesk pelas tags `sys_grupo_*`)" if back > 1 else "") + "."
        else:
            txt += f": o grupo atual ({group_name(gid_now)}) não é o drop."
        notes.append(txt)

    if ativo:
        code = "RETORNO_ATIVO"
        notes.append("O grupo do drop " + ("bate" if exp_gid and gid == exp_gid else "não bate") + f" com o drop que o status daria ({group_name(exp_gid)}).")
    elif "menu completo" in ramo:
        code = "FORA_DA_ATIVACAO"
    elif gid in AIDA_GROUPS:
        code = "OK_IA" if gid == ia_first else "IA_INESPERADA"
    elif not exp_gid:
        code = "SEM_DADOS"
    elif gid == exp_gid:
        code = "OK_VIA_IA" if escalated_ai else "OK"
    else:
        code = "DIVERGENTE"
    return {"codigo": code, "ramo": ramo, "entrada_ativo": entrada, "sem_ia": sem_ia, "grupo_atual": gid_now, "grupo_drop": gid, "grupo_esperado": ia_first or exp_gid, "drop_por_status": exp_gid, "motivo_esperado": exp_why,
            "processo_usado": pid, "status_usado": status, "status_fonte": "--status (informado)" if status_override else "rota de dados do bot, status ATUAL",
            "plano": plano, "rollout_segundo": sec, "notas": notes}


# ---------- report ----------

def links(tk: dict, tags: dict, st: dict, start_day: str, end_day: str, trail_link: str | None) -> list[str]:
    bp = (tags.get("businessphone") or [""])[0]
    bot = CFG["bots"].get(bp, CFG["bot_padrao"])
    conv = tk.get("sunshine_conversation_id") or (tags.get("conversationid") or [None])[0]
    out = [f"- Ticket no Zendesk: https://contabilizei.zendesk.com/agent/tickets/{tk['id']}"]
    if conv:
        out.append(f"- Log da conversa na Ultimate ({bot['nome']}): https://contabilizei.zendesk.com/ai-agents/dashboard/agent/{bot['id']}/optimize/monitoring/conversation-logs/{CFG['ultimate_log_id']}"
                   f"?endDate={end_day}+23%3A59&startDate={start_day}+00%3A00&platformConversationId={conv}")
    for pid, p in st["processos"].items():
        if p.get("idJira"):
            out.append(f"- Processo `{pid}`: SOCI https://contabilizeicontabilidade.atlassian.net/browse/{p['idJira']} · admin da Abertura https://app.contabilizei.com/abertura/sistema-admin/#/processo/{pid}")
    if trail_link:
        out.append(f"- Trilha de chamadas do bot (Cloud Logging): {trail_link}")
    return out


def render(tk, tags, st, trail, start, verdict, link_lines, others, ctx) -> str:
    created = parse_ts(tk["created_at"]).astimezone(BRT)
    L = [f"# Validação de drop: ticket {tk['id']}", ""]
    L += [f"**Veredito automático: `{verdict['codigo']}`** · drop do bot {fmt_group(verdict['grupo_drop'])} · grupo atual {fmt_group(verdict['grupo_atual'])} · esperado {fmt_group(verdict['grupo_esperado'])} · drop pelo status {fmt_group(verdict['drop_por_status'])}", "",
          f"- Ramo provável: {verdict['ramo']}", f"- Por que esse esperado: {verdict['motivo_esperado']}",
          f"- Processo usado: `{verdict['processo_usado']}` · status: `{verdict['status_usado']}` ({verdict['status_fonte']}) · plano: `{verdict['plano']}`"]
    L += [f"- {n}" for n in verdict["notas"]]
    L += ["", "## Links", *link_lines, "", "## Ticket", ""]
    L += [f"- Criado: {created:%Y-%m-%d %H:%M:%S} BRT · status `{tk.get('status')}` · via `{tk.get('via')}` · grupo atual {fmt_group(tk.get('group_id'))} ({tk.get('group_name')})",
          f"- Telefone: `{tk.get('requester_phone')}` · CNPJ da org: `{tk.get('organization_cnpj') or '-'}` · plano da org: `{tk.get('organization_plano') or '-'}`",
          f"- Conversa Sunshine: `{tk.get('sunshine_conversation_id')}` · bot: `{', '.join(tags.get('businessphone') or ['?'])}`",
          f"- Tags de roteamento: {', '.join(f'`{t}`' for t in sorted(tags['flags']) if t.startswith(('sys_grupo', 'escalated', 'processo', 'sys_template', 'id_mensagem', 'src_', 'jira_', 'atv_', 'etapa_', 'ticket_whatsapp')) ) or '-'}"]
    if ctx["ativos"]:
        L += ["", "## Mensagem ativa", ""]
        for at in ctx["ativos"]:
            L.append(f"- `{at['id']}` · {at.get('integracao')}/{at.get('categoria')} · template `{at.get('template')}` · autor `{at.get('autor')}` · grupo `{at.get('nome_grupo')}` · csat_source `{at.get('csat_source')}` · doc `{at.get('doc_tipo')}={at.get('doc_valor')}` · habilitado `{at.get('habilitado')}`")
            L.append("  - status: " + " → ".join(f"{x['status']} {hhmm(x['em'])}" for x in (at.get("status") or [])))
    if ctx["csat"]["linhas_bot"] or ctx["csat"]["tema"]:
        L += ["", "## Caminho no bot (transcrição)", ""]
        L += [f"- Bot {x}" for x in ctx["csat"]["linhas_bot"][:20]]
        if ctx["csat"]["quero_atendimento"]:
            L.append(f"- Cliente pediu \"Quero atendimento\" às {ctx['csat']['quero_atendimento']}")
        L += [f"- Cliente respondeu {x}" for x in ctx["csat"]["tema"]]
    if ctx["transfers"]:
        L += ["", "## Histórico de grupo (transferências registradas no ticket)", ""]
        L += [f"- {x['hora']} {x['autor']}: {x['de_nome']} (`{x['de']}`) → {x['para_nome']} (`{x['para']}`), agente `{x['agente']}`" for x in ctx["transfers"]]
    L += ["", "## Estado atual pelas rotas do bot", ""]
    if st["empresas"]:
        for k in ("empresasAtivasOuRascunho", "empresasInativas"):
            q = (st["empresas"].get(k) or {}).get("quantidades", {})
            lst = [f"{e.get('cnpj')} ({e.get('categoriaPlano')})" for e in ((st["empresas"].get(k) or {}).get("listasEmpresas", {}).get("total") or [])]
            L.append(f"- {k}: {q.get('total', 0)} (experts {q.get('experts', 0)}, BP {q.get('basicoPadraoMultibeneficios', 0)}) {', '.join(lst)}")
    for c, e in st["empresas_cnpj"].items():
        L.append(f"- Consulta CNPJ `{c}`: status `{e.get('status')}`, plano `{e.get('categoriaPlano')}`, abertura `{e.get('abertura')}`, jiraStatus `{e.get('jiraStatus')}`, jiraFinalizado `{e.get('jiraFinalizado')}`, assessor ongoing `{e.get('assessor')}`")
    cont = st["contagem"] if isinstance(st["contagem"], dict) else {}
    L.append(f"- Contagem de processos: {json.dumps(cont.get('listasIDs', cont), ensure_ascii=False)}")
    for pid, p in st["processos"].items():
        L.append(f"- Processo `{pid}` ({'na contagem' if p['na_contagem'] else 'FORA da contagem'}): {p.get('idJira')} · statusJira `{p.get('statusJira')}` · plano `{p.get('plano')}` · pagamento `{p.get('statusPagto')}` · CNPJ `{p.get('cnpj')}` · assessor `{p.get('assessor')}`")
    L += [f"- Erro: {e}" for e in st["erros"]]
    L += ["", "## Trilha de chamadas do bot (load balancer)", ""]
    if start:
        L.append(f"Início estimado da conversa: {start.astimezone(BRT):%H:%M:%S} BRT (segundo :{start.second:02d}). POSTs (consulta CNPJ, buscar-por-telefone) não aparecem aqui: o telefone vai no corpo.\n")
    L += [f"- {parse_ts(t['ts']).astimezone(BRT):%H:%M:%S} {t['method']} {t['status']} {t['label'] or ''} `{t['url'][:180]}`" for t in trail] or ["- (sem chamadas com o telefone/conversa/processo na janela)"]
    if others:
        L += ["", "## Outros tickets do telefone (15 dias antes)", ""]
        L += [f"- {o['id']} · {parse_ts(o['created_at']).astimezone(BRT):%Y-%m-%d %H:%M} · `{o['status']}` · {o['via']} · {o['group_name']}" for o in others]
    if ctx["blocks"]:
        txt = "\n\n".join(f"[{b['hora']}] {b['autor']}{' (privado)' if b['privado'] else ''}\n{b['texto']}" for b in ctx["blocks"])
        L += ["", "## Transcrição em ordem cronológica (até 8000 caracteres)", "", "```", txt[:8000], "```"]
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ticket")
    ap.add_argument("--status", help="SOCI status at the conversation time (from the changelog)")
    ap.add_argument("--processo", help="process id to use instead of the tagged/first one")
    ap.add_argument("--janela-min", type=int, default=180, help="minutes before the ticket creation to read the bot trail")
    ap.add_argument("--sem-logs", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    m = re.search(r"(\d{6,})", a.ticket)
    if not m:
        sys.exit("ticket id not found in the argument")
    tid = int(m.group(1))

    started = start_proxy()
    try:
        tk = fetch_ticket(tid)
        if not tk:
            sys.exit(f"ticket {tid} not found in {PG_SERVICE}.tickets (sync gap?). Ask the user for the phone or conversationid tag.")
        tags = parse_tags(tk.get("tags") or [])
        phone = tk.get("requester_phone") or next((t for t in tags.get("telefone", []) if not t.upper().startswith(("BR.", "+BR."))), "")
        phone = b.normalize_phone(phone) if phone else ""
        others = fetch_other_tickets(phone, tk["created_at"], tid) if phone else []
        ativos = fetch_ativos(tags.get("id_mensagem_ativa") or [])
    finally:
        if started:
            stop_proxy()

    created = parse_ts(tk["created_at"])
    t0, t1 = created - timedelta(minutes=a.janela_min), created + timedelta(minutes=10)
    needles = phone_variants(phone) + (tags.get("conversationid") or []) + ([tk["sunshine_conversation_id"]] if tk.get("sunshine_conversation_id") else []) \
        + (tags.get("processo_id") or []) + (tags.get("processo") or []) + [re.sub(r"\D", "", c) for c in (tags.get("cnpj") or [])]
    needles = [n for n in dict.fromkeys(needles) if n]
    trail, trail_link = [], None
    if needles and not a.sem_logs:
        flt = trail_filter(needles, t0, t1)
        trail_link = logs_console_link(flt, t0, t1)
        try:
            trail = read_trail(flt)
        except Exception as e:  # noqa: BLE001
            print(f"warning: trail not read: {e}", file=sys.stderr)
    start = conversation_start(trail, created)

    extra_proc = list(dict.fromkeys((tags.get("processo_id") or []) + (tags.get("processo") or []) + ([a.processo] if a.processo else [])))
    extra_cnpj = list(dict.fromkeys([re.sub(r"\D", "", c) for c in (tags.get("cnpj") or [])] + ([tk["organization_cnpj"]] if tk.get("organization_cnpj") else [])))
    st = state_now(phone, extra_proc, extra_cnpj) if phone else {"empresas": None, "empresas_cnpj": {}, "contagem": None, "processos": {}, "erros": ["sem telefone no ticket"]}

    blocks = parse_blocks(tk.get("transcript"))
    ctx = {"ativos": ativos, "blocks": blocks, "transfers": transfers(blocks), "csat": csat_answers(blocks)}
    verdict = analyse(tk, tags, st, trail, start, a.status, a.processo, ctx)
    day0 = (start or created).astimezone(BRT).strftime("%Y-%m-%d")
    day1 = created.astimezone(BRT).strftime("%Y-%m-%d")
    link_lines = links(tk, tags, st, day0, day1, trail_link)

    if a.json:
        tags_out = {k: (sorted(v) if isinstance(v, set) else v) for k, v in tags.items()}
        print(json.dumps({"ticket": {k: v for k, v in tk.items() if k != "transcript"}, "tags": tags_out, "estado": st, "trilha": trail, "veredito": verdict, "links": link_lines, "ativos": ativos, "transferencias": ctx["transfers"], "csat": ctx["csat"]}, ensure_ascii=False, indent=2, default=str))
        return
    md = render(tk, tags, st, trail, start, verdict, link_lines, others, ctx)
    out = Path.home() / "Downloads" / f"validar-drop-{tid}.md"
    out.write_text(md)
    print(md)
    print(f"Relatório salvo em {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
