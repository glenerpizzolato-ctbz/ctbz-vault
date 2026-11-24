"""Últimos tickets do requester de teste (21878313229212) no Zendesk prd, com grupo e tags. Uso: zd_tickets.py [n] [--since-id ID]"""
import sys, json, pathlib
sys.path.insert(0, str(pathlib.Path.home() / ".claude/skills/fechar-tickets-teste-zendesk/scripts"))
import fechar_tickets as f
auth = f.load_auth()
n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 3
since = int(sys.argv[sys.argv.index('--since-id') + 1]) if '--since-id' in sys.argv else 0
d = f.request(auth, "GET", f"{f.BASE_URL}/api/v2/users/{f.REQUESTER_ID}/tickets/requested?sort_by=created_at&sort_order=desc&per_page={n}")
groups = {}
for t in d.get("tickets", []):
    if t["id"] <= since: continue
    g = t.get("group_id")
    if g and g not in groups:
        try: groups[g] = f.request(auth, "GET", f"{f.BASE_URL}/api/v2/groups/{g}")["group"]["name"]
        except Exception: groups[g] = "?"
    print(json.dumps({"id": t["id"], "created": t["created_at"], "status": t["status"], "group_id": g, "group": groups.get(g), "via": t.get("via", {}).get("channel"), "tags": [x for x in t.get("tags", []) if x.startswith(("sys_", "ultimate", "grupo"))][:8]}, ensure_ascii=False))
