---
name: dependencias-agrupamento-guias-service
description: "Dependências do agrupamento-guias-service: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - agrupamento-guias-service
repositorio: agrupamento-guias-service
---

# Dependências do agrupamento-guias-service

O que o `agrupamento-guias-service` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `feat/parcelas-metadados-whatsapp` @ `7510966` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `email-service` (43×): `src/clients/email-service/dto/send-email.dto.ts:1`, `src/clients/email-service/email-service.publisher.ts:7`, `src/clients/index.ts:3`
- `atendimento-zendesk` (21×): `src/clients/whatsapp-ativo/dto/whatsapp-request.dto.ts:12`, `src/clients/whatsapp-ativo/whatsapp-ativo.publisher.ts:7`, `src/domain/callback/objects/callback.object.ts:13`
- `contabilizei-guias` (4×): `.env.example:13`, `vitest.config.ts:14`, `src/infra/env/index.spec.ts:9`
- `experts-service` (4×): `src/domain/notifica/helpers/metadados-guia.helper.ts:58`, `AGENTS.md:197`, `README.md:54`
- `microsservico-agrupamento-guias` (4×): `src/model/enums.ts:10`, `src/shared/notificacao/constants/parcelamento.constants.ts:2`, `docs/bruno/notifica/bp-simples-wpp.bru:37`
- `contabilizei-back-core` (2×): `src/shared/notificacao/constants/parcelamento.constants.ts:2`, `README.md:42`
- `contato-service` (1×): `src/shared/notificacao/constants/notificacao.constants.ts:10`

### Repositórios que citam este

_Nenhum._

### Libs internas

- `@contabilizei-private/event-workers` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/pino-logger` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/telemetry` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/zezu-core` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

- Cloud Storage: `@google-cloud/storage`
- Postgres: `pg`
- Pub/Sub: `@google-cloud/pubsub`
- Redis: `ioredis`
- SQL (query builder/ORM): `drizzle-orm`

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
