"""Fecha um ticket do requester de teste sem CSAT: adiciona a tag sys_nao_oferecer_csat e põe status closed. Uso: zd_fechar_sem_csat.py <ticketId>"""
import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path.home() / ".claude/skills/fechar-tickets-teste-zendesk/scripts"))
import fechar_tickets as f
a = f.load_auth(); tid = int(sys.argv[1])
t = f.request(a, "GET", f"{f.BASE_URL}/api/v2/tickets/{tid}.json")["ticket"]
assert t["requester_id"] == f.REQUESTER_ID, "ticket não é do requester de teste"
f.request(a, "PUT", f"{f.BASE_URL}/api/v2/tickets/{tid}/tags.json", {"tags": ["sys_csat_survey_sent", "sys_csat_response_exp", "sys_nao_oferecer_csat"]})
print("tag:", "sys_csat_survey_sent" in f.request(a, "GET", f"{f.BASE_URL}/api/v2/tickets/{tid}.json")["ticket"]["tags"])
f.request(a, "PUT", f"{f.BASE_URL}/api/v2/tickets/{tid}.json", {"ticket": {"status": "closed"}})
t = f.request(a, "GET", f"{f.BASE_URL}/api/v2/tickets/{tid}.json")["ticket"]
print(tid, t["status"], "sys_nao_oferecer_csat" in t["tags"])
