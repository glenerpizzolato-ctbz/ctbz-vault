---
name: dependencias-email-service
description: "Dependências do email-service: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - email-service
repositorio: email-service
---

# Dependências do email-service

O que o `email-service` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

## Consome

### Repositórios internos

- `contato-service`: consulta de opt-out de e-mail antes de enviar (`optout_purpose`, `cnpj`), pelo api-gateway, ver [[contrato-optout]]

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

- atendimento-canais-admin lê `email_replications` e `email_templates` pela cópia CDC no BigQuery (trusted), não pela API: dashboard de e-mail, `src/server/domains/email-dashboard/email-dashboard.source.ts`. Mudança de coluna nessas tabelas quebra o dashboard (ver [[dados-no-bigquery]])
- experts-functions (`function-email-holerites`) publica em `email-service.p2p.file-upload` e `email-service.p2p.send-email` (`application: function-email-holerites`, `optout_purpose: TRANSACTIONAL`), `functions/email-holerites/src/services/email-service.publisher.ts` (PRD-178571, MR experts-functions!10, em draft em 24/11/2026)

<!-- deps:auto:inicio (gerado por mapear-dependencias; não editar à mão) -->

## Levantamento automático

Gerado em 2026-11-19 sobre `master` @ `3642d61` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contato-service` (26×): `.env.example:32`, `src/clients/contato-service/contato-service.client.ts:9`, `src/clients/contato-service/dto/optout.dto.ts:8`
- `experts-service` (9×): `src/domain/sender/consumers/validation.worker.spec.ts:393`, `src/domain/sender/dispatch-priority.integration.spec.ts:113`, `AGENTS.md:184`
- `microsservico-agrupamento-guias` (3×): `src/domain/sender/dispatch-priority.integration.spec.ts:114`, `src/domain/sender/helpers/send-alert-card.helper.spec.ts:87`
- `bots-api` (1×): `AGENTS.md:328`
- Configuração, CI e documentação citadas: `vault-roleset`

### Repositórios que citam este

- `atendimento-canais-admin` (198×): `src/routes/api/notificacoes/email-arquivos.tsx:12`, `src/routes/api/notificacoes/email-envios.list.tsx:10`, `src/routes/api/notificacoes/email-envios.tsx:17`
- `agrupamento-guias-service` (43×): `src/clients/email-service/dto/send-email.dto.ts:1`, `src/clients/email-service/email-service.publisher.ts:7`, `src/clients/index.ts:3`
- `survey-service` (39×): `.dockerignore:1`, `src/clients/atendimento-zendesk/atendimento-zendesk.client.ts:40`, `src/modules/channels/email/email-callback.consumer.ts:6`
- `microsservico-agrupamento-guias` (18×): `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/integrations/dto/EnviarEmailRequestDTO.kt:14`, `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/integrations/impl/EnvioEmailAgrupamentoServiceImpl.kt:32`, `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/services/EmailTemplateService.kt:7`
- `experts-service` (3×): `src/domain/guia-imposto/services/schedule-notification-email-task/schedule-notification-email-task.service.ts:42`, `src/domain/guia-imposto/services/schedule-notification-email-task/schedule-notification-email-task.service.spec.ts:62`
- `agent-eval` (1×): `docs/08-deployment.md:174`
- `contato-service` (1×): `biome.json:22`
- `meta-webhooks` (1×): `.dockerignore:1`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `ide-bahcode`, `k8s-configmap`, `kong-config`, `pipeline`

### Libs internas

- `@contabilizei-private/event-workers` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/pino-logger` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/simple-cache` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/telemetry` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/zezu-core` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `email-service.p2p.file-upload`, `email-service.p2p.file-upload.dlq`, `email-service.p2p.send-email`, `email-service.p2p.send-email-callback`, `email-service.p2p.send-email-callback.dlq`, `email-service.p2p.send-email-validated`, `email-service.p2p.send-email-validated.dlq`, `email-service.p2p.send-email.dlq`, `test-topic`
- **Subscription**: `email-service.p2p.file-upload.dlq.inspect.sub`, `email-service.p2p.file-upload.sub`, `email-service.p2p.send-email-callback.dlq.inspect.sub`, `email-service.p2p.send-email-callback.invalid-payload.sub`, `email-service.p2p.send-email-callback.replication-not-found.sub`, `email-service.p2p.send-email-callback.smtp-unavailable.sub`, `email-service.p2p.send-email-callback.update-db.sub`, `email-service.p2p.send-email-callback.validation-error.sub`, `email-service.p2p.send-email-validated.dlq.inspect.sub`, `email-service.p2p.send-email-validated.enqueue-dispatch.sub`, `email-service.p2p.send-email-validated.replicate-record.sub`, `email-service.p2p.send-email.dlq.inspect.sub`, `email-service.p2p.send-email.sub`
- **Cloud Run / function**: `bots-api`

### Bancos e dados

- Cloud Storage: `@google-cloud/storage`
- Postgres: `pg`
- Pub/Sub: `@google-cloud/pubsub`
- Redis: `ioredis`
- SQL (query builder/ORM): `drizzle-orm`

### Terceiros

- Google Chat: `chat.googleapis.com` em `.env.example:30`

<!-- deps:auto:fim -->
