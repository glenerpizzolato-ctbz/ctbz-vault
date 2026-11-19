---
name: dependencias-front-admin
description: "Dependências do front-admin: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - front-admin
repositorio: front-admin
---

# Dependências do front-admin

O que o `front-admin` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `main` @ `ff6dd3e` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `back-email-service` (9×): `functions/api/backend/[[path]].ts:1`, `src/api/backEmail.ts:1`, `src/pages/SendingsPage.tsx:97`
- `atendimento-canais-admin` (3×): `AGENTS.md:69`, `README.md:11`, `docs/DESIGN-SYSTEM.md:4`
- Configuração, CI e documentação citadas: `gateway-kong`

### Repositórios que citam este

- `tarefas-assessor-admin` (4×): `package.json:19`, `packageExtended.json:5`, `src/App.vue:26`
- `front-tenteador` (1×): `README.md:17`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `gateway-kong`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
