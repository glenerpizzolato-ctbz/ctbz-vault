---
name: dependencias-saude-empresa-pendencias
description: "Dependências do saude-empresa-pendencias: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - saude-empresa-pendencias
repositorio: saude-empresa-pendencias
---

# Dependências do saude-empresa-pendencias

O que o `saude-empresa-pendencias` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `a44001f` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-guias` (4×): `src/main/resources/application-dev.properties:13`, `src/main/resources/application-local.properties:12`, `src/main/resources/application-prod.properties:20`

### Repositórios que citam este

- `plataforma-web` (9×): `src/main/resources/filtered/parametro.desenv.properties:1039`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:794`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:802`
- `plataforma-central-rotinas` (8×): `src/main/resources/filtered/parametro.desenv.properties:1035`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:795`, `src/main/resources/filtered/parametro.desenvolvimento-3.properties:857`
- `contabilizei-guias` (4×): `contabilizei-guias-core/src/main/resources/environment/application-dev.properties:123`, `contabilizei-guias-core/src/main/resources/environment/application-hom-reg.properties:110`, `contabilizei-guias-core/src/main/resources/environment/application-homol.properties:116`
- `aida-back` (2×): `contabilizeiai/clients/fiscal/saude_empresa_client.py:5`
- `sql2bq` (2×): `configs/prod/saude-empresa-pendencias.json:5`, `cronjobs/params-prd.yaml:199`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `pipeline`

### Libs internas

- `br.com.contabilizei:saude-empresa-pendencias` (`pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/main/resources/application-prod.properties:10`

<!-- deps:auto:fim -->
