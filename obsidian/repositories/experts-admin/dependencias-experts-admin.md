---
name: dependencias-experts-admin
description: "Dependências do experts-admin: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - experts-admin
repositorio: experts-admin
---

# Dependências do experts-admin

O que o `experts-admin` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `3079b99` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `plataforma-web` (3×): `docs/components/experts-admin.yaml:20`, `docs/systems/plataforma-web.yaml:4`
- `bots-api` (3×): `src/modules/AvisosChatbot/interface/index.ts:4`, `src/webApi/index.js:10`, `src/modules/AvisosChatbot/tests/services/warningMessagesService.spec.ts:96`
- `contabilizei-front` (1×): `src/webApi/README.md:29`
- `contabilizei-front-vue` (1×): `src/webApi/README.md:29`

### Repositórios que citam este

- `bots-api` (3×): `src/domain/ultimateai/warning-messages/warning-messages.bff.ts:11`, `src/domain/ultimateai/warning-messages/warning-messages.module.ts:21`, `src/domain/ultimateai/warning-messages/warning-messages.bff.spec.ts:42`
- `survey-service` (1×): `docs/PLAN.md:462`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `cnpj-alfanumerico`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Cloud Run / function**: `bots-api`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
