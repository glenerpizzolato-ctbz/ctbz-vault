#!/usr/bin/env python3
"""
List prod companies by plan (BASICO, AVANCADO, EXPERT...) from BigQuery, to use as test data.

Source: contabilizei-dataflow.saude_empresa.empresa (monthly snapshot, prod only), latest period of each company.
Runs the query through the `bq` CLI (read-only); companies are picked at random so each run returns a different sample.

Usage:
    buscar_empresas.py BASICO                      # 10 active BASICO companies
    buscar_empresas.py BASICO -n 5                 # 5 companies
    buscar_empresas.py EXPERT --status INATIVO     # EXPERT matches EXPERT_ESSENCIAL and EXPERT_PRO
    buscar_empresas.py AVANCADO --uf SP --regime SIMPLES_NACIONAL
    buscar_empresas.py --planos                    # plans available in the latest snapshot
"""

import argparse
import json
import re
import subprocess
import sys

PROJECT = "contabilizei-dataflow"
TABLE = "`contabilizei-dataflow.saude_empresa.empresa`"
COLUMNS = ["cnpj", "razao_social", "plano", "status", "motivo_status", "regime_tributario", "uf", "municipio", "cnae_principal", "periodo"]


def run_query(sql: str) -> list[dict]:
    cmd = ["bq", "query", f"--project_id={PROJECT}", "--use_legacy_sql=false", "--format=json", "--max_rows=1000", sql]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        sys.exit(f"bq query failed: {res.stderr.strip() or res.stdout.strip()}")
    out = res.stdout.strip()
    return json.loads(out) if out else []


def safe(value: str, name: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_ ]+", value):
        sys.exit(f"invalid {name}: {value!r}")
    return value.upper()


def list_plans() -> None:
    rows = run_query(f"""
        SELECT IFNULL(plano, '(null)') AS plano, status, COUNT(*) AS empresas
        FROM {TABLE}
        WHERE periodo = (SELECT MAX(periodo) FROM {TABLE})
        GROUP BY 1, 2
        ORDER BY 1, 2
    """)
    print("plano\tstatus\tempresas")
    for r in rows:
        print(f"{r['plano']}\t{r['status']}\t{r['empresas']}")


def search(args: argparse.Namespace) -> None:
    plano = safe(args.plano, "plano")
    filters = [f"STARTS_WITH(plano, '{plano}')" if args.prefixo else f"plano = '{plano}'"]
    if args.status != "TODOS":
        filters.append(f"status = '{safe(args.status, 'status')}'")
    if args.uf:
        filters.append(f"uf = '{safe(args.uf, 'uf')}'")
    if args.regime:
        filters.append(f"regime_tributario = '{safe(args.regime, 'regime')}'")
    # Inactive companies drop out of later snapshots; everyone else must be in the latest one, so the data is current
    if args.status not in ("INATIVO", "TODOS"):
        filters.append(f"periodo = (SELECT MAX(periodo) FROM {TABLE})")

    rows = run_query(f"""
        WITH ultimo AS (
            SELECT {', '.join(COLUMNS)}
            FROM {TABLE}
            WHERE cnpj IS NOT NULL
            QUALIFY ROW_NUMBER() OVER (PARTITION BY cnpj ORDER BY periodo DESC) = 1
        )
        SELECT * FROM ultimo
        WHERE {' AND '.join(filters)}
        ORDER BY RAND()
        LIMIT {args.n}
    """)
    if not rows:
        print("nenhuma empresa encontrada")
        return
    print("\t".join(COLUMNS))
    for r in rows:
        print("\t".join(str(r.get(c) or "") for c in COLUMNS))
    print(f"total: {len(rows)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="List prod companies by plan (BigQuery saude_empresa.empresa)")
    parser.add_argument("plano", nargs="?", help="plan, e.g. BASICO, AVANCADO, PREMIUM, MULTIBENEFICIOS, EXPERT")
    parser.add_argument("-n", type=int, default=10, help="how many companies (default 10)")
    parser.add_argument("--status", default="ATIVO", help="ATIVO (default), INATIVO, RASCUNHO or TODOS")
    parser.add_argument("--uf", help="filter by state, e.g. SP")
    parser.add_argument("--regime", help="filter by regime_tributario")
    parser.add_argument("--exato", action="store_true", help="exact plan match (by default EXPERT matches EXPERT_*)")
    parser.add_argument("--planos", action="store_true", help="list the plans available and exit")
    args = parser.parse_args()

    args.status = args.status.upper()
    if args.planos:
        list_plans()
        return
    if not args.plano:
        parser.error("plano is required (or use --planos)")
    if args.n < 1 or args.n > 1000:
        parser.error("-n must be between 1 and 1000")
    args.prefixo = not args.exato and args.plano.upper() == "EXPERT"
    search(args)


if __name__ == "__main__":
    main()
