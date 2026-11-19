---
name: dependencias-emissor-whatsapp
description: "Dependências do emissor-whatsapp: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - emissor-whatsapp
repositorio: emissor-whatsapp
---

# Dependências do emissor-whatsapp

O que o `emissor-whatsapp` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `f4c2fc3` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `experts-nfs` (2×): `app/src/utils/config-manager/config.dev.ts:9`, `app/src/utils/config-manager/config.ts:9`
- `experts-api-gateway` (2×): `docs/bruno/environments/ctbz-exp-dev.bru:11`, `docs/bruno/environments/ctbz-exp-prd.bru:12`

### Repositórios que citam este

- `experts-nfs` (20×): `src/modules/internal/emissor-massivo/schemas/create-nota-massiva.zod.ts:2`, `src/modules/internal/emissor-whatsapp/emissor-whatsapp.controller.ts:7`, `src/modules/internal/emissor-whatsapp/emissor-whatsapp.router.ts:3`
- `experts-twilio-flows` (16×): `whatsapp/main/hom/parent_flow.json:2016`, `whatsapp/main/hom/subflows/CadTomador.json:153`, `whatsapp/main/hom/subflows/NFIndiv.json:1438`
- `experts-api-gateway` (15×): `config/kong-template.yml:15`
- `emissor-whatsapp-reports` (13×): `bitbucket-pipelines.yml:140`, `package.json:2`, `src/emissor-massivo.router.ts:6`
- `plataforma-crm-web` (9×): `src/main/resources/filtered/parametro.desenv.properties:201`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:144`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:147`
- `atendimento-zendesk` (6×): `src/domain/bots/whatsapp/experts/fluxo-notafiscal/nota-massiva/services/publicar-notas-massiva.service.ts:27`, `src/domain/bots/whatsapp/experts/fluxo-notafiscal/services/enfileirar-nfs-elegivel.service.ts:22`, `src/domain/bots/whatsapp/experts/fluxo-notafiscal/nota-massiva/services/publicar-notas-massiva.service.spec.ts:46`
- `canais-adk` (4×): `src/domain/empresa/empresa.types.ts:24`, `src/infra/clients/experts-nfs/experts-nfs.client.ts:39`, `src/infra/clients/experts-nfs/experts-nfs.client.spec.ts:207`
- `firestore-to-bigquery` (3×): `configs/experts-notaswpp-massivo-lotes.json:3`, `configs/experts-notaswpp-massivo-notas.json:3`, `configs/experts-notaswpp-singular.json:3`
- `atendimento-api-gateway` (2×): `config/kong-template-dev.yaml:1510`, `config/kong-template-prod.yaml:1301`
- `contabilizei-agents` (2×): `app/clients/experts_nfs/__init__.py:17`, `app/clients/experts_nfs/__tests__/test_experts_nfs_client.py:31`
- `mcp-notas-fiscais` (2×): `app/clients/experts_nfs_client.py:125`, `app/clients/__tests__/test_experts_nfs_client.py:90`
- `experts-service` (1×): `src/domain/nfs/services/nfs-sheet.service.ts:67`
- `experts-twilio` (1×): `src/domain/nota-massiva/usecase/processar-notas.usecase.ts:61`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `cnpj-alfanumerico`, `experts-drawio`, `pipeline`

### Libs internas

- `@contabilizei-private/contabilizei-sso-client-javascript` (`app/package.json`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `emissor-massivo-check-issuance`, `emissor-massivo-processar`, `emissor-massivo-reports`, `twilio-metrics-flow`
- **Subscription**: `emissor-massivo-processar`, `emissor-massivo-reports`, `twilio-metrics-flow`
- **Fila Cloud Tasks**: `emissor-whatsapp`, `emissor-whatsapp-massivo`
- **Cloud Run / function**: `emissor-whatsapp`, `emissor-whatsapp-massivo`

### Bancos e dados

- Cloud Tasks: `@google-cloud/tasks`
- Firestore: `@google-cloud/firestore`
- Pub/Sub: `@google-cloud/pubsub`
- Secret Manager: `@google-cloud/secret-manager`

### Terceiros

- Firebase: `firebase-admin`
- Google Chat: `chat.googleapis.com` em `app/src/shared/google-chat/google-chat.service.ts:9`
- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `Readme.md:11`
- Twilio: `api.twilio.com` em `app/src/shared/contabilizei/__tests__/jira.service.test.ts:17`

<!-- deps:auto:fim -->
