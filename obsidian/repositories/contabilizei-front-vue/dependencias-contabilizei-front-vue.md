---
name: dependencias-contabilizei-front-vue
description: "Dependências do contabilizei-front-vue: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - contabilizei-front-vue
repositorio: contabilizei-front-vue
---

# Dependências do contabilizei-front-vue

O que o `contabilizei-front-vue` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `feat/PRD-150576` @ `3584c1ebd` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-front` (31×): `.dependency-cruiser.js:191`, `.vscode/settings.json:10`, `catalog-info.yaml:4`
- `plataforma-web` (5×): `catalog-info.yaml:9`, `STACK.md:15`, `docs/components/contabilizei-front-vue.yaml:19`
- `contabilizei-guias` (1×): `src/modules/pagamentosFintech/constants/mocks.js:196`

### Repositórios que citam este

- `contabilizei-front` (2×): `CONTRIBUTING.md:100`, `README.md:3`
- `tarefas-assessor-admin` (2×): `src/storage/README.md:15`, `src/webApi/README.md:29`
- `experts-admin` (1×): `src/webApi/README.md:29`
- `experts-nfs` (1×): `src/modules/common/utils/texto-caracteres.utils.ts:2`
- `zendeskapp-concierge` (1×): `src/javascripts/lib/validacaoCaracteres.js:5`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `pipeline`

### Libs internas

- `@contabilizei-private/componentizei` (`package.json`)
- `@contabilizei-private/dot-foundations` (`package.json`)
- `@contabilizei-private/dot-webapps` (`package.json`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Fila Cloud Tasks**: `certificado-digital`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Datadog: `datadoghq.com` em `src/monitoring/monitoring.service.js:28`
- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `CONTRIBUTING.md:153`
- Mixpanel: `mixpanel-browser`
- Zendesk: `contabilizei.zendesk.com` em `src/modules/dashboard/v1/components/CardCalendarioRotinas/CardCalendarioRotinas.vue:13`, `contabilizei1566477659.zendesk.com` em `.env.dev:17`, `contabilizei1637606740.zendesk.com` em `src/modules/impostos/components/parcelamento-impostos/ModalContratacaoParcelamentoSucesso/ModalContratacaoParcelamentoSucesso.spec.js:20`

<!-- deps:auto:fim -->
