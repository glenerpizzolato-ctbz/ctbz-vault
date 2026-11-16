---
name: cdc-atendimento-canais
description: "Tabelas da instância atendimento-canais (prd) migradas do sql2bq para o CDC (Datastream) no BigQuery, por banco, com o modo de merge e o histórico da migração"
metadata:
  type: reference
tags:
  - db
  - cdc
  - datastream
  - bigquery
---

# CDC (Datastream) do atendimento-canais

Migração da ingestão para o BigQuery do sql2bq para o CDC (Datastream), conduzida pelo time de dados (Geovanni Corsino) no chat do Google Chat "CDC | Atendimento Canais" (space `AAQAPSVXqVM`). A configuração por tabela fica na planilha "Datastream | atendimento-canais-prd" (`1EgNbNzs1HAQQ1FvxxKUnAapAYA1i3eu2yXJYWa9p0ag`), e o detalhe da GMUD no Outline (`gmud-migracao-cdc-datastream-atendimento-canais-prd`).

Datasets em `contabilizei-data`: `cloudsql_atendimento_canais_prd_atendimento_canais_<banco>_raw` (bruto) e `..._trusted` (consumo, criado pelo analytics). O sql2bq do atendimento-canais-prd foi desativado em 19/10/2026.

## Tabelas com CDC ativo (planilha, coluna activate_stream = Sim)

| Banco | Tabelas | Modo |
| --- | --- | --- |
| `bots_api` | `flags_empresas_v2`, `business_hours_overrides`, `groups_flags`, `business_hours` | Merge (ALL) |
| `canais_adk` | `public.events`, `public.sessions`, `ticket_session` | Merge (ALL) |
| `contato_service` | `bsp_contact` | Merge (ALL) |
| `email_service` | `email_replications`, `email_templates` | — |
| `ms_agrupamento_guias` | `controle_guias`, `controle_notificacao`, `historico_processamento_grupo_guia`, `grupo_guia`, `item_grupo_guia`, `diagnostico_aumento_imposto` | — |

Fora do CDC: `bots_api.encerramento`, `bots_api.flags_empresas`, `canais_adk` schema `public-1-1-0` (events, sessions, user_states) e `canais_adk.public.user_states`, `ms_agrupamento_guias.flyway_schema_history`.

## Histórico

- 06/08/2026: Gabriel pede CDC de `bots_api`, `canais_adk` e `contato_service`; datasets raw criados em 25/08.
- 26/08/2026: `email_service` e `ms_agrupamento_guias` (também no sql2bq) entram; abas preenchidas pelo Rafael. Ver [[agrupamento-guias-bigquery]].
- 17/09/2026: começa a migração da instância `contabilizei-experts` (projeto `contabilizei-experts-prd`), flag aplicada em 21/09; datasets legados `dw_experts_*` migrados pelo analytics (out–nov) e ingestões antigas desligadas em 06/11.

Acesso: o usuário comum não tem permissão de `bigquery.tables.list` nesses datasets raw.
