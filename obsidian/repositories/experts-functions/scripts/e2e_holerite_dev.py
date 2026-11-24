#!/usr/bin/env python3
"""
E2E test of the holerite email in DEV, from the event arriving at function-email-holerites
to the email-service dispatch.

Flow under test:
    functions.email-holerites (Pub/Sub, contabilizei-experts-dev)
      -> function-email-holerites (builds the HTML of each holerite)
      -> function-html-to-pdf (one PDF per employee with a valid movement)
      -> email-service.p2p.file-upload (PDFs, atendimento-canais-dev)
      -> email-service.p2p.send-email (template exp-email-holerite-v1)
      -> email-service dispatch (HubSpot SMTP)

What it checks, step by step:
    1. function log "Holerites enviados por email ... emailId" for the run (and no ERROR);
    2. the email_replications row of that emailId: template, from, to, subject, variables, application,
       opt-out data and one attachment per valid employee (the BASE_CALCULO-only one is left out);
    3. each attachment in the email-service bucket is a PDF with the employee name, company and period;
    4. the rendered email (template + variables) is saved as HTML and PNG for visual review;
    5. the final status of the send (SENT, or FAILED: dev SMTP has been rejected by HubSpot with
       421 "connected email sending domain" since 2026-08-20, see the vault note smtp-dev-hubspot-dominio);
    6. a second event with no valid employee must not produce any send.

Requirements: gcloud authenticated (pubsub publish in contabilizei-experts-dev, logging read,
storage read in ctbz-email-service-dev-storage), the psql service `dev_atendimento_canais_email_service`
(proxy `sql_atendimento_dev` up), pdftotext and google-chrome (optional, for the PNG).

Usage:
    python3 functions/email-holerites/e2e/run_dev.py --to you@contabilizei.com.br [--out ./e2e-out]
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone

EXPERTS_PROJECT = 'contabilizei-experts-dev'
TOPIC = 'functions.email-holerites'
FUNCTION_SERVICE = 'function-email-holerites'
BUCKET = 'ctbz-email-service-dev-storage'
PG_SERVICE = 'dev_atendimento_canais_email_service'
TEMPLATE_NAME = 'exp-email-holerite-v1'
EXPECTED_FROM = 'Equipe Contabilizei Experts <atendimento.experts@contabilizei.com.br>'
EXPECTED_SUBJECT = 'A folha de pagamento da sua empresa está pronta'
EXPECTED_APPLICATION = 'function-email-holerites'
CNPJ = '00000000000191'
ANO, MES = '2026', 'NOVEMBRO'

results: list[tuple[str, bool, str]] = []


def check(step: str, ok: bool, detail: str = '') -> bool:
    results.append((step, ok, detail))
    print(f"[{'OK' if ok else 'FALHA'}] {step}{' — ' + detail if detail else ''}", flush=True)
    return ok


def run(cmd: list[str], **kw) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw).stdout


def movimento(natureza: str, descricao: str, valor: float) -> dict:
    return {
        'naturezaMovimento': natureza,
        'codigo': '001',
        'descricao': descricao,
        'quantidade': 1,
        'siglaUnidadeDeMedida': 'DIA',
        'valor': valor,
    }


def colaborador(nome: str, movimentos: list[dict]) -> dict:
    return {
        'nomeColaborador': nome,
        'pisPasep': '12345678901',
        'dataAdmissao': '2015-06-20T00:00:00.000Z',
        'categoria': 'Operacional',
        'cargoCbo': '411010',
        'cargoDescricao': 'Assistente Administrativo',
        'folhaColaborador': {
            'totalProventos': 3000.0,
            'totalDescontos': 500.0,
            'salarioBase': 3000.0,
            'salarioINSS': 2500.0,
            'numeroDependentes': 1,
            'salarioBaseIRRF': 2800.0,
            'valorFGTS': 240.0,
            'salarioBaseFGTS': 3000.0,
        },
        'movimentos': movimentos,
    }


def payload(to: str, nome_responsavel: str, colaboradores: list[dict]) -> dict:
    return {
        'emailResponsavel': to,
        'nomeResponsavel': nome_responsavel,
        'ano': ANO,
        'mes': MES,
        'razaoSocialEmpresaSearch': 'Empresa E2E Holerite LTDA',
        'cnpjEmpresaSearch': CNPJ,
        'colaboradores': colaboradores,
    }


def publish(message: dict) -> str:
    out = run([
        'gcloud', 'pubsub', 'topics', 'publish', TOPIC,
        f'--project={EXPERTS_PROJECT}', f'--message={json.dumps(message, ensure_ascii=False)}',
        '--format=value(messageIds)',
    ])
    return out.strip()


def function_logs(marker: str, since: str) -> list[str]:
    flt = (
        f'resource.type="cloud_run_revision" resource.labels.service_name="{FUNCTION_SERVICE}" '
        f'timestamp>="{since}" SEARCH("{marker}")'
    )
    out = run(['gcloud', 'logging', 'read', flt, f'--project={EXPERTS_PROJECT}', '--format=json', '--limit=50'])
    lines = []
    for entry in json.loads(out or '[]'):
        msg = (entry.get('jsonPayload') or {}).get('message') or entry.get('textPayload') or ''
        lines.append(str(msg))
    return lines


def wait_function_log(marker: str, since: str, timeout_s: int) -> tuple[str | None, list[str]]:
    deadline = time.time() + timeout_s
    lines: list[str] = []
    while time.time() < deadline:
        lines = function_logs(marker, since)
        if any(' ERROR ' in line for line in lines):
            return None, lines
        for line in lines:
            match = re.search(r'Holerites enviados por email.*emailId "([^"]+)"', line)
            if match:
                return match.group(1), lines
        time.sleep(10)
    return None, lines


def psql_json(sql: str) -> list[dict]:
    out = run(['psql', '-w', f'service={PG_SERVICE}', '-At', '-c', f'select coalesce(json_agg(t), \'[]\') from ({sql}) t'])
    return json.loads(out.strip() or '[]')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--to', required=True, help='recipient (the responsible email in the payload)')
    parser.add_argument('--out', default='e2e-out', help='folder for the PDFs, rendered email and report')
    parser.add_argument('--timeout', type=int, default=300, help='seconds to wait for each async step')
    args = parser.parse_args()

    run_id = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
    out_dir = os.path.join(args.out, run_id)
    os.makedirs(out_dir, exist_ok=True)
    since = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    nome = f'Responsavel E2E {run_id}'
    nome_vazio = f'Responsavel E2E Vazio {run_id}'
    validos = ['Maria José da Silva', 'Ana Paula Souza']
    msg_ok = payload(args.to, nome, [
        colaborador(validos[0], [movimento('PROVENTO', 'Salário', 3000.0), movimento('DESCONTO', 'INSS', 250.0)]),
        colaborador(validos[1], [movimento('PROVENTO', 'Salário', 2000.0)]),
        colaborador('Somente Base Calculo', [movimento('BASE_CALCULO', 'Base INSS', 3000.0)]),
    ])
    msg_vazio = payload(args.to, nome_vazio, [
        colaborador('Somente Base Calculo', [movimento('BASE_CALCULO', 'Base INSS', 3000.0)]),
    ])
    with open(os.path.join(out_dir, 'payload.json'), 'w') as f:
        json.dump(msg_ok, f, ensure_ascii=False, indent=2)

    print(f'Run {run_id}: publicando em {TOPIC} ({EXPERTS_PROJECT})', flush=True)
    check('evento publicado', bool(publish(msg_ok)))
    check('evento sem colaborador válido publicado', bool(publish(msg_vazio)))

    # 1. function
    email_id, lines = wait_function_log(nome, since, args.timeout)
    if not check('function enviou ao email-service', email_id is not None, email_id or ' | '.join(lines[-3:]) or 'sem log'):
        return report(out_dir)

    # 2. email_replications
    rows = psql_json(f"select * from email_replications where id = '{email_id}'")
    if not check('registro em email_replications', len(rows) == 1, email_id):
        return report(out_dir)
    rep = rows[0]
    template = psql_json(f"select id, html_content from email_templates where name = '{TEMPLATE_NAME}'")
    check('template exp-email-holerite-v1', bool(template) and rep['template_id'] == template[0]['id'], rep['template_id'])
    check('remetente', rep['from'] == EXPECTED_FROM, rep['from'])
    check('destinatário', rep['to'] == [args.to], str(rep['to']))
    check('assunto', rep['subject'] == EXPECTED_SUBJECT, rep['subject'])
    check('application', rep['application'] == EXPECTED_APPLICATION, rep['application'])
    check('variáveis NOME e PERIODO', rep['variables'] == {'NOME': nome, 'PERIODO': f'{ANO} / {MES}'}, json.dumps(rep['variables'], ensure_ascii=False))
    check('opt-out TRANSACTIONAL com CNPJ', rep.get('optout_purpose') == 'TRANSACTIONAL' and rep.get('cnpj') == CNPJ, f"{rep.get('optout_purpose')} {rep.get('cnpj')}")
    expected_files = sorted(f"{n.upper().replace(' ', '_')}_{ANO}/{MES}.pdf" for n in validos)
    filenames = sorted(a['filename'] for a in rep['attachments'])
    check('um anexo por colaborador válido', filenames == expected_files, ', '.join(filenames))

    # 3. PDFs
    for i, attachment in enumerate(rep['attachments']):
        local = os.path.join(out_dir, f'anexo-{i + 1}.pdf')
        try:
            run(['gcloud', 'storage', 'cp', f"gs://{BUCKET}/files/{attachment['path']}", local])
        except subprocess.CalledProcessError as error:
            check(f"PDF {attachment['filename']} no bucket", False, error.stderr.strip()[-200:])
            continue
        is_pdf = open(local, 'rb').read(5) == b'%PDF-'
        text = run(['pdftotext', '-layout', local, '-']) if is_pdf and shutil.which('pdftotext') else ''
        nome_colab = next((n for n in validos if attachment['filename'].startswith(n.upper().replace(' ', '_'))), '')
        ok = is_pdf and nome_colab in text and 'Empresa E2E Holerite LTDA' in text and f'{MES} / {ANO}' in ' '.join(text.split())
        check(f"PDF {attachment['filename']}", ok, local)

    # 4. rendered email
    if template:
        html = template[0]['html_content']
        for key, value in rep['variables'].items():
            html = html.replace('{{' + key + '}}', value)
        html_path = os.path.join(out_dir, 'email.html')
        with open(html_path, 'w') as f:
            f.write(html)
        if shutil.which('google-chrome'):
            subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', '--window-size=700,1600',
                            f"--screenshot={os.path.join(out_dir, 'email.png')}", f'file://{os.path.abspath(html_path)}'],
                           capture_output=True)
        check('e-mail renderizado', nome in html and f'{ANO} / {MES}' in html, html_path)

    # 5. dispatch status
    deadline = time.time() + args.timeout
    status = rep['status']
    while status == 'PENDING' and time.time() < deadline:
        time.sleep(10)
        status = psql_json(f"select status from email_replications where id = '{email_id}'")[0]['status']
    known_dev_smtp = status == 'FAILED'
    check('envio pelo SMTP', status == 'SENT' or known_dev_smtp,
          status + (' (esperado em dev: HubSpot de dev recusa o domínio com 421)' if known_dev_smtp else ''))

    # 6. no send for the event without valid employees
    vazio = [line for line in function_logs(nome_vazio, since) if 'enviados por email' in line]
    rows_vazio = psql_json(f"select id from email_replications where application = '{EXPECTED_APPLICATION}' and variables->>'NOME' = '{nome_vazio}'")
    check('sem envio quando nenhum colaborador é válido', not vazio and not rows_vazio)

    return report(out_dir)


def report(out_dir: str) -> int:
    failed = [r for r in results if not r[1]]
    lines = [f"# E2E holerite dev — {os.path.basename(out_dir)}", '', '| Passo | Resultado | Detalhe |', '|---|---|---|']
    lines += [f"| {s} | {'OK' if ok else 'FALHA'} | {d.replace('|', '/')} |" for s, ok, d in results]
    with open(os.path.join(out_dir, 'report.md'), 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"\n{len(results) - len(failed)}/{len(results)} OK. Evidências em {out_dir}", flush=True)
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())
