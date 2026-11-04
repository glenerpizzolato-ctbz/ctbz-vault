#!/usr/bin/env python3
"""Map the WhatsApp conversations hit by Ultimate (Zendesk AI agents) errors, per bot, into a CSV.

Sources:
1. The error events logged by the `ultimateai-webhook` Cloud Run (project atendimento-canais-prd): `Technical Error`, `Action Failed`, `API Integration...`, with the Ultimate `conversationId` and the Sunshine `platformConversationId`.
2. The Sunshine Conversations API (credentials from the `zendeskbot-config` Cloud Function, never printed): conversation metadata (phone, CNPJ, ticket, sunshine user), WhatsApp client (BSUID) and the last 100 messages.

The error message variants are detected from the data: the bot text sent right after each error event is grouped by normalized text, and the texts that mostly show up after errors become variants V1..Vn, ordered by first appearance.

Usage:
  mapear_erros.py --since 2026-11-03T09:00:00Z [--until ...] [--bots main,ouvidoria] [--out file.csv] [--cache dir] [--refresh] [--threads 8]

Outputs <out>.csv (one row per bot + Sunshine conversation) and <out>-variantes.csv (catalog of the detected error messages).
"""
import argparse
import base64
import collections
import concurrent.futures as cf
import csv
import datetime as dt
import importlib.util
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PROJECT = "atendimento-canais-prd"
DASH = "https://contabilizei.zendesk.com/ai-agents/dashboard/bot/{}/conversations/{}"
BOTS = {  # bot name in the webhook log -> Ultimate bot id (dashboard URL)
    "[prod] ctbz wpp main": "66c6220557465548f3ff0d6e",
    "[prod] ctbz wpp fina + avisos": "693ffec1181a1a7f14d05c18",
    "[prod] ctbz wpp survey": "673c0518f9cf7058160ec9ae",
    "[prod] ctbz wpp trial": "693ffe9b7e0f42bd5e15a973",
    "[prod] ctbz wpp ouvidoria": "68289a56392101722adee8da",
    "[prod] ctbz chat main": "66bf4a1be43522b403cd876b",  # no real-time webhook configured
}
BOTS_API = Path.home() / "dotfiles/docs/ai/skills/ctbz/empresas/buscar-empresas-por-telefone/scripts/bots_api.py"
WINDOW_BEFORE, WINDOW_AFTER = dt.timedelta(seconds=10), dt.timedelta(seconds=40)
BOT_AUTHORS = (None, "Bot")
# A text only becomes an error variant if it reads like one, or if it went out after errors many times (low-volume bots make greetings look like fallbacks).
ERROR_HINT = re.compile(r"indispon|instabilidade|fora de servi|tente novamente|erro|falha|problema t[eé]cnico|transtorno", re.I)
CENARIO_ORDER = ["sem_resposta_apos_erro", "erro_sem_mensagem_de_fallback", "bot_voltou_a_responder", "atendido_por_humano_apos_erro"]


def parse_ts(s):
    s = s.replace("Z", "")
    s = re.sub(r"(\.\d{6})\d+", r"\1", s)
    s = re.sub(r"\+00:00$", "", s)
    return dt.datetime.fromisoformat(s).replace(tzinfo=dt.timezone.utc)


def norm_text(t):
    return re.sub(r"\s+", " ", (t or "").strip().lower())


def norm_phone(v):
    v = re.sub(r"\D", "", str(v or ""))
    return "+" + v if len(v) >= 10 else ""


def resolve_bots(arg):
    if not arg:
        return None
    out = []
    for b in arg.split(","):
        b = b.strip()
        hit = [n for n, i in BOTS.items() if b in (n, i) or n.endswith(" " + b) or n.endswith(b)]
        if not hit:
            sys.exit(f"bot desconhecido: {b} (conhecidos: {', '.join(BOTS)})")
        out += hit
    return sorted(set(out))


def read_events(since, until, bots):
    flt = [f'resource.labels.service_name="ultimateai-webhook"', 'jsonPayload.message="ultimateai_event"', f'timestamp>="{since}"']
    if until:
        flt.append(f'timestamp<"{until}"')
    if bots:
        flt.append("(" + " OR ".join(f'jsonPayload.bot="{b}"' for b in bots) + ")")
    cmd = ["gcloud", "logging", "read", " AND ".join(flt), "--project", PROJECT, "--limit", "500000", "--format", "json"]
    print("# lendo eventos do ultimateai-webhook...", file=sys.stderr)
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    evs = []
    for e in json.loads(out or "[]"):
        p = e.get("jsonPayload") or {}
        if re.search("test", str(p.get("event", "")), re.I):
            continue
        evs.append({"ts": e["timestamp"], "bot": p.get("bot") or "unknown", "event": p.get("event"), "ult": p.get("conversationId"), "sun": p.get("platformConversationId")})
    return evs


ATZ_PROJECT = "contabilizei-prod-01"
ATZ_TERMS = ["temporariamente indispon", "temporariamente fora de servi", "instabilidade", "Cliente recebeu a mensagem de erro"]
CHAT_BOT = "[prod] ctbz chat main"


def read_atz(since, until):
    """Second source, independent of Ultimate: the Sunshine webhooks our atz-worker-webhooks logs (NotificarAgente* with the bot's last message, and the MonitoramentoMensagensSistemaIndisponivel monitor)."""
    flt = ['resource.labels.container_name="atz-worker-webhooks-prd"', f'timestamp>="{since}"', "(" + " OR ".join(f'"{t}"' for t in ATZ_TERMS) + ")"]
    if until:
        flt.append(f'timestamp<"{until}"')
    cmd = ["gcloud", "logging", "read", " AND ".join(flt), "--project", ATZ_PROJECT, "--limit", "1000000", "--format", "json(timestamp,jsonPayload.message)"]
    print("# lendo os logs do atz-worker-webhooks...", file=sys.stderr)
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    evs, info = [], collections.defaultdict(dict)
    for e in json.loads(out or "[]"):
        msg = (e.get("jsonPayload") or {}).get("message") or ""
        j = re.search(r"'(\{.*\})'\s*$", msg, re.S)
        o = {}
        if j:
            try:
                o = json.loads(j.group(1))
            except ValueError:
                o = {}
        cid = o.get("sunshineConversationId")
        if not cid:
            m = re.search(r"conversationId '?([0-9a-f]{24})", msg)
            cid = m.group(1) if m else None
        text = o.get("textoUltimaMensagemAgenteOuBot") or (msg.split(" - ", 3)[-1] if "Cliente recebeu a mensagem de erro" in msg else "")
        if not cid or not ERROR_HINT.search(text or ""):
            continue
        evs.append({"ts": e["timestamp"], "bot": None, "event": "log_atendimento", "ult": None, "sun": cid})
        for k in ("ticketId", "nomeGrupo", "nomeSolicitante", "emailSolicitante", "telefoneSolicitante"):
            if o.get(k):
                info[cid][k] = o[k]
    return evs, info


def channel(r):
    types = {c.get("type") for c in r.get("clients") or []}
    if "whatsapp" in types:
        return "whatsapp"
    if types & {"sdk", "web"}:
        return "web"
    src = {(m.get("source") or {}).get("type") for m in r.get("msgs", []) if m["author"]["type"] == "user"}
    return "whatsapp" if "whatsapp" in src else ("web" if "web" in src else "")


class Sunshine:
    def __init__(self):
        spec = importlib.util.spec_from_file_location("bots_api", BOTS_API)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        url, tok = mod.gcloud_function("prd")
        with urllib.request.urlopen(f"{url}?auth_token={tok}", timeout=30) as r:
            s = json.load(r)["config"]["app"]["services"]["sunshine"]
        self.app, tok = s["appId"], s["token"].strip()
        if tok.lower().startswith(("basic ", "bearer ")):
            self.auth = tok
        else:  # a base64 "key:secret" is basic auth; anything else is a JWT
            decoded = base64.b64decode(tok + "==").decode("latin1", "ignore")
            self.auth = ("Basic " if ":" in decoded else "Bearer ") + tok

    def get(self, path):
        req = urllib.request.Request(f"https://api.smooch.io/v2/apps/{self.app}{path}", headers={"Authorization": self.auth})
        for i in range(7):
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    return r.status, json.load(r)
            except urllib.error.HTTPError as e:
                if e.code == 429 or e.code >= 500:
                    time.sleep(2 ** i)
                    continue
                return e.code, {}
            except (urllib.error.URLError, TimeoutError):
                time.sleep(2 ** i)
        return 599, {}

    def fetch(self, cid):
        st, conv = self.get(f"/conversations/{cid}")
        _, msgs = self.get(f"/conversations/{cid}/messages")
        r = {"conv_status": st, "conv": conv.get("conversation", {}), "msgs": msgs.get("messages", []), "fetched_at": dt.datetime.now(dt.timezone.utc).isoformat()}
        uid = (r["conv"].get("metadata") or {}).get("userId")
        if not uid and st == 200:
            _, parts = self.get(f"/conversations/{cid}/participants")
            uid = ((parts.get("participants") or [{}])[0]).get("userId")
        if uid:
            r["user_id"] = uid
            r["clients"] = self.get(f"/users/{uid}/clients")[1].get("clients", [])
        return r


def collect(evs, cache, refresh, threads):
    cache.mkdir(parents=True, exist_ok=True)
    last_ev = collections.defaultdict(str)
    for e in evs:
        if e["sun"]:
            last_ev[e["sun"]] = max(last_ev[e["sun"]], e["ts"])
    todo = []
    for cid, last in last_ev.items():
        f = cache / f"{cid}.json"
        cached = json.loads(f.read_text()) if f.exists() else {}
        if refresh or cached.get("conv_status") != 200 or cached.get("fetched_at", "") < last:
            todo.append(cid)
    print(f"# {len(last_ev)} conversas no Sunshine, {len(todo)} para buscar (cache em {cache})", file=sys.stderr)
    if todo:
        sun = Sunshine()

        def one(cid):
            r = sun.fetch(cid)
            if r["conv_status"] in (401, 403):
                raise SystemExit(f"Sunshine recusou as credenciais (HTTP {r['conv_status']})")
            tmp = cache / f"{cid}.json.tmp"
            tmp.write_text(json.dumps(r, ensure_ascii=False))
            os.replace(tmp, cache / f"{cid}.json")

        with cf.ThreadPoolExecutor(threads) as ex:
            for n, _ in enumerate(ex.map(one, todo), 1):
                if n % 250 == 0:
                    print(f"#   {n}/{len(todo)}", file=sys.stderr)
    return {cid: json.loads((cache / f"{cid}.json").read_text()) for cid in last_ev}


def bot_msgs(r, since):
    out = []
    for m in r.get("msgs", []):
        if m.get("received", "") < since[:19]:
            continue
        out.append(m)
    return out


def detect_variants(by_key, data, since):
    """Group the bot text sent right after each error event; keep the texts that mostly appear after errors."""
    after_err, total = collections.Counter(), collections.Counter()
    sample, first, last = {}, {}, {}
    for (bot, cid), evs in by_key.items():
        msgs = [m for m in bot_msgs(data[cid], since) if m["author"]["type"] == "business" and m["author"].get("displayName") in BOT_AUTHORS and m["content"].get("text")]
        for m in msgs:
            total[norm_text(m["content"]["text"])] += 1
        used = set()
        for e in evs:
            t = parse_ts(e["ts"])
            for m in msgs:
                mt = parse_ts(m["received"])
                if t - WINDOW_BEFORE <= mt <= t + WINDOW_AFTER and m["id"] not in used:
                    k = norm_text(m["content"]["text"])
                    used.add(m["id"])
                    after_err[k] += 1
                    sample.setdefault(k, m["content"]["text"].strip())
                    first[k] = min(first.get(k, m["received"]), m["received"])
                    last[k] = max(last.get(k, m["received"]), m["received"])
                    break
    keys = [k for k, n in after_err.items() if n >= 3 and n / total[k] >= 0.6 and (ERROR_HINT.search(k) or n >= 50)]
    keys.sort(key=lambda k: first[k])
    return [{"variante": f"V{i}", "texto": sample[k], "norm": k, "primeira_utc": first[k][:19], "ultima_utc": last[k][:19], "vezes_apos_erro": after_err[k], "vezes_total": total[k]} for i, k in enumerate(keys, 1)]


def build_rows(by_key, data, variants, since, atz_info):
    vmap = {v["norm"]: v["variante"] for v in variants}
    rows = []
    for (bot, cid), evs in by_key.items():
        evs.sort(key=lambda e: e["ts"])
        r = data[cid]
        conv, meta = r.get("conv") or {}, (r.get("conv") or {}).get("metadata") or {}
        tags = dict(p.split(":", 1) for p in (meta.get("tags") or "").split(",") if ":" in p)
        cnt = collections.Counter(e["event"] for e in evs if e["event"] != "log_atendimento")
        in_atz = any(e["event"] == "log_atendimento" for e in evs)
        ai = atz_info.get(cid, {})
        ult_ids = list(dict.fromkeys(e["ult"] for e in evs if e["ult"]))
        first_err = parse_ts(evs[0]["ts"])

        tag_phone = tags.get("telefone", "")
        phone = norm_phone(meta.get("5359989415708")) or ("" if "BR." in tag_phone else norm_phone(tag_phone))
        client_id = bsuid = ""
        for c in r.get("clients") or []:
            if c.get("type") != "whatsapp":
                continue
            client_id, ext = c.get("id", ""), c.get("externalId") or ""
            if ext.startswith("BR."):
                bsuid = ext
            ids = {i.get("key"): i.get("value") for i in c.get("additionalIdentifiers") or []}
            phone = phone or norm_phone(ids.get("phoneNumber")) or norm_phone((c.get("raw") or {}).get("from")) or ("" if bsuid else norm_phone(ext))
        if "BR." in tag_phone and not bsuid:
            bsuid = tag_phone.lstrip("+")
        phone = phone or norm_phone(ai.get("telefoneSolicitante"))

        msgs = bot_msgs(r, since)
        var_cnt, last_var, last_err_msg = collections.Counter(), None, None
        human_after = bot_ok_after = False
        last_user, tries = None, 0
        for m in msgs:
            a, mt = m["author"], parse_ts(m["received"])
            if a["type"] == "user":
                last_user = m
                tries += mt >= first_err - dt.timedelta(minutes=2)
                continue
            v = vmap.get(norm_text(m["content"].get("text")))
            if v:
                var_cnt[v] += 1
                last_var, last_err_msg = v, mt
            elif mt >= first_err:
                if a.get("displayName") not in BOT_AUTHORS:
                    human_after = True
                elif last_err_msg and mt > last_err_msg:
                    bot_ok_after = True
        last_business = next((m for m in reversed(msgs) if m["author"]["type"] == "business"), None)
        ends_on_error = bool(last_business and vmap.get(norm_text(last_business["content"].get("text"))))
        if human_after:
            cenario = "atendido_por_humano_apos_erro"
        elif bot_ok_after and not ends_on_error:
            cenario = "bot_voltou_a_responder"
        elif var_cnt:
            cenario = "sem_resposta_apos_erro"
        else:
            cenario = "erro_sem_mensagem_de_fallback"

        bot_id = BOTS.get(bot, "")
        rows.append({
            "bot": bot,
            "bot_id": bot_id,
            "canal": channel(r),
            "fonte": "ambos" if cnt and in_atz else ("webhook_ultimate" if cnt else "log_atendimento"),
            "cenario": cenario,
            "tipo_erro_ultimate": "+".join(sorted(cnt)) or "sem_evento_na_ultimate",
            "qtd_technical_error": cnt.get("Technical Error", 0),
            "qtd_action_failed": cnt.get("Action Failed", 0),
            "qtd_outros_eventos": sum(n for k, n in cnt.items() if k not in ("Technical Error", "Action Failed")),
            "primeiro_erro_utc": evs[0]["ts"][:19],
            "ultimo_erro_utc": evs[-1]["ts"][:19],
            "mensagens_erro_recebidas": "|".join(f"{k}x{v}" for k, v in sorted(var_cnt.items(), key=lambda x: int(x[0][1:]))),
            "ultima_variante_recebida": last_var or "",
            "qtd_msgs_cliente_no_periodo_do_erro": tries,
            "ultima_msg_cliente_utc": (last_user or {}).get("received", "")[:19],
            "ultima_msg_cliente": ((last_user or {}).get("content", {}).get("text") or "")[:200].replace("\n", " "),
            "telefone": phone,
            "nome_whatsapp": next((m["author"].get("displayName") for m in reversed(msgs) if m["author"]["type"] == "user" and m["author"].get("displayName")), ""),
            "cnpj": tags.get("cnpj") or meta.get("15818063240348") or "",
            "carteira": tags.get("carteira", ""),
            "zendesk_ticket_id": meta.get("ezvoice_zendesk_ticket_id") or ai.get("ticketId", ""),
            "grupo_zendesk": ai.get("nomeGrupo", ""),
            "nome_solicitante": ai.get("nomeSolicitante", ""),
            "email_solicitante": ai.get("emailSolicitante", ""),
            "sunshine_conversation_id": cid,
            "sunshine_user_id": meta.get("userId") or r.get("user_id", ""),
            "sunshine_whatsapp_client_id": client_id,
            "whatsapp_bsuid": bsuid,
            "controle_atual": (conv.get("activeSwitchboardIntegration") or {}).get("name", ""),
            "ultimate_conversation_ids": "|".join(ult_ids),
            "link_ultimate": DASH.format(bot_id, ult_ids[-1]) if bot_id and ult_ids else "",
            "sunshine_status": r.get("conv_status"),
        })
    rows.sort(key=lambda x: (x["bot"], CENARIO_ORDER.index(x["cenario"]), x["ultimo_erro_utc"]))
    return rows


def err_count(row):
    """Error messages the client actually received (V1x2|V3x1 -> 3); at least 1, since the conversation is in the list."""
    n = sum(int(p.rsplit("x", 1)[1]) for p in row["mensagens_erro_recebidas"].split("|") if p)
    return max(n, 1)


def summary(rows):
    """One row per bot plus a TOTAL row: affected conversations, repeated errors, error type, message variant and scenario."""
    groups = collections.defaultdict(list)
    for x in rows:
        groups[x["bot"]].append(x)
    out = []
    for bot, xs in sorted(groups.items(), key=lambda g: -len(g[1])) + [("TOTAL", rows)]:
        n = len(xs)
        errs = [err_count(x) for x in xs]
        tipo = collections.Counter(x["tipo_erro_ultimate"] for x in xs)
        r = {
            "bot": bot,
            "conversas_afetadas": n,
            "clientes_unicos": len({x["telefone"] or x["sunshine_user_id"] for x in xs}),
            "mensagens_de_erro_recebidas": sum(errs),
            "conversas_com_1_erro": sum(1 for e in errs if e == 1),
            "conversas_com_mais_de_1_erro": sum(1 for e in errs if e > 1),
            "pct_mais_de_1_erro": f"{100 * sum(1 for e in errs if e > 1) / n:.1f}%",
            "conversas_com_3_ou_mais_erros": sum(1 for e in errs if e >= 3),
            "max_erros_numa_conversa": max(errs),
            "so_technical_error": tipo.get("Technical Error", 0),
            "so_action_failed": tipo.get("Action Failed", 0),
            "technical_e_action_failed": tipo.get("Action Failed+Technical Error", 0),
            "outros_eventos_ultimate": sum(k for t, k in tipo.items() if t not in ("Technical Error", "Action Failed", "Action Failed+Technical Error", "sem_evento_na_ultimate")),
            "sem_evento_na_ultimate": tipo.get("sem_evento_na_ultimate", 0),
            "eventos_technical_error": sum(int(x["qtd_technical_error"]) for x in xs),
            "eventos_action_failed": sum(int(x["qtd_action_failed"]) for x in xs),
            "canal_whatsapp": sum(1 for x in xs if x["canal"] == "whatsapp"),
            "canal_web": sum(1 for x in xs if x["canal"] == "web"),
            "fonte_webhook_ultimate": sum(1 for x in xs if x["fonte"] == "webhook_ultimate"),
            "fonte_log_atendimento": sum(1 for x in xs if x["fonte"] == "log_atendimento"),
            "fonte_ambos": sum(1 for x in xs if x["fonte"] == "ambos"),
        }
        for c in CENARIO_ORDER:
            r[c] = sum(1 for x in xs if x["cenario"] == c)
        out.append(r)
    return out


SHEET_COLUMNS = [
    "bot", "canal", "qtd_erros_recebidos", "mais_de_1_erro", "tipo_erro_ultimate", "cenario", "primeiro_erro_utc", "ultimo_erro_utc",
    "qtd_msgs_cliente_no_periodo_do_erro", "ultima_msg_cliente_utc", "ultima_msg_cliente",
    "telefone", "nome_whatsapp", "nome_solicitante", "email_solicitante", "cnpj", "carteira", "zendesk_ticket_id", "grupo_zendesk",
    "sunshine_conversation_id", "sunshine_user_id", "sunshine_whatsapp_client_id", "whatsapp_bsuid", "controle_atual",
    "link_ultimate", "ultimate_conversation_ids", "fonte", "qtd_technical_error", "qtd_action_failed",
]


def sheet_rows(rows):
    """The spreadsheet: one row per conversation, grouped by bot (biggest bot first), most errors first inside each bot; no per-variant columns, so it can be filtered freely."""
    vol = collections.Counter(x["bot"] for x in rows)
    out = []
    for x in rows:
        n = err_count(x)
        out.append({**{k: x.get(k, "") for k in SHEET_COLUMNS}, "qtd_erros_recebidos": n, "mais_de_1_erro": "sim" if n > 1 else "nao"})
    out.sort(key=lambda x: (-vol[x["bot"]], x["bot"], -x["qtd_erros_recebidos"], x["primeiro_erro_utc"]))
    return out


def write_csv(path, rows):
    with open(path, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--since", required=True, help="início em UTC, ex: 2026-11-03T09:00:00Z")
    ap.add_argument("--until", help="fim em UTC (padrão: agora)")
    ap.add_argument("--bots", help="nomes curtos ou ids separados por vírgula (padrão: todos os bots com eventos)")
    ap.add_argument("--out", help="CSV de saída (padrão: ~/Downloads/ultimate-erros-<since>.csv)")
    ap.add_argument("--cache", default=str(Path.home() / ".cache/mapear-erros-ultimate"), help="pasta do cache das conversas do Sunshine")
    ap.add_argument("--refresh", action="store_true", help="buscar de novo todas as conversas, ignorando o cache")
    ap.add_argument("--threads", type=int, default=8)
    ap.add_argument("--so-webhook", action="store_true", help="usar só os eventos do ultimateai-webhook, sem os logs do atz-worker-webhooks")
    a = ap.parse_args()

    bots = resolve_bots(a.bots)
    out = Path(a.out or Path.home() / f"Downloads/ultimate-erros-{a.since[:10]}.csv").expanduser()
    evs = read_events(a.since, a.until, None)
    atz_evs, atz_info = ([], {}) if a.so_webhook else read_atz(a.since, a.until)
    if not evs and not atz_evs:
        sys.exit("nenhum evento de erro no período")
    data = collect(evs + atz_evs, Path(a.cache).expanduser(), a.refresh, a.threads)

    # Bot of each conversation: the webhook says it; for the ones only in our logs, web -> chat main and WhatsApp -> the bot of the same WhatsApp integration.
    conv_bot, integ = {}, collections.defaultdict(collections.Counter)
    for e in evs:
        if e["sun"]:
            conv_bot.setdefault(e["sun"], e["bot"])
            src = ((data[e["sun"]].get("conv") or {}).get("metadata") or {}).get("origin_source_integration")
            if src:
                integ[src][e["bot"]] += 1
    for e in atz_evs:
        cid = e["sun"]
        if cid not in conv_bot:
            r = data[cid]
            src = ((r.get("conv") or {}).get("metadata") or {}).get("origin_source_integration")
            ch = channel(r)
            conv_bot[cid] = CHAT_BOT if ch == "web" else (integ[src].most_common(1)[0][0] if integ.get(src) else f"desconhecido ({ch or 'sem canal'})")
        e["bot"] = conv_bot[cid]
    by_key = collections.defaultdict(list)
    for e in evs + atz_evs:
        if e["sun"] and (not bots or conv_bot[e["sun"]] in bots):
            by_key[(conv_bot[e["sun"]], e["sun"])].append(e)
    variants = detect_variants(by_key, data, a.since)
    rows = build_rows(by_key, data, variants, a.since, atz_info)

    write_csv(out, sheet_rows(rows))
    sout = out.with_name(out.stem + "-resumo-por-bot.csv")
    resumo = summary(rows)
    write_csv(sout, resumo)

    print(f"{len(evs)} eventos, {len(rows)} conversas -> {out}")
    print(f"resumo por bot -> {sout}")
    for r in resumo:
        print(f"  {r['bot']}: {r['conversas_afetadas']} conversas, {r['conversas_com_mais_de_1_erro']} com mais de 1 erro ({r['pct_mais_de_1_erro']}), max {r['max_erros_numa_conversa']}")
    print("mensagens de erro detectadas (usadas só para classificar o cenário):")
    for v in variants:
        print(f"  {v['variante']} {v['primeira_utc']} -> {v['ultima_utc']} ({v['vezes_apos_erro']}x): {v['texto'][:90]!r}")
    print("por bot, canal e fonte:")
    for (b, c, f), n in sorted(collections.Counter((x["bot"], x["canal"], x["fonte"]) for x in rows).items()):
        print(f"  {n:6d}  {b} | {c} | {f}")
    print("por bot e cenario:")
    for (b, c), n in sorted(collections.Counter((x["bot"], x["cenario"]) for x in rows).items()):
        print(f"  {n:6d}  {b} | {c}")
    print("por bot e tipo de erro:")
    for (b, t), n in sorted(collections.Counter((x["bot"], x["tipo_erro_ultimate"]) for x in rows).items()):
        print(f"  {n:6d}  {b} | {t}")
    print(f"sem telefone: {sum(1 for x in rows if not x['telefone'])} | sunshine != 200: {sum(1 for x in rows if x['sunshine_status'] != 200)}")


if __name__ == "__main__":
    main()
