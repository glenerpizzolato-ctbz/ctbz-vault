---
name: dependencias-contabilizei-front
description: "Dependências do contabilizei-front: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - contabilizei-front
repositorio: contabilizei-front
---

# Dependências do contabilizei-front

O que o `contabilizei-front` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `develop` @ `22a6d830b2` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-front-vue` (2×): `CONTRIBUTING.md:100`, `README.md:3`

### Repositórios que citam este

- `contabilizei-front-vue` (31×): `.dependency-cruiser.js:191`, `.vscode/settings.json:10`, `catalog-info.yaml:4`
- `contabilizei-front-admin` (6×): `.gitignore:11`, `bitbucket-pipelines.yml:25`, `package.json:2`
- `tarefas-assessor-admin` (3×): `src/main.ts:7`, `src/storage/README.md:15`, `src/webApi/README.md:29`
- `experts-admin` (1×): `src/webApi/README.md:29`
- `experts-nfs` (1×): `src/modules/common/utils/texto-caracteres.utils.ts:2`
- `zendeskapp-concierge` (1×): `src/javascripts/lib/validacaoCaracteres.js:5`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `local-dev`, `pipeline`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Fila Cloud Tasks**: `certificado-digital`, `fechamento-exercicio`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Iugu: `api.iugu.com` em `src/main/webapp/main/assets/js/bs3/iugu-v2.js:1`
- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `CONTRIBUTING.md:94`
- Zendesk: `contabilizei.zendesk.com` em `src/main/webapp/main/sistema/app/src/controllers/dashboardController.js:252`, `contabilizei1566477659.zendesk.com` em `src/main/webapp/main/sistema/js/constants/zendesk/formularios-zendesk.js:3`

<!-- deps:auto:fim -->
