---
name: dependencias-contabilizei-front-admin
description: "Dependências do contabilizei-front-admin: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - contabilizei-front-admin
repositorio: contabilizei-front-admin
---

# Dependências do contabilizei-front-admin

O que o `contabilizei-front-admin` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `1a0a186` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-pagamentos` (8×): `src/sistema-admin/assets/js/endpoint_hom.js:6`, `src/sistema-admin/assets/js/parametros_beta.js:24`, `src/sistema-admin/assets/js/parametros_desenvolvimento_1.js:24`
- `contabilizei-front` (6×): `.gitignore:11`, `bitbucket-pipelines.yml:25`, `package.json:2`
- `contabilizei-guias` (2×): `src/sistema-admin/assets/js/endpoint.js:73`, `src/sistema-admin/assets/js/endpoint_hom.js:18`
- `contabilizei-impostos` (2×): `src/sistema-admin/assets/js/endpoint_hom.js:16`
- `contabilizei-abertura` (2×): `src/sistema-admin/assets/js/endpoint_hom.js:24`, `src/sistema-admin/assets/js/endpoint_stg.js:26`

### Repositórios que citam este

- `tarefas-assessor-admin` (1×): `src/main.ts:7`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Fila Cloud Tasks**: `fechamento-exercicio`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Iugu: `api.iugu.com` em `src/sistema-admin/assets/js/bs3/iugu-v2.js:1`
- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `README.md:3`

<!-- deps:auto:fim -->
