---
name: dependencias-aida-back
description: "Dependências do aida-back: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - aida-back
repositorio: aida-back
---

# Dependências do aida-back

O que o `aida-back` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `b06efdbae` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `experts-nfs` (23×): `contabilizeiai/clients/experts_nfs_client.py:8`, `contabilizeiai/functions/fiscal/notas/notas_fiscais_builder_v2.py:158`, `contabilizeiai/services/openai/prompting/handlers/nota_fiscal/fluxo_emissao_nota_fiscal_handler_v1.py:3`
- `plataforma-web` (9×): `contabilizeiai/functions/fiscal/notas/notas_fiscais_utils.py:90`, `contabilizeiai/utils/health_checker.py:24`, `tests/functions/fiscal/notas/test_notas_fiscais_utils.py:25`
- `contabilizei-impostos` (5×): `contabilizeiai/clients/fiscal/guias_client.py:13`, `contabilizeiai/clients/fiscal/impostos_client.py:12`, `tests/clients/test_impostos_client.py:19`
- `contabilizei-guias` (5×): `contabilizeiai/functions/fiscal/imposto/guias_functions.py:90`, `contabilizeiai/functions/fiscal/parcela/parcelamento_imposto_functions.py:90`, `tests/functions/fiscal/imposto/test_guias_functions.py:229`
- `contabilizei-abertura` (3×): `contabilizeiai/clients/abertura_client.py:7`, `contabilizeiai/services/certificado/documentos_certificado_service.py:295`, `contabilizeiai/services/certificado/entrevista_certisign_service.py:227`
- `saude-empresa-pendencias` (2×): `contabilizeiai/clients/fiscal/saude_empresa_client.py:5`
- `atendimento-zendesk` (2×): `contabilizeiai/config/config.py:137`
- `plataforma-central-rotinas` (1×): `contabilizeiai/clients/empresa_client.py:19`
- `aida-classifier` (1×): `contabilizeiai/config/config.py:86`
- `aida-front` (1×): `docs/app-settings.md:153`

### Repositórios que citam este

- `canais-adk` (102×): `.env.example:49`, `src/application/agents/attempt-timeout-llm.ts:106`, `src/application/agents/copilot/model.ts:10`
- `sentinela-atendimento` (55×): `sentinela_atendimento/infra/config/config.py:109`, `sentinela_atendimento/super_ouvidoria/api/dto/super_ouvidoria_dto.py:1`, `sentinela_atendimento/super_ouvidoria/repository/classificador_temas_repository.py:1`
- `atendimento-zendesk` (19×): `.config.json:254`, `environments/_deprecated/config-dev.json:331`, `environments/_deprecated/config-local.json:329`
- `experts-nfs` (17×): `prisma/schema.prisma:206`, `src/modules/common/contabilizei/aida-back/aida-back.facade.ts:11`, `src/modules/common/contabilizei/ctbz-http.client.ts:46`
- `aida-classifier` (13×): `.env.example:23`, `app/routers/aida_back.py:2`, `app/schemas/aida_back.py:54`
- `canais-certificado-digital` (10×): `src/certificado-digital/certificado/certificado.client.ts:24`, `src/certificado-digital/certificado/certificado.entity.ts:64`, `src/shared/sso/sso-signature.ts:17`
- `zendesk-agents` (6×): `src/infra/config/dev.ts:110`, `src/infra/config/prod.ts:111`, `src/infra/google-cloud/firestore/aida/ai-flag.dao.ts:3`
- `atendimento-canais-admin` (1×): `src/server/domains/agents-ferramentas/agents-ferramentas.descricoes.ts:176`
- `bots-api` (1×): `src/domain/zendesk/ativo-workflow/usecases/handle-answer.usecase.ts:108`
- `zendeskapp-concierge` (1×): `src/javascripts/view/app-container.jsx:21`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-bruno`, `ide-bahcode`, `k8s-configmap`, `kong-config`, `pipeline`

### No grafo manual ([[grafo-chamadas-canais]])

- Consome: `bots-api`, `canais-adk`, `experts-nfs`, `atendimento-zendesk`, `knowledge-book-agent`
- Consumido por: `zendesk-agents`, `canais-adk`, `experts-nfs`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `aida-ticket-tema`, `atendimento-zendesk-atualizar-ticket`, `atendimento-zendesk-enviar-mensagem-sunshine`, `dl-zendesk-webhooks-tickets`, `test-topic`
- **Subscription**: `dl-zendesk-webhooks-tickets`
- **Fila Cloud Tasks**: `aida-analise-mensagem-travada`, `aida-analise-transferencia`, `aida-autopilot`, `aida-autopilot-new-message`, `aida-classifier`, `aida-controle-ticket`, `aida-despedida`, `aida-encerramento`, `aida-extratos`, `aida-funcoes-agendadas`, `aida-jobs-default`, `aida-message-separator`, `aida-nf-emissao`, `aida-nf-emissao-callback`, `aida-processamento-msg`, `aida-queue`, `aida-router-fila`, `aida-score`, `aida-simulador`, `aida-tag`, `aida-temperature`, `aida-transference`, `aida-update-ticket`, `aida-ura-inteligente`, `certificado-digital`
- **Cloud Run / function**: `arquivos-fator-r`, `experts-nfs`, `find_situacao_voucher`

### Bancos e dados

- BigQuery: `google-cloud-bigquery`
- Cloud Storage: `google-cloud-storage`
- Cloud Tasks: `google-cloud-tasks`
- Datastore: `google-cloud-datastore`
- Firestore: `google-cloud-firestore`
- Pub/Sub: `google-cloud-pubsub`
- Redis: `redis`
- SQL (SQLAlchemy): `SQLAlchemy`
- Tabelas/datasets do BigQuery citados: `contabilizei-data.aida_prd_raw.zendesk_ticket_raw`, `contabilizei-data.aida_prd_trusted.ai_flag`, `contabilizei-data.aida_prd_trusted.aida_ticket_classification`, `contabilizei-data.aida_prd_trusted.concierge_classify`, `contabilizei-data.aida_prd_trusted.concierge_requests`, `contabilizei-data.aida_prd_trusted.response_score_view`, `contabilizei-data.aida_prd_trusted.zendesk_controle_ticket`, `contabilizei-dataflow.cloudsql_banking_kyc_orchestrator.processo_kyc`, `contabilizei-dataflow.cloudsql_fintech_collections.empresa`, `contabilizei-dataflow.cloudsql_fintech_collections.endereco`, `contabilizei-dataflow.dw_aida_comunicados.comunicado_creasp`, `contabilizei-dataflow.dw_aida_comunicados.comunicado_diferenca_ata`, `contabilizei-dataflow.dw_aida_comunicados.comunicado_dimob`, `contabilizei-dataflow.dw_aida_comunicados.comunicado_irregular_desenquadrado`, `contabilizei-dataflow.dw_aida_comunicados.comunicado_tributacao` …

### Terceiros

- Anthropic (Claude): `anthropic`
- Firebase: `firebase-admin`
- Google Gemini / Vertex AI: `google-cloud-aiplatform`, `google-genai`
- Google Workspace APIs: `google-api-python-client`
- HubSpot: `api.hubapi.com` em `contabilizeiai/clients/hubspot/hubspot_client.py:13`
- Jira: `jira`
- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `README.md:227`
- LiteLLM (gateway de LLMs): `litellm`
- OpenAI: `openai`
- Sentry: `sentry-sdk`
- Zendesk: `contabilizei.zendesk.com` em `contabilizeiai/functions/jira/serfin/fields/jira_serfin_fields.py:25`

<!-- deps:auto:fim -->
