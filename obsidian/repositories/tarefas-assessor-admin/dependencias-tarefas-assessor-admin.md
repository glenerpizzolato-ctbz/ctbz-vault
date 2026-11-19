---
name: dependencias-tarefas-assessor-admin
description: "Dependências do tarefas-assessor-admin: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - tarefas-assessor-admin
repositorio: tarefas-assessor-admin
---

# Dependências do tarefas-assessor-admin

O que o `tarefas-assessor-admin` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `63da22b` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `plataforma-web` (4×): `catalog-info.yaml:9`, `docs/components/admin-front-vue.yaml:21`, `docs/systems/plataforma-web.yaml:4`
- `front-admin` (4×): `package.json:19`, `packageExtended.json:5`, `src/App.vue:26`
- `contabilizei-front` (3×): `src/main.ts:7`, `src/storage/README.md:15`, `src/webApi/README.md:29`
- `contabilizei-front-vue` (2×): `src/storage/README.md:15`, `src/webApi/README.md:29`
- `contabilizei-front-admin` (1×): `src/main.ts:7`

### Repositórios que citam este

_Nenhum._
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `cnpj-alfanumerico`

### Libs internas

- `@contabilizei-private/front-admin-utils` (`package.json`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
