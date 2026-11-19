---
name: dependencias-bots-api
description: "Dependências do bots-api: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - bots-api
repositorio: bots-api
---

# Dependências do bots-api

O que o `bots-api` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

## Consome

### Repositórios internos

- `contato-service`: `GET /api/v1/bsp-contacts` (resolver o contato pelo telefone) — por `src/clients/contato-service/contato-service.ts`

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

Gerado em 2026-11-19 sobre `fix/PRD-174639` @ `3398386` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `atendimento-zendesk` (46×): `src/clients/atendimento-zendesk/atendimento-zendesk.ts:150`, `src/clients/atendimento-zendesk/dto/ativos-workflow.dto.ts:2`, `src/clients/atendimento-zendesk/dto/mensagem-ativa.dto.ts:2`
- `contato-service` (18×): `src/clients/contato-service/contato-service.ts:23`, `src/clients/index.ts:5`, `src/domain/ultimateai/telefone/telefone.router.ts:66`
- `experts-service` (16×): `.env.example:3`, `src/clients/index.ts:7`, `src/domain/ultimateai/csat/csat-fup/csat-fup.service.ts:33`
- `zendesk-agents` (15×): `src/domain/ultimateai/notasfiscais/usecase/warmup.usecase.ts:67`, `src/domain/zendesk/encerramento/services/failover.service.ts:4`, `src/domain/zendesk/encerramento/usecase/ia-inference/ticket-reopening.helper.ts:6`
- `experts-nfs` (10×): `src/clients/index.ts:6`, `src/domain/ultimateai/notasfiscais/elegibilidade.service.ts:2`, `src/domain/ultimateai/notasfiscais/nfs-flows.service.ts:4`
- `experts-admin` (3×): `src/domain/ultimateai/warning-messages/warning-messages.bff.ts:11`, `src/domain/ultimateai/warning-messages/warning-messages.module.ts:21`, `src/domain/ultimateai/warning-messages/warning-messages.bff.spec.ts:42`
- `aida-back` (1×): `src/domain/zendesk/ativo-workflow/usecases/handle-answer.usecase.ts:108`

### Repositórios que citam este

- `canais-adk` (81×): `.env.example:35`, `src/application/agents/concierge-experts/certificado-digital/horario-fila-expressa.ts:2`, `src/application/agents/concierge-experts/index.ts:51`
- `atendimento-canais-admin` (62×): `src/routes/api/bots/flags.$cnpj.$flag.tsx:2`, `src/routes/api/bots/flags.$cnpj.tsx:3`, `src/routes/api/bots/flags.bulk.$flag.tsx:2`
- `survey-service` (49×): `.env.example:20`, `src/clients/bots-api/bots-api.client.ts:37`, `src/clients/index.ts:4`
- `atendimento-zendesk` (40×): `.config.json:272`, `environments/_deprecated/config-dev.json:353`, `environments/_deprecated/config-local.json:351`
- `experts-nfs` (17×): `src/modules/common/contabilizei/bots-api/bots-api.facade.ts:12`, `src/modules/common/contabilizei/bots-api/dto/empresa.ts:11`, `src/modules/common/contabilizei/ctbz-http.client.ts:47`
- `ultimate-ai-bpmn` (15×): `"bots/[prod] ctbz wpp main/use_cases/custom/bank/Wpp Bank | Autentica\303\247\303\243o Bank [A] [B] [E]/reply.bpmn":399`, `bots/[prod] ctbz wpp main/use_cases/custom/bank/Wpp Bank | Hours Router [A] [B] [E]/reply.bpmn:147`, `bots/[prod] ctbz wpp main/use_cases/custom/corretora/Wpp Corretora | Hours Router [A] [B] [E]/reply.bpmn:146`
- `zendesk-proxy` (12×): `src/domain/identity/__fixture__/consumer.fixture.ts:6`, `src/domain/identity/consumer.dao.spec.ts:31`, `src/domain/identity/consumers.router.spec.ts:30`
- `js-libraries` (7×): `packages/telemetry/src/lib/env-defaults.spec.ts:85`, `packages/zezu-core/README.md:9`
- `experts-service` (5×): `src/domain/survey-csat/constants/templates_config.ts:73`, `src/domain/survey-csat/usecase/send-expiracao.usecase.ts:36`, `src/infra/http-clients/atendimento-zendesk/atendimento-zendesk.client.ts:129`
- `zendesk-agents` (5×): `src/infra/clients/bots-api.client.ts:12`, `src/infra/clients/index.ts:4`, `src/modules/agents/agent-warmup.service.ts:2`
- `contabilizei-agents` (3×): `app/utils/env.py:63`, `app/clients/__tests__/test_bots_api_client.py:53`
- `experts-admin` (3×): `src/modules/AvisosChatbot/interface/index.ts:4`, `src/webApi/index.js:10`, `src/modules/AvisosChatbot/tests/services/warningMessagesService.spec.ts:96`
- `email-service` (1×): `AGENTS.md:328`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `cnpj-alfanumerico`, `ide-bahcode`, `k8s-configmap`, `kong-config`, `pipeline`

### No grafo manual ([[grafo-chamadas-canais]])

- Consome: `experts-service`, `experts-nfs`, `atendimento-zendesk`
- Consumido por: `atendimento-canais-admin`, `zendesk-agents`, `canais-adk`, `experts-nfs`, `aida-back`

### Libs internas

- `@contabilizei-private/event-workers` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/pino-logger` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/simple-cache` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/telemetry` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/zezu-core` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `atendimento-zendesk-atualizar-ticket`, `atendimento-zendesk-criar-ticket`, `atendimento-zendesk-enviar-mensagem-sunshine`, `atendimento-zendesk-whatsapp-experts-carregar-integracoes`, `atendimento-zendesk.erros.atualizar-ticket`, `bots-api.p2p.nota-fiscal.warmup`, `topic-name`, `zendesk-webhooks-conversations`, `zendesk-webhooks-messages`, `zendesk-webhooks-tickets`
- **Subscription**: `bots-api.encerramento.initialize`, `bots-api.encerramento.on-message`, `bots-api.encerramento.on-ticket-closed`, `bots-api.encerramento.on-ticket-open`, `bots-api.encerramento.on-update-ticket-error`, `bots-api.re-route.ticket`, `bots-api.sub.nota-fiscal.warmup`, `bots-api.sub.ultimate-ai.warmup`, `subscription-name`, `zendesk-webhooks-tickets`
- **Cloud Run / function**: `bots-api`, `experts-nfs`

### Bancos e dados

- Datastore: `@google-cloud/datastore`
- Firestore: `@google-cloud/firestore`
- Postgres: `pg`
- Pub/Sub: `@google-cloud/pubsub`
- Redis: `ioredis`
- SQL (query builder/ORM): `drizzle-orm`

### Terceiros

- Google Chat: `chat.googleapis.com` em `src/clients/google-chat/google-chat.spec.ts:18`
- Google Gemini / Vertex AI: `@google/genai`
- Zendesk: `contabilizei.zendesk.com` em `src/domain/zendesk/agent-workspace-preso/constants.ts:29`

<!-- deps:auto:fim -->
