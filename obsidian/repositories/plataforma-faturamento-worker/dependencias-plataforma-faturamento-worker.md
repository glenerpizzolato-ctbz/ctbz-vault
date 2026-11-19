---
name: dependencias-plataforma-faturamento-worker
description: "Dependências do plataforma-faturamento-worker: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - plataforma-faturamento-worker
repositorio: plataforma-faturamento-worker
---

# Dependências do plataforma-faturamento-worker

O que o `plataforma-faturamento-worker` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `a31483be` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-guias` (44×): `src/main/java/admin/contabilizei/fiscal/view/ParcelamentoEmpresaView.java:32`, `src/main/java/admin/contabilizei/fiscal/view/ParcelamentoGuiaView.java:26`, `src/main/resources/filtered/parametro.desenv.properties:248`
- `contabilizei-impostos` (19×): `src/main/java/admin/contabilizei/fiscal/view/CadastroIssFixoView.java:45`, `src/test/java/br/com/contabilizei/faturamento/utils/MessageTest.kt:15`, `src/main/resources/filtered/parametro.desenv.properties:586`
- `contabilizei-pagamentos` (7×): `src/main/resources/filtered/parametro.desenv.properties:9`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:15`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:15`
- `contabilizei-abertura` (4×): `src/main/resources/filtered/parametro.desenv.properties:664`, `src/main/resources/filtered/parametro.prod.properties:709`
- `ms-relatorio-faturamento` (2×): `src/main/java/br/com/contabilizei/faturamento/dto/relatoriofaturamento/RelatorioFaturamentoDTO.java:19`, `src/main/java/br/com/contabilizei/faturamento/jersey/MesContabilJersey.java:401`
- `contabilizei-back-core` (1×): `pom.xml:139`

### Repositórios que citam este

- `contabilizei-back-core` (3×): `src/main/java/br/com/contabilizei/escrituracao/client/ModuloGuiaClient.kt:20`, `src/main/java/br/com/contabilizei/escrituracao/enumeration/TipoGuia.java:5`, `src/test/java/br/com/contabilizei/escrituracao/client/ModuloGuiaClientTest.kt:28`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `k8s-configmap`, `kong-config`, `pipeline`

### Libs internas

- `br.com.contabilizei:contabilizei-back-core` (`pom.xml`)
- `br.com.contabilizei:contabilizei-back-parent` (`pom.xml`)
- `br.com.contabilizei:contabilizei-obrigacoes-firebase` (`pom.xml`)
- `br.com.contabilizei:contabilizei-sso-client` (`pom.xml`)
- `br.com.contabilizei:contabilizei-testes` (`pom.xml`)
- `br.com.contabilizei:contabilizei-utils` (`pom.xml`)
- `br.com.contabilizei:feign-apis-guias` (`pom.xml`)
- `br.com.contabilizei:feign-apis-impostos` (`pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `agrupar-guias-empresa`, `alteracao-empresa`, `audit-pagamentos-tfe`, `audit-parcelamento-especial`, `calcula-impostos-nota-tomada`, `calcular-impostos-lucro-presumido`, `callback-calculo-impostos-nota-tomada`, `consultar-desenquadramento-dte`, `consultar-tfe`, `criar-empresa-pre-fator-r`, `darf-entrada`, `finalizar-importacao-lucro-presumido`, `gerar-iss`, `gerar-tfe`, `gestao-regime-tributario`, `gps-solicita-recalculo`, `integra-contador`, `migrar-impostos-lucro-presumido`, `recalculo-iss`, `transmitir-pgdas`, `varredura-dte`, `verificador-pendencias`, `verificador-pendencias-cnd`
- **Subscription**: `consulta-enquadramento-final`, `consulta-enquadramento-inicial`, `consulta-solicitacao-enquadramento`, `dados.gerar-iss-retorno`, `solicita-enquadramento`, `troca-regime-tributario-final`, `troca-regime-tributario-lp`, `troca-regime-tributario-restricao-cidade`
- **Fila Cloud Tasks**: `acesso-simples-queue`, `agendamento-queue`, `ativacao-empresa`, `auditoria-das-queue`, `bigquery-exporter-queue`, `calculo-faturamento-queue`, `call-back-obrigacao`, `carregarDados-queue`, `cnae-queue`, `criar-obrigacao`, `darf-pagamento`, `das-pagamento`, `das-queue`, `escrituracao-queue`, `fast-obrigacao-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `folha-queue`, `gerar-arquivo-obrigacao`, `gps-pagamento`, `importacao-queue`, `nfe-entrada-queue`, `notificacao-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacoes-core-queue`, `optimize-queue`, `particionamento-notas-queue`, `processamento-impostos-queue`, `processar-recibo-obrigacao`, `push-notification`, `recibo-queue`, `regime-tributario-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `zendesk-queue`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/main/resources/filtered/parametro.desenv.properties:59`
- Zendesk: `contabilizei1595352016.zendesk.com` em `src/main/resources/filtered/parametro.desenv.properties:648`

<!-- deps:auto:fim -->
