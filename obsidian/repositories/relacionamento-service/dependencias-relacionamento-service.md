---
name: dependencias-relacionamento-service
description: "Dependências do relacionamento-service: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - relacionamento-service
repositorio: relacionamento-service
---

# Dependências do relacionamento-service

O que o `relacionamento-service` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `chore/fix-migration-jobb` @ `31b87c0` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

_Nenhum._
- Configuração, CI e documentação citadas: `k8s-configmap`

### Repositórios que citam este

- `atendimento-zendesk` (2×): `src/domain/zendeskapps/hub-eficiencia/cliente/fontes-externas.ts:8`, `docs/hub-eficiencia/openapi.yaml:1375`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `cnpj-alfanumerico`, `k8s-configmap`, `kong-config`

### Libs internas

- `@contabilizei-private/jira-api` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `relacionamento.jira-updater`, `relacionamento.jira-updater-v2`

### Bancos e dados

- Postgres (Prisma): `@prisma/client`, `prisma`
- Pub/Sub: `@google-cloud/pubsub`

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/infrastructure/config/dev.config.ts:16`

<!-- deps:auto:fim -->
