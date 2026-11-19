---
name: dependencias-experts-scripts
description: "Dependências do experts-scripts: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - experts-scripts
repositorio: experts-scripts
---

# Dependências do experts-scripts

O que o `experts-scripts` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `50d7ea1` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `atendimento-zendesk` (2×): `batch-single-calls/clients/atendimento-zendesk_kong.js:8`
- `contabilizei-guias` (2×): `gcp/cloud-tasks/create-tasks/migr-templates-tw-to-zd/segundo-lote-templates.json:4213`
- `contabilizei-impostos` (1×): `gcp/cloud-tasks/create-tasks/migr-templates-tw-to-zd/segundo-lote-templates.json:4213`

### Repositórios que citam este

_Nenhum._
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-bruno`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Fila Cloud Tasks**: `certificado-digital`, `notas-recorrentes`

### Bancos e dados

- BigQuery: `@google-cloud/bigquery`
- Cloud Storage: `@google-cloud/storage`
- Cloud Tasks: `@google-cloud/tasks`
- Datastore: `@google-cloud/datastore`
- Firestore: `@google-cloud/firestore`
- Postgres: `pg`
- SQL (query builder/ORM): `knex`

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `fs2sql-etl/README.md:4`
- Meta (WhatsApp Cloud API / Graph): `graph.facebook.com` em `meta/whatsapp/1-list-templates/clients/meta.js:16`
- Ultimate (bots): `ultimate.ai` em `gcp/gcs/ext-endpoint-upload/clients/ultimate_ai.js:5`
- Zendesk: `contabilizei.zendesk.com` em `gcp/bq/IP-987/index.ts:57`

<!-- deps:auto:fim -->
