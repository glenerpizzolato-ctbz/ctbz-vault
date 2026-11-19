---
name: dependencias-experts-alertas
description: "Dependências do experts-alertas: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - experts-alertas
repositorio: experts-alertas
---

# Dependências do experts-alertas

O que o `experts-alertas` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `01c39b3` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

_Nenhum._

### Repositórios que citam este

- `experts-twilio` (11×): `environments/.env-dev:45`, `environments/.env-local:41`, `environments/.env-prod:45`
- `experts-service` (2×): `src/infra/config/dev.ts:88`, `src/infra/config/prod.ts:90`
- `canais-adk` (1×): `docs/concierge-experts.md:483`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `cnpj-alfanumerico`, `experts-bruno`, `experts-drawio`, `pipeline`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Cloud Run / function**: `experts-alertas`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Google Chat: `chat.googleapis.com` em `src/internal/google-chat/google-chat.service.ts:9`

<!-- deps:auto:fim -->
