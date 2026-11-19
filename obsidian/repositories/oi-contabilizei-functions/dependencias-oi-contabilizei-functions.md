---
name: dependencias-oi-contabilizei-functions
description: "Dependências do oi-contabilizei-functions: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - oi-contabilizei-functions
repositorio: oi-contabilizei-functions
---

# Dependências do oi-contabilizei-functions

O que o `oi-contabilizei-functions` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `develop` @ `27fab95f` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-abertura` (1×): `functions/tests/settings/mockFirebaseConfigs.json:176`

### Repositórios que citam este

_Nenhum._
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-bruno`, `kong-config`, `pipeline`

### Libs internas

- `@contabilizei-private/contabilizei-sso-client-javascript` (`functions/package.json`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `zendesk-criar-ticket`

### Bancos e dados

- BigQuery: `@google-cloud/bigquery`
- Cloud Tasks: `@google-cloud/tasks`
- Firestore: `@google-cloud/firestore`
- Pub/Sub: `@google-cloud/pubsub`

### Terceiros

- Firebase: `firebase-admin`
- Google Chat: `chat.googleapis.com` em `functions/tests/settings/mockFirebaseConfigs.json:66`
- Google Workspace APIs: `sheets.googleapis.com` em `functions/services/googleSheetsService.js:66`
- HubSpot: `api.hubapi.com` em `functions/services/hubspotDealsService.js:4`
- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `README.md:18`
- Meta (WhatsApp Cloud API / Graph): `graph.facebook.com` em `functions/tests/services/blipDeskService.test.js:1281`

<!-- deps:auto:fim -->
