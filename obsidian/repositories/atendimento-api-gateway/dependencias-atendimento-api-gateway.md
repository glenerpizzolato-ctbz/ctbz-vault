---
name: dependencias-atendimento-api-gateway
description: "Dependências do atendimento-api-gateway: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - atendimento-api-gateway
repositorio: atendimento-api-gateway
---

# Dependências do atendimento-api-gateway

O que o `atendimento-api-gateway` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `develop` @ `1b3027d` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `atendimento-zendesk` (4×): `.env.example:39`, `config/kong-template-dev.yaml:95`, `config/kong-template-prod.yaml:146`
- `emissor-whatsapp` (2×): `config/kong-template-dev.yaml:1510`, `config/kong-template-prod.yaml:1301`
- `plataforma-crm-web` (1×): `.env.example:17`
- `contabilizei-crm-webhooks` (1×): `.env.example:22`

### Repositórios que citam este

_Nenhum._
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-drawio`, `pipeline`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `atendimento-zendesk-atualizar-ticket`, `zendesk-webhooks-capacidade-agentes`, `zendesk-webhooks-conversations`, `zendesk-webhooks-events-tickets`, `zendesk-webhooks-messages`, `zendesk-webhooks-notifications`, `zendesk-webhooks-pesquisa-satisfacao`, `zendesk-webhooks-retorno-desconexao-sem-interacao`, `zendesk-webhooks-tickets`
- **Subscription**: `zendesk-webhooks-tickets`
- **Fila Cloud Tasks**: `emissor-whatsapp`
- **Cloud Run / function**: `atendimento-front`, `contabilizei-crm-webhooks`, `emissor-whatsapp`, `historico-atendimento`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
