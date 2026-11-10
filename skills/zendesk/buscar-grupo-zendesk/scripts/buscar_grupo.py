#!/usr/bin/env python3
"""
Look up Zendesk (prod) groups by id or by name, read-only.

Credentials come from the experts-bruno zendesk-api collection .env (user_email, personal_user_token_prod); they are never printed.
Same route as the collection's "Support API/groups/fetch" request (GET /api/v2/groups/{id}).

Usage:
    buscar_grupo.py 15262373080476 [17824694735388 ...]   # fetch by id (name, description, deleted, dates)
    buscar_grupo.py --name "suporte"                        # list groups whose name contains the text (case-insensitive)
    buscar_grupo.py 15262373080476 --members                # also list the group's agents
"""

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = "https://contabilizei.zendesk.com"
ENV_FILE = Path.home() / "repositories/experts-bruno/zendesk-api/.env"


def load_auth() -> str:
    env = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip().strip('"').strip("'")
    email = env.get("user_email") or os.environ.get("user_email")
    token = env.get("personal_user_token_prod") or os.environ.get("personal_user_token_prod")
    if not email or not token:
        sys.exit(f"user_email/personal_user_token_prod missing in {ENV_FILE}")
    return "Basic " + base64.b64encode(f"{email}/token:{token}".encode()).decode()


def get(auth: str, url: str) -> dict:
    if not url.startswith("http"):
        url = BASE_URL + url
    req = urllib.request.Request(url, headers={"Authorization": auth, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read() or b"{}")


def print_group(g: dict) -> None:
    deleted = " (EXCLUÍDO)" if g.get("deleted") else ""
    print(f"{g['id']}\t{g['name']}{deleted}")
    if g.get("description"):
        print(f"  descrição: {g['description']}")
    print(f"  default: {g.get('default')} | privado: {g.get('is_public') is False} | criado: {g['created_at'][:10]} | atualizado: {g['updated_at'][:10]}")
    print(f"  {BASE_URL}/admin/people/team/groups/{g['id']}")


def print_members(auth: str, group_id: int) -> None:
    url = f"/api/v2/groups/{group_id}/users.json?per_page=100"
    users = []
    while url:
        page = get(auth, url)
        users += page.get("users", [])
        url = page.get("next_page")
    print(f"  membros ({len(users)}):")
    for u in sorted(users, key=lambda u: u["name"]):
        print(f"    {u['id']}\t{u['name']}\t{u.get('email') or ''}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("ids", nargs="*", type=int)
    parser.add_argument("--name", help="substring of the group name (case-insensitive)")
    parser.add_argument("--members", action="store_true", help="also list the group's agents")
    args = parser.parse_args()
    if not args.ids and not args.name:
        parser.error("pass at least one group id or --name")

    auth = load_auth()
    groups = []
    for gid in args.ids:
        try:
            groups.append(get(auth, f"/api/v2/groups/{gid}.json")["group"])
        except urllib.error.HTTPError as e:
            print(f"{gid}\tERRO HTTP {e.code} ({'grupo não encontrado' if e.code == 404 else e.reason})")
    if args.name:
        url, needle = "/api/v2/groups.json?per_page=100", args.name.lower()
        while url:
            page = get(auth, url)
            groups += [g for g in page.get("groups", []) if needle in g["name"].lower()]
            url = page.get("next_page")
        if not groups:
            print(f"nenhum grupo com '{args.name}' no nome")

    for g in groups:
        print_group(g)
        if args.members:
            print_members(auth, g["id"])


if __name__ == "__main__":
    main()
