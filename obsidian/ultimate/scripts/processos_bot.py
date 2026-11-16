"""Consulta as rotas de processos do bot (contagem e dados) em prd. Uso: processos_bot.py <+55telefone> [idProcesso...]"""
import json, sys, pathlib
sys.path.insert(0, str(pathlib.Path.home() / ".claude/skills/buscar-empresas-por-telefone/scripts"))
import bots_api as b
base = '/atendimento/zendesk/bots/whatsapp/fluxo/interacao/api/v1/bots/whatsapp/identificacao/processos'
url, tok = b.credentials('prd')
def get(p):
    s, r = b.http('GET', url + base + p, b.gateway_headers(tok))
    return s, r
tel = sys.argv[1]
s, r = get(f'/contagem/{tel}')
print('CONTAGEM', s, json.dumps(r.get('data', r) if isinstance(r, dict) else r, ensure_ascii=False))
for pid in sys.argv[2:]:
    s, r = get(f'/dados/{pid}/telefone/{tel}')
    d = r.get('data', r) if isinstance(r, dict) else r
    if isinstance(d, dict):
        d = {k: d.get(k) for k in ('id', 'idJira', 'statusJira', 'plano', 'statusPagto')}
    print('DADOS', pid, s, json.dumps(d, ensure_ascii=False))
