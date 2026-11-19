---
name: dependencias-experts-twilio
description: "Dependências do experts-twilio: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - experts-twilio
repositorio: experts-twilio
---

# Dependências do experts-twilio

O que o `experts-twilio` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `6151847` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `experts-alertas` (11×): `environments/.env-dev:45`, `environments/.env-local:41`, `environments/.env-prod:45`
- `plataforma-crm-web` (4×): `environments/.env-dev:32`, `environments/.env-local:27`, `environments/.env-prod:32`
- `experts-nfs` (2×): `src/domain/nota-massiva/usecase/processar-notas.usecase.ts:49`
- `experts-contabil` (2×): `thunder-tests/thunderCollection.json:19`, `thunder-tests/thunderEnvironment.json:176`
- `emissor-whatsapp` (1×): `src/domain/nota-massiva/usecase/processar-notas.usecase.ts:61`

### Repositórios que citam este

- `experts-api-gateway` (4×): `Makefile:12`, `config/kong-template.yml:5`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `experts-drawio`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `jira-troca-assessor-elogio-sugestao`, `nfs.instabilidade-prefeitura`, `nfs.non-elegible`, `twilio-metrics-flow`, `zendesk-tickets-upsert`
- **Subscription**: `twilio-metrics-flow`
- **Fila Cloud Tasks**: `emissor-whatsapp-massivo`, `feedback-hub`
- **Cloud Run / function**: `emissor-whatsapp-massivo`, `experts-alertas`, `experts-contabil`

### Bancos e dados

- Cloud Tasks: `@google-cloud/tasks`
- Postgres (Prisma): `@prisma/client`, `prisma`
- Pub/Sub: `@google-cloud/pubsub`

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/domain/feedback-hub/feedback-hub.service.spec.ts:219`
- Twilio: `api.twilio.com` em `src/domain/nota-massiva/usecase/test/processar-notas.usecase.spec.ts:80`, `twilio`

<!-- deps:auto:fim -->
