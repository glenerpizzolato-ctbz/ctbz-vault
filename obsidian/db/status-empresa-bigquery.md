---
name: status-empresa-bigquery
description: "Como consultar status, motivo de inatividade, plano e regime de uma empresa de prod pelo BigQuery (saude_empresa.empresa), quando a API ou o admin não estão à mão"
metadata:
  type: reference
tags:
  - db
  - bigquery
  - prd
atualizado_em: 2026-10-26
---

# Status da empresa (prod) pelo BigQuery

Os dados de empresa da plataforma não ficam nos Postgres de [[bancos-prd]]. Para conferir em prod o status (`ATIVO`/`INATIVO`), o motivo (`BAIXA`, `INADIMPLENCIA`, `CANCELAMENTO`...), a data de inativação, o plano e o regime de uma empresa, a fonte mais rápida é a tabela `contabilizei-dataflow.saude_empresa.empresa`:

```sql
SELECT cnpj, periodo, status, motivo_status, data_inativacao, plano, regime_tributario, razao_social
FROM `contabilizei-dataflow.saude_empresa.empresa`
WHERE cnpj IN ('<cnpj>')
QUALIFY ROW_NUMBER() OVER (PARTITION BY cnpj ORDER BY periodo DESC) = 1
```

- Rodar com `bq query --project_id contabilizei-dataflow --use_legacy_sql=false "..."`. O usuário tem leitura no `contabilizei-dataflow`, mas no `contabilizei-data` só vê poucos datasets.
- É um **snapshot mensal** (uma linha por `periodo` AAAAMM): uma mudança de status recente pode ainda não aparecer. Em 2026-10-26, o período mais recente era `202609`.
- Só tem prod. Para dev, usar o admin (`admin-dev-03`) ou a API do bot (ver [[clientes-inativos-cnpjs-teste]]); a API do monolito em dev exige token autorizado para `monolito-dev-0N` (ver [[rotas-busca-empresa]]).
- Outras tabelas com `motivo_status` (histórico): `trusted_engajamento.hist_status_clientes_periodo`, `vw_obrigacoes_folha.vw_listaHistoricoStatusEmpresa`.
- Para listar empresas por plano (massa de teste), usar a skill `buscar-empresas-por-plano` (`~/ctbz-vault/skills/empresas/buscar-empresas-por-plano/`). Planos na coluna `plano`: `BASICO`, `AVANCADO`, `PREMIUM`, `MULTIBENEFICIOS`, `EXPERT_ESSENCIAL`, `EXPERT_PRO` (`NULL` em `TRIAL`).
- **Alternativa em tempo real (prd):** a API do monolito pela coleção `contabilizeiapp` do experts-bruno, com `getByCnpj` (uma empresa) e `auth/filtrarempresas` (listagem paginada, com o plano em `planoPagamentoEmpresa.pagtoPlano.categoriaV2.nome`). Ver [[rotas-busca-empresa]]. Usar para confirmar o plano/status atual, já que o BigQuery pode estar até um mês defasado.
