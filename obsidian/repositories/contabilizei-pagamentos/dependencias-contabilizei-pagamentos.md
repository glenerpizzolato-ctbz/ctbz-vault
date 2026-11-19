---
name: dependencias-contabilizei-pagamentos
description: "Dependências do contabilizei-pagamentos: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - contabilizei-pagamentos
repositorio: contabilizei-pagamentos
---

# Dependências do contabilizei-pagamentos

O que o `contabilizei-pagamentos` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `982e83c7a` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-abertura` (5×): `contabilizei-pagamentos-core/src/main/resources/parametro.desenv.properties:3`, `contabilizei-pagamentos-core/src/main/resources/parametro.desenv3.properties:3`, `contabilizei-pagamentos-core/src/main/resources/parametro.homolog-reg.properties:3`

### Repositórios que citam este

- `ctbz-acessos` (11×): `.config/projetos-e-roles.json:47`, `reports/lista_devsecops_roles_owner_all_projects.csv:37`
- `contabilizei-back-core` (8×): `src/main/resources/filtered/parametro.desenv.properties:11`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:17`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:17`
- `contabilizei-front-admin` (8×): `src/sistema-admin/assets/js/endpoint_hom.js:6`, `src/sistema-admin/assets/js/parametros_beta.js:24`, `src/sistema-admin/assets/js/parametros_desenvolvimento_1.js:24`
- `plataforma-central-rotinas` (8×): `src/main/resources/filtered/parametro.desenv.properties:11`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:20`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:20`
- `plataforma-web` (8×): `src/main/resources/filtered/parametro.desenv.properties:13`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:22`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:22`
- `contabilizei-movimentacao-back` (7×): `src/main/kotlin/br/com/contabilizei/movimentacao/domain/sustentacao/SustentacaoService.kt:74`, `src/main/kotlin/br/com/contabilizei/movimentacao/infra/resteasy/RestEasyClientConfig.kt:74`, `src/main/resources/application.properties:84`
- `plataforma-back-worker` (7×): `src/main/resources/filtered/parametro.desenv.properties:11`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:17`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:17`
- `plataforma-crm-web` (7×): `src/main/resources/filtered/parametro.desenv.properties:6`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:12`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:12`
- `plataforma-faturamento-worker` (7×): `src/main/resources/filtered/parametro.desenv.properties:9`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:15`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:15`
- `plataforma-fopag-worker` (7×): `src/main/resources/filtered/parametro.desenv.properties:5`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:13`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:14`
- `plataforma-importacao-notas-worker` (7×): `src/main/resources/filtered/parametro.desenv.properties:10`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:15`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:15`
- `plataforma-monolito` (7×): `src/main/resources/filtered/parametro.desenv.properties:11`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:18`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:18`
- `fintech-payments` (6×): `src/main/kotlin/br/com/contabilizei/fintech/app/task/service/FaturaDebitoAutomaticoCloudTaskService.kt:23`, `src/main/resources/application-stg.yml:43`, `src/main/resources/application.yml:123`
- `sql2bq` (5×): `configs/prod/contabilizei-ms-gateway-adyen-diario.json:2`, `configs/prod/contabilizei-ms-gestao-pagamentos-diario.json:2`, `configs/prod/contabilizei-pagamentos-cupom-diario.json:2`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `k8s-configmap`, `kong-config`, `pipeline`, `vault-roleset`

### Libs internas

- `br.com.contabilizei:audit-client` (`contabilizei-pagamentos-core/pom.xml`)
- `br.com.contabilizei:contabil-eventos` (`contabilizei-pagamentos-core/pom.xml`)
- `br.com.contabilizei:contabilizei-api-contabil` (`contabilizei-pagamentos-core/pom.xml`)
- `br.com.contabilizei:contabilizei-configcat` (`contabilizei-pagamentos-core/pom.xml`)
- `br.com.contabilizei:contabilizei-data-streaming` (`contabilizei-pagamentos-core/pom.xml`)
- `br.com.contabilizei:contabilizei-datastore` (`contabilizei-pagamentos-core/pom.xml`)
- `br.com.contabilizei:contabilizei-metadados` (`contabilizei-pagamentos-core/pom.xml`)
- `br.com.contabilizei:contabilizei-pagamentos` (`contabilizei-pagamentos-barramento/pom.xml`)
- `br.com.contabilizei:contabilizei-pagamentos-barramento` (`contabilizei-pagamentos-report/pom.xml`)
- `br.com.contabilizei:contabilizei-pagamentos-commons` (`pom.xml`)
- `br.com.contabilizei:contabilizei-pagamentos-core` (`contabilizei-pagamentos-barramento/pom.xml`)
- `br.com.contabilizei:contabilizei-pagamentos-test` (`contabilizei-pagamentos-barramento/pom.xml`)
- `br.com.contabilizei:contabilizei-pagamentos-web` (`contabilizei-pagamentos-report/pom.xml`)
- `br.com.contabilizei:contabilizei-sso-client` (`contabilizei-pagamentos-core/pom.xml`)
- `br.com.contabilizei:contabilizei-utils` (`contabilizei-pagamentos-core/pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `processar-faturas`
- **Fila Cloud Tasks**: `audit-queue`, `push-notification`

### Bancos e dados

- Tabelas/datasets do BigQuery citados: `contabilizei-dataflow:dw_contabilizei_pagamentos.mensagememail`, `contabilizei-dataflow:dw_contabilizei_pagamentos.mensagemsms`, `contabilizei-dataflow:dw_contabilizeiapp.notafiscal`

### Terceiros

- Google Chat: `chat.googleapis.com` em `contabilizei-pagamentos-core/src/main/resources/parametro.properties:80`
- Iugu: `api.iugu.com` em `contabilizei-pagamentos-core/src/main/resources/parametro.properties:33`
- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `contabilizei-pagamentos-core/src/main/java/br/com/contabilizei/domain/cobranca/CobrancaService.java:14`

<!-- deps:auto:fim -->
