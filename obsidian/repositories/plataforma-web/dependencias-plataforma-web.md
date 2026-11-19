---
name: dependencias-plataforma-web
description: "Dependências do plataforma-web: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - plataforma-web
repositorio: plataforma-web
---

# Dependências do plataforma-web

O que o `plataforma-web` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `develop` @ `26888197b` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-guias` (35×): `src/main/resources/filtered/parametro.desenv.properties:406`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:321`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:345`
- `contabilizei-abertura` (26×): `src/main/resources/filtered/parametro.desenv.properties:844`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:621`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:644`
- `contabilizei-impostos` (25×): `src/main/resources/filtered/parametro.desenv.properties:819`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:506`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:522`
- `atendimento-zendesk` (11×): `src/main/java/br/com/contabilizei/plataforma/service/ZendeskService.kt:40`, `src/test/java/br/com/contabilizei/plataforma/atendimento/widget/jersey/FaleConoscoJerseyTest.kt:218`, `src/main/resources/filtered/parametro.desenv.properties:978`
- `fintech-payments` (10×): `src/main/java/br/com/contabilizei/plataforma/impostos/facade/ImpostoPagarV3Facade.kt:316`, `src/main/resources/filtered/parametro.desenv.properties:874`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:645`
- `experts-contabil` (10×): `src/main/resources/filtered/parametro.desenv.properties:1024`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:763`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:772`
- `plataforma-central-rotinas` (9×): `src/main/resources/filtered/parametro.desenv.properties:39`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:36`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:34`
- `saude-empresa-pendencias` (9×): `src/main/resources/filtered/parametro.desenv.properties:1039`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:794`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:802`
- `contabilizei-pagamentos` (8×): `src/main/resources/filtered/parametro.desenv.properties:13`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:22`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:22`
- `plataforma-crm-web` (3×): `sonar-project.properties:10`
- `contabilizei-back-core` (1×): `pom.xml:93`

### Repositórios que citam este

- `aida-back` (9×): `contabilizeiai/functions/fiscal/notas/notas_fiscais_utils.py:90`, `contabilizeiai/utils/health_checker.py:24`, `tests/functions/fiscal/notas/test_notas_fiscais_utils.py:25`
- `plataforma-central-rotinas` (8×): `catalog-info.yaml:4`, `docs/apis/plataforma-web-api.yaml:12`, `docs/components/plataforma-web.yaml:4`
- `contabilizei-front-vue` (5×): `catalog-info.yaml:9`, `STACK.md:15`, `docs/components/contabilizei-front-vue.yaml:19`
- `plataforma-monolito` (5×): `src/main/java/br/com/contabilizei/monolito/jersey/SuporteJersey.java:77`, `src/main/java/br/com/contabilizei/monolito/notafiscal/jersey/Nota001Jersey.java:119`, `src/main/java/br/com/contabilizei/monolito/notafiscal/jersey/Nota002Jersey.java:102`
- `tarefas-assessor-admin` (4×): `catalog-info.yaml:9`, `docs/components/admin-front-vue.yaml:21`, `docs/systems/plataforma-web.yaml:4`
- `experts-admin` (3×): `docs/components/experts-admin.yaml:20`, `docs/systems/plataforma-web.yaml:4`
- `fintech-payments` (2×): `src/test/kotlin/br/com/contabilizei/fintech/app/externo/debitoautomatico/service/DebitoAutomaticoExternoServiceTest.kt:585`, `src/test/kotlin/br/com/contabilizei/fintech/app/infra/pubsub/worker/ProcessadorAlteracaoFormaPagamentoWorkerTest.kt:29`
- `plataforma-importacao-notas-worker` (2×): `src/test/java/br/com/contabilizei/notafiscal/registro/facade/RegistroNotaFacadeOrquestradorTest.kt:582`
- `plataforma-app-config` (1×): `src/main/webapp/WEB-INF/dispatch.xml:33`
- `plataforma-crm-web` (1×): `README.md:49`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-bruno`, `experts-drawio`, `kong-config`, `pipeline`

### Libs internas

- `br.com.contabilizei:amazon-client` (`pom.xml`)
- `br.com.contabilizei:contabilizei-back-core` (`pom.xml`)
- `br.com.contabilizei:contabilizei-back-parent` (`pom.xml`)
- `br.com.contabilizei:contabilizei-configcat` (`pom.xml`)
- `br.com.contabilizei:contabilizei-obrigacoes-firebase` (`pom.xml`)
- `br.com.contabilizei:contabilizei-sso-client` (`pom.xml`)
- `br.com.contabilizei:contabilizei-testes` (`pom.xml`)
- `br.com.contabilizei:contabilizei-utils` (`pom.xml`)
- `br.com.contabilizei:feign-apis-back` (`pom.xml`)
- `br.com.contabilizei:feign-apis-guias` (`pom.xml`)
- `br.com.contabilizei:feign-apis-impostos` (`pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `alteracao-empresa`, `audit-pagamentos-tfe`, `audit-parcelamento-especial`, `consultar-tfe`, `gerar-tfe`, `verificador-pendencias`, `verificador-pendencias-cnd`, `zendesk-criar-ticket`
- **Fila Cloud Tasks**: `acesso-simples-queue`, `agendamento-queue`, `ativacao-empresa`, `bigquery-exporter-queue`, `call-back-obrigacao`, `carregarDados-queue`, `certificado-digital`, `cnae-queue`, `conclusao-importacao-queue`, `criar-obrigacao`, `darf-pagamento`, `das-pagamento`, `das-queue`, `escrituracao-queue`, `fast-obrigacao-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `fintech-processos-consultas`, `folha-queue`, `gerar-arquivo-obrigacao`, `gps-pagamento`, `importacao-queue`, `nfe-entrada-queue`, `notificacao-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacoes-core-queue`, `optimize-queue`, `particionamento-notas-queue`, `processar-recibo-obrigacao`, `recibo-queue`, `regime-tributario-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `zendesk-queue`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/main/resources/filtered/parametro.desenv.properties:134`
- Meta (WhatsApp Cloud API / Graph): `graph.facebook.com` em `src/main/java/br/com/contabilizei/plataforma/indicacao/facade/IndicacaoFacade.java:174`
- Zendesk: `contabilizei.zendesk.com` em `src/test/java/br/com/contabilizei/plataforma/atendimento/chamado/facade/ChamadoFacadeTest.kt:52`, `contabilizei1637606740.zendesk.com` em `src/main/resources/filtered/parametro.desenv.properties:971`, `suporte.zendesk.com` em `src/test/java/br/com/contabilizei/plataforma/impostos/parcelamento/functions/ParcelamentoFunctionsKtTest.kt:452`

<!-- deps:auto:fim -->
