---
name: dependencias-monitoria-ia
description: "Dependências do monitoria-ia: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - monitoria-ia
repositorio: monitoria-ia
---

# Dependências do monitoria-ia

O que o `monitoria-ia` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `0e548d9` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `atendimento-zendesk` (19×): `src/executor/services/prompt/external-data-resolver.ts:2`, `src/executor/services/prompt/tools/get-ticket-tags.tool.ts:1`, `src/internal/infra/clients/atendimento-zendesk/index.ts:3`
- `file-transcriber` (11×): `environments/.env.local:12`, `environments/.env.test:12`, `src/aggregator/usecases/aggregate/aggregate.stub.ts:7`
- `atendimento-canais-admin` (11×): `docs/bruno/web/avaliacao/get avaliacao by ticketid.bru:23`, `docs/validacao-ajuste-avaliacoes.md:15`
- `canais-adk` (3×): `src/internal/infra/knowledge-book/tools.ts:16`, `src/internal/infra/knowledge-book/types.ts:45`
- `experts-nfs` (1×): `docs/validacao-ajuste-avaliacoes.md:261`
- Configuração, CI e documentação citadas: `kong-config`, `vault-roleset`

### Repositórios que citam este

- `atendimento-canais-admin` (89×): `src/env.ts:57`, `src/routes/monitoria/-SeletorAtendimento.tsx:14`, `src/routes/monitoria/-TabelaCriterios.tsx:32`
- `atendimento-zendesk` (14×): `environments/_deprecated/config-dev.json:213`, `environments/_deprecated/config-local.json:213`, `environments/_deprecated/config-prod.json:213`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `k8s-configmap`, `pipeline`

### Libs internas

- `@contabilizei-private/fastify-instrumentation` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/fastify-logging` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/pino-logger` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/telemetry` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `atendimento-zendesk-full-conversation`, `file-transcriber.bcast.transcription`, `zendesk-webhooks-tickets`
- **Subscription**: `monitoria-ia-aggregator.sub.transcriptions`, `monitoria-ia-parser.sub.zendesk-full-conversation`, `zendesk-webhooks-tickets`
- **Fila Cloud Tasks**: `monitoria-ia-agregador`, `monitoria-ia-executor`
- **Cloud Run / function**: `contabilizei-crm-suporte-webhooks`, `file-transcriber`, `monitoria-ia-aggregator`, `monitoria-ia-executor`, `monitoria-ia-parser`, `monitoria-ia-web`

### Bancos e dados

- Cloud Tasks: `@google-cloud/tasks`
- Postgres: `pg`
- SQL (query builder/ORM): `drizzle-orm`

### Terceiros

- Google Gemini / Vertex AI: `@google/genai`
- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `README.md:11`
- Zendesk: `contabilizei.zendesk.com` em `docs/arquitetura.drawio:7`, `contabilizei1637606740.zendesk.com` em `docs/event-examples/full-conversation/off/email.json:5`

<!-- deps:auto:fim -->
