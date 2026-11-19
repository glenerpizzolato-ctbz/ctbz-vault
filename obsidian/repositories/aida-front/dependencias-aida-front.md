---
name: dependencias-aida-front
description: "Dependências do aida-front: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - aida-front
repositorio: aida-front
---

# Dependências do aida-front

O que o `aida-front` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `feat/PRD-143338` @ `66ed34b` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `sentinela-atendimento` (4×): `.env.development:26`, `.env.production:27`, `.env.staging:22`

### Repositórios que citam este

- `sentinela-atendimento` (4×): `sentinela_atendimento/super_ouvidoria/repository/super_ouvidoria_repository.py:3`, `.context/_meta/key-decisions.md:342`, `.context/workflows/super-ouvidoria-flow.md:15`
- `aida-back` (1×): `docs/app-settings.md:153`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `pipeline`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Firebase: `firebase`
- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/page/supervisor/supervisor/components/RequestInfo.tsx:749`
- OpenAI: `api.openai.com` em `src/constants/auth.ts:1`
- Zendesk: `contabilizei.zendesk.com` em `.env.development:32`, `contabilizei1637606740.zendesk.com` em `.env.staging:29`

<!-- deps:auto:fim -->
