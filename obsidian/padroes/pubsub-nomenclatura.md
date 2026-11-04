---
name: pubsub-nomenclatura
description: "Padrão de nomes de Pub/Sub do time: tópico <serviço>.p2p.<nome>, subscription <serviço>.sub.<nome> (sem .sub no fim) e sufixo -local nas subscriptions da execução local"
metadata:
  type: feedback
tags:
  - padroes
  - pubsub
atualizado_em: 2026-10-15
---

# Nomenclatura de tópicos e subscriptions

- **Tópico:** `<serviço>.p2p.<nome>` (ex.: `agrupamento-guias-service.p2p.notifica-exp-simples-email`).
- **Subscription:** `<serviço-consumidor>.sub.<nome>` (ex.: `agrupamento-guias-service.sub.notifica-exp-simples-email`, `ms-agrupamento-guias.sub.notifies-email`). **Não** usar `<tópico>.sub` com `.sub` no fim, mesmo que o `email-service` faça assim (`email-service.p2p.send-email.sub`): o Glener corrigiu isso como errado.
- **Execução local:** o consumer rodando na máquina se conecta a uma subscription própria com `-local` no fim (ex.: `ms-agrupamento-guias.sub.notificacao-diagnostico-bp-local`, `agrupamento-guias-service.sub.notifica-exp-simples-email-local`), para não disputar mensagens com o pod de dev. Essas subs só existem no terraform de dev.

**Why:** padrão do time de canais; o prefixo da subscription é o consumidor (o catálogo de infra infere o "consumidor provável" por ele).

**How to apply:** ao criar tópico/subscription em qualquer serviço, seguir esse formato; em serviço Node, ligar o sufixo `-local` por uma variável de ambiente (no `agrupamento-guias-service`: `IS_LOCAL=true` → `subscriptionPath`), e criar as subs `-local` no terraform de dev.
