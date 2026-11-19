---
name: dependencias-experts-service
description: "Dependências do experts-service: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - experts-service
repositorio: experts-service
---

# Dependências do experts-service

O que o `experts-service` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

## Consome

### Repositórios internos

- `contato-service`: client HTTP `src/infra/http-clients/contato-service/` (token `TOKEN_CONTATO_SERVICE`), rotas a conferir; o opt-out da notificação individual de guias passa pelo `email-service`, ver [[notificacao-individual-guias-x-agrupamento]]

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

Gerado em 2026-11-19 sobre `fix/PRD-165484` @ `da4e671` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `atendimento-zendesk` (65×): `migrations/0055_backfill_csat_validade_e_status.sql:4`, `src/consumers/desconexao/update-error.consumer.ts:20`, `src/consumers/survey-csat/ativo-status/ativo-status.consumer.ts:18`
- `ticketing-service` (14×): `src/domain/index.ts:16`, `src/domain/ticket-transbordo/strategies/process-experts-transbordo.strategy.ts:2`, `src/domain/ticket-transbordo/usecase/fetch-transbordo.usecase.ts:2`
- `microsservico-agrupamento-guias` (7×): `src/domain/guia-imposto/services/index.ts:10`, `src/domain/guia-imposto/services/schedule-notification-wpp-task/schedule-notification-wpp-task.service.ts:20`, `src/domain/guia-imposto/services/should-schedule/should-schedule.service.ts:6`
- `bots-api` (5×): `src/domain/survey-csat/constants/templates_config.ts:73`, `src/domain/survey-csat/usecase/send-expiracao.usecase.ts:36`, `src/infra/http-clients/atendimento-zendesk/atendimento-zendesk.client.ts:129`
- `contato-service` (4×): `src/infra/config/dev.ts:100`, `src/infra/config/prod.ts:102`, `src/infra/http-clients/index.ts:18`
- `email-service` (3×): `src/domain/guia-imposto/services/schedule-notification-email-task/schedule-notification-email-task.service.ts:42`, `src/domain/guia-imposto/services/schedule-notification-email-task/schedule-notification-email-task.service.spec.ts:62`
- `experts-alertas` (2×): `src/infra/config/dev.ts:88`, `src/infra/config/prod.ts:90`
- `experts-nfs` (2×): `src/infra/config/dev.ts:91`, `src/infra/config/prod.ts:93`
- `plataforma-back-worker` (1×): `src/domain/event/events/internal/empresa/updated-assessor-empresa.test.ts:28`
- `emissor-whatsapp` (1×): `src/domain/nfs/services/nfs-sheet.service.ts:67`
- `survey-service` (1×): `src/domain/utils/env.ts:13`

### Repositórios que citam este

- `survey-service` (95×): `.env.example:15`, `AGENTS.md:3`, `README.md:3`
- `atendimento-zendesk` (45×): `.config.json:244`, `environments/_deprecated/config-dev.json:315`, `environments/_deprecated/config-local.json:315`
- `canais-adk` (28×): `.env.example:45`, `src/application/hooks/customer-summary/before-agent.ts:7`, `src/application/tools/experts-feedback/register-feedback.tool.ts:7`
- `bots-api` (16×): `.env.example:3`, `src/clients/index.ts:7`, `src/domain/ultimateai/csat/csat-fup/csat-fup.service.ts:33`
- `experts-nfs` (10×): `src/modules/common/contabilizei/ctbz-http.client.ts:141`, `src/modules/common/contabilizei/index.ts:5`, `src/modules/internal/emissor-jira/services/usecase/create-nfs-jira.usecase.ts:14`
- `email-service` (9×): `src/domain/sender/consumers/validation.worker.spec.ts:393`, `src/domain/sender/dispatch-priority.integration.spec.ts:113`, `AGENTS.md:184`
- `mcp-notas-fiscais` (6×): `app/clients/experts_service_client.py:24`, `app/clients/__tests__/test_experts_service_client.py:45`
- `zendesk-agents` (5×): `src/infra/auth/keycloak.ts:19`, `src/infra/google-cloud/pubsub/topics.ts:11`, `src/modules/csat/csat-response.dto.ts:3`
- `agrupamento-guias-service` (4×): `src/domain/notifica/helpers/metadados-guia.helper.ts:58`, `AGENTS.md:197`, `README.md:54`
- `microsservico-agrupamento-guias` (2×): `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/integrations/MetadadosGuiaFactory.kt:16`
- `ticketing-service` (2×): `environments/.env.dev:10`, `environments/.env.prd:10`
- `contabilizei-agents` (1×): `app/utils/env.py:74`
- `js-libraries` (1×): `packages/google-pubsub/src/experts/v1/topics/feedback-hub/feedback-hub.topics.ts:8`
- `ms-relatorio-faturamento` (1×): `README.md:3`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `cnpj-alfanumerico`, `experts-bruno`, `ide-bahcode`, `k8s-configmap`, `kong-config`, `pipeline`

### No grafo manual ([[grafo-chamadas-canais]])

- Consome: `atendimento-zendesk` (Pub/Sub), `ticketing-service`
- Consumido por: `canais-adk`, `bots-api`, `experts-nfs`, `mcp-notas-fiscais`

### Libs internas

- `@contabilizei-private/event-workers` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/fastify-healthz` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/fastify-instrumentation` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/fastify-logging` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/google-pubsub` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/jira-api` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/pino-logger` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/telemetry` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `atendimento-zendesk-atualizar-ticket`, `atendimento-zendesk-ticket-criado-atualizado-banco-de-dados`, `atendimento-zendesk.envio-whatsapp-ativo`, `atendimento-zendesk.erros.atualizar-ticket`, `email-service.p2p.send-email`, `experts-service.bcast.csat-response`, `experts-service.dead-letters`, `experts-service.p2p.csat-fup-sla-16h`, `experts-service.p2p.feedback-hub.create-jira-issue`, `experts.assessor`, `experts.empresa`, `p2p.update-assessor-empresa`, `plataforma.bcast.empresa-alteracao-plano`, `processar-guia-imposto`, `test-topic`, `ticketing.bcast.ticket-jira`, `ticketing.bcast.v2.ticket-jira`, `zendesk-trigger.p2p.csat-survey`, `zendesk-webhooks-conversations`, `zendesk-webhooks-tickets`
- **Subscription**: `experts-service.p2p.update-assessor-empresa.sub`, `experts-service.sub.csat-fup-sla-16h`, `experts-service.sub.csat-fup.ticket-off-closed`, `experts-service.sub.csat-fup.ticket-off-merged`, `experts-service.sub.desconexao.create`, `experts-service.sub.desconexao.evalutate-message-ia`, `experts-service.sub.desconexao.ticket-update-error`, `experts-service.sub.feedback-hub.create-jira-issue`, `experts-service.sub.guia-imposto`, `experts-service.sub.guia-imposto-local`, `experts-service.sub.plataforma-alteracao-plano`, `experts-service.sub.run-survey-engine`, `experts-service.sub.send-csat-fup-atendimento`, `experts-service.sub.ticket-transbordo.ticket-jira-v1`, `experts-service.sub.ticket-transbordo.ticket-jira-v2`, `experts.empresa__experts-service__events-consumer-sub`, `plataforma.update-assessor-empresa-sub`, `zendesk-webhooks-tickets`
- **Scheduler**: `executar_task_scheduler`
- **Fila Cloud Tasks**: `emissor-whatsapp-massivo`, `feedback-hub`
- **Cloud Run / function**: `bots-api`, `emissor-whatsapp-massivo`

### Bancos e dados

- Cloud Tasks: `@google-cloud/tasks`
- Firestore: `@google-cloud/firestore`
- Postgres: `pg`
- Pub/Sub: `@google-cloud/pubsub`
- Redis: `ioredis`
- SQL (query builder/ORM): `drizzle-orm`

### Terceiros

- Google Gemini / Vertex AI: `@google-cloud/vertexai`, `@google/genai`
- Jira / Confluence: `ctbz-experimentos.atlassian.net` em `src/domain/feedback-hub/services/feedback-hub.service.ts:90`, `ctbz-experts.atlassian.net` em `src/domain/feedback-hub/services/feedback-hub.service.ts:89`
- Zendesk: `contabilizei.zendesk.com` em `src/domain/errors/errors.md:8`, `contabilizei1637606740.zendesk.com` em `src/domain/desconexao/__assets__/ticket.message.json:5`

<!-- deps:auto:fim -->
