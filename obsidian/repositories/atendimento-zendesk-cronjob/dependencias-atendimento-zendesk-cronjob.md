---
name: dependencias-atendimento-zendesk-cronjob
description: "Dependências do atendimento-zendesk-cronjob: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - atendimento-zendesk-cronjob
repositorio: atendimento-zendesk-cronjob
---

# Dependências do atendimento-zendesk-cronjob

O que o `atendimento-zendesk-cronjob` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `feat-segundo-transf-corujao` @ `8e6eed0` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `atendimento-zendesk` (8×): `atendimento-zendesk-cronjob-dev.yml:37`, `atendimento-zendesk-cronjob-prod.yml:37`, `readme.md:10`

### Repositórios que citam este

- `atendimento-zendesk` (7×): `src/app/worker/worker-desconexao-cliente-sem-interacao/schedule/controllers/desconexao-automatica.controller.ts:25`, `.context/tasks/prd-externalizar-configuracoes-env-vars/gap-analysis-env-dev.md:423`, `painel-assessor/agenda-origens.md:38`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-drawio`, `k8s-configmap`, `pipeline`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
