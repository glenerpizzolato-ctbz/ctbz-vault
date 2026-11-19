---
name: dependencias-zendesk-proxy
description: "Dependências do zendesk-proxy: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - zendesk-proxy
repositorio: zendesk-proxy
---

# Dependências do zendesk-proxy

O que o `zendesk-proxy` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `7207c13` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `bots-api` (12×): `src/domain/identity/__fixture__/consumer.fixture.ts:6`, `src/domain/identity/consumer.dao.spec.ts:31`, `src/domain/identity/consumers.router.spec.ts:30`

### Repositórios que citam este

- `atendimento-canais-admin` (51×): `src/env.ts:37`, `src/lib/auth/access-config.ts:91`, `src/routeTree.gen.ts:129`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `pipeline`

### Libs internas

- `@contabilizei-private/pino-logger` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/simple-cache` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/telemetry` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/zezu-core` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

- Postgres: `pg`
- Redis: `ioredis`
- SQL (query builder/ORM): `drizzle-orm`

### Terceiros

- Zendesk: `a.zendesk.com` em `src/clients/upstream.client.spec.ts:17`, `contabilizei1637606740.zendesk.com` em `.env.example:12`, `z.zendesk.com` em `src/clients/oauth-client-credentials.spec.ts:7`

<!-- deps:auto:fim -->
