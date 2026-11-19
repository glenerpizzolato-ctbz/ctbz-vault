---
name: dependencias-experts-tarefas-assessor
description: "Dependências do experts-tarefas-assessor: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - experts-tarefas-assessor
repositorio: experts-tarefas-assessor
---

# Dependências do experts-tarefas-assessor

O que o `experts-tarefas-assessor` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `4526547` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `experts-zendesk` (7×): `bitbucket-pipelines.yml:206`, `docs/bruno/environments/dev.bru:3`, `docs/bruno/environments/prod.bru:3`

### Repositórios que citam este

_Nenhum._
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `cnpj-alfanumerico`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `submit-single-wpp-message`, `test-topic`, `zendesk-tickets-callback`, `zendesk-tickets-upsert`
- **Scheduler**: `tarefas-organicas`
- **Fila Cloud Tasks**: `experts-zendesk`
- **Cloud Run / function**: `experts-zendesk`

### Bancos e dados

- BigQuery: `@google-cloud/bigquery`
- Postgres (Prisma): `@prisma/client`, `prisma`
- Pub/Sub: `@google-cloud/pubsub`

### Terceiros

- Google Chat: `chat.googleapis.com` em `src/__tests__/modules/shared/google-chat/google-chat.test.ts:24`
- Zendesk: `contabilizei.zendesk.com` em `environments/.env.prod:10`, `contabilizei1637606740.zendesk.com` em `environments/.env.dev:10`

<!-- deps:auto:fim -->
