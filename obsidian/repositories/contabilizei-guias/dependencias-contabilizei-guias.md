---
name: dependencias-contabilizei-guias
description: "Dependências do contabilizei-guias: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - contabilizei-guias
repositorio: contabilizei-guias
---

# Dependências do contabilizei-guias

O que o `contabilizei-guias` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `develop` @ `a90a848e1` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-impostos` (101×): `Makefile:6`, `bitbucket-pipelines.yml:164`, `contabilizei-guias-core/pom.xml:292`
- `saude-empresa-pendencias` (4×): `contabilizei-guias-core/src/main/resources/environment/application-dev.properties:123`, `contabilizei-guias-core/src/main/resources/environment/application-hom-reg.properties:110`, `contabilizei-guias-core/src/main/resources/environment/application-homol.properties:116`

### Repositórios que citam este

- `plataforma-faturamento-worker` (44×): `src/main/java/admin/contabilizei/fiscal/view/ParcelamentoEmpresaView.java:32`, `src/main/java/admin/contabilizei/fiscal/view/ParcelamentoGuiaView.java:26`, `src/main/resources/filtered/parametro.desenv.properties:248`
- `contabilizei-back-core` (38×): `src/main/java/br/com/contabilizei/imposto/dto/ImpostoUploadArquivoManual.java:99`, `src/main/java/br/com/contabilizei/imposto/paginacao/processor/DisponibilizarGuiasProcessor.java:86`, `src/main/java/br/com/contabilizei/imposto/paginacao/processor/LiberarGuiasProcessor.java:101`
- `plataforma-central-rotinas` (37×): `anotacoes.md:26`, `src/main/resources/filtered/parametro.desenv.properties:404`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:317`
- `plataforma-web` (35×): `src/main/resources/filtered/parametro.desenv.properties:406`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:321`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:345`
- `plataforma-back-worker` (33×): `src/main/resources/filtered/parametro.desenv.properties:393`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:302`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:328`
- `plataforma-importacao-notas-worker` (33×): `src/main/resources/filtered/parametro.desenv.properties:257`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:184`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:212`
- `plataforma-monolito` (33×): `src/main/resources/filtered/parametro.desenv.properties:393`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:302`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:328`
- `microsservico-agrupamento-guias` (28×): `src/main/resources/application-dev.yml:74`, `src/main/resources/application-local.yml:85`, `src/main/resources/application-prod.yml:80`
- `plataforma-fopag-worker` (12×): `src/main/resources/filtered/parametro.desenvolvimento-1.properties:186`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:192`, `src/main/resources/filtered/parametro.desenvolvimento-3.properties:180`
- `plataforma-crm-web` (7×): `src/main/resources/filtered/parametro.desenvolvimento-1.properties:88`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:93`, `src/main/resources/filtered/parametro.desenvolvimento-3.properties:10`
- `contabilizei-impostos` (6×): `contabilizei-impostos-core/src/main/java/br/com/contabilizei/queue/enumeration/ImpostosModules.java:7`, `contabilizei-impostos-core/src/main/resources/environment/application-homol.properties:10`, `contabilizei-impostos-core/src/main/resources/environment/application-prod.properties:10`
- `aida-back` (5×): `contabilizeiai/functions/fiscal/imposto/guias_functions.py:90`, `contabilizeiai/functions/fiscal/parcela/parcelamento_imposto_functions.py:90`, `tests/functions/fiscal/imposto/test_guias_functions.py:229`
- `contabilizei-abertura` (5×): `contabilizei-abertura-core/src/main/resources/filtered/parametro.desenv.properties:257`, `contabilizei-abertura-core/src/main/resources/filtered/parametro.homolog.properties:262`, `contabilizei-abertura-core/src/main/resources/filtered/parametro.prod.properties:270`
- `contabilizei-abertura-BB` (5×): `contabilizei-abertura-core/src/main/resources/filtered/parametro.desenv.properties:255`, `contabilizei-abertura-core/src/main/resources/filtered/parametro.homolog.properties:261`, `contabilizei-abertura-core/src/main/resources/filtered/parametro.prod.properties:269`
- `agrupamento-guias-service` (4×): `.env.example:13`, `vitest.config.ts:14`, `src/infra/env/index.spec.ts:9`
- `saude-empresa-pendencias` (4×): `src/main/resources/application-dev.properties:13`, `src/main/resources/application-local.properties:12`, `src/main/resources/application-prod.properties:20`
- `canais-adk` (3×): `docs/concierge-experts.md:55`
- `contabilizei-front-admin` (2×): `src/sistema-admin/assets/js/endpoint.js:73`, `src/sistema-admin/assets/js/endpoint_hom.js:18`
- `experts-scripts` (2×): `gcp/cloud-tasks/create-tasks/migr-templates-tw-to-zd/segundo-lote-templates.json:4213`
- `contabilizei-front-vue` (1×): `src/modules/pagamentosFintech/constants/mocks.js:196`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `k8s-configmap`, `kong-config`, `pipeline`

### Libs internas

- `br.com.contabilizei.jira:contabilizei-jira` (`contabilizei-guias-core/pom.xml`)
- `br.com.contabilizei:contabil-eventos` (`contabilizei-guias-core/pom.xml`)
- `br.com.contabilizei:contabilizei-api-contabil` (`contabilizei-guias-core/pom.xml`)
- `br.com.contabilizei:contabilizei-bigdata-client` (`contabilizei-guias-core/pom.xml`)
- `br.com.contabilizei:contabilizei-datastore` (`contabilizei-guias-core/pom.xml`)
- `br.com.contabilizei:contabilizei-guias` (`pom.xml`)
- `br.com.contabilizei:contabilizei-guias-core` (`contabilizei-guias-web/pom.xml`)
- `br.com.contabilizei:contabilizei-issue-client` (`contabilizei-guias-core/pom.xml`)
- `br.com.contabilizei:contabilizei-metadata` (`contabilizei-guias-web/pom.xml`)
- `br.com.contabilizei:contabilizei-nfe-api-dtos` (`contabilizei-guias-core/pom.xml`)
- `br.com.contabilizei:contabilizei-queue` (`contabilizei-guias-core/pom.xml`)
- `br.com.contabilizei:contabilizei-sso-client` (`contabilizei-guias-core/pom.xml`)
- `br.com.contabilizei:contabilizei-tarefa-paginada` (`contabilizei-guias-core/pom.xml`)
- `br.com.contabilizei:contabilizei-testes` (`contabilizei-guias-core/pom.xml`)
- `br.com.contabilizei:contabilizei-utils` (`contabilizei-guias-core/pom.xml`)
- `br.com.contabilizei:feign-apis-back` (`contabilizei-guias-core/pom.xml`)
- `br.com.contabilizei:feign-apis-impostos` (`contabilizei-guias-core/pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `audit-inss`, `audit-simples-ecac`, `buscar-baixa-das`, `buscar-baixa-das-anterior`, `callback-plataforma-confirmar-mes`, `callback-plataforma-confirmar-mes-dev`, `callback-plataforma-confirmar-mes-homol`, `callback.plataforma`, `cobranca.recalculo.guia`, `confirmar-mes-lucro-presumido`, `darf-entrada`, `emitir-parcela`, `emitir-parcela-pgfn`, `finalizar-importacao-lucro-presumido`, `gerar-darf-inss-avulsa`, `gerar-das-avulsa`, `gerar-guia-darf`, `gerar-guia-das`, `gerar-iss`, `gerar-tfe`, `ingestor-streaming`, `notificacao.recalculo.guia`, `notificacao.vencimento.guia`, `notificacao.vencimento.parcela`, `notificar-liberacao-guia-tfe`, `notificar-liberacao-guias-compra`, `notificar-liberacao-guias-compra-homol`, `notificar-liberacao-parcela-guia`, `processar-guia-imposto`, `recalcular-guia-das`, `recalculo-iss`, `rpa-regularize-pgfn`, `rpa-simples-nacional-teste`, `test-topic`, `verificar-cancelamento-parcelamento`, `verificar-pagamento`, `verificar-pagamento-darf`, `verificar-pagamento-tfe`, `verificar-sincronizacao-empresa-lote`, `verificar-sincronizacao-parcelamento`
- **Subscription**: `dados.darf-saida`, `notificacao.recalculo.guia`, `notificacao.vencimento.parcela`, `notificar-liberacao-parcela-guia`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Google Chat: `chat.googleapis.com` em `contabilizei-guias-core/src/test/java/br/com/contabilizei/googlechat/GoogleChatClientTest.kt:54`
- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `contabilizei-guias-core/src/test/java/br/com/contabilizei/jira/JiraSdcTestTemplate.kt:11`

<!-- deps:auto:fim -->
