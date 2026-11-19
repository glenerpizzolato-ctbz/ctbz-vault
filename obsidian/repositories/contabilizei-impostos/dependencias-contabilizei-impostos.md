---
name: dependencias-contabilizei-impostos
description: "Dependências do contabilizei-impostos: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - contabilizei-impostos
repositorio: contabilizei-impostos
---

# Dependências do contabilizei-impostos

O que o `contabilizei-impostos` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `6236184e8` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-guias` (6×): `contabilizei-impostos-core/src/main/java/br/com/contabilizei/queue/enumeration/ImpostosModules.java:7`, `contabilizei-impostos-core/src/main/resources/environment/application-homol.properties:10`, `contabilizei-impostos-core/src/main/resources/environment/application-prod.properties:10`

### Repositórios que citam este

- `contabilizei-guias` (101×): `Makefile:6`, `bitbucket-pipelines.yml:164`, `contabilizei-guias-core/pom.xml:292`
- `plataforma-central-rotinas` (27×): `anotacoes.md:44`, `src/main/resources/filtered/parametro.desenv.properties:817`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:501`
- `plataforma-web` (25×): `src/main/resources/filtered/parametro.desenv.properties:819`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:506`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:522`
- `plataforma-fopag-worker` (24×): `src/main/resources/filtered/parametro.desenv.properties:40`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:180`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:81`
- `fintech-payments` (22×): `src/main/catalog-model/resources/fintech-payments-pubsub-subscriptions-resource.yaml:19`, `src/main/kotlin/br/com/contabilizei/fintech/app/recorrencia/component/AtualizarStatusGuiaClient.kt:11`, `src/test/kotlin/br/com/contabilizei/fintech/app/recorrencia/component/AtualizarStatusGuiaClientServiceTest.kt:28`
- `microsservico-agrupamento-guias` (20×): `src/main/catalog-model/resources/microsservico-agrupamento-guias-resource.yaml:5`, `src/main/resources/application-dev.yml:62`, `src/main/resources/application-prod.yml:67`
- `contabilizei-back-core` (19×): `src/main/java/br/com/contabilizei/imposto/dao/GuiaDAOBack.java:35`, `src/main/resources/filtered/parametro.desenv.properties:609`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:487`
- `plataforma-faturamento-worker` (19×): `src/main/java/admin/contabilizei/fiscal/view/CadastroIssFixoView.java:45`, `src/test/java/br/com/contabilizei/faturamento/utils/MessageTest.kt:15`, `src/main/resources/filtered/parametro.desenv.properties:586`
- `plataforma-crm-web` (18×): `src/test/java/br/com/contabilizei/crm/domain/atendimento/v2/apps/diagnosticocliente/impostos/facade/MemoriaCalculoFacadeTest.kt:34`, `src/main/resources/filtered/parametro.desenv.properties:11`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:9`
- `plataforma-back-worker` (16×): `src/main/resources/filtered/parametro.desenv.properties:609`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:486`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:504`
- `plataforma-importacao-notas-worker` (16×): `src/main/resources/filtered/parametro.desenv.properties:453`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:339`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:364`
- `plataforma-monolito` (16×): `src/main/resources/filtered/parametro.desenv.properties:609`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:487`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:505`
- `ctbz-acessos` (14×): `.config/projetos-e-roles.json:35`, `reports/lista_devsecops_roles_owner_all_projects.csv:53`
- `sql2bq` (7×): `configs/prod/impostos-codigos-tributarios.json:2`, `configs/prod/impostos-comprovantes-pagamento-federal.json:2`, `configs/prod/impostos-consulta-caixa-postal-ecac.json:2`
- `aida-back` (5×): `contabilizeiai/clients/fiscal/guias_client.py:13`, `contabilizeiai/clients/fiscal/impostos_client.py:12`, `tests/clients/test_impostos_client.py:19`
- `contabilizei-abertura` (3×): `contabilizei-abertura-core/src/main/resources/filtered/parametro.desenv.properties:252`, `contabilizei-abertura-core/src/main/resources/filtered/parametro.homolog.properties:257`, `contabilizei-abertura-core/src/main/resources/filtered/parametro.teste.properties:263`
- `contabilizei-abertura-BB` (3×): `contabilizei-abertura-core/src/main/resources/filtered/parametro.desenv.properties:250`, `contabilizei-abertura-core/src/main/resources/filtered/parametro.homolog.properties:256`, `contabilizei-abertura-core/src/main/resources/filtered/parametro.teste.properties:262`
- `contabilizei-front-admin` (2×): `src/sistema-admin/assets/js/endpoint_hom.js:16`
- `experts-scripts` (1×): `gcp/cloud-tasks/create-tasks/migr-templates-tw-to-zd/segundo-lote-templates.json:4213`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-bruno`, `k8s-configmap`, `pipeline`, `vault-roleset`

### Libs internas

- `br.com.contabilizei.jira:contabilizei-jira` (`contabilizei-impostos-core/pom.xml`)
- `br.com.contabilizei:contabil-eventos` (`contabilizei-impostos-core/pom.xml`)
- `br.com.contabilizei:contabilizei-impostos` (`pom.xml`)
- `br.com.contabilizei:contabilizei-impostos-core` (`contabilizei-impostos-web/pom.xml`)
- `br.com.contabilizei:contabilizei-issue-client` (`contabilizei-impostos-core/pom.xml`)
- `br.com.contabilizei:contabilizei-metadata` (`contabilizei-impostos-core/pom.xml`)
- `br.com.contabilizei:contabilizei-queue` (`contabilizei-impostos-core/pom.xml`)
- `br.com.contabilizei:contabilizei-sso-client` (`contabilizei-impostos-core/pom.xml`)
- `br.com.contabilizei:contabilizei-tarefa-paginada` (`contabilizei-impostos-core/pom.xml`)
- `br.com.contabilizei:contabilizei-testes` (`contabilizei-impostos-core/pom.xml`)
- `br.com.contabilizei:contabilizei-utils` (`contabilizei-impostos-core/pom.xml`)
- `br.com.contabilizei:feign-apis-back` (`contabilizei-impostos-core/pom.xml`)
- `br.com.contabilizei:feign-apis-guias` (`contabilizei-impostos-core/pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `calcula-impostos-nota-tomada`, `callback.plataforma`, `efetivar-perfil-fator-r`, `importar-guias-empresa`
- **Subscription**: `dados.processar-impostos-push`

### Bancos e dados

- Tabelas/datasets do BigQuery citados: `contabilizei-dataflow.dw_contabilizei_impostos.guia`, `contabilizei-dataflow.dw_contabilizei_impostos.impostopagar`, `contabilizei-dataflow.dw_contabilizeiapp.empresa`

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
