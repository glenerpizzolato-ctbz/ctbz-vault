---
name: dependencias-meta-webhooks
description: "Dependências do meta-webhooks: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - meta-webhooks
repositorio: meta-webhooks
---

# Dependências do meta-webhooks

O que o `meta-webhooks` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

- `contato-service`: tópico `meta-webhooks.bcast.whatsapp.messages`, pela subscription `contato-service.sub.meta-webhooks-messages` — por `src/infra/gcp/pubsub-subs.ts` e o `metaWebhooksMessagesWorker` do contato-service

<!-- deps:auto:inicio (gerado por mapear-dependencias; não editar à mão) -->

## Levantamento automático

Gerado em 2026-11-19 sobre `master` @ `369655d` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contato-service` (8×): `AGENTS.md:72`, `README.md:64`, `docs/adr/001-borda-sem-banco-fan-out-por-dominio.md:8`
- `email-service` (1×): `.dockerignore:1`
- `survey-service` (1×): `docs/adr/002-cloud-run-publish-aguardado.md:14`
- Configuração, CI e documentação citadas: `k8s-configmap`, `vault-roleset`

### Repositórios que citam este

- `contato-service` (25×): `src/domain/bsp-contact/bsp-contact.module.ts:36`, `src/domain/bsp-contact/consumers/on-message-event-meta.worker.ts:27`, `src/infra/gcp/pubsub-subs.ts:5`
- `atendimento-zendesk` (3×): `src/app/worker/worker-webhooks/meta-templates-worker/consumers/meta-templates.consumer.ts:18`, `src/app/worker/worker-webhooks/meta-templates-worker/consumers/meta-templates.consumer.spec.ts:42`

### Libs internas

- `@contabilizei-private/pino-logger` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/zezu-core` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

- Pub/Sub: `@google-cloud/pubsub`

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
