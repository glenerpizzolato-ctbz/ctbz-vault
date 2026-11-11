#!/usr/bin/env python3
"""
Show the details of Zendesk triggers (gatilhos), read-only: by id, admin link or name.

Prints title, status, category, position, dates and the conditions (all/any) and actions in readable form, resolving
ids of groups, users, ticket fields (custom_fields_<id>), ticket forms, brands, webhooks, targets and trigger categories.

Credentials come from the experts-bruno zendesk-api collection .env (user_email + personal_user_token_<env>); they are
never printed. Same routes as the collection's "Support API/triggers" requests. Only GET requests.

The default environment is the sandbox. Production (--env prod) is blocked by the team policy against AI calling the
Zendesk prod API (vault note apis/zendesk-sunco-prod-politica) and also requires --i-confirm-prod.

Usage:
    buscar_gatilho.py 5138317000988                                     # by id (sandbox)
    buscar_gatilho.py https://contabilizei.zendesk.com/admin/objects-rules/rules/triggers/5138317000988
    buscar_gatilho.py --name "ouvidoria"                                # title contains text (case-insensitive)
    buscar_gatilho.py 5138317000988 --json                              # raw JSON of the trigger
    buscar_gatilho.py 5138317000988 --env prod --i-confirm-prod         # production, only with explicit approval
"""

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ENVS = {
    "sandbox": ("https://contabilizei1637606740.zendesk.com", "personal_user_token_sandbox"),
    "prod": ("https://contabilizei.zendesk.com", "personal_user_token_prod"),
}
ENV_FILE = Path.home() / "repositories/experts-bruno/zendesk-api/.env"

FIELD_LABELS = {
    "status": "Status",
    "type": "Tipo",
    "priority": "Prioridade",
    "group_id": "Grupo",
    "assignee_id": "Responsável",
    "requester_id": "Solicitante",
    "organization_id": "Organização",
    "current_tags": "Tags",
    "set_tags": "Definir tags",
    "remove_tags": "Remover tags",
    "update_type": "Ticket é",
    "via_id": "Canal",
    "brand_id": "Marca",
    "ticket_form_id": "Formulário",
    "subject_includes_word": "Assunto contém palavra",
    "comment_includes_word": "Comentário contém palavra",
    "comment_is_public": "Comentário é",
    "current_via_id": "Atualização via",
    "role": "Papel do atualizador",
    "notification_webhook": "Notificar webhook",
    "notification_target": "Notificar alvo",
    "notification_user": "E-mail para usuário",
    "notification_group": "E-mail para grupo",
    "notification_sms_user": "SMS para usuário",
    "notification_messaging_csat": "CSAT do messaging",
    "satisfaction_score": "Satisfação",
    "reopens": "Reaberturas",
    "replies": "Respostas",
    "sla_policy": "Política de SLA",
    "locale_id": "Idioma",
    "requester_role": "Papel do solicitante",
    "follower": "Seguidor",
    "cc": "CC",
    "side_conversation": "Conversa paralela",
}

VIA = {0: "Web form", 4: "E-mail", 5: "Web service (API)", 8: "Regra", 29: "Chat", 30: "Twitter", 33: "Voz",
       38: "Facebook", 55: "Sistema", 56: "Messaging", 57: "Messaging", 74: "SDK", 88: "Native messaging",
       90: "WhatsApp", 94: "Messaging social", 97: "WhatsApp"}


def load_auth(env: str) -> tuple[str, str]:
    base_url, token_key = ENVS[env]
    values = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip().strip('"').strip("'")
    email = values.get("user_email") or os.environ.get("user_email")
    token = values.get(token_key) or os.environ.get(token_key)
    if not email or not token:
        sys.exit(f"user_email/{token_key} missing in {ENV_FILE}")
    return base_url, "Basic " + base64.b64encode(f"{email}/token:{token}".encode()).decode()


class Client:
    def __init__(self, base_url: str, auth: str):
        self.base_url = base_url
        self.auth = auth
        self.cache: dict[str, dict | None] = {}

    def get(self, path: str) -> dict:
        url = path if path.startswith("http") else self.base_url + path
        req = urllib.request.Request(url, headers={"Authorization": self.auth, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read() or b"{}")

    def get_all(self, path: str, key: str) -> list:
        items, url = [], path
        while url:
            page = self.get(url)
            items += page.get(key, [])
            url = page.get("next_page") or (page.get("links") or {}).get("next")
            if not page.get("meta", {}).get("has_more", True) and "meta" in page:
                url = None
        return items

    def lookup(self, kind: str, obj_id) -> dict | None:
        """Fetch one object (group, user, ticket field...) by id, cached; None if missing."""
        key = f"{kind}:{obj_id}"
        if key not in self.cache:
            try:
                self.cache[key] = self.get(f"/api/v2/{kind}/{obj_id}.json")
            except urllib.error.HTTPError:
                self.cache[key] = None
        return self.cache[key]


def parse_ref(ref: str) -> int | None:
    if ref.isdigit():
        return int(ref)
    match = re.search(r"/triggers/(\d+)", ref)
    return int(match.group(1)) if match else None


def name_of(client: Client, kind: str, singular: str, obj_id, attr: str = "name") -> str:
    if obj_id in (None, "", "current_user", "requester_id", "assignee_id", "current_groups"):
        return {"current_user": "(atualizador)", "requester_id": "(solicitante)", "assignee_id": "(responsável)",
                "current_groups": "(grupos do atualizador)", "": "(vazio)", None: "(vazio)"}.get(obj_id, str(obj_id))
    data = client.lookup(kind, obj_id)
    obj = (data or {}).get(singular)
    if not obj:
        return f"{obj_id} (não encontrado)"
    suffix = " [EXCLUÍDO]" if obj.get("deleted") else ""
    return f"{obj.get(attr)} ({obj_id}){suffix}"


def custom_field(client: Client, field_id: str, value) -> tuple[str, str]:
    data = client.lookup("ticket_fields", field_id)
    field = (data or {}).get("ticket_field")
    if not field:
        return f"Campo {field_id} (não encontrado)", json.dumps(value, ensure_ascii=False)
    label = f"Campo \"{field['title']}\" ({field_id})"
    options = {o["value"]: o["name"] for o in field.get("custom_field_options") or []}
    values = value if isinstance(value, list) else [value]
    shown = [f"{options[v]} [{v}]" if v in options else json.dumps(v, ensure_ascii=False) for v in values]
    return label, ", ".join(shown)


def describe(client: Client, field: str, value) -> tuple[str, str]:
    if field.startswith("custom_fields_"):
        return custom_field(client, field.removeprefix("custom_fields_"), value)
    label = FIELD_LABELS.get(field, field)
    if field == "group_id":
        return label, name_of(client, "groups", "group", value)
    if field in ("assignee_id", "requester_id", "notification_user", "notification_sms_user"):
        target = value[0] if isinstance(value, list) else value
        rest = value[1:] if isinstance(value, list) else []
        shown = name_of(client, "users", "user", target)
        return label, shown + (f" | {json.dumps(rest, ensure_ascii=False)}" if rest else "")
    if field == "notification_group":
        target = value[0] if isinstance(value, list) else value
        rest = value[1:] if isinstance(value, list) else []
        return label, name_of(client, "groups", "group", target) + (f" | {json.dumps(rest, ensure_ascii=False)}" if rest else "")
    if field == "organization_id":
        return label, name_of(client, "organizations", "organization", value)
    if field == "brand_id":
        return label, name_of(client, "brands", "brand", value)
    if field == "ticket_form_id":
        return label, name_of(client, "ticket_forms", "ticket_form", value)
    if field == "notification_webhook":
        webhook_id, body = (value[0], value[1:]) if isinstance(value, list) else (value, [])
        try:
            hook = client.get(f"/api/v2/webhooks/{webhook_id}").get("webhook", {})
            shown = f"{hook.get('name')} ({webhook_id}) → {hook.get('http_method')} {hook.get('endpoint')}"
        except urllib.error.HTTPError:
            shown = f"{webhook_id} (não encontrado)"
        if body:
            shown += "\n        corpo: " + "\n        ".join(str(b) for b in body)
        return label, shown
    if field == "notification_target":
        target_id, body = (value[0], value[1:]) if isinstance(value, list) else (value, [])
        return label, name_of(client, "targets", "target", target_id, "title") + (f" | {body}" if body else "")
    if field in ("via_id", "current_via_id"):
        try:
            return label, f"{VIA.get(int(value), value)} ({value})"
        except (TypeError, ValueError):
            return label, str(value)
    if isinstance(value, list):
        return label, ", ".join(json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v for v in value)
    return label, str(value)


def print_trigger(client: Client, t: dict) -> None:
    active = "ativo" if t.get("active") else "INATIVO"
    print(f"{t['id']}\t{t['title']} [{active}]")
    if t.get("description"):
        print(f"  descrição: {t['description']}")
    category = "-"
    if t.get("category_id"):
        try:
            cat = client.get(f"/api/v2/trigger_categories/{t['category_id']}").get("trigger_category", {})
            category = f"{cat.get('name')} ({t['category_id']})"
        except urllib.error.HTTPError:
            category = str(t["category_id"])
    print(f"  categoria: {category} | posição: {t.get('position')} | criado: {t['created_at'][:10]} | atualizado: {t['updated_at'][:10]}")
    print(f"  {client.base_url}/admin/objects-rules/rules/triggers/{t['id']}")
    for block, title in (("all", "Atender TODAS as condições"), ("any", "Atender QUALQUER condição")):
        conds = (t.get("conditions") or {}).get(block) or []
        if conds:
            print(f"  {title}:")
            for c in conds:
                label, shown = describe(client, c["field"], c.get("value"))
                print(f"    - {label} {c.get('operator', '')} {shown}")
    print("  Ações:")
    for a in t.get("actions") or []:
        label, shown = describe(client, a["field"], a.get("value"))
        print(f"    - {label}: {shown}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("refs", nargs="*", help="trigger id or admin link")
    parser.add_argument("--name", help="substring of the trigger title (case-insensitive)")
    parser.add_argument("--env", choices=ENVS, default="sandbox")
    parser.add_argument("--i-confirm-prod", action="store_true", help="explicit approval to read production")
    parser.add_argument("--json", action="store_true", help="print the raw trigger JSON")
    args = parser.parse_args()
    if not args.refs and not args.name:
        parser.error("pass a trigger id/link or --name")
    if args.env == "prod" and not args.i_confirm_prod:
        sys.exit("prod bloqueado: política de não chamar a API de produção do Zendesk por IA "
                 "(vault apis/zendesk-sunco-prod-politica). Só com aprovação explícita do usuário: --i-confirm-prod")

    client = Client(*load_auth(args.env))
    triggers = []
    for ref in args.refs:
        trigger_id = parse_ref(ref)
        if trigger_id is None:
            sys.exit(f"não reconheci id nem link de gatilho em: {ref}")
        try:
            triggers.append(client.get(f"/api/v2/triggers/{trigger_id}.json")["trigger"])
        except urllib.error.HTTPError as err:
            if err.code != 404:
                raise
            print(f"{trigger_id}\tnão encontrado em {args.env} (HTTP 404)", file=sys.stderr)
    if args.name:
        query = urllib.parse.quote(args.name)
        found = client.get_all(f"/api/v2/triggers/search.json?query={query}&per_page=100", "triggers")
        needle = args.name.lower()
        triggers += [t for t in found if needle in t["title"].lower()] or found
        if not found:
            print(f"nenhum gatilho com \"{args.name}\" no título em {args.env}", file=sys.stderr)

    for i, t in enumerate(triggers):
        if i:
            print()
        if args.json:
            print(json.dumps(t, ensure_ascii=False, indent=2))
        else:
            print_trigger(client, t)
    if not triggers:
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as err:
        if err.code in (401, 403):
            sys.exit(f"HTTP {err.code}: token do Zendesk inválido ou sem permissão de admin para ler gatilhos "
                     f"(conferir user_email/personal_user_token_<env> em {ENV_FILE})")
        raise
