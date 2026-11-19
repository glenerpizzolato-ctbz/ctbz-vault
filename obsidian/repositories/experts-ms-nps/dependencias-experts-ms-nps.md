---
name: dependencias-experts-ms-nps
description: "Dependências do experts-ms-nps: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - experts-ms-nps
repositorio: experts-ms-nps
---

# Dependências do experts-ms-nps

O que o `experts-ms-nps` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `a9fd4d7` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

_Nenhum._

### Repositórios que citam este

- `atendimento-zendesk` (14×): `.config.json:264`, `environments/_deprecated/config-dev.json:345`, `environments/_deprecated/config-local.json:343`
- `survey-service` (11×): `AGENTS.md:3`, `README.md:3`, `docs/PLAN.md:7`
- `canais-adk` (2×): `.env.example:41`
- `ctbz-cli` (2×): `src/commands/recurso.ts:112`, `src/commands/sa.ts:76`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `cnpj-alfanumerico`, `ide-bahcode`, `k8s-configmap`, `kong-config`

### Libs internas

- `@contabilizei-private/fastify-healthz` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/fastify-instrumentation` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/telemetry` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `experts.assessor`, `nps.p2p.save`, `test-topic`
- **Subscription**: `plataforma.save-nps-sub`

### Bancos e dados

- Postgres: `pg`
- Pub/Sub: `@google-cloud/pubsub`
- SQL (query builder/ORM): `drizzle-orm`

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
