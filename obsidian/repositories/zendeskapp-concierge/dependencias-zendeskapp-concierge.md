---
name: dependencias-zendeskapp-concierge
description: "Dependências do zendeskapp-concierge: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - zendeskapp-concierge
repositorio: zendeskapp-concierge
---

# Dependências do zendeskapp-concierge

O que o `zendeskapp-concierge` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `579200a` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `experts-nfs` (39×): `src/javascripts/constants/currencies.js:3`, `src/javascripts/modules/common/acoes/Acoes.jsx:537`, `src/javascripts/modules/common/acoes/acao/detalhes/Detalhes.jsx:138`
- `zendesk-agents` (17×): `src/javascripts/contexts/session-emissor.js:4`, `src/javascripts/modules/common/acoes/acao/detalhes/Detalhes.jsx:139`, `src/javascripts/modules/common/acoes/actionErrorMessage.js:4`
- `atendimento-zendesk` (2×): `src/javascripts/modules/common/acoes/bulk-approve/loteResponseError.js:24`, `src/javascripts/services/dados-cliente.service.js:33`
- `contabilizei-front` (1×): `src/javascripts/lib/validacaoCaracteres.js:5`
- `contabilizei-front-vue` (1×): `src/javascripts/lib/validacaoCaracteres.js:5`
- `aida-back` (1×): `src/javascripts/view/app-container.jsx:21`

### Repositórios que citam este

- `atendimento-zendesk` (12×): `src/domain/zendeskapps/concierge/actions/zendeskapp-concierge-actions.controller.ts:5`, `src/domain/zendeskapps/concierge/actions/zendeskapp-concierge-actions.module.ts:1`, `src/domain/zendeskapps/concierge/consultor/zendeskapp-concierge-consultor.controller.ts:18`

### No grafo manual ([[grafo-chamadas-canais]])

- Consome: `atendimento-zendesk` (BFF)

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Firebase: `firebase`
- Zendesk: `assets.zendesk.com` em `src/templates/iframe.html:12`

<!-- deps:auto:fim -->
