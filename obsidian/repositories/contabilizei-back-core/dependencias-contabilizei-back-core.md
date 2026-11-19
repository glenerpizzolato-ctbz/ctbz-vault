---
name: dependencias-contabilizei-back-core
description: "Dependências do contabilizei-back-core: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - contabilizei-back-core
repositorio: contabilizei-back-core
---

# Dependências do contabilizei-back-core

O que o `contabilizei-back-core` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `develop` @ `371ff9e3` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-guias` (38×): `src/main/java/br/com/contabilizei/imposto/dto/ImpostoUploadArquivoManual.java:99`, `src/main/java/br/com/contabilizei/imposto/paginacao/processor/DisponibilizarGuiasProcessor.java:86`, `src/main/java/br/com/contabilizei/imposto/paginacao/processor/LiberarGuiasProcessor.java:101`
- `contabilizei-abertura` (28×): `src/main/resources/filtered/parametro.desenv.properties:811`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:610`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:639`
- `contabilizei-impostos` (19×): `src/main/java/br/com/contabilizei/imposto/dao/GuiaDAOBack.java:35`, `src/main/resources/filtered/parametro.desenv.properties:609`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:487`
- `contabilizei-pagamentos` (8×): `src/main/resources/filtered/parametro.desenv.properties:11`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:17`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:17`
- `plataforma-faturamento-worker` (3×): `src/main/java/br/com/contabilizei/escrituracao/client/ModuloGuiaClient.kt:20`, `src/main/java/br/com/contabilizei/escrituracao/enumeration/TipoGuia.java:5`, `src/test/java/br/com/contabilizei/escrituracao/client/ModuloGuiaClientTest.kt:28`

### Repositórios que citam este

- `ctbzapp-utils` (16×): `internal/cli/changephones.go:222`, `internal/clone/nextsteps.go:36`, `internal/gcp/edit.go:21`
- `plataforma-monolito` (3×): `pom.xml:41`
- `agrupamento-guias-service` (2×): `src/shared/notificacao/constants/parcelamento.constants.ts:2`, `README.md:42`
- `plataforma-back-worker` (2×): `pom.xml:38`
- `plataforma-central-rotinas` (2×): `pom.xml:87`, `README.md:9`
- `plataforma-fopag-worker` (2×): `pom.xml:26`
- `microsservico-agrupamento-guias` (1×): `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/enums/TipoParcelamento.kt:4`
- `plataforma-crm-web` (1×): `pom.xml:101`
- `plataforma-faturamento-worker` (1×): `pom.xml:139`
- `plataforma-importacao-notas-worker` (1×): `pom.xml:159`
- `plataforma-web` (1×): `pom.xml:93`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-drawio`

### Libs internas

- `br.com.contabilizei.jira:contabilizei-jira` (`pom.xml`)
- `br.com.contabilizei:amazon-client` (`pom.xml`)
- `br.com.contabilizei:audit-client` (`pom.xml`)
- `br.com.contabilizei:contabil-eventos` (`pom.xml`)
- `br.com.contabilizei:contabilizei-api-contabil` (`pom.xml`)
- `br.com.contabilizei:contabilizei-back-core` (`pom.xml`)
- `br.com.contabilizei:contabilizei-back-parent` (`pom.xml`)
- `br.com.contabilizei:contabilizei-backup` (`pom.xml`)
- `br.com.contabilizei:contabilizei-bigdata-client` (`pom.xml`)
- `br.com.contabilizei:contabilizei-bigquery-stream` (`pom.xml`)
- `br.com.contabilizei:contabilizei-common-client` (`pom.xml`)
- `br.com.contabilizei:contabilizei-issue-client` (`pom.xml`)
- `br.com.contabilizei:contabilizei-metadados` (`pom.xml`)
- `br.com.contabilizei:contabilizei-metadata` (`pom.xml`)
- `br.com.contabilizei:contabilizei-nfe-api-client` (`pom.xml`)
- `br.com.contabilizei:contabilizei-nfe-api-dtos` (`pom.xml`)
- `br.com.contabilizei:contabilizei-nfse-dtos` (`pom.xml`)
- `br.com.contabilizei:contabilizei-obrigacoes-firebase` (`pom.xml`)
- `br.com.contabilizei:contabilizei-queue` (`pom.xml`)
- `br.com.contabilizei:contabilizei-sso-client` (`pom.xml`)
- `br.com.contabilizei:contabilizei-storage` (`pom.xml`)
- `br.com.contabilizei:contabilizei-tarefa-paginada` (`pom.xml`)
- `br.com.contabilizei:contabilizei-testes` (`pom.xml`)
- `br.com.contabilizei:contabilizei-utils` (`pom.xml`)
- `br.com.contabilizei:feign-apis-guias` (`pom.xml`)
- `br.com.contabilizei:feign-apis-impostos` (`pom.xml`)
- `br.com.contabilizei:relatorio-contabil-model` (`pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `alteracao-empresa`, `audit-inss`, `audit-simples-ecac`, `comercio-20-topic-empresas-inativas`, `comercio-notify-evento-cancelamento`, `consulta-situacao-fiscal`, `consulta-situacao-fiscal-retorno`, `darf-entrada`, `darf-saida`, `dataflow-streaming-eventos-solicitacao-contas`, `empresa-alterada`, `empresa-ativada`, `eventos-solicitacao-contas-crm`, `gerar-das`, `gps-solicita-recalculo`, `mes-contabil-listener`, `notificar-alteracao-inss-darf`, `plataforma.bcast.empresa-alteracao-plano`, `processar-guia-imposto`, `simular-transmissao-pgdas`, `update-empresa`, `update-guia`, `update-guia-batch`, `update-integracao-conta-bancaria`, `verificador-pendencias-divida-ativa`, `verificador-pendencias-divida-ativa-dev`, `verificar-pagamento-darf`, `vinculo-certificado`
- **Subscription**: `dados.darf-saida`
- **Fila Cloud Tasks**: `aceite-portabilidade-queue`, `acesso-simples-queue`, `agendamento-importacao-notas-queue`, `agendamento-queue`, `alterar-regime-empresa`, `ativacao-contabil-histocio`, `ativacao-empresa`, `ativar-empresa-mei`, `atualizar-campos-jira-processo-migracao-queue`, `atualizar-contratos-empresa-queue`, `audit-queue`, `auditoria-das-queue`, `backup-queue`, `bank-integration-first-of-month-run`, `bigquery-exporter-queue`, `cadastro-automatico-queue`, `calcular-grupo-nota-tomada-queue`, `call-back-obrigacao`, `carregar-notificar-faturamento-zero`, `carregarDados-queue`, `certificado-digital`, `cnae-queue`, `cnd-queue`, `cobranca-avulsa-jira`, `conclusao-importacao-comercio-queue`, `conclusao-importacao-queue`, `correcao-movimentacao`, `criar-obrigacao`, `darf-pagamento`, `das-pagamento`, `das-queue`, `dte-queue`, `email-boas-vindas-csa`, `email-follow-certificado`, `emissao-nota-fiscal-contabilizei`, `empresa-queue`, `enviar-email-finalizacao-abertura-queue`, `escrituracao-processamento-evento`, `escrituracao-queue`, `execucao-importacao-comercio-queue`, `execucao-importacao-queue`, `fast-obrigacao-queue`, `faturamento-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `fintech-criacao-contas`, `fintech-processos-consultas`, `firebase-callback-queue`, `fiscal-queue`, `folha-queue`, `gerar-arquivo-obrigacao`, `gerar-pdf-aceite-queue`, `gps-pagamento`, `importacao-automatica-nfse-queue`, `importacao-comercio-queue`, `importacao-ofx`, `importacao-queue`, `imposto-comercio-queue`, `iss-queue`, `jira-queue`, `limpar-mes-contabil`, `lucro-presumido-queue`, `mes-contabil-queue`, `modulo-impostos-queue`, `nfe-entrada-queue`, `notificacao-queue`, `notificacao-worker-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacao-recibo-impostos-queue`, `obrigacoes-core-fast-queue`, `obrigacoes-core-queue`, `optimize-queue`, `pagamentos-service-queue`, `particionamento-notas-queue`, `pendencia-exclusao-simples-nacional-queue`, `processa-lancamento-contabil-bk-queue`, `processamento-impostos-queue`, `processar-recibo-obrigacao`, `processar-transmissao-queue`, `qc-queue`, `qc-queue-slow`, `recibo-queue`, `regime-tributario-queue`, `relatorio-contabil-queue`, `salvar-novo-onboarding-queue`, `sedex-queue`, `sincronizar-contabil-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `verificador-pendencias-queue`, `zendesk-queue`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Google Chat: `chat.googleapis.com` em `src/main/resources/filtered/parametro.desenv.properties:714`
- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/main/java/br/com/contabilizei/imposto/facade/ImpostoFacade.java:328`
- Zendesk: `contabilizei.zendesk.com` em `src/test/java/br/com/contabilizei/zendesk/facade/ZendeskAPIFacadeTest.java:29`, `contabilizei1595352016.zendesk.com` em `src/main/resources/filtered/parametro.desenv.properties:882`, `developer.zendesk.com` em `src/main/java/br/com/contabilizei/zendesk/facade/ZendeskAPIFacade.java:54`

<!-- deps:auto:fim -->
