#!/usr/bin/env python3
"""
E2E in DEV of the push subscription of function-email-holerites (PRD-178821 / PRD-178827):
the own subscription `function-email-holerites-sub` (ack 600 s, backoff 10-600 s, DLQ after 10 attempts)
that replaced the Eventarc one (ack 10 s, no DLQ).

Cases:
    slow  - a valid event with many employees, so the push request takes longer than 10 s (the old ack
            deadline). Expected: one request, one "Holerites enviados" log and one email_replications row
            (no duplicate holerite).
    dlq   - an event whose PDF is too big for the email-service file-upload topic (10 MB message limit,
            Buffer.toJSON inflates ~3.5x), so the function answers 500 on every attempt. Expected:
            the message reaches `functions.email-holerites.dlq-sub` with
            CloudPubSubDeadLetterSourceDeliveryCount = 10, the function got 10 requests and nothing was sent.

Requirements: the same as e2e_holerite_dev.py (gcloud, psql service dev_atendimento_canais_email_service).

Usage:
    python3 -I e2e_holerite_sub_dlq_dev.py --to you@contabilizei.com.br [--cases slow,dlq] [--out DIR]
"""

import argparse
import base64
import json
import os
import random
import string
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import e2e_holerite_dev as base  # noqa: E402

SUBSCRIPTION = 'function-email-holerites-sub'
DLQ_SUB = 'functions.email-holerites.dlq-sub'
MAX_ATTEMPTS = 10


def now() -> str:
    return datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def publish_big(message: dict) -> str:
    """REST publish: gcloud --message does not take a multi-MB argument."""
    token = base.run(['gcloud', 'auth', 'print-access-token']).strip()
    body = json.dumps({'messages': [{'data': base64.b64encode(json.dumps(message, ensure_ascii=False).encode()).decode()}]})
    req = urllib.request.Request(
        f'https://pubsub.googleapis.com/v1/projects/{base.EXPERTS_PROJECT}/topics/{base.TOPIC}:publish',
        data=body.encode(), headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)['messageIds'][0]


def push_requests(since: str, until: str) -> list[dict]:
    flt = (
        f'resource.type="cloud_run_revision" resource.labels.service_name="{base.FUNCTION_SERVICE}" '
        f'httpRequest.requestUrl:"/rhc/folha/notificar" timestamp>="{since}" timestamp<="{until}"'
    )
    out = base.run(['gcloud', 'logging', 'read', flt, f'--project={base.EXPERTS_PROJECT}', '--format=json', '--limit=200'])
    return [
        {'ts': e['timestamp'], 'status': e['httpRequest'].get('status'), 'latency': e['httpRequest'].get('latency')}
        for e in json.loads(out or '[]')
    ]


def replications(nome: str) -> list[dict]:
    return base.psql_json(
        f"select id, status, created_at from email_replications where application = '{base.EXPECTED_APPLICATION}' "
        f"and variables->>'NOME' = '{nome}'"
    )


def case_slow(to: str, run_id: str, n: int, timeout: int) -> None:
    nome = f'Responsavel E2E Lenta {run_id}'
    colabs = [
        base.colaborador(f'Colaborador {i:03d}', [base.movimento('PROVENTO', 'Salário', 3000.0 + i), base.movimento('DESCONTO', 'INSS', 250.0)])
        for i in range(n)
    ]
    since = now()
    base.check(f'[lenta] evento com {n} colaboradores publicado', bool(base.publish(base.payload(to, nome, colabs))))
    email_id, lines = base.wait_function_log(nome, since, timeout)
    base.check('[lenta] function enviou ao email-service', email_id is not None, email_id or ' | '.join(lines[-3:]) or 'sem log')
    # Old ack deadline was 10 s: wait well past it and past the first backoff to catch any redelivery.
    time.sleep(180)
    reqs = push_requests(since, now())
    latencies = ', '.join(f"{r['status']} {r['latency']}" for r in reqs)
    slow = any(float((r['latency'] or '0s').rstrip('s')) > 10 for r in reqs)
    base.check('[lenta] requisição passou de 10 s (cenário do bug antigo)', slow, latencies)
    base.check('[lenta] uma única entrega (1 requisição, 202)', len(reqs) == 1 and reqs[0]['status'] == 202, latencies)
    sent = [line for line in base.function_logs(nome, since) if 'enviados por email' in line]
    base.check('[lenta] um único log "Holerites enviados"', len(sent) == 1, str(len(sent)))
    rows = replications(nome)
    base.check('[lenta] um único registro em email_replications', len(rows) == 1, ', '.join(r['id'] for r in rows))


def case_dlq(to: str, run_id: str, movimentos: int, timeout: int) -> None:
    nome = f'Responsavel E2E DLQ {run_id}'
    rnd = random.Random(run_id)
    movs = [
        base.movimento('PROVENTO', ''.join(rnd.choices(string.ascii_letters + string.digits, k=60)), 1.0 + i)
        for i in range(movimentos)
    ]
    msg = base.payload(to, nome, [base.colaborador('Colaborador PDF Gigante', movs)])
    since = now()
    message_id = publish_big(msg)
    base.check(f'[dlq] evento com PDF gigante publicado ({movimentos} movimentos, {len(json.dumps(msg)) // 1024} KB)', bool(message_id), message_id)

    deadline = time.time() + timeout
    found = None
    while time.time() < deadline and not found:
        time.sleep(60)
        out = base.run(['gcloud', 'pubsub', 'subscriptions', 'pull', DLQ_SUB, f'--project={base.EXPERTS_PROJECT}', '--limit=20', '--format=json'])
        for item in json.loads(out or '[]'):
            data = base64.b64decode(item['message'].get('data', '')).decode(errors='replace')
            if nome in data:
                found = item
                base.run(['gcloud', 'pubsub', 'subscriptions', 'ack', DLQ_SUB, f'--project={base.EXPERTS_PROJECT}', f"--ack-ids={item['ackId']}"])
        print(f'  {now()} aguardando DLQ... requisições até agora: {len(push_requests(since, now()))}', flush=True)
    until = now()
    if not base.check('[dlq] mensagem chegou na functions.email-holerites.dlq-sub', found is not None, f'após {(time.time() - (deadline - timeout)) / 60:.0f} min'):
        return
    attrs = found['message'].get('attributes', {})
    base.check('[dlq] origem é a function-email-holerites-sub',
               attrs.get('CloudPubSubDeadLetterSourceSubscription') == SUBSCRIPTION, attrs.get('CloudPubSubDeadLetterSourceSubscription', ''))
    base.check(f'[dlq] {MAX_ATTEMPTS} tentativas de entrega',
               attrs.get('CloudPubSubDeadLetterSourceDeliveryCount') == str(MAX_ATTEMPTS), attrs.get('CloudPubSubDeadLetterSourceDeliveryCount', ''))
    reqs = push_requests(since, until)
    statuses = sorted({str(r['status']) for r in reqs})
    base.check(f'[dlq] function recebeu {MAX_ATTEMPTS} requisições, todas com erro',
               len(reqs) == MAX_ATTEMPTS and all(r['status'] not in (102, 200, 201, 202, 204) for r in reqs),
               f"{len(reqs)} requisições, status {', '.join(statuses)}; primeira {reqs[-1]['ts'] if reqs else '-'}, última {reqs[0]['ts'] if reqs else '-'}")
    errors = [line for line in base.function_logs(nome, since) if 'ERROR' in line or 'rror' in line]
    base.check('[dlq] log de erro da function', bool(errors), (errors[0][:200] if errors else 'sem log'))
    base.check('[dlq] nenhum envio em email_replications', not replications(nome))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--to', required=True)
    parser.add_argument('--cases', default='slow,dlq')
    parser.add_argument('--out', default='e2e-out')
    parser.add_argument('--employees', type=int, default=40, help='employees in the slow case')
    parser.add_argument('--movements', type=int, default=30000, help='movements in the DLQ case (PDF size)')
    parser.add_argument('--timeout', type=int, default=600, help='seconds to wait for the slow case')
    parser.add_argument('--dlq-timeout', type=int, default=5400, help='seconds to wait for the DLQ case')
    args = parser.parse_args()

    run_id = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
    out_dir = os.path.join(args.out, f'sub-dlq-{run_id}')
    os.makedirs(out_dir, exist_ok=True)
    print(f'Run {run_id}: {base.TOPIC} -> {SUBSCRIPTION} ({base.EXPERTS_PROJECT})', flush=True)
    cases = args.cases.split(',')
    if 'slow' in cases:
        case_slow(args.to, run_id, args.employees, args.timeout)
    if 'dlq' in cases:
        case_dlq(args.to, run_id, args.movements, args.dlq_timeout)
    return base.report(out_dir)


if __name__ == '__main__':
    sys.exit(main())
