---
name: pubsub-atendimento-canais-dev
description: "Tópicos e subscriptions do Pub/Sub em atendimento-canais-dev (Atendimento / canais, dev) com consumidor e repositórios que citam cada um"
metadata:
  type: reference
tags:
  - infra
  - pubsub
atualizado_em: 2026-10-09
---

# Pub/Sub: atendimento-canais-dev

Atendimento / canais, dev. Fotografia de 2026-10-09. Formato: tópico → subscriptions (tipo e consumidor) · repositórios que citam o nome do tópico/subscription em `~/repositories` (`config:` = repos de configuração que citam quase tudo). Ver [[_infra-indice]] para o significado de cada campo.

- **`agrupar-guias-empresa`** (tópico de `contabilizei-impostos-teste`) · repos: microsservico-agrupamento-guias, plataforma-faturamento-worker
    - `ms-agrupamento-guias.sub.agrupar-guias` (pull, consumidor provável `ms-agrupamento-guias`) · repos: microsservico-agrupamento-guias
- **`atendimento-zendesk-whatsapp-experts-carregar-integracoes`** (tópico de `contabilizei-crm-dev`) · repos: atendimento-zendesk, bots-api
    - `bots-api.sub.ultimate-ai.warmup` (push → `api-dev.contabilizei.com.br/bots-api/ultimate-ai/v1/warmup`) · repos: bots-api
- **`atendimento-zendesk.erros.atualizar-ticket`** (tópico de `contabilizei-crm-dev`) · repos: atendimento-zendesk, bots-api, experts-service
    - `bots-api.encerramento.on-update-ticket-error` (pull, consumidor provável `bots-api`) · repos: bots-api
- **`atendimento-zendesk.p2p.att-ticket-status`** · repos: atendimento-zendesk
- **`atendimento-zendesk.whatsapp-ativo-status`** (tópico de `contabilizei-crm-dev`) · repos: atendimento-zendesk, microsservico-agrupamento-guias
    - `ms-agrupamento-guias.sub.send-wpp-callback` (pull, consumidor provável `ms-agrupamento-guias`) · repos: microsservico-agrupamento-guias
- **`bots-api.p2p.nota-fiscal.warmup`** · repos: bots-api
    - `bots-api.sub.nota-fiscal.warmup` (pull, consumidor provável `bots-api`) · repos: bots-api
- **`contabilizei-agents.bcast.metrics`** (tópico de `aida-stg`) · repos: canais-adk, contabilizei-agents, zendesk-agents
    - `zendesk-agents.sub.etl.agent-latency` (pull, consumidor provável `zendesk-agents`) · repos: zendesk-agents
    - `zendesk-agents.sub.v1.agents-control.on-metrics` (pull, consumidor provável `zendesk-agents`) · repos: zendesk-agents
- **`contato-service.topic.on-message-event-meta`** · repos: contato-service
    - `contato-service.sub.on-message-event-meta` (pull, consumidor provável `contato-service`, DLQ `contato-service.topic.on-message-event-meta.dlq`) · repos: contato-service, pipeline
- **`contato-service.topic.on-message-event-meta.dlq`** · repos: contato-service
    - `contato-service.sub.on-message-event-meta.dlq` (pull, consumidor provável `contato-service`) · repos: contato-service
- **`email-service.p2p.file-upload`** · repos: email-service, microsservico-agrupamento-guias
    - `email-service.p2p.file-upload.sub` (pull, consumidor provável `email-service`, DLQ `email-service.p2p.file-upload.dlq`) · repos: email-service
- **`email-service.p2p.file-upload.dlq`** · repos: email-service
    - `email-service.p2p.file-upload.dlq.inspect.sub` (pull, consumidor provável `email-service`) · repos: email-service
- **`email-service.p2p.send-email`** · repos: email-service, experts-service, microsservico-agrupamento-guias
    - `email-service.p2p.send-email.sub` (pull, consumidor provável `email-service`, DLQ `email-service.p2p.send-email.dlq`) · repos: email-service, pipeline
- **`email-service.p2p.send-email-callback`** · repos: email-service, microsservico-agrupamento-guias
    - `email-service.p2p.send-email-callback.update-db.sub` (pull, consumidor provável `email-service`, DLQ `email-service.p2p.send-email-callback.dlq`) · repos: email-service
    - `ms-agrupamento-guias.sub.send-email-callback` (pull, consumidor provável `ms-agrupamento-guias`) · repos: microsservico-agrupamento-guias
- **`email-service.p2p.send-email-callback.dlq`** · repos: email-service
    - `email-service.p2p.send-email-callback.dlq.inspect.sub` (pull, consumidor provável `email-service`) · repos: email-service
- **`email-service.p2p.send-email-validated`** · repos: email-service
    - `email-service.p2p.send-email-validated.enqueue-dispatch.sub` (pull, consumidor provável `email-service`, DLQ `email-service.p2p.send-email-validated.dlq`) · repos: email-service
    - `email-service.p2p.send-email-validated.replicate-record.sub` (pull, consumidor provável `email-service`, DLQ `email-service.p2p.send-email-validated.dlq`) · repos: email-service
- **`email-service.p2p.send-email-validated.dlq`** · repos: email-service
    - `email-service.p2p.send-email-validated.dlq.inspect.sub` (pull, consumidor provável `email-service`) · repos: email-service
- **`email-service.p2p.send-email.dlq`** · repos: email-service
    - `email-service.p2p.send-email.dlq.inspect.sub` (pull, consumidor provável `email-service`) · repos: email-service
- **`experts-nfs.bcast.nfs.result`** (tópico de `contabilizei-experts-dev`) · repos: experts-nfs, zendesk-agents
    - `zendesk-agents.sub.v1.concierge-acknowledge-nf` (pull, consumidor provável `zendesk-agents`) · repos: zendesk-agents
    - `zendesk-agents.sub.v1.concierge-acknowledge-nf-massivo` (pull, consumidor provável `zendesk-agents`)
- **`experts-service.bcast.csat-response`** (tópico de `contabilizei-experts-dev`) · repos: experts-service, zendesk-agents
    - `zendesk-agents.sub.v1.agents-control.on-csat-response` (pull, consumidor provável `zendesk-agents`) · repos: zendesk-agents
- **`ms-agrupamento-guias.p2p.agrupar-guias`**
- **`ms-agrupamento-guias.p2p.agrupar-guias-retry`** · repos: microsservico-agrupamento-guias
    - `ms-agrupamento-guias.sub.agrupar-guias-retry` (pull, consumidor provável `ms-agrupamento-guias`) · repos: microsservico-agrupamento-guias
- **`ms-agrupamento-guias.p2p.notificacao-diagnostico-bp`** · repos: microsservico-agrupamento-guias
    - `ms-agrupamento-guias.sub.notificacao-diagnostico-bp` (pull, consumidor provável `ms-agrupamento-guias`) · repos: microsservico-agrupamento-guias
    - `ms-agrupamento-guias.sub.notificacao-diagnostico-bp-local` (pull, consumidor provável `ms-agrupamento-guias`) · repos: microsservico-agrupamento-guias
- **`ms-agrupamento-guias.p2p.notifies-email`** · repos: microsservico-agrupamento-guias
    - `ms-agrupamento-guias.sub.notifies-email` (pull, consumidor provável `ms-agrupamento-guias`) · repos: microsservico-agrupamento-guias
- **`ms-agrupamento-guias.p2p.notifies-wpp`** · repos: microsservico-agrupamento-guias
    - `ms-agrupamento-guias.sub.notifies-wpp` (pull, consumidor provável `ms-agrupamento-guias`) · repos: microsservico-agrupamento-guias
- **`ms-agrupamento-guias.p2p.processar-guia`**
- **`processar-guia-imposto`** (tópico de `contabilizei-fintech-dev-01`) · repos: contabilizei-back-core, contabilizei-guias, experts-service, microsservico-agrupamento-guias, plataforma-fopag-worker, plataforma-importacao-notas-worker
    - `ms-agrupamento-guias.sub.processar-guia` (pull, consumidor provável `ms-agrupamento-guias`) · repos: microsservico-agrupamento-guias
- **`zendesk-agents.bcast.etl.agent-latency-results`** · repos: zendesk-agents
    - `zendesk-agents.sub.bq.agent-latency-results` (BigQuery → `contabilizei-dataflow-teste.ctbz_agents_metrics.agent_latency`) · repos: zendesk-agents
- **`zendesk-agents.bcast.v1.recalculo-ticket-off-criado`**
    - `zendesk-agents.sub.v1.recalculo-ticket-off-criado` (pull, consumidor provável `zendesk-agents`)
- **`zendesk-webhooks-conversations`** (tópico de `contabilizei-crm-dev`) · repos: atendimento-api-gateway, atendimento-zendesk, bots-api, contabilizei-crm-webhooks, experts-service, kong-config, pipeline, zendesk-agents
    - `bots-api.lock90.conversations` (pull, consumidor provável `bots-api`)
    - `zendesk-agents.sub.conversations` (pull, consumidor provável `zendesk-agents`) · repos: zendesk-agents
    - `zendesk-agents.sub.v1.copilot-actions.dictionary-on-message` (pull, consumidor provável `zendesk-agents`) · repos: zendesk-agents
- **`zendesk-webhooks-messages`** (tópico de `contabilizei-crm-dev`) · repos: atendimento-api-gateway, atendimento-zendesk, bots-api, kong-config
    - `bots-api.ativo-workflow.on-message` (pull, consumidor provável `bots-api`)
    - `bots-api.encerramento.on-message` (pull, consumidor provável `bots-api`) · repos: bots-api
- **`zendesk-webhooks-tickets`** (tópico de `contabilizei-crm-dev`) · repos: atendimento-api-gateway, bots-api, contabilizei-crm-webhooks, experts-drawio, experts-service, kong-config, monitoria-ia, pipeline, zendesk-agents
    - `bots-api.ativo-workflow.initialize` (pull, consumidor provável `bots-api`)
    - `bots-api.encerramento.initialize` (pull, consumidor provável `bots-api`) · repos: bots-api
    - `bots-api.encerramento.on-ticket-closed` (pull, consumidor provável `bots-api`) · repos: bots-api
    - `bots-api.encerramento.on-ticket-open` (pull, consumidor provável `bots-api`) · repos: bots-api
    - `bots-api.re-route.ticket` (pull, consumidor provável `bots-api`) · repos: bots-api
    - `zendesk-agents.sub.v1.agents-control.on-ticket-update` (pull, consumidor provável `zendesk-agents`) · repos: zendesk-agents
    - `zendesk-agents.sub.v1.copilot-actions.on-ticket-update` (pull, consumidor provável `zendesk-agents`) · repos: zendesk-agents
    - `zendesk-agents.sub.v1.customer-summary.on-ticket-update` (pull, consumidor provável `zendesk-agents`) · repos: zendesk-agents
