---
name: dependencias-canais-adk
description: "Dependências do canais-adk: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - canais-adk
repositorio: canais-adk
---

# Dependências do canais-adk

O que o `canais-adk` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `7075873` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `experts-nfs` (201×): `.env.example:21`, `src/application/agents/concierge-experts/certificado-digital/nf-contexto.ts:2`, `src/application/agents/concierge-experts/certificado-digital/status-pedido.ts:5`
- `zendesk-agents` (113×): `.env.example:94`, `src/application/agents/concierge-experts/certificado-digital/fila-expressa.ts:155`, `src/application/agents/concierge-experts/certificado-digital/lembrete-webview.ts:11`
- `aida-back` (102×): `.env.example:49`, `src/application/agents/attempt-timeout-llm.ts:106`, `src/application/agents/copilot/model.ts:10`
- `bots-api` (81×): `.env.example:35`, `src/application/agents/concierge-experts/certificado-digital/horario-fila-expressa.ts:2`, `src/application/agents/concierge-experts/index.ts:51`
- `agent-eval` (54×): `.env.example:55`, `src/application/use-cases/automatic-sending-eval/automatic-sending-eval.use-case.ts:6`, `src/application/use-cases/automatic-sending-eval/judges/quality.judge.ts:1`
- `experts-service` (28×): `.env.example:45`, `src/application/hooks/customer-summary/before-agent.ts:7`, `src/application/tools/experts-feedback/register-feedback.tool.ts:7`
- `canais-certificado-digital` (24×): `.env.example:23`, `src/application/agents/concierge-experts/certificado-digital/contexto-cd.ts:8`, `src/application/agents/concierge-experts/certificado-digital/contrato-cd.ts:2`
- `atendimento-zendesk` (22×): `src/application/hooks/notafiscal/oferta-renovacao-after-model.ts:40`, `src/application/tools/zendesk/get-average-resolution-time.tool.ts:3`, `src/infra/pubsub/pubsub.client.ts:34`
- `contabilizei-agents` (11×): `src/infra/metrics/otel.ts:3`, `src/infra/pubsub/pubsub.client.ts:28`, `src/application/agents/artifact-service.spec.ts:39`
- `emissor-whatsapp` (4×): `src/domain/empresa/empresa.types.ts:24`, `src/infra/clients/experts-nfs/experts-nfs.client.ts:39`, `src/infra/clients/experts-nfs/experts-nfs.client.spec.ts:207`
- `contabilizei-guias` (3×): `docs/concierge-experts.md:55`
- `experts-ms-nps` (2×): `.env.example:41`
- `atendimento-canais-admin` (2×): `src/domain/feature-flags/test-session.ts:4`, `src/presentation/dev-ui/index.html:279`
- `experts-alertas` (1×): `docs/concierge-experts.md:483`
- `aida-knowledge` (1×): `src/domain/knowledge-book/index.ts:23`
- Configuração, CI e documentação citadas: `k8s-configmap`

### Repositórios que citam este

- `canais-certificado-digital` (69×): `.env.cenario.example:15`, `.env.example:30`, `api/01 - Contexto do CD.bru:26`
- `zendesk-agents` (59×): `.env.example:29`, `src/modules/agents/whatsapp/agent/agent-envelope.ts:51`, `src/modules/contabilizei-agents/index.ts:3`
- `atendimento-canais-admin` (42×): `src/routes/bots/agents/-AnalyticsFerramentasSection.tsx:500`, `src/routes/bots/agents/-AnalyticsTrilhaSection.tsx:55`, `src/routes/bots/agents/-adkSession.ts:84`
- `agent-eval` (8×): `deploy.sh:48`, `scripts/simulate-canais.ts:2`, `README.md:158`
- `survey-service` (8×): `src/modules/nps/nps.router.ts:78`, `src/modules/nps/nps.router.spec.ts:46`, `docs/PLAN.md:182`
- `monitoria-ia` (3×): `src/internal/infra/knowledge-book/tools.ts:16`, `src/internal/infra/knowledge-book/types.ts:45`
- `atendimento-zendesk` (2×): `src/domain/zendeskapps/concierge/consultor/zendeskapp-concierge-consultor.controller.ts:17`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `ide-bahcode`, `k8s-configmap`, `kong-config`, `pipeline`

### No grafo manual ([[grafo-chamadas-canais]])

- Consome: `aida-back`, `experts-nfs`, `experts-service`, `bots-api`, `atendimento-zendesk`
- Consumido por: `atendimento-canais-admin`, `zendesk-agents`, `aida-back`

### Libs internas

- `@contabilizei-private/pino-logger` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/telemetry` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/zezu-core` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `atendimento-zendesk-atualizar-ticket`, `contabilizei-agents.bcast.metrics`
- **Fila Cloud Tasks**: `emissor-whatsapp`
- **Cloud Run / function**: `bots-api`, `canais-adk-dev`, `contabilizei-agents`, `emissor-whatsapp`, `experts-nfs`

### Bancos e dados

- Cloud Storage: `@google-cloud/storage`
- Firestore: `@google-cloud/firestore`
- Pub/Sub: `@google-cloud/pubsub`

### Terceiros

- Google Gemini / Vertex AI: `@google/genai`

<!-- deps:auto:fim -->
