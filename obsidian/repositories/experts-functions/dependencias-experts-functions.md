---
name: dependencias-experts-functions
description: "Dependências do experts-functions: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - experts-functions
repositorio: experts-functions
---

# Dependências do experts-functions

O que o `experts-functions` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

## Consome

### Repositórios internos

_Nada confirmado ainda._

### Libs internas

_Nada confirmado ainda._

### Infra GCP

- `email-service` (tópicos em `atendimento-canais-prd`/`-dev`): a `function-email-holerites` publica os PDFs em `email-service.p2p.file-upload` (`{content: Buffer.toJSON()}`, o messageId vira o `fileId`) e o envio em `email-service.p2p.send-email`, em `functions/email-holerites/src/services/email-service.publisher.ts` (PRD-178571, MR experts-functions!10; publisher da SA via vault-roleset!723)

### Bancos e dados

_Nada confirmado ainda._

### Terceiros

_Nada confirmado ainda._

## Consumido por

Quem consome os contratos deste repositório; a revisão de MRs confere se o diff quebra algum deles.

_Nada confirmado ainda._

<!-- deps:auto:inicio (gerado por mapear-dependencias; não editar à mão) -->

## Levantamento automático

Gerado em 2026-11-19 sobre `fix/html-to-pdf-chromium` @ `abd9e0b` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `html-to-pdf` (31×): `Dockerfile:14`, `catalog-info.yaml:11`, `catalog-model/apis/html-to-pdf-api.yaml:4`

### Repositórios que citam este

- `experts-dominios-functions` (2×): `package.json:2`, `test-report.xml:3`

### Libs internas

- `@contabilizei-private/event-workers` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `expired-twilio-tasks`, `functions.email-holerites`, `functions.ia-desvio-conduta.single-from-batch`, `functions.ia-desvio-conduta.single_chat-from-batch`, `functions.p2p.email-sender`, `functions.pendencias-oportunidades`, `twilio-republish-evts-from-crm`, `twilio-webhooks-tasks`
- **Subscription**: `functions.ia-desvio-conduta.single-from-batch.3-5-turbo-0125-temp0-sub`, `functions.ia-desvio-conduta.single-from-batch.4o-temp0-sub`, `functions.ia-desvio-conduta.single-from-evt.system-deleted.4o-sub`, `functions.ia-desvio-conduta.single-from-evt.task-completed.4o-sub`, `functions.ia-desvio-conduta.single_chat-from-batch-sub`, `tw-tasks-republish-to-experts-sub`
- **Scheduler**: `pendencias-oportunidades-scheduler`
- **Cloud Run / function**: `function-email-holerites`, `function-email-sender`, `function-html-to-pdf`, `function-pendencias-oportunidades`, `html-to-pdf`

### Bancos e dados

- BigQuery: `@google-cloud/bigquery`
- Cloud Storage: `@google-cloud/storage`
- Postgres: `pg`
- Pub/Sub: `@google-cloud/pubsub`
- SQL (query builder/ORM): `drizzle-orm`
- Tabelas/datasets do BigQuery citados: `contabilizei-data.output_analytics_trusted.view_sintese_pendencias_oportunidades`, `contabilizei-dataflow.dw_contabilizeiapp.socio`

### Terceiros

- OpenAI: `api.openai.com` em `packages/openai/src/lib/openai.facade.ts:12`

<!-- deps:auto:fim -->
