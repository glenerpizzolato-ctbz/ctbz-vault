---
name: dependencias-experts-bruno
description: "Dependências do experts-bruno: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - experts-bruno
repositorio: experts-bruno
---

# Dependências do experts-bruno

O que o `experts-bruno` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `093e953` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-impostos` (13×): `contabilizei-impostos/auth/gerar token sso.bru:30`, `contabilizei-impostos/bruno.json:3`, `contabilizei-impostos/collection.bru:15`
- `atendimento-zendesk` (7×): `atendimento-zendesk/bruno.json:3`, `"fintech-payments/Obter recorr\303\252ncias ativas.bru":15`, `hubspot/collection.bru:14`
- `contabilizei-abertura` (6×): `contabilizei-abertura/Atualiza campos abertura-Jira Soci/Iniciar rotina.bru:8`, `contabilizei-abertura/Atualiza campos abertura-Jira Soci/Sincroniza processo jira.bru:8`, `contabilizei-abertura/Atualiza campos abertura-Jira Soci/Update processo.bru:8`
- `aida-back` (3×): `aida-back/bruno.json:3`, `aida-back/environments/prd.bru:2`, `aida-back/environments/stg.bru:2`
- `experts-alertas` (3×): `experts-alertas/bruno.json:3`, `experts-alertas/environments/dev.bru:2`, `experts-alertas/environments/prod.bru:2`
- `plataforma-central-rotinas` (2×): `contabilizeiapp/environments/dev03-libera_meu_ip.bru:10`, `contabilizeiapp/environments/prod.bru:7`
- `contabilizei-crm-webhooks` (2×): `crm-webhooks/environments/dev.bru:2`, `crm-webhooks/environments/prod.bru:2`
- `experts-nfs` (1×): `atendimento-zendesk/zendesk_apps/wpp-ativo/submeter-local.bru:30`
- `experts-scripts` (1×): `atendimento-zendesk_heimdall/whatsapp-ativo/messaging/submit/current/submit_scripts.bru:18`
- `experts-service` (1×): `atendimento-zendesk_heimdall/whatsapp-ativo/templates/create.bru:20`
- `plataforma-crm-web` (1×): `contabilizei-sso/criar token.bru:24`
- `fintech-payments` (1×): `fintech-payments/bruno.json:3`
- `oi-contabilizei-functions` (1×): `oi-contabilizei-functions/bruno.json:3`
- `plataforma-back-worker` (1×): `plataforma-back-worker/bruno.json:3`
- `plataforma-web` (1×): `plataforma-web/bruno.json:3`
- `zendeskapp-whatsapp-ativo` (1×): `zendesk-api/Support API/apps/single_app/upload.bru:14`

### Repositórios que citam este

- `atendimento-zendesk` (6×): `docs/bruno/web_v1/wpp-ativo/msg/submit/single/send-doc-header.bru:21`, `docs/bruno/web_v1/wpp-ativo/msg/submit/single/send-flow-button.bru:21`, `docs/bruno/web_v1/wpp-ativo/msg/submit/single/send-img-header.bru:21`
- `atendimento-canais-admin` (1×): `src/server/domains/zendesk-sustentacao/zendesk-sustentacao.identity.ts:9`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `ide-bahcode`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `twilio-webhooks-channels`, `zendesk-webhooks-notifications`
- **Fila Cloud Tasks**: `feedback-hub`
- **Cloud Run / function**: `check-numerical-answer`, `compare-values`, `experts-alertas`, `experts-nfs`, `multiply-two-string-values`, `return-element-at-index`, `return-list-property`, `validate-date`, `zendeskbot-conditional`, `zendeskbot-config`, `zendeskbot-delay`, `zendeskbot-loop`, `zendeskbot-parse-string-to-number`, `zendeskbot-validate-finantial-value`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Google Chat: `chat.googleapis.com` em `google-chat/environments/prod.bru:2`
- HubSpot: `api.hubapi.com` em `hubspot/collection.bru:12`
- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `.claude/skills/zendesk-contatos/SKILL.md:129`
- Meta (WhatsApp Cloud API / Graph): `graph.facebook.com` em `facebook-api/collection.bru:11`
- OpenAI: `api.openai.com` em `openai-api/environments/dev.bru:2`
- Ultimate (bots): `ultimate.ai` em `ultimate-ai-api/collection.bru:4`
- Zendesk: `2fjiraplugin.zendesk.com` em `zendesk-api/Support API/tickets/{id}/update/plugin jira/v1/submit_link.bru:8`, `contabilizei.zendesk.com` em `ultimate-ai-bots/bots/wpp-survery/teste_media/file.bru:49`, `sunco-shoplifter.zendesk.com` em `sunhine-api-full/Sunshine Conversations API/Sunshine Conversations Connect/folder.bru:24`

<!-- deps:auto:fim -->
