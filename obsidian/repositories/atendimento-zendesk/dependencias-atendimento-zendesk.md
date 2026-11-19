---
name: dependencias-atendimento-zendesk
description: "Dependências do atendimento-zendesk: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - atendimento-zendesk
repositorio: atendimento-zendesk
---

# Dependências do atendimento-zendesk

O que o `atendimento-zendesk` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `fc5b2fe3f` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `plataforma-crm-web` (274×): `.config.json:184`, `environments/_deprecated/config-dev.json:255`, `environments/_deprecated/config-local.json:255`
- `contabilizei-abertura` (73×): `.config.json:190`, `environments/_deprecated/config-dev.json:261`, `environments/_deprecated/config-local.json:261`
- `plataforma-central-rotinas` (51×): `.config.json:206`, `environments/_deprecated/config-dev.json:277`, `environments/_deprecated/config-local.json:277`
- `contato-service` (48×): `environments/_deprecated/config-dev.json:357`, `environments/_deprecated/config-local.json:355`, `environments/_deprecated/config-prod.json:357`
- `experts-service` (45×): `.config.json:244`, `environments/_deprecated/config-dev.json:315`, `environments/_deprecated/config-local.json:315`
- `zendesk-agents` (44×): `.config.json:268`, `environments/_deprecated/config-dev.json:349`, `environments/_deprecated/config-local.json:347`
- `bots-api` (40×): `.config.json:272`, `environments/_deprecated/config-dev.json:353`, `environments/_deprecated/config-local.json:351`
- `experts-nfs` (28×): `src/domain/bots/whatsapp/experts/fluxo-notafiscal/experts-fluxo-notafiscal-v4.controller.ts:17`, `src/domain/bots/whatsapp/experts/fluxo-notafiscal/nota-massiva/services/publicar-notas-massiva.service.ts:17`, `src/domain/bots/whatsapp/experts/fluxo-notafiscal/services/buscar-elegibilidade.service.ts:12`
- `fintech-payments` (21×): `.config.json:159`, `environments/_deprecated/config-dev.json:224`, `environments/_deprecated/config-local.json:224`
- `aida-back` (19×): `.config.json:254`, `environments/_deprecated/config-dev.json:331`, `environments/_deprecated/config-local.json:329`
- `experts-ms-nps` (14×): `.config.json:264`, `environments/_deprecated/config-dev.json:345`, `environments/_deprecated/config-local.json:343`
- `monitoria-ia` (14×): `environments/_deprecated/config-dev.json:213`, `environments/_deprecated/config-local.json:213`, `environments/_deprecated/config-prod.json:213`
- `ticketing-service` (12×): `.config.json:236`, `environments/_deprecated/config-dev.json:307`, `environments/_deprecated/config-local.json:307`
- `zendeskapp-concierge` (12×): `src/domain/zendeskapps/concierge/actions/zendeskapp-concierge-actions.controller.ts:5`, `src/domain/zendeskapps/concierge/actions/zendeskapp-concierge-actions.module.ts:1`, `src/domain/zendeskapps/concierge/consultor/zendeskapp-concierge-consultor.controller.ts:18`
- `atendimento-zendesk-cronjob` (7×): `src/app/worker/worker-desconexao-cliente-sem-interacao/schedule/controllers/desconexao-automatica.controller.ts:25`, `.context/tasks/prd-externalizar-configuracoes-env-vars/gap-analysis-env-dev.md:423`, `painel-assessor/agenda-origens.md:38`
- `emissor-whatsapp` (6×): `src/domain/bots/whatsapp/experts/fluxo-notafiscal/nota-massiva/services/publicar-notas-massiva.service.ts:27`, `src/domain/bots/whatsapp/experts/fluxo-notafiscal/services/enfileirar-nfs-elegivel.service.ts:22`, `src/domain/bots/whatsapp/experts/fluxo-notafiscal/nota-massiva/services/publicar-notas-massiva.service.spec.ts:46`
- `plataforma-importacao-notas-worker` (6×): `src/infra/clients/plataforma-notas-worker/notas-fiscais/notas-fiscais.service.ts:154`, `src/infra/clients/plataforma-notas-worker/tomadores/tomadores.service.ts:34`
- `meta-webhooks` (3×): `src/app/worker/worker-webhooks/meta-templates-worker/consumers/meta-templates.consumer.ts:18`, `src/app/worker/worker-webhooks/meta-templates-worker/consumers/meta-templates.consumer.spec.ts:42`
- `relacionamento-service` (2×): `src/domain/zendeskapps/hub-eficiencia/cliente/fontes-externas.ts:8`, `docs/hub-eficiencia/openapi.yaml:1375`
- `canais-adk` (2×): `src/domain/zendeskapps/concierge/consultor/zendeskapp-concierge-consultor.controller.ts:17`
- `microsservico-agrupamento-guias` (1×): `docs/hubspot/README.md:69`
- `zendeskapp-whatsapp-ativo` (1×): `src/domain/zendeskapps/zendeskapps.module.ts:4`
- Configuração, CI e documentação citadas: `experts-bruno`, `k8s-configmap`, `kong-config`, `vault-roleset`

### Repositórios que citam este

- `atendimento-canais-admin` (76×): `src/lib/validators/telefone-internacional.ts:4`, `src/routes/api/contatos/telefones-internacionais.$cnpj.tsx:2`, `src/routes/api/contatos/telefones-internacionais.tsx:2`
- `survey-service` (66×): `src/clients/atendimento-zendesk/atendimento-zendesk.client.ts:81`, `src/clients/index.ts:3`, `src/modules/channels/whatsapp/whatsapp-status.consumer.ts:9`
- `experts-service` (65×): `migrations/0055_backfill_csat_validade_e_status.sql:4`, `src/consumers/desconexao/update-error.consumer.ts:20`, `src/consumers/survey-csat/ativo-status/ativo-status.consumer.ts:18`
- `bots-api` (46×): `src/clients/atendimento-zendesk/atendimento-zendesk.ts:150`, `src/clients/atendimento-zendesk/dto/ativos-workflow.dto.ts:2`, `src/clients/atendimento-zendesk/dto/mensagem-ativa.dto.ts:2`
- `canais-adk` (22×): `src/application/hooks/notafiscal/oferta-renovacao-after-model.ts:40`, `src/application/tools/zendesk/get-average-resolution-time.tool.ts:3`, `src/infra/pubsub/pubsub.client.ts:34`
- `agrupamento-guias-service` (21×): `src/clients/whatsapp-ativo/dto/whatsapp-request.dto.ts:12`, `src/clients/whatsapp-ativo/whatsapp-ativo.publisher.ts:7`, `src/domain/callback/objects/callback.object.ts:13`
- `monitoria-ia` (19×): `src/executor/services/prompt/external-data-resolver.ts:2`, `src/executor/services/prompt/tools/get-ticket-tags.tool.ts:1`, `src/internal/infra/clients/atendimento-zendesk/index.ts:3`
- `microsservico-agrupamento-guias` (14×): `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/integrations/MetadadosGuiaFactory.kt:24`, `src/main/resources/application-dev.yml:67`, `src/main/resources/application-local.yml:56`
- `contabilizei-agents` (13×): `app/tools/zendesk/close_ticket.py:41`, `app/tools/zendesk/transfer_common.py:86`, `app/tools/zendesk/transfer_to_human/transfer_action.py:55`
- `plataforma-web` (11×): `src/main/java/br/com/contabilizei/plataforma/service/ZendeskService.kt:40`, `src/test/java/br/com/contabilizei/plataforma/atendimento/widget/jersey/FaleConoscoJerseyTest.kt:218`, `src/main/resources/filtered/parametro.desenv.properties:978`
- `plataforma-central-rotinas` (9×): `src/main/resources/filtered/parametro.desenv.properties:975`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:719`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:738`
- `atendimento-zendesk-cronjob` (8×): `atendimento-zendesk-cronjob-dev.yml:37`, `atendimento-zendesk-cronjob-prod.yml:37`, `readme.md:10`
- `experts-nfs` (8×): `src/modules/common/contabilizei/index.ts:9`, `src/modules/internal/emissor-whatsapp/services/emissor-whatsapp.service.ts:5`, `src/modules/internal/nota-recorrente/services/acknowledge.service.ts:3`
- `experts-bpmn` (6×): `PRD-88296/empresas.bpmn:7`, `PRD-88296/processos.bpmn:7`
- `sql2bq` (5×): `configs/prod/contabilizei-crm-relacionamento.json:3`, `configs/prod/ctbz-crm-atendimento-zendesk-diario.json:3`, `configs/prod/ctbz-crm-atendimento-zendesk-horario.json:3`
- `atendimento-api-gateway` (4×): `.env.example:39`, `config/kong-template-dev.yaml:95`, `config/kong-template-prod.yaml:146`
- `contabilizei-crm-webhooks` (4×): `configs/.env.dev:12`, `configs/.env.example:12`, `configs/.env.prod:12`
- `ultimate-as-a-code` (3×): `docs/flows/prd/mensagem-ativa.md:3`
- `zendesk-agents` (3×): `src/infra/google-cloud/pubsub/topics.ts:7`, `src/modules/messages/service/send-message-sunshine.service.spec.ts:34`
- `aida-back` (2×): `contabilizeiai/config/config.py:137`
- `experts-scripts` (2×): `batch-single-calls/clients/atendimento-zendesk_kong.js:8`
- `js-libraries` (2×): `packages/google-pubsub/src/crm/topics/atendimento-zendesk/envio-whatsapp-ativo.ts:61`, `packages/google-pubsub/src/crm/topics/index.ts:3`
- `sentinela-atendimento` (2×): `sentinela_atendimento/infra/config/config.py:76`
- `zendeskapp-concierge` (2×): `src/javascripts/modules/common/acoes/bulk-approve/loteResponseError.js:24`, `src/javascripts/services/dados-cliente.service.js:33`
- `experts-shell` (1×): `workspace/workspace.sh:44`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `dev-tools`, `experts-bruno`, `experts-drawio`, `experts-erd`, `experts-excalidraw`, `ide-bahcode`, `k8s-configmap`, `kong-config`, `pipeline`

### No grafo manual ([[grafo-chamadas-canais]])

- Consome: `zendesk-agents` (actions, chat do consultor)
- Consumido por: `zendeskapp-concierge` (BFF), `canais-adk`, `bots-api`, `experts-service` (Pub/Sub), `aida-back`

### Libs internas

- `@contabilizei-private/telemetry` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `atendimento-zendesk-agregador-conversa`, `atendimento-zendesk-atualizar-registro-ticket-formalizacao-sem-interacao`, `atendimento-zendesk-atualizar-ticket`, `atendimento-zendesk-chat-carregamento-dados-integracoes`, `atendimento-zendesk-classificacao-automatica-fechamento-tickets`, `atendimento-zendesk-criar-ticket`, `atendimento-zendesk-desconexao-atualizar-ticket-na-zendesk`, `atendimento-zendesk-desconexao-cliente-deseja-continuar`, `atendimento-zendesk-desconexao-cliente-nao-deseja-continuar`, `atendimento-zendesk-desconexao-criar-novo-ticket-atendimento`, `atendimento-zendesk-desconexao-envio-de-mensagem-na-conversa`, `atendimento-zendesk-desconexao-manual`, `atendimento-zendesk-desconexao-mensagem-cliente-desconectado`, `atendimento-zendesk-desconexao-reconectar-atendimento-no-mesmo-ticket`, `atendimento-zendesk-encerramento-atualizar-ticket-na-zendesk`, `atendimento-zendesk-encerramento-automatico-executar-ia`, `atendimento-zendesk-encerramento-enviar-para-em-espera`, `atendimento-zendesk-enviar-arquivo-ticket`, `atendimento-zendesk-enviar-mensagem-com-documento`, `atendimento-zendesk-enviar-mensagem-sunshine`, `atendimento-zendesk-full-conversation`, `atendimento-zendesk-notificar-cliente-desconexao`, `atendimento-zendesk-rotina-mensagem-cliente-em-fila`, `atendimento-zendesk-rotina-sincronizacao-agentes`, `atendimento-zendesk-rotina-sincronizacao-grupos`, `atendimento-zendesk-ticket-criado-atualizado-banco-de-dados`, `atendimento-zendesk-whatsapp-ativo-comentario-privado`, `atendimento-zendesk-whatsapp-carregamento-dados-integracoes`, `atendimento-zendesk-whatsapp-experts-carregar-integracoes`, `atendimento-zendesk.envio-whatsapp-ativo`, `atendimento-zendesk.erros.atualizar-ticket`, `atendimento-zendesk.experts.update-assessor-empresa-callback`, `atendimento-zendesk.experts.zendesk-job-pooler`, `atendimento-zendesk.p2p.att-ticket-status`, `atendimento-zendesk.whatsapp-ativo-status`, `bq-contabilizei-data-tb-tickets`, `classificacao-atendimento`, `dashboard-metricas-agentes-sync`, `dashboard-metricas-email-backfill`, `emissor-callback`, `experts.empresa`, `ingestor-streaming`, `jira-inativacao-empresa`, `jira-inativacao-empresa-consultas`, `nfs.non-elegible`, `notificacao-autenticacao-empresa-2fa`, `notificacao-empresa-2fa`, `pesquisa-nps-whatsapp`, `topic-name`, `zendesk-webhooks-capacidade-agentes`, `zendesk-webhooks-conversations`, `zendesk-webhooks-messages`, `zendesk-webhooks-notifications`, `zendesk-webhooks-pesquisa-satisfacao`, `zendesk-webhooks-retorno-desconexao-sem-interacao`, `zendesk-webhooks-users`, `zendeskapps-events-frontends`
- **Subscription**: `atendimento-zendesk.sub.att-ticket-status`
- **Fila Cloud Tasks**: `certificado-digital`, `emissor-whatsapp`, `emissor-whatsapp-massivo`, `feedback-hub`, `pesquisa-nps-whatsapp`
- **Cloud Run / function**: `bots-api`, `emissor-whatsapp`, `emissor-whatsapp-massivo`, `experts-nfs`

### Bancos e dados

- BigQuery: `@google-cloud/bigquery`
- Cloud Storage: `@google-cloud/storage`
- Cloud Tasks: `@google-cloud/tasks`
- Postgres: `pg`
- Postgres (Prisma): `@prisma/client`, `prisma`
- Pub/Sub: `@google-cloud/pubsub`
- Redis: `ioredis`
- Tabelas/datasets do BigQuery citados: `contabilizei-dataflow.dw_contabilizeiapp.empresa`, `contabilizei-dataflow.dw_contabilizeiapp.folhamensalempresa`, `contabilizei-dataflow:dw_contabilizeiapp.a`

### Terceiros

- Firebase: `firebase-admin`
- Google Gemini / Vertex AI: `aiplatform.googleapis.com` em `src/infra/vertex/internal/classificador-categoria-template-vertex.service.ts:74`
- HubSpot: `api.hubapi.com` em `docs/hubspot/README.md:22`
- Jira / Confluence: `contabilizei.atlassian.net` em `.context/tasks/prd-externalizar-configuracoes-env-vars/gap-analysis-env-dev.md:169`, `contabilizeicontabilidade.atlassian.net` em `.context/README.md:248`
- Meta (WhatsApp Cloud API / Graph): `graph.facebook.com` em `environments/_deprecated/config-dev.json:250`
- Mixpanel: `mixpanel`
- Zendesk: `accounts.zendesk.com` em `src/domain/webhooks/services/conversations/test/mock.ts:861`, `contabilizei.zendesk.com` em `environments/_deprecated/config-prod.json:228`, `contabilizei1637606740.zendesk.com` em `.config.json:163`

<!-- deps:auto:fim -->
