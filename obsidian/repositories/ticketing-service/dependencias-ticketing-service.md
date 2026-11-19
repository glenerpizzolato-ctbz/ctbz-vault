---
name: dependencias-ticketing-service
description: "Dependências do ticketing-service: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - ticketing-service
repositorio: ticketing-service
---

# Dependências do ticketing-service

O que o `ticketing-service` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

## Consome

### Repositórios internos

_Nada confirmado ainda._

### Libs internas

_Nada confirmado ainda._

### Infra GCP

_Nada confirmado ainda._

### Bancos e dados

_Nada confirmado ainda._

### Terceiros

_Nada confirmado ainda._

## Consumido por

Quem consome os contratos deste repositório; a revisão de MRs confere se o diff quebra algum deles.

_Nada confirmado ainda._

<!-- deps:auto:inicio (gerado por mapear-dependencias; não editar à mão) -->

## Levantamento automático

Gerado em 2026-11-19 sobre `master` @ `7cc6bcd` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `experts-service` (2×): `environments/.env.dev:10`, `environments/.env.prd:10`
- `atendimento-canais-admin` (1×): `src/routes/sla-bff.router.ts:46`

### Repositórios que citam este

- `atendimento-canais-admin` (43×): `src/components/navigation/nav-config.ts:465`, `src/env.ts:50`, `src/lib/auth/access-config.ts:101`
- `experts-service` (14×): `src/domain/index.ts:16`, `src/domain/ticket-transbordo/strategies/process-experts-transbordo.strategy.ts:2`, `src/domain/ticket-transbordo/usecase/fetch-transbordo.usecase.ts:2`
- `atendimento-zendesk` (12×): `.config.json:236`, `environments/_deprecated/config-dev.json:307`, `environments/_deprecated/config-local.json:307`
- `survey-service` (9×): `.env.example:6`, `vitest.config.ts:16`, `src/clients/ticketing/ticketing.client.spec.ts:58`
- `experts-nfs` (8×): `src/modules/common/contabilizei/ctbz-http.client.ts:130`, `src/modules/internal/emissor/services/notafiscalv2.service.ts:4`, `src/modules/common/contabilizei/ctbz-http.client.test.ts:112`
- `sql2bq` (1×): `cronjobs/params-prd.yaml:215`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `cnpj-alfanumerico`, `k8s-configmap`, `kong-config`, `pipeline`

### No grafo manual ([[grafo-chamadas-canais]])

- Consumido por: `experts-nfs`, `experts-service`

### Libs internas

- `@contabilizei-private/event-workers` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/fastify-healthz` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/fastify-instrumentation` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/fastify-logging` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/jira-api` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/pino-logger` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/telemetry` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `ticketing.bcast.dados-gerais-jira-result`, `ticketing.bcast.ticket-jira`, `ticketing.bcast.v2.ticket-jira`, `ticketing.dead-letters`, `ticketing.p2p.add-dados-empresa`, `ticketing.p2p.add-dados-gerais-ticket-jira`, `ticketing.p2p.v1.sla`, `ticketing.p2p.v2.dados-empresa`
- **Subscription**: `ticketing.sub.add-dados-empresa`, `ticketing.sub.add-dados-gerais-ticket-jira`, `ticketing.sub.bq.dados-gerais-jira-result`, `ticketing.sub.upsert-ticket-jira`, `ticketing.sub.v1.sla`, `ticketing.sub.v2.dados-empresa`, `ticketing.sub.v2.upsert-ticket-jira`

### Bancos e dados

- Datastore: `@google-cloud/datastore`
- Postgres: `pg`
- Pub/Sub: `@google-cloud/pubsub`
- Redis: `redis`
- SQL (query builder/ORM): `drizzle-orm`
- Tabelas/datasets do BigQuery citados: `contabilizei-dataflow.dw_ticketing_service.dados_gerais_jira_result`

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/routes/tickets.router.ts:14`, `ctbz-experts.atlassian.net` em `docs/bruno/v2/empresa-dados/Dados Empresa Ticket.bru:17`

<!-- deps:auto:fim -->
