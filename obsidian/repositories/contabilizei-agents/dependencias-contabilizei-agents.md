---
name: dependencias-contabilizei-agents
description: "Dependências do contabilizei-agents: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - contabilizei-agents
repositorio: contabilizei-agents
---

# Dependências do contabilizei-agents

O que o `contabilizei-agents` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `36f4173` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `mcp-notas-fiscais` (14×): `app/agents/before_tool.py:31`, `app/agents/mcp.py:9`, `app/agents/__tests__/before_tool_test.py:248`
- `atendimento-zendesk` (13×): `app/tools/zendesk/close_ticket.py:41`, `app/tools/zendesk/transfer_common.py:86`, `app/tools/zendesk/transfer_to_human/transfer_action.py:55`
- `bots-api` (3×): `app/utils/env.py:63`, `app/clients/__tests__/test_bots_api_client.py:53`
- `emissor-whatsapp` (2×): `app/clients/experts_nfs/__init__.py:17`, `app/clients/experts_nfs/__tests__/test_experts_nfs_client.py:31`
- `experts-nfs` (1×): `app/utils/env.py:69`
- `experts-service` (1×): `app/utils/env.py:74`

### Repositórios que citam este

- `zendesk-agents` (13×): `src/infra/google-cloud/pubsub/topics.ts:12`, `src/modules/agents/orchestration/usecase/agent-runner/base-agent-runner.strategy.ts:10`, `src/modules/ai-agent/metrics.service.ts:26`
- `canais-adk` (11×): `src/infra/metrics/otel.ts:3`, `src/infra/pubsub/pubsub.client.ts:28`, `src/application/agents/artifact-service.spec.ts:39`
- `mcp-notas-fiscais` (3×): `Makefile:29`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `cnpj-alfanumerico`, `k8s-configmap`, `kong-config`, `pipeline`

### No grafo manual ([[grafo-chamadas-canais]])

- Consome: `mcp-notas-fiscais`
- Consumido por: `zendesk-agents`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `atendimento-zendesk-atualizar-ticket`, `contabilizei-agents.bcast.metrics`, `contabilizei-agents.p2p.triagem_result`
- **Fila Cloud Tasks**: `emissor-whatsapp`
- **Cloud Run / function**: `bots-api`, `contabilizei-agents`, `emissor-whatsapp`

### Bancos e dados

- Firestore: `google-cloud-firestore`
- Postgres: `psycopg2-binary`
- Pub/Sub: `google-cloud-pubsub`

### Terceiros

- Google Gemini / Vertex AI: `google-cloud-aiplatform`
- LiteLLM (gateway de LLMs): `litellm`
- OpenAI: `openai`

<!-- deps:auto:fim -->
