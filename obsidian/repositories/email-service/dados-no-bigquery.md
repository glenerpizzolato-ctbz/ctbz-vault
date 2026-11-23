---
name: email-service-dados-no-bigquery
description: "email_replications e email_templates do email-service no BigQuery (trusted do CDC): particionamento, cluster, atraso D-1, completude contra o Postgres e o que falta"
metadata:
  type: reference
tags:
  - email-service
  - bigquery
  - cdc
---

# Dados do email-service no BigQuery

As tabelas do banco `email_service` (instância atendimento-canais prd) chegam ao BigQuery pelo CDC (ver [[cdc-atendimento-canais]]), no dataset `contabilizei-data.cloudsql_atendimento_canais_prd_atendimento_canais_email_service_trusted` (o `_raw` dá Access Denied para usuário comum).

- `email_replications`: particionada por dia em `created_at` e clusterizada por `status, template_id, application, from`, label `contains_pii:yes` (`to`, `variables`, `attachments`). Colunas: `id, subject, template_id, variables, text, attachments, application, status, created_at, updated_at, to, from` + metadados do CDC (`last_event_ts, _min_target_ts, __op`).
- `email_templates`: `id, name, html_content, variables, author, created_at, updated_at`. **Não tem a coluna `status`** (soft delete, ver [[status-de-templates]]), adicionada depois do CDC; quem precisa do status lê do email-service.
- **Atraso D-1**: o trusted é materializado por dbt uma vez por dia (~04:15 UTC, dados até ~03:00 UTC, isto é, até a meia-noite de Brasília). Em 23/11/2026 às 11h BRT, o último `created_at` era 00:00 BRT.
- **Completude**: conferido em 23/11/2026 contra o Postgres de prod até o mesmo corte: 193.906 linhas no PG x 193.921 no BQ (diferença só da borda do segundo de corte), 37 templates distintos, histórico desde 27/03/2026 (início da tabela também no PG). Status refletem o último estado (PENDING que virou SENT aparece SENT).
- **Custo**: agregado de 30 dias por `template_id, application, status` processa ~2,7 MB.
- Só existe prd: em dev o BigQuery traz os UUIDs de prd, que não batem com os de dev (templates copiados ganham UUID novo, ver [[replicar-template-prd-para-dev]]).
- Status vistos nos últimos 30 dias: `SENT`, `FAILED`, `PENDING` e `BLOCKED_OPTOUT`.

O atendimento-canais-admin já consulta trusted desse mesmo CDC (`canais_adk`) com o client `src/server/clients/bigquery` (projeto de job `contabilizei-dataflow`), então o acesso já existe.

## Custo das consultas (medido em 23/11/2026)

Jobs rodados no projeto `contabilizei-dataflow` (o mesmo do client do admin):

| Consulta | Processado | Cobrado |
| --- | --- | --- |
| Agregado 30d por `template_id, application, status` + `max(created_at)` | 2,7 MB (31 partições) | 0 |
| O mesmo, filtrando só alguns `template_id` | 2,7 MB (o cluster não reduz numa tabela deste tamanho) | 0 |
| Último envio de todo o histórico (`max(created_at)` por template) | 8,9 MB | 0 |
| Mesma consulta repetida com data fixa | 0 (cache) | 0 |

- O cobrado vem 0 porque as consultas rodam **100% aceleradas pelo BI Engine** (`biEngineMode: FULL`) do projeto: a capacidade já é paga, não há custo por byte. Se o BI Engine não acelerar (memória cheia, mudança de reserva), cai no on-demand (US$ 6,25/TiB, mínimo de 10 MB por tabela): ~US$ 0,00006 por consulta.
- `current_timestamp()` no filtro impede o cache de resultado do BigQuery; usar a data como parâmetro fixo do dia (o trusted só muda uma vez por dia).
- Latência: ~250–330 ms por consulta.
