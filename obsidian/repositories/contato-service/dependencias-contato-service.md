---
name: dependencias-contato-service
description: "Dependências do contato-service: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - contato-service
repositorio: contato-service
---

# Dependências do contato-service

O que o `contato-service` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

## Consome

### Repositórios internos

- `meta-webhooks`: tópico `meta-webhooks.bcast.whatsapp.messages` (no projeto do `GCLOUD_PROJECT_META`), lido pela subscription `contato-service.sub.meta-webhooks-messages` — por `src/infra/gcp/pubsub-subs.ts` e o `metaWebhooksMessagesWorker` de `src/domain/bsp-contact/bsp-contact.module.ts` (só liga quando `GCLOUD_PROJECT_META` está definido)

### Libs internas

- `js-libraries`: `@contabilizei-private/zezu-core`, `event-workers`, `simple-cache` e `telemetry` (`package.json`); instalar exige o token do registry privado, ver [[contato-service/install-local|Install local]]

### Infra GCP

- Pub/Sub próprio: publica e consome `contato-service.topic.on-message-event-meta` (sub `contato-service.sub.on-message-event-meta`, com DLQ) — por `src/infra/gcp/pubsub-topics.ts` e o `onMessageEventMetaWorker`

### Bancos e dados

- Postgres pelo `DATABASE_URL` (Drizzle + `pg`) — por `src/infra/database/index.ts`
- Redis (`ioredis`) — por `src/infra/cache/`

### Terceiros

_Nada confirmado ainda._

## Consumido por

Quem consome os contratos deste repositório; a revisão de MRs confere se o diff quebra algum deles.

- `atendimento-canais-admin`: `POST /api/v1/optouts`, um por registro, pela tela de contato — por `src/routes/api/proxy/contato-service.$.tsx` (proxy `/api/proxy/contato-service`), ver [[optout-tela-contato]]
- `email-service`: consulta de opt-out de e-mail antes de enviar (`optout_purpose`, `cnpj`), pelo api-gateway, ver [[contrato-optout]]
- `experts-service`: a notificação individual de guias manda `optout_purpose: 'TAX'` e `cnpj` ao `email-service`, que consulta o opt-out aqui, ver [[notificacao-individual-guias-x-agrupamento]]; tem também o client HTTP direto `src/infra/http-clients/contato-service/` (token `TOKEN_CONTATO_SERVICE`), com as rotas usadas a conferir
- `bots-api`: `GET /api/v1/bsp-contacts` (resolver o contato pelo telefone, no fluxo da Ultimate) — por `src/clients/contato-service/contato-service.ts`
- `zendeskapp-whatsapp-ativo`: `GET`/`POST /api/v1/contacts` e `PATCH /api/v1/contacts/:id`, pelo api-gateway (`…/whatsapp-ativo/contato-service/api/v1`) — por `src/javascripts/services/contato-service/contato-service.client.ts`

<!-- deps:auto:inicio (gerado por mapear-dependencias; não editar à mão) -->

## Levantamento automático

Gerado em 2026-11-19 sobre `master` @ `b63ac08` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `meta-webhooks` (25×): `src/domain/bsp-contact/bsp-contact.module.ts:36`, `src/domain/bsp-contact/consumers/on-message-event-meta.worker.ts:27`, `src/infra/gcp/pubsub-subs.ts:5`
- `plataforma-monolito` (2×): `docs/arquitetura.excalidraw:1999`
- `email-service` (1×): `biome.json:22`

### Repositórios que citam este

- `atendimento-canais-admin` (103×): `src/routeTree.gen.ts:125`, `src/routes/api/proxy/contato-service.$.tsx:2`, `src/routes/contatos/$id.tsx:30`
- `atendimento-zendesk` (48×): `environments/_deprecated/config-dev.json:357`, `environments/_deprecated/config-local.json:355`, `environments/_deprecated/config-prod.json:357`
- `email-service` (26×): `.env.example:32`, `src/clients/contato-service/contato-service.client.ts:9`, `src/clients/contato-service/dto/optout.dto.ts:8`
- `zendeskapp-whatsapp-ativo` (25×): `src/javascripts/modules/WhatsappIndividual/ContatoSearch.tsx:5`, `src/javascripts/modules/WhatsappIndividual/CriarContato.tsx:5`, `src/javascripts/modules/WhatsappIndividual/contact-helpers.ts:7`
- `bots-api` (18×): `src/clients/contato-service/contato-service.ts:23`, `src/clients/index.ts:5`, `src/domain/ultimateai/telefone/telefone.router.ts:66`
- `survey-service` (10×): `docs/PLAN.md:19`, `docs/adr/001-arquitetura-modular.md:27`, `docs/dados/dicionario.md:359`
- `meta-webhooks` (8×): `AGENTS.md:72`, `README.md:64`, `docs/adr/001-borda-sem-banco-fan-out-por-dominio.md:8`
- `microsservico-agrupamento-guias` (5×): `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/integrations/dto/EnviarEmailRequestDTO.kt:16`, `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/integrations/dto/EnvioEmailCallbackDTO.kt:9`, `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/integrations/dto/WhatsAppRequestDTO.kt:48`
- `experts-service` (4×): `src/infra/config/dev.ts:100`, `src/infra/config/prod.ts:102`, `src/infra/http-clients/index.ts:18`
- `agent-eval` (1×): `docs/08-deployment.md:174`
- `agrupamento-guias-service` (1×): `src/shared/notificacao/constants/notificacao.constants.ts:10`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `ide-bahcode`, `k8s-configmap`, `kong-config`, `pipeline`

### Libs internas

- `@contabilizei-private/event-workers` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/simple-cache` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/telemetry` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/zezu-core` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `contato-service.topic.on-message-event-meta`, `contato-service.topic.on-message-event-meta.dlq`
- **Subscription**: `contato-service.sub.on-message-event-meta`, `contato-service.sub.on-message-event-meta.dlq`

### Bancos e dados

- Postgres: `pg`
- Pub/Sub: `@google-cloud/pubsub`
- Redis: `ioredis`
- SQL (query builder/ORM): `drizzle-orm`

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
