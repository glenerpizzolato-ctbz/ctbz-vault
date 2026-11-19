---
name: dependencias-atendimento-canais-admin
description: "Dependências do atendimento-canais-admin: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - atendimento-canais-admin
repositorio: atendimento-canais-admin
---

# Dependências do atendimento-canais-admin

O que o `atendimento-canais-admin` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

## Consome

### Repositórios internos

- `contato-service`: `POST /api/v1/optouts`, um por registro, na tela de contato — por `src/routes/api/proxy/contato-service.$.tsx` (proxy `/api/proxy/contato-service`), ver [[optout-tela-contato]]

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

Gerado em 2026-11-19 sobre `feat/email-template-inativar-listagem` @ `1309fedf` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `experts-nfs` (549×): `src/lib/collections/nfs.collection.ts:20`, `src/lib/collections/operator-nfs.collection.ts:9`, `src/lib/validators/foreign-postal.ts:4`
- `email-service` (198×): `src/routes/api/notificacoes/email-arquivos.tsx:12`, `src/routes/api/notificacoes/email-envios.list.tsx:10`, `src/routes/api/notificacoes/email-envios.tsx:17`
- `zendesk-agents` (159×): `src/lib/firebase/firebase.ts:31`, `src/lib/mastra/connection.ts:3`, `src/lib/utils.ts:87`
- `contato-service` (103×): `src/routeTree.gen.ts:125`, `src/routes/api/proxy/contato-service.$.tsx:2`, `src/routes/contatos/$id.tsx:30`
- `monitoria-ia` (89×): `src/env.ts:57`, `src/routes/monitoria/-SeletorAtendimento.tsx:14`, `src/routes/monitoria/-TabelaCriterios.tsx:32`
- `atendimento-zendesk` (76×): `src/lib/validators/telefone-internacional.ts:4`, `src/routes/api/contatos/telefones-internacionais.$cnpj.tsx:2`, `src/routes/api/contatos/telefones-internacionais.tsx:2`
- `bots-api` (62×): `src/routes/api/bots/flags.$cnpj.$flag.tsx:2`, `src/routes/api/bots/flags.$cnpj.tsx:3`, `src/routes/api/bots/flags.bulk.$flag.tsx:2`
- `survey-service` (52×): `src/routeTree.gen.ts:127`, `src/routes/admin/acessos/vocabulario.ts:154`, `src/routes/api/proxy/survey-service.$.tsx:2`
- `zendesk-proxy` (51×): `src/env.ts:37`, `src/lib/auth/access-config.ts:91`, `src/routeTree.gen.ts:129`
- `ticketing-service` (43×): `src/components/navigation/nav-config.ts:465`, `src/env.ts:50`, `src/lib/auth/access-config.ts:101`
- `canais-adk` (42×): `src/routes/bots/agents/-AnalyticsFerramentasSection.tsx:500`, `src/routes/bots/agents/-AnalyticsTrilhaSection.tsx:55`, `src/routes/bots/agents/-adkSession.ts:84`
- `aida-back` (1×): `src/server/domains/agents-ferramentas/agents-ferramentas.descricoes.ts:176`
- `microsservico-agrupamento-guias` (1×): `src/server/domains/controle-notificacao/controle-notificacao.status.ts:5`
- Configuração, CI e documentação citadas: `experts-bruno`

### Repositórios que citam este

- `monitoria-ia` (11×): `docs/bruno/web/avaliacao/get avaliacao by ticketid.bru:23`, `docs/validacao-ajuste-avaliacoes.md:15`
- `front-admin` (3×): `AGENTS.md:69`, `README.md:11`, `docs/DESIGN-SYSTEM.md:4`
- `canais-adk` (2×): `src/domain/feature-flags/test-session.ts:4`, `src/presentation/dev-ui/index.html:279`
- `survey-service` (1×): `docs/PLAN.md:352`
- `ticketing-service` (1×): `src/routes/sla-bff.router.ts:46`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `k8s-configmap`, `kong-config`

### No grafo manual ([[grafo-chamadas-canais]])

- Consome: `guardiao`, `experts-nfs`, `zendesk-agents`, `canais-adk`, `bots-api`

### Libs internas

- `@contabilizei-private/ds-tokens` (`package.json`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Fila Cloud Tasks**: `certificado-digital`, `notas-recorrentes`
- **Cloud Run / function**: `atendimento-canais-admin-dev`, `bots-api`, `experts-nfs`, `monitoria-ia-web`

### Bancos e dados

- BigQuery: `@google-cloud/bigquery`
- Firestore: `@google-cloud/firestore`
- Tabelas/datasets do BigQuery citados: `contabilizei-data.aida_prd_trusted.aida_ticket_classification`, `contabilizei-data.aida_prd_trusted.zendesk_controle_ticket`, `contabilizei-data.cloudsql_atendimento_canais_prd_atendimento_canais_canais_adk_trusted.events_atendimento_canais_prd`, `contabilizei-data.contabilizei_agents_raw.ctbz_agents_metrics`, `contabilizei-dataflow.dw_atendimento_zendesk.mensagem_ativa_flow`, `contabilizei-dataflow.dw_atendimento_zendesk.zendeskapps_events_frontend`, `contabilizei-dataflow.dw_contabilizeiapp.notafiscal`, `contabilizei-dataflow.dw_experts_nfs.nota_fiscal`, `contabilizei-dataflow.dw_experts_nfs.nota_fiscal_retencao`, `contabilizei-dataflow.dw_experts_service.survey_csat_response`, `contabilizei-dataflow.dw_experts_service.survey_csat_sent`, `contabilizei-dataflow.dw_ms_agrupamento_guias`, `contabilizei-dataflow.dw_ms_agrupamento_guias.controle_guias`, `contabilizei-dataflow.dw_ms_agrupamento_guias.controle_notificacao`, `contabilizei-dataflow.dw_ms_agrupamento_guias.diagnostico_aumento_imposto` …

### Terceiros

- Firebase: `firebase-admin`, `firebase`
- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/routes/bots/agents/-AnalyticsRecalculoDrill.test.tsx:653`, `ctbz.atlassian.net` em `src/server/clients/jira/jira.http.test.ts:5`, `x.atlassian.net` em `src/routes/sustentacao/scriptbooks/$id.test.tsx:121`
- Zendesk: `contabilizei.zendesk.com` em `README.md:88`

<!-- deps:auto:fim -->
