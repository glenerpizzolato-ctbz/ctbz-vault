---
name: pubsub-contabilizei-issue
description: "Tópicos e subscriptions do Pub/Sub em contabilizei-issue (Issue, dev/prod) com consumidor e repositórios que citam cada um"
metadata:
  type: reference
tags:
  - infra
  - pubsub
atualizado_em: 2026-10-09
---

# Pub/Sub: contabilizei-issue

Issue, dev/prod. Fotografia de 2026-10-09. Formato: tópico → subscriptions (tipo e consumidor) · repositórios que citam o nome do tópico/subscription em `~/repositories` (`config:` = repos de configuração que citam quase tudo). Ver [[_infra-indice]] para o significado de cada campo.

- **`ticketing.bcast.dados-gerais-jira-result`** · repos: ticketing-service
    - `ticketing.sub.bq.dados-gerais-jira-result` (BigQuery → `contabilizei-dataflow.dw_ticketing_service.dados_gerais_jira_result`) · repos: ticketing-service
- **`ticketing.bcast.ticket-jira`** · repos: experts-service, ticketing-service
    - `ticketing.sub.upsert-ticket-jira` (pull, consumidor provável `ticketing`) · repos: ticketing-service
- **`ticketing.bcast.v2.ticket-jira`** · repos: experts-service, ticketing-service
    - `ticketing.sub.v2.upsert-ticket-jira` (pull, consumidor provável `ticketing`) · repos: ticketing-service
- **`ticketing.dead-letters`** · repos: ticketing-service
    - `ticketing.dead-letters-sub` (pull, consumidor provável `ticketing`)
- **`ticketing.p2p.add-dados-gerais-ticket-jira`** · repos: ticketing-service
    - `ticketing.sub.add-dados-gerais-ticket-jira` (pull, consumidor provável `ticketing`, DLQ `ticketing.dead-letters`) · repos: ticketing-service
- **`ticketing.p2p.v1.sla`** · repos: ticketing-service
    - `ticketing.sub.v1.sla` (pull, consumidor provável `ticketing`) · repos: ticketing-service
- **`ticketing.p2p.v2.dados-empresa`** · repos: ticketing-service
    - `ticketing.sub.v2.dados-empresa` (pull, consumidor provável `ticketing`) · repos: ticketing-service
