---
name: dependencias-js-libraries
description: "Dependências do js-libraries: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - js-libraries
repositorio: js-libraries
---

# Dependências do js-libraries

O que o `js-libraries` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

- `contato-service`: `@contabilizei-private/zezu-core`, `event-workers`, `simple-cache` e `telemetry` (`package.json`)

<!-- deps:auto:inicio (gerado por mapear-dependencias; não editar à mão) -->

## Levantamento automático

Gerado em 2026-11-19 sobre `master` @ `9ffe312` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `bots-api` (7×): `packages/telemetry/src/lib/env-defaults.spec.ts:85`, `packages/zezu-core/README.md:9`
- `atendimento-zendesk` (2×): `packages/google-pubsub/src/crm/topics/atendimento-zendesk/envio-whatsapp-ativo.ts:61`, `packages/google-pubsub/src/crm/topics/index.ts:3`
- `experts-service` (1×): `packages/google-pubsub/src/experts/v1/topics/feedback-hub/feedback-hub.topics.ts:8`

### Repositórios que citam este

_O nome `js-libraries` é comum demais para busca por token; procurar pelo host, rota ou tópico._

### Libs internas

- `@contabilizei-private/event-workers` (`packages/zezu-workers/package.json`)
- `@contabilizei-private/fastify-instrumentation` (`packages/zezu-core/package.json`)
- `@contabilizei-private/fastify-logging` (`packages/zezu-core/package.json`)
- `@contabilizei-private/pino-logger` (`packages/event-workers/package.json`)
- `@contabilizei-private/telemetry` (`packages/google-pubsub/package.json`)
- `@contabilizei-private/zezu-core` (`packages/zezu-workers/package.json`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `atendimento-zendesk.envio-whatsapp-ativo`, `experts-service.p2p.feedback-hub.create-jira-issue`, `test-topic`
- **Fila Cloud Tasks**: `feedback-hub`
- **Cloud Run / function**: `bots-api`

### Bancos e dados

- Pub/Sub: `@google-cloud/pubsub`
- Redis: `ioredis`
- Secret Manager: `@google-cloud/secret-manager`

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `packages/jira-api/src/v3/client.spec.ts:22`

<!-- deps:auto:fim -->
