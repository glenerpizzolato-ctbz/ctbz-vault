---
name: dependencias-plataforma-central-rotinas
description: "Dependências do plataforma-central-rotinas: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - plataforma-central-rotinas
repositorio: plataforma-central-rotinas
---

# Dependências do plataforma-central-rotinas

O que o `plataforma-central-rotinas` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `29d082b` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-guias` (37×): `anotacoes.md:26`, `src/main/resources/filtered/parametro.desenv.properties:404`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:317`
- `contabilizei-impostos` (27×): `anotacoes.md:44`, `src/main/resources/filtered/parametro.desenv.properties:817`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:501`
- `contabilizei-abertura` (26×): `src/main/resources/filtered/parametro.desenv.properties:842`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:616`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:640`
- `experts-contabil` (10×): `src/main/resources/filtered/parametro.desenv.properties:1020`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:753`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:765`
- `fintech-payments` (9×): `src/main/resources/filtered/parametro.desenv.properties:872`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:640`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:664`
- `atendimento-zendesk` (9×): `src/main/resources/filtered/parametro.desenv.properties:975`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:719`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:738`
- `plataforma-web` (8×): `catalog-info.yaml:4`, `docs/apis/plataforma-web-api.yaml:12`, `docs/components/plataforma-web.yaml:4`
- `contabilizei-pagamentos` (8×): `src/main/resources/filtered/parametro.desenv.properties:11`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:20`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:20`
- `saude-empresa-pendencias` (8×): `src/main/resources/filtered/parametro.desenv.properties:1035`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:795`, `src/main/resources/filtered/parametro.desenvolvimento-3.properties:857`
- `plataforma-crm-web` (3×): `sonar-project.properties:10`
- `contabilizei-back-core` (2×): `pom.xml:87`, `README.md:9`

### Repositórios que citam este

- `atendimento-zendesk` (51×): `.config.json:206`, `environments/_deprecated/config-dev.json:277`, `environments/_deprecated/config-local.json:277`
- `plataforma-web` (9×): `src/main/resources/filtered/parametro.desenv.properties:39`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:36`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:34`
- `aida-back` (1×): `contabilizeiai/clients/empresa_client.py:19`
- `plataforma-app-config` (1×): `src/main/webapp/WEB-INF/queue.xml:1463`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-bruno`, `k8s-configmap`, `pipeline`

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

- **Tópico**: `alteracao-empresa`, `audit-pagamentos-tfe`, `audit-parcelamento-especial`, `consultar-tfe`, `gerar-tfe`, `verificador-pendencias`, `verificador-pendencias-cnd`
- **Fila Cloud Tasks**: `acesso-simples-queue`, `agendamento-queue`, `ativacao-empresa`, `bigquery-exporter-queue`, `call-back-obrigacao`, `carregarDados-queue`, `certificado-digital`, `cnae-queue`, `criar-obrigacao`, `darf-pagamento`, `das-pagamento`, `das-queue`, `escrituracao-queue`, `fast-obrigacao-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `folha-queue`, `gerar-arquivo-obrigacao`, `gps-pagamento`, `importacao-queue`, `nfe-entrada-queue`, `notificacao-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacoes-core-queue`, `optimize-queue`, `particionamento-notas-queue`, `processar-recibo-obrigacao`, `recibo-queue`, `regime-tributario-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `zendesk-queue`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/main/resources/filtered/parametro.desenv.properties:131`
- Zendesk: `contabilizei1637606740.zendesk.com` em `src/main/resources/filtered/parametro.desenv.properties:968`

<!-- deps:auto:fim -->
