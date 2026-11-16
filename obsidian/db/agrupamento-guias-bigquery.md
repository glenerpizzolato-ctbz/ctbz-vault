---
name: agrupamento-guias-bigquery
description: "Dados do agrupamento de guias no BigQuery: desde 16/10/2026 vêm por CDC (Datastream) em contabilizei-data.cloudsql_atendimento_canais_prd_atendimento_canais_ms_agrupamento_guias_{raw,trusted}; o legado dw_ms_agrupamento_guias (sql2bq) foi desligado em 19/10/2026 e está congelado, o dashboard de Notificação do atendimento-canais-admin foi migrado para a trusted em 16/11/2026 (branch feat/agrupamento-guias-cdc), com cast de DATETIME"
metadata:
  type: reference
tags:
  - db
  - bigquery
  - microsservico-agrupamento-guias
  - cdc
  - datastream
---

# Agrupamento de guias no BigQuery

## Fonte atual: CDC (Datastream), desde 16/10/2026

A migração do sql2bq para o CDC das bases do `atendimento-canais-prd` está na GMUD `END-3020` ([Outline](https://outline.ctbz.com.br/doc/gmud-migracao-cdc-datastream-atendimento-canais-prd-3MC1lGD7WM)) e foi combinada no chat "CDC | Atendimento Canais" (Google Chat `AAQAPSVXqVM`, com o time de dados: Geovanni Corsino na engenharia, Raissa Rosa no analytics e Thiago Geovane no DevOps). A migração terminou em 16/10/2026.

- **Raw:** `contabilizei-data.cloudsql_atendimento_canais_prd_atendimento_canais_ms_agrupamento_guias_raw`, tabelas com prefixo `public_` (`public_controle_notificacao`, `public_grupo_guia`, `public_controle_guias`, `public_item_grupo_guia`, `public_historico_processamento_grupo_guia`, `public_diagnostico_aumento_imposto`). O Datastream grava em modo Append-Only com atraso de até 15 min: cada insert, update ou delete vira uma linha nova. As partições expiram em 180 dias.
- **Trusted:** `contabilizei-data.cloudsql_atendimento_canais_prd_atendimento_canais_ms_agrupamento_guias_trusted`, com os mesmos nomes do banco (`controle_notificacao`, `grupo_guia` etc.). É o espelho deduplicado e sem expiração, gerado pelo dbt numa DAG do Airflow (`dbt_cloudsql_atendimento_canais_prd_atendimento_canais_ms_agrupamento_guias_trusted`) que roda **todo dia às 03:00 UTC** (00:00 BRT). Ou seja, o dado de um dia só aparece na trusted depois da meia-noite.
- O mesmo padrão vale para `contato_service`, `email_service`, `bots_api` e `canais_adk` (`cloudsql_atendimento_canais_prd_atendimento_canais_<banco>_{raw,trusted}`).
- **Acesso:** o `contabilizei-data` exige liberação por card com SecOps (foi assim com o Lucas Knabben em 15/10). Em 16/11/2026, a conta do Glener ainda não tinha acesso (`Access Denied` em `raw` e `trusted`).

## Legado: `contabilizei-dataflow.dw_ms_agrupamento_guias` (congelado)

- Era carregado pelo [[_sql2bq-indice|sql2bq]] (CronJob `atendimento-canais-prd-ms-agrupamento-guias-sql2bq`, 08:00, namespace `data` do `contabilizei-private-cluster-prod-01`), que recarregava as tabelas inteiras.
- Foi desligado de propósito em 19/10/2026 (commit `3dcc62a` do sql2bq e CronJob apagado), como previsto na GMUD, depois que o time de dados viu consumo só do Lucas Knabben, que já tinha migrado. A última carga é de 19/10 08:12 (`controle_notificacao` até 18/10 12:00). O `dw_email_service` e o `dw_contato_service` seguiram o mesmo caminho.
- O dataset mais antigo `dw_cloudsql_impostos` está parado desde 09/06/2026.

## Admin migrado para a trusted (branch `feat/agrupamento-guias-cdc`, 16/11/2026)

O dashboard de Notificação do `atendimento-canais-admin` (`controle-notificacao.source.ts` e `shared/periodos-apuracao.ts`) passou a apontar para a trusted na branch `feat/agrupamento-guias-cdc`. O deploy só pode sair depois que a service account do admin tiver leitura no `contabilizei-data` (sem isso a tela quebra), e o dado é D-1 (00:00 BRT).

**Quem precisa de acesso:** o client do admin (`bigquery.server.ts`) usa ADC sem chave, e os jobs rodam no projeto `contabilizei-dataflow`, só a tabela é lida no `contabilizei-data`. Localmente, a conta é a do `gcloud auth application-default login` do dev (não há `GOOGLE_APPLICATION_CREDENTIALS` no `.env`). No Cloud Run, é a service account padrão do Compute: `852985851006-compute@developer.gserviceaccount.com` em prd (`atendimento-canais-prd`) e `410826691463-compute@developer.gserviceaccount.com` em dev (`atendimento-canais-dev`). As duas precisam de `roles/bigquery.dataViewer` no dataset trusted, e o dev também, para testar localmente.

## Tipos: legado x CDC (armadilha)

O schema da trusted não pôde ser conferido (Access Denied), mas os tipos no Postgres indicam o que o Datastream gera, diferente do que o sql2bq gravava:

- `timestamp without time zone` (`controle_notificacao.created_at/updated_at/data_envio_notificacao`, `controle_guias.*` datas, `diagnostico_aumento_imposto.created_at`) vira **DATETIME** no Datastream; no legado era TIMESTAMP. `FORMAT_TIMESTAMP` sobre DATETIME dá erro, então o admin usa `CAST(col AS TIMESTAMP)`, que lê o DATETIME como UTC (mesma leitura do sql2bq) e não mexe num TIMESTAMP.
- `timestamp with time zone` (`grupo_guia.created_at/updated_at`, `item_grupo_guia.*`) segue TIMESTAMP.
- `numeric` (`periodo_apuracao`, `valor_*`) vira NUMERIC (no legado era FLOAT); `CAST(... AS INT64)` funciona igual.
- `jsonb` (`grupo_guia.contato`, `diagnostico_aumento_imposto.contato/resultado/memoria_calculo_anexo_simples`) vira JSON (no legado era STRING); quem fizer `JSON_EXTRACT` de string precisa ajustar.

Assim que houver acesso, conferir com `bq show --schema contabilizei-data:cloudsql_atendimento_canais_prd_atendimento_canais_ms_agrupamento_guias_trusted.<tabela>` se o dbt manteve esses tipos.

## Como conferir

- Legado: `SELECT table_id, TIMESTAMP_MILLIS(last_modified_time) FROM \`contabilizei-dataflow.dw_ms_agrupamento_guias.__TABLES__\``.
- Dado real sem BigQuery: banco `prd_atendimento_canais_ms_agrupamento_guias` (proxy `sql_atendimento_prd`, 5443) ou a skill `relatorio-notificacoes-agrupamento` ([[relatorio-notificacoes-dia-15]]). Em 15/11/2026 foram 24.706 e-mails e 24.371 WhatsApps.
- A config antiga do sql2bq tinha a senha do usuário `ingestor` em texto no JSON, e ela continua no histórico do git.
