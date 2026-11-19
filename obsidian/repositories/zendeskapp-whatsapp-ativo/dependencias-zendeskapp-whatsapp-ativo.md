---
name: dependencias-zendeskapp-whatsapp-ativo
description: "Dependências do zendeskapp-whatsapp-ativo: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - zendeskapp-whatsapp-ativo
repositorio: zendeskapp-whatsapp-ativo
---

# Dependências do zendeskapp-whatsapp-ativo

O que o `zendeskapp-whatsapp-ativo` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

## Consome

### Repositórios internos

- `contato-service`: `GET`/`POST /api/v1/contacts` e `PATCH /api/v1/contacts/:id`, pelo api-gateway — por `src/javascripts/services/contato-service/contato-service.client.ts`

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

Gerado em 2026-11-19 sobre `feat/PRD-163393` @ `cfce6f2` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contato-service` (25×): `src/javascripts/modules/WhatsappIndividual/ContatoSearch.tsx:5`, `src/javascripts/modules/WhatsappIndividual/CriarContato.tsx:5`, `src/javascripts/modules/WhatsappIndividual/contact-helpers.ts:7`

### Repositórios que citam este

- `atendimento-zendesk` (1×): `src/domain/zendeskapps/zendeskapps.module.ts:4`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-bruno`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/javascripts/modules/WhatsappConsulta/__tests__/WhatsappConsulta.spec.tsx:10`
- Zendesk: `assets.zendesk.com` em `webpack.config.js:10`, `developer.zendesk.com` em `README.md:8`

<!-- deps:auto:fim -->
