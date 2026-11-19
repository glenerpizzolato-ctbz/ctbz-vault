---
name: dependencias-zendesk-agents
description: "Dependências do zendesk-agents: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - zendesk-agents
repositorio: zendesk-agents
---

# Dependências do zendesk-agents

O que o `zendesk-agents` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `f4a9563` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `canais-adk` (59×): `.env.example:29`, `src/modules/agents/whatsapp/agent/agent-envelope.ts:51`, `src/modules/contabilizei-agents/index.ts:3`
- `experts-nfs` (31×): `src/consumers/copilot/acknowledge-nf.consumer.ts:6`, `src/infra/clients/experts-nfs.client.ts:5`, `src/infra/clients/experts-nfs/emitir.dto.ts:1`
- `contabilizei-agents` (13×): `src/infra/google-cloud/pubsub/topics.ts:12`, `src/modules/agents/orchestration/usecase/agent-runner/base-agent-runner.strategy.ts:10`, `src/modules/ai-agent/metrics.service.ts:26`
- `file-transcriber` (12×): `src/consumers/ai-agent/transcription-result.consumer.ts:7`, `src/consumers/file-transcriber/file-transcription.worker.ts:4`, `src/consumers/index.ts:4`
- `aida-back` (6×): `src/infra/config/dev.ts:110`, `src/infra/config/prod.ts:111`, `src/infra/google-cloud/firestore/aida/ai-flag.dao.ts:3`
- `experts-service` (5×): `src/infra/auth/keycloak.ts:19`, `src/infra/google-cloud/pubsub/topics.ts:11`, `src/modules/csat/csat-response.dto.ts:3`
- `bots-api` (5×): `src/infra/clients/bots-api.client.ts:12`, `src/infra/clients/index.ts:4`, `src/modules/agents/agent-warmup.service.ts:2`
- `mcp-notas-fiscais` (4×): `src/infra/clients/index.ts:3`, `src/infra/clients/mcp-notas-fiscais.client.ts:11`, `src/infra/clients/mcp-notas-fiscais.client.spec.ts:2`
- `atendimento-zendesk` (3×): `src/infra/google-cloud/pubsub/topics.ts:7`, `src/modules/messages/service/send-message-sunshine.service.spec.ts:34`
- `aida-classifier` (1×): `src/infra/google-cloud/pubsub/topics.ts:9`
- Configuração, CI e documentação citadas: `vault-roleset`

### Repositórios que citam este

- `atendimento-canais-admin` (159×): `src/lib/firebase/firebase.ts:31`, `src/lib/mastra/connection.ts:3`, `src/lib/utils.ts:87`
- `canais-adk` (113×): `.env.example:94`, `src/application/agents/concierge-experts/certificado-digital/fila-expressa.ts:155`, `src/application/agents/concierge-experts/certificado-digital/lembrete-webview.ts:11`
- `atendimento-zendesk` (44×): `.config.json:268`, `environments/_deprecated/config-dev.json:349`, `environments/_deprecated/config-local.json:347`
- `survey-service` (21×): `src/modules/csat/csat-response-state.worker.ts:33`, `terraform/dev/pubsub.tf:1`, `terraform/prd/pubsub.tf:1`
- `canais-certificado-digital` (18×): `src/certificado-digital/acompanhamento/acompanhamento.client.ts:40`, `src/certificado-digital/acompanhamento/status-alterado.client.ts:7`, `src/certificado-digital/emissao/aviso-webview/aviso-webview.client.ts:26`
- `zendeskapp-concierge` (17×): `src/javascripts/contexts/session-emissor.js:4`, `src/javascripts/modules/common/acoes/acao/detalhes/Detalhes.jsx:139`, `src/javascripts/modules/common/acoes/actionErrorMessage.js:4`
- `bots-api` (15×): `src/domain/ultimateai/notasfiscais/usecase/warmup.usecase.ts:67`, `src/domain/zendesk/encerramento/services/failover.service.ts:4`, `src/domain/zendesk/encerramento/usecase/ia-inference/ticket-reopening.helper.ts:6`
- `experts-nfs` (10×): `src/modules/v3/emissor/copilot-massivo/constants/copilot-massivo.ts:7`, `src/modules/v3/emissor/copilot-massivo/usecases/ack/copilot-massivo-ack.usecase.ts:35`, `docs/bruno/v3/emissor/copilot-massivo/callback-from-pubsub.bru:27`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `cnpj-alfanumerico`, `ide-bahcode`, `k8s-configmap`, `kong-config`, `pipeline`

### No grafo manual ([[grafo-chamadas-canais]])

- Consome: `canais-adk`, `aida-back`, `bots-api`, `experts-nfs`, `contabilizei-agents`
- Consumido por: `atendimento-canais-admin`, `atendimento-zendesk` (actions, chat do consultor)

### Libs internas

- `@contabilizei-private/event-workers` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/fastify-healthz` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/fastify-instrumentation` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/fastify-logging` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/pino-logger` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/telemetry` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/zezu-core` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/zezu-workers` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `aida-classifier-classification-event`, `atendimento-zendesk-atualizar-ticket`, `atendimento-zendesk-enviar-mensagem-sunshine`, `contabilizei-agents.bcast.metrics`, `experts-nfs.bcast.nfs.result`, `experts-service.bcast.csat-response`, `file-transcriber.bcast.transcription`, `test-topic`, `zendesk-agents.bcast.etl.agent-latency-results`, `zendesk-atualizar-ticket`, `zendesk-webhooks-conversations`, `zendesk-webhooks-tickets`
- **Subscription**: `subscription-name`, `zendesk-agents.sub.bq.agent-latency-results`, `zendesk-agents.sub.conversations`, `zendesk-agents.sub.etl.agent-latency`, `zendesk-agents.sub.file-transcriber-result`, `zendesk-agents.sub.tickets`, `zendesk-agents.sub.v1.agents-control.on-csat-response`, `zendesk-agents.sub.v1.agents-control.on-metrics`, `zendesk-agents.sub.v1.agents-control.on-ticket-update`, `zendesk-agents.sub.v1.concierge-acknowledge-nf`, `zendesk-agents.sub.v1.copilot-actions`, `zendesk-agents.sub.v1.copilot-actions.dictionary-on-message`, `zendesk-agents.sub.v1.copilot-actions.on-ticket-update`, `zendesk-agents.sub.v1.customer-summary.on-ticket-update`, `zendesk-webhooks-tickets`
- **Cloud Run / function**: `bots-api`, `contabilizei-agents`, `experts-nfs`, `file-transcriber`

### Bancos e dados

- Firestore: `@google-cloud/firestore`
- Postgres: `pg`
- Pub/Sub: `@google-cloud/pubsub`
- Redis: `ioredis`
- SQL (query builder/ORM): `drizzle-orm`
- Tabelas/datasets do BigQuery citados: `contabilizei-data.contabilizei_agents_raw.agent_latency`

### Terceiros

- Google Chat: `chat.googleapis.com` em `src/modules/gchat-alerts/gchat-alerts.service.spec.ts:4`
- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/infra/config/prod.ts:19`, `ctbz-experimentos.atlassian.net` em `src/infra/config/dev.ts:17`
- Zendesk: `contabilizei.zendesk.com` em `src/modules/gchat-alerts/gchat-alerts.service.spec.ts:61`

<!-- deps:auto:fim -->
