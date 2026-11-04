#!/usr/bin/env python3
"""
Close the open Zendesk (prod) tickets requested by Glener's test end-user.

Only ever touches tickets whose requester is REQUESTER_ID (the end-user used to test the WhatsApp bots), and double-checks each ticket's requester before closing it.
Credentials come from the experts-bruno zendesk-api collection .env (user_email, personal_user_token_prod); they are never printed.

Usage:
    fechar_tickets.py list            # list the requester's tickets that are not solved/closed
    fechar_tickets.py close           # close them (update_many + wait for the job)
    fechar_tickets.py close --dry-run # show what would be closed
"""

import base64
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

BASE_URL = "https://contabilizei.zendesk.com"
REQUESTER_ID = 21878313229212
ENV_FILE = Path.home() / "repositories/experts-bruno/zendesk-api/.env"
FINAL_STATUSES = {"solved", "closed"}
BATCH_SIZE = 100


def load_auth() -> str:
    env = {}
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


def request(auth: str, method: str, url: str, body: dict | None = None) -> dict:
    if not url.startswith("http"):
        url = BASE_URL + url
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={"Authorization": auth, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read() or b"{}")


def open_tickets(auth: str) -> list[dict]:
    tickets, url = [], f"/api/v2/users/{REQUESTER_ID}/tickets/requested.json?per_page=100"
    while url:
        page = request(auth, "GET", url)
        tickets += page.get("tickets", [])
        url = page.get("next_page")
    return [t for t in tickets if t["status"] not in FINAL_STATUSES and t["requester_id"] == REQUESTER_ID]


def print_tickets(tickets: list[dict]) -> None:
    for t in sorted(tickets, key=lambda t: t["id"]):
        print(f"{t['id']}\t{t['status']}\t{t['created_at'][:10]}\t{t['subject']}\t{BASE_URL}/agent/tickets/{t['id']}")
    print(f"total: {len(tickets)}")


def close(auth: str, tickets: list[dict]) -> None:
    ids = [t["id"] for t in tickets]
    for i in range(0, len(ids), BATCH_SIZE):
        batch = ids[i : i + BATCH_SIZE]
        job = request(auth, "PUT", "/api/v2/tickets/update_many.json", {"tickets": [{"id": tid, "status": "closed"} for tid in batch]})["job_status"]
        while job["status"] in ("queued", "working"):
            time.sleep(2)
            job = request(auth, "GET", f"/api/v2/job_statuses/{job['id']}.json")["job_status"]
        for result in job.get("results") or []:
            ok = result.get("success", result.get("status") == "Updated")
            print(f"{result.get('id')}\t{'fechado' if ok else 'ERRO'}\t{result.get('error') or result.get('details') or ''}")
        print(f"job {job['id']}: {job['status']}")


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] not in ("list", "close"):
        sys.exit(__doc__)
    auth = load_auth()
    tickets = open_tickets(auth)
    print_tickets(tickets)
    if args[0] == "close" and tickets and "--dry-run" not in args:
        close(auth, tickets)


if __name__ == "__main__":
    main()
