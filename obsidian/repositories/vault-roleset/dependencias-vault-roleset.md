---
name: dependencias-vault-roleset
description: "Dependências do vault-roleset: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - vault-roleset
repositorio: vault-roleset
---

# Dependências do vault-roleset

O que o `vault-roleset` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `feat/PRD-170317` @ `42f07463` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-impostos` (238×): `gcp-roleset-bb_pipelines/atendimento-canais-dev/pipeline-kubernetes.hcl:58`, `gcp-roleset-bb_pipelines/atendimento-canais-prd/pipeline-kubernetes.hcl:63`, `gcp-roleset-bb_pipelines/contabilizei-impostos-hom/pipeline-appengine.hcl:1`
- `contabilizei-abertura` (150×): `gcp-roleset-bb_pipelines/contabilizei-abertura-func-tes/pipeline-cloudrun.hcl:1`, `gcp-roleset-bb_pipelines/contabilizei-abertura-func-tes/pipeline-function.hcl:1`, `gcp-roleset-bb_pipelines/contabilizei-abertura-func/pipeline-cloudrun.hcl:1`
- `contabilizei-pagamentos` (84×): `gcp-roleset-bb_pipelines/contabilizei-data/pipeline-scriptautomation.hcl:61`, `gcp-roleset-bb_pipelines/contabilizei-pagamentos-dev/pipeline-appengine.hcl:1`, `gcp-roleset-bb_pipelines/contabilizei-pagamentos-dev/pipeline-cloudrun.hcl:1`

### Repositórios que citam este

- `survey-service` (25×): `terraform/dev/pubsub.tf:25`, `terraform/prd/pubsub.tf:25`, `.claude/skills/add-channel/SKILL.md:20`
- `ctbz-cli` (9×): `src/commands/sa.ts:19`
- `agent-eval` (2×): `deploy.sh:156`, `docs/08-deployment.md:316`
- `atendimento-zendesk` (2×): `.context/tasks/prd-externalizar-configuracoes-env-vars/gap-analysis-env-dev.md:463`, `README.md:301`
- `canais-certificado-digital` (2×): `README.md:647`
- `email-service` (2×): `terraform/dev/pubsub.dlq.tf:5`, `terraform/prd/pubsub.dlq.tf:5`
- `meta-webhooks` (2×): `.claude/skills/add-domain/SKILL.md:18`, `README.md:66`
- `monitoria-ia` (1×): `docs/validacao-ajuste-avaliacoes.md:361`
- `zendesk-agents` (1×): `.env.example:33`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `ide-bahcode`, `k8s-configmap`, `pipeline`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

- Tabelas/datasets do BigQuery citados: `contabilizei-data.appspot.com`

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `create_secret_value.sh:4`

<!-- deps:auto:fim -->
