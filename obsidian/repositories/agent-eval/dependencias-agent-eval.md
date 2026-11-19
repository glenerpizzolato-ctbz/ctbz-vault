---
name: dependencias-agent-eval
description: "Dependências do agent-eval: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - agent-eval
repositorio: agent-eval
---

# Dependências do agent-eval

O que o `agent-eval` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `9bd4694` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `canais-adk` (8×): `deploy.sh:48`, `scripts/simulate-canais.ts:2`, `README.md:158`
- `contato-service` (1×): `docs/08-deployment.md:174`
- `email-service` (1×): `docs/08-deployment.md:174`
- Configuração, CI e documentação citadas: `vault-roleset`

### Repositórios que citam este

- `canais-adk` (54×): `.env.example:55`, `src/application/use-cases/automatic-sending-eval/automatic-sending-eval.use-case.ts:6`, `src/application/use-cases/automatic-sending-eval/judges/quality.judge.ts:1`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `pipeline`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

- Tabelas/datasets do BigQuery citados: `contabilizei-data.aida_prd_trusted.zendesk_ticket`, `contabilizei-dataflow.dw_experts_service.survey_csat_response`, `contabilizei-dataflow.dw_experts_service.survey_csat_sent`, `contabilizei-dataflow.dw_monitoria_ia`, `contabilizei-dataflow.dw_monitoria_ia.atendimento`, `contabilizei-dataflow.dw_monitoria_ia.prompt`, `contabilizei-dataflow.dw_monitoria_ia.prompt_request`, `contabilizei-dataflow.dw_monitoria_ia.prompt_response`, `contabilizei-dataflow.dw_monitoria_ia.subtema`, `contabilizei-dataflow.dw_monitoria_ia.tema`

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
