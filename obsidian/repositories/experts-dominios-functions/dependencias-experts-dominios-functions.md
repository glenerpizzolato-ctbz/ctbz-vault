---
name: dependencias-experts-dominios-functions
description: "Dependências do experts-dominios-functions: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - experts-dominios-functions
repositorio: experts-dominios-functions
---

# Dependências do experts-dominios-functions

O que o `experts-dominios-functions` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `feat-updatenode` @ `1aa3292` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `html-to-pdf` (28×): `bitbucket-pipelines.yml:301`, `functions/email-holerites/src/services/holerite-sender.service.ts:6`, `functions/email-holerites/terraform/development/variables.tf:25`
- `experts-functions` (2×): `package.json:2`, `test-report.xml:3`

### Repositórios que citam este

_Nenhum._
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `cnpj-alfanumerico`

### Libs internas

- `@contabilizei-private/event-workers` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `expired-twilio-tasks`, `functions.email-holerites`, `functions.ia-desvio-conduta.single-from-batch`, `functions.ia-desvio-conduta.single_chat-from-batch`, `functions.p2p.email-sender`, `functions.pendencias-oportunidades`, `twilio-republish-evts-from-crm`, `twilio-webhooks-tasks`
- **Subscription**: `functions.ia-desvio-conduta.single-from-batch.3-5-turbo-0125-temp0-sub`, `functions.ia-desvio-conduta.single-from-batch.4o-temp0-sub`, `functions.ia-desvio-conduta.single-from-evt.system-deleted.4o-sub`, `functions.ia-desvio-conduta.single-from-evt.task-completed.4o-sub`, `functions.ia-desvio-conduta.single_chat-from-batch-sub`, `tw-tasks-republish-to-experts-sub`
- **Scheduler**: `pendencias-oportunidades-scheduler`
- **Cloud Run / function**: `function-email-holerites`, `function-email-sender`, `function-html-to-pdf`, `function-pendencias-oportunidades`, `html-to-pdf`

### Bancos e dados

- BigQuery: `@google-cloud/bigquery`
- Postgres: `pg`
- Pub/Sub: `@google-cloud/pubsub`
- SQL (query builder/ORM): `drizzle-orm`
- Tabelas/datasets do BigQuery citados: `contabilizei-data.output_analytics_trusted.view_sintese_pendencias_oportunidades`

### Terceiros

- OpenAI: `api.openai.com` em `packages/openai/src/lib/openai.facade.ts:12`

<!-- deps:auto:fim -->
