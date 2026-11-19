---
name: dependencias-experts-nfs
description: "Dependências do experts-nfs: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - experts-nfs
repositorio: experts-nfs
---

# Dependências do experts-nfs

O que o `experts-nfs` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `fix/cve-node2shell` @ `e1343151` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `emissor-whatsapp` (20×): `src/modules/internal/emissor-massivo/schemas/create-nota-massiva.zod.ts:2`, `src/modules/internal/emissor-whatsapp/emissor-whatsapp.controller.ts:7`, `src/modules/internal/emissor-whatsapp/emissor-whatsapp.router.ts:3`
- `aida-back` (17×): `prisma/schema.prisma:206`, `src/modules/common/contabilizei/aida-back/aida-back.facade.ts:11`, `src/modules/common/contabilizei/ctbz-http.client.ts:46`
- `bots-api` (17×): `src/modules/common/contabilizei/bots-api/bots-api.facade.ts:12`, `src/modules/common/contabilizei/bots-api/dto/empresa.ts:11`, `src/modules/common/contabilizei/ctbz-http.client.ts:47`
- `zendesk-agents` (10×): `src/modules/v3/emissor/copilot-massivo/constants/copilot-massivo.ts:7`, `src/modules/v3/emissor/copilot-massivo/usecases/ack/copilot-massivo-ack.usecase.ts:35`, `docs/bruno/v3/emissor/copilot-massivo/callback-from-pubsub.bru:27`
- `experts-service` (10×): `src/modules/common/contabilizei/ctbz-http.client.ts:141`, `src/modules/common/contabilizei/index.ts:5`, `src/modules/internal/emissor-jira/services/usecase/create-nfs-jira.usecase.ts:14`
- `atendimento-zendesk` (8×): `src/modules/common/contabilizei/index.ts:9`, `src/modules/internal/emissor-whatsapp/services/emissor-whatsapp.service.ts:5`, `src/modules/internal/nota-recorrente/services/acknowledge.service.ts:3`
- `ticketing-service` (8×): `src/modules/common/contabilizei/ctbz-http.client.ts:130`, `src/modules/internal/emissor/services/notafiscalv2.service.ts:4`, `src/modules/common/contabilizei/ctbz-http.client.test.ts:112`
- `contabilizei-front` (1×): `src/modules/common/utils/texto-caracteres.utils.ts:2`
- `contabilizei-front-vue` (1×): `src/modules/common/utils/texto-caracteres.utils.ts:2`
- `plataforma-importacao-notas-worker` (1×): `src/modules/v3/confianca/usecases/registrar-desfecho/registrar-desfecho.usecase.ts:35`

### Repositórios que citam este

- `atendimento-canais-admin` (549×): `src/lib/collections/nfs.collection.ts:20`, `src/lib/collections/operator-nfs.collection.ts:9`, `src/lib/validators/foreign-postal.ts:4`
- `canais-adk` (201×): `.env.example:21`, `src/application/agents/concierge-experts/certificado-digital/nf-contexto.ts:2`, `src/application/agents/concierge-experts/certificado-digital/status-pedido.ts:5`
- `zendeskapp-concierge` (39×): `src/javascripts/constants/currencies.js:3`, `src/javascripts/modules/common/acoes/Acoes.jsx:537`, `src/javascripts/modules/common/acoes/acao/detalhes/Detalhes.jsx:138`
- `zendesk-agents` (31×): `src/consumers/copilot/acknowledge-nf.consumer.ts:6`, `src/infra/clients/experts-nfs.client.ts:5`, `src/infra/clients/experts-nfs/emitir.dto.ts:1`
- `atendimento-zendesk` (28×): `src/domain/bots/whatsapp/experts/fluxo-notafiscal/experts-fluxo-notafiscal-v4.controller.ts:17`, `src/domain/bots/whatsapp/experts/fluxo-notafiscal/nota-massiva/services/publicar-notas-massiva.service.ts:17`, `src/domain/bots/whatsapp/experts/fluxo-notafiscal/services/buscar-elegibilidade.service.ts:12`
- `aida-back` (23×): `contabilizeiai/clients/experts_nfs_client.py:8`, `contabilizeiai/functions/fiscal/notas/notas_fiscais_builder_v2.py:158`, `contabilizeiai/services/openai/prompting/handlers/nota_fiscal/fluxo_emissao_nota_fiscal_handler_v1.py:3`
- `bots-api` (10×): `src/clients/index.ts:6`, `src/domain/ultimateai/notasfiscais/elegibilidade.service.ts:2`, `src/domain/ultimateai/notasfiscais/nfs-flows.service.ts:4`
- `plataforma-importacao-notas-worker` (9×): `src/main/resources/filtered/parametro.desenv.properties:656`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:450`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:491`
- `mcp-notas-fiscais` (7×): `app/tools/emitir_nota.py:47`, `app/tools/emitir_nota_exterior_retroativa.py:14`, `app/tools/emitir_nota_nacional_retroativa.py:14`
- `experts-api-gateway` (6×): `config/kong-template.yml:40`
- `emissor-whatsapp-reports` (3×): `src/emissor-massivo/nota-link.ts:6`, `src/utils/config-manager/config.dev.ts:7`, `src/utils/config-manager/config.ts:7`
- `emissor-whatsapp` (2×): `app/src/utils/config-manager/config.dev.ts:9`, `app/src/utils/config-manager/config.ts:9`
- `experts-service` (2×): `src/infra/config/dev.ts:91`, `src/infra/config/prod.ts:93`
- `experts-twilio` (2×): `src/domain/nota-massiva/usecase/processar-notas.usecase.ts:49`
- `contabilizei-agents` (1×): `app/utils/env.py:69`
- `monitoria-ia` (1×): `docs/validacao-ajuste-avaliacoes.md:261`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `cnpj-alfanumerico`, `experts-bruno`, `experts-drawio`, `ide-bahcode`, `k8s-configmap`, `kong-config`, `pipeline`

### No grafo manual ([[grafo-chamadas-canais]])

- Consome: `experts-service`, `ticketing-service`, `bots-api`, `aida-back`
- Consumido por: `atendimento-canais-admin`, `zendesk-agents`, `canais-adk`, `bots-api`, `aida-back`, `mcp-notas-fiscais`

### Libs internas

- `@contabilizei-private/br-utils` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/fastify-instrumentation` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/google-pubsub` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/jira-api` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/simple-cache` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/telemetry` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `atendimento-zendesk.envio-whatsapp-ativo`, `emissor-callback`, `emissor-experts`, `emissor-massivo-reports`, `experts-nfs.bcast.nfs.result`, `experts-nfs.dead-letter`, `experts-nfs.p2p.create-nfs-jira`, `experts-nfs.p2p.nfs.retroativa`, `nfs.non-elegible`, `notas-worker.bcast.nfs-concluida`, `test-topic`
- **Subscription**: `emissor-massivo-reports`, `experts-nfs.sub.ack-nfs-recorrente`, `experts-nfs.sub.create-nfs-jira`, `experts-nfs.sub.emissor-callback.google-chat`, `experts-nfs.sub.emissor-callback.massivo`, `experts-nfs.sub.emissor-callback.whatsapp`, `experts-nfs.sub.nfs-concluida`, `experts-nfs.sub.nfs-jira.send-whatsapp-message`, `experts-nfs.sub.nfs-jira.update-issue`, `experts-nfs.sub.nfs.non-elegible.google-chat`, `experts-nfs.sub.nfs.retroativa`, `experts-nfs.sub.nfs.retroativa.google-chat`, `experts-nfs.sub.v3.emissor-callback.massivo`, `experts-nfs.sub.v3.emissor-callback.result`, `experts-nfs.sub.v3.emissor-callback.whatsapp-message`
- **Scheduler**: `experts-nfs-monitoring-check-queue`
- **Fila Cloud Tasks**: `emissor-experts`, `emissor-experts-pooler`, `emissor-whatsapp`, `notas-recorrentes`
- **Cloud Run / function**: `emissor-whatsapp`, `experts-nfs`

### Bancos e dados

- Cloud Storage: `@google-cloud/storage`
- Cloud Tasks: `@google-cloud/tasks`
- Postgres (Prisma): `@prisma/client`, `prisma`
- Pub/Sub: `@google-cloud/pubsub`
- Redis: `ioredis`

### Terceiros

- Google Chat: `chat.googleapis.com` em `src/modules/common/google-cloud/google-chat/google-chat.facade.ts:36`
- Jira / Confluence: `custom-jira.atlassian.net` em `src/modules/common/jira/jira-client.factory.test.ts:89`, `mock-jira.atlassian.net` em `src/modules/common/jira/jira-client.factory.test.ts:35`

<!-- deps:auto:fim -->
