---
name: dependencias-ms-relatorio-faturamento
description: "Dependências do ms-relatorio-faturamento: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - ms-relatorio-faturamento
repositorio: ms-relatorio-faturamento
---

# Dependências do ms-relatorio-faturamento

O que o `ms-relatorio-faturamento` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `f381757` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `html-to-pdf` (5×): `src/domain/relatorio-financeiro/facade/index.ts:4`, `src/domain/relatorio-financeiro/facade/sign-relatorio/index.ts:6`, `src/infra/http-clients/index.ts:4`
- `experts-service` (1×): `README.md:3`

### Repositórios que citam este

- `plataforma-faturamento-worker` (2×): `src/main/java/br/com/contabilizei/faturamento/dto/relatoriofaturamento/RelatorioFaturamentoDTO.java:19`, `src/main/java/br/com/contabilizei/faturamento/jersey/MesContabilJersey.java:401`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `cnpj-alfanumerico`, `k8s-configmap`, `kong-config`, `pipeline`

### Libs internas

- `@contabilizei-private/fastify-healthz` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/fastify-instrumentation` (`package.json`) — publicada por `js-libraries`
- `@contabilizei-private/telemetry` (`package.json`) — publicada por `js-libraries`

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `experts.assessor`, `relatorio-faturamento.p2p.processing`, `test-topic`
- **Subscription**: `relatorio-faturamento.p2p.processing-sub`
- **Cloud Run / function**: `html-to-pdf`

### Bancos e dados

- BigQuery: `@google-cloud/bigquery`
- Cloud Storage: `@google-cloud/storage`
- Postgres: `pg`
- Pub/Sub: `@google-cloud/pubsub`
- SQL (query builder/ORM): `drizzle-orm`
- Secret Manager: `@google-cloud/secret-manager`

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
