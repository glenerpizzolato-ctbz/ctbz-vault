---
name: dependencias-contabilizei-crm-webhooks
description: "Dependências do contabilizei-crm-webhooks: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - contabilizei-crm-webhooks
repositorio: contabilizei-crm-webhooks
---

# Dependências do contabilizei-crm-webhooks

O que o `contabilizei-crm-webhooks` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `76abc29` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `atendimento-zendesk` (4×): `configs/.env.dev:12`, `configs/.env.example:12`, `configs/.env.prod:12`

### Repositórios que citam este

- `atendimento-api-gateway` (1×): `.env.example:22`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-bruno`, `experts-drawio`, `kong-config`, `pipeline`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `atendimento-zendesk-atualizar-ticket`, `test-topic`, `twilio-webhooks-messages`, `twilio-webhooks-messages-local`, `twilio-webhooks-tasks`, `twilio-webhooks-tasks-local`, `zendesk-webhooks-agents`, `zendesk-webhooks-capacidade-agentes`, `zendesk-webhooks-comments`, `zendesk-webhooks-conversations`, `zendesk-webhooks-events-tickets`, `zendesk-webhooks-notifications`, `zendesk-webhooks-pesquisa-satisfacao`, `zendesk-webhooks-retorno-desconexao-sem-interacao`, `zendesk-webhooks-tickets`, `zendesk-webhooks-tickets-new`, `zendesk-webhooks-users`
- **Subscription**: `zendesk-webhooks-tickets`
- **Cloud Run / function**: `contabilizei-crm-webhooks`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
