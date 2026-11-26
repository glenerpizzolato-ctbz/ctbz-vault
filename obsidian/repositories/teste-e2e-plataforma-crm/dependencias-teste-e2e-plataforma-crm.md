---
name: dependencias-teste-e2e-plataforma-crm
description: "Dependências do teste-e2e-plataforma-crm: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - teste-e2e-plataforma-crm
repositorio: teste-e2e-plataforma-crm
---

# Dependências do teste-e2e-plataforma-crm

O que o `teste-e2e-plataforma-crm` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

## Consome

### Repositórios internos

- [[_contabilizei-crm-widget-window-indice|contabilizei-crm-widget-window]] — a UI do widget em `<baseUrl>/widget-window/#/helpdesk` (direto) e no iframe `iframe[data-testid="iframe-helpdesk"]` aberto pelo botão "Fale conosco" da home; seletores `data-testid` (`primary-btn`, `confirm-theme-button`, `confirm-subtheme-button`, `channel-btn`, `history-btn`, `attendance-button`, `tracked-link`, `title-ref`) e textos do bot nas fixtures `cypress/fixtures/messages/*.json`. Arquivos: `cypress/support/autoatendimento/{elements,actions}.js`
- BFF do widget (via app, interceptado com `cy.intercept`): `atendimento/widget/v2/temas`, `atendimento/widget/v2/roteamento/**` (confere `data.roteamento.tags`), `atendimento/widget/dados-empresa`, `atendimento/faleconosco/atendimentos-em-aberto` (+ `/incluir-comentario`), `atendimento/tickets/criar-ticket-formalizacao`. Arquivo: `cypress/support/autoatendimento/actions.js`
- [[_contabilizei-pagamentos-indice|contabilizei-pagamentos]] — `POST {urlBaseApiNewInvoice}/rest/carregar-dados/deleta-e-cria-fatura-pendente/{cnpj}` (`contabilizei-pagamentos-teste.appspot.com`) para recriar a fatura pendente no teste de segunda via. Arquivo: `cypress/support/autoatendimento/services.js`
- `plataforma-web` — login em `/painel-de-controle/#/home` e `GET **/plataforma/**/appbar/get` (pega os cookies para chamar o pagamentos); `helpers/warm-up-stg.js` aquece o stg antes da pipeline

### Libs internas

_Nada confirmado ainda._

### Infra GCP

- Template de CI `~/repositories/pipeline/templates/e2e-plataforma-crm/template.yml` (job `e2e-plataforma-crm-feat-autoatendimento`), habilitado pelas variáveis `E2E_PLATAFORMA_CRM` e `E2E_PLATAFORMA_CRM_FEAT_AUTOATENDIMENTO` no `pipeline/custom/...` de cada repo que o roda. Imagem `$DOCKER_HUB_NAMESPACE/teste-e2e-plataforma-crm:latest`, gerada pela pipeline deste repo

### Bancos e dados

_Nada confirmado ainda._

### Terceiros

- Zendesk sandbox `contabilizei1637606740.zendesk.com` — `POST /api/v2/tickets`, `PUT /api/v2/tickets/{id}` (fecha) e `GET /api/v2/search.json` (tickets abertos do requester), com token Basic em `env.token.zendesk` dos configs de ambiente. Arquivo: `cypress/support/autoatendimento/services.js`
- Currents (`cy.currents.dev`, projeto `DXFHsV`) — gravação das execuções da pipeline (`currents.config.js`, `cypress-cloud`)

## Consumido por

Quem consome os contratos deste repositório; a revisão de MRs confere se o diff quebra algum deles.

- Pipelines de `plataforma-web`, `contabilizei-front` e demais repos com `E2E_ENABLED` e `E2E_PLATAFORMA_CRM` ligados (ex.: `custom/ctbz.yml`, `experts.yml`): rodam a imagem deste repo no stage `post-staging`

<!-- deps:auto:inicio (gerado por mapear-dependencias; não editar à mão) -->

## Levantamento automático

Gerado em 2026-11-26 sobre `master` @ `ece483c` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-pagamentos` (2×): `cypress/environments/dev03.config.js:22`, `cypress/environments/stg.config.js:22`
- `plataforma-web` (2×): `helpers/warm-up-stg.js:6`

### Repositórios que citam este

_Nenhum._
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `pipeline`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Zendesk: `contabilizei1637606740.zendesk.com` em `cypress/environments/dev03.config.js:23`

<!-- deps:auto:fim -->
