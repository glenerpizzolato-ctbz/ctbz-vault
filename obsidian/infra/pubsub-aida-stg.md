---
name: pubsub-aida-stg
description: "Tópicos e subscriptions do Pub/Sub em aida-stg (AIDA, dev/stg) com consumidor e repositórios que citam cada um"
metadata:
  type: reference
tags:
  - infra
  - pubsub
atualizado_em: 2026-10-09
---

# Pub/Sub: aida-stg

AIDA, dev/stg. Fotografia de 2026-10-09. Formato: tópico → subscriptions (tipo e consumidor) · repositórios que citam o nome do tópico/subscription em `~/repositories` (`config:` = repos de configuração que citam quase tudo). Ver [[_infra-indice]] para o significado de cada campo.

- **`aida-classifier-classification-event`** · repos: aida-classifier, zendesk-agents
    - `sentinela-atendimento-classification-event-sub.v1` (push → Cloud Run `sentinela-atendimento-stg` /zendesk-worker/ticket/classification/update)
- **`aida-memoria-pagamentos-teste`**
- **`aida-ticket-tema`** · repos: aida-back
- **`atendimento-zendesk-full-conversation`** (tópico de `contabilizei-crm-dev`) · repos: atendimento-zendesk, monitoria-ia
    - `monitoria-ia-parser.sub.zendesk-full-conversation` (push → Cloud Run `monitoria-ia-parser` /full-conversation) · repos: monitoria-ia
- **`central-disparos-zendesk-webhooks-comments-dlt.v1`**
    - `central-disparos-zendesk-webhooks-comments-dlt.v1-sub` (pull, consumidor provável `central-disparos-zendesk-webhooks-comments-dlt`)
- **`central-disparos-zendesk-webhooks-messages-dlt.v1`**
    - `central-disparos-zendesk-webhooks-messages-dlt.v1-sub` (pull, consumidor provável `central-disparos-zendesk-webhooks-messages-dlt`)
- **`central-disparos-zendesk-webhooks-tickets-dlt.v1`**
    - `central-disparos-zendesk-webhooks-tickets-dlt.v1-sub` (pull, consumidor provável `central-disparos-zendesk-webhooks-tickets-dlt`)
- **`contabilizei-agents.bcast.metrics`** · repos: canais-adk, contabilizei-agents, zendesk-agents
- **`contabilizei-agents.p2p.triagem_result`** · repos: contabilizei-agents
- **`emissor-callback`** (tópico de `contabilizei-experts-dev`) · repos: atendimento-zendesk, experts-nfs
    - `aida-back.sub.nfs.emissor-callback.aida` (push → Cloud Run `aida-back-dev` /auth/nf/v2/callback)
- **`eventarc-nam5-firestore-aida-jarvis-712`** (Eventarc)
    - `firestore-aida-jarvis-ia-pull` (pull)
- **`file-transcriber.bcast.transcription`** · repos: file-transcriber, monitoria-ia, zendesk-agents
    - `monitoria-ia-aggregator.sub.transcriptions` (push → Cloud Run `monitoria-ia-aggregator` /aggregate) · repos: monitoria-ia
- **`firestore-aida-jarvis-ia-dlq`**
- **`inbound-outbound-ai-aida-responses`**
    - `inbound-outbound-ai-aida-responses-sub` (push → Cloud Run `inbound-outbound-ai-stg` /outbound/zendesk/responses, DLQ `inbound-outbound-ai-dlq-aida-responses`)
- **`inbound-outbound-ai-comment-events`**
    - `contador-inteligente-off-comment-events-sub` (push → Cloud Run `contador-inteligente-off-stg` /contador-inteligente-off/api/v1/run, DLQ `inbound-outbound-ai-dlq-aida-consumer`)
- **`inbound-outbound-ai-csat-events`**
    - `contador-inteligente-off-csat-events-sub` (push → Cloud Run `contador-inteligente-off-dev` /contador-inteligente-off/api/v1/csat-event, DLQ `inbound-outbound-ai-dlq-csat-events`)
- **`inbound-outbound-ai-dlq-aida-consumer`**
- **`inbound-outbound-ai-dlq-aida-responses`**
- **`inbound-outbound-ai-dlq-csat-events`**
    - `inbound-outbound-ai-dlq-csat-events-inspecao` (pull)
- **`inbound-outbound-ai-dlq-ticket-updates`**
- **`inbound-outbound-ai-ticket-updates`**
    - `contador-inteligente-off-ticket-updates-sub` (push → Cloud Run `contador-inteligente-off-stg` /contador-inteligente-off/api/v1/ticket-update, DLQ `inbound-outbound-ai-dlq-ticket-updates`)
- **`sentinela-atendimento-ticket-transfer-skipped.v1`**
- **`sentinela-atendimento-ticket-transferred.v1`**
    - `sentinela-atendimento-ticket-transferred-sub.v2` (push → Cloud Run `aida-back-dev` /auth/sentinela/transferencia)
- **`super-ouvidoria-temas-classificados`**
    - `sentinela-atendimento-super-ouvidoria-classificado-sub.v1` (push → Cloud Run `sentinela-atendimento-stg` /zendesk-worker/ticket/super-ouvidoria/classificado)
- **`upload-file-event`**
- **`zendesk-webhooks-comments`** (tópico de `contabilizei-crm-dev`) · repos: contabilizei-crm-webhooks, kong-config, pipeline
    - `central-disparos-zendesk-webhooks-comments-sub.v1` (push → Cloud Run `central-disparos-stg` /v1/eventos/zendesk/comentario, DLQ `central-disparos-zendesk-webhooks-comments-dlt.v1`)
    - `zendesk-webhooks-novo-comentario` (push → Cloud Run `aida-back-dev` /auth/zendesk_worker/novo-comentario)
- **`zendesk-webhooks-messages`** (tópico de `contabilizei-crm-dev`) · repos: atendimento-api-gateway, atendimento-zendesk, bots-api, kong-config
    - `central-disparos-zendesk-webhooks-messages-sub.v1` (push → Cloud Run `central-disparos-stg` /v1/eventos/zendesk/mensagem, DLQ `central-disparos-zendesk-webhooks-messages-dlt.v1`)
    - `sentinela-zendesk-webhooks-messages-sub.v1` (push → Cloud Run `sentinela-atendimento-stg` /zendesk-worker/ticket/message/new)
    - `zendesk-webhooks-nova-mensagem` (push → Cloud Run `aida-back-dev` /auth/zendesk_worker/nova-mensagem)
- **`zendesk-webhooks-tickets`** (tópico de `contabilizei-crm-dev`) · repos: atendimento-api-gateway, bots-api, contabilizei-crm-webhooks, experts-drawio, experts-service, kong-config, monitoria-ia, pipeline, zendesk-agents
    - `central-disparos-zendesk-webhooks-tickets-sub.v1` (push → Cloud Run `central-disparos-stg` /v1/eventos/zendesk/ticket, DLQ `central-disparos-zendesk-webhooks-tickets-dlt.v1`)
    - `sentinela-zendesk-webhooks-tickets-sub.v1` (push → Cloud Run `sentinela-atendimento-stg` /zendesk-worker/ticket/update)
    - `zendesk-webhooks-tickets` (push → Cloud Run `aida-back-dev` /auth/zendesk_worker/atualizacao-ticket) · repos: atendimento-api-gateway, bots-api, contabilizei-crm-webhooks, experts-drawio, experts-service, kong-config, monitoria-ia, pipeline, zendesk-agents
