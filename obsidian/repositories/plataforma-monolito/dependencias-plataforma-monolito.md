---
name: dependencias-plataforma-monolito
description: "Dependências do plataforma-monolito: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - plataforma-monolito
repositorio: plataforma-monolito
---

# Dependências do plataforma-monolito

O que o `plataforma-monolito` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `0c815f17` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-guias` (33×): `src/main/resources/filtered/parametro.desenv.properties:393`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:302`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:328`
- `contabilizei-abertura` (19×): `src/main/resources/filtered/parametro.desenv.properties:811`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:603`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:632`
- `contabilizei-impostos` (16×): `src/main/resources/filtered/parametro.desenv.properties:609`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:487`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:505`
- `contabilizei-pagamentos` (7×): `src/main/resources/filtered/parametro.desenv.properties:11`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:18`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:18`
- `plataforma-web` (5×): `src/main/java/br/com/contabilizei/monolito/jersey/SuporteJersey.java:77`, `src/main/java/br/com/contabilizei/monolito/notafiscal/jersey/Nota001Jersey.java:119`, `src/main/java/br/com/contabilizei/monolito/notafiscal/jersey/Nota002Jersey.java:102`
- `contabilizei-back-core` (3×): `pom.xml:41`

### Repositórios que citam este

- `contato-service` (2×): `docs/arquitetura.excalidraw:1999`
- `ctbzapp-utils` (2×): `docs/datastore-insights.md:294`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-drawio`

### Libs internas

- `br.com.contabilizei:contabilizei-back-core` (`pom.xml`)
- `br.com.contabilizei:contabilizei-back-parent` (`pom.xml`)
- `br.com.contabilizei:contabilizei-datastore-console` (`pom.xml`)
- `br.com.contabilizei:contabilizei-obrigacoes-firebase` (`pom.xml`)
- `br.com.contabilizei:contabilizei-sso-client` (`pom.xml`)
- `br.com.contabilizei:contabilizei-testes` (`pom.xml`)
- `br.com.contabilizei:contabilizei-utils` (`pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `alteracao-empresa`, `audit-pagamentos-tfe`, `audit-parcelamento-especial`, `consultar-tfe`, `gerar-tfe`, `verificador-pendencias`, `verificador-pendencias-cnd`
- **Fila Cloud Tasks**: `aceite-portabilidade-queue`, `acesso-simples-queue`, `agendamento-importacao-notas-queue`, `agendamento-queue`, `alterar-regime-empresa`, `ativacao-contabil-histocio`, `ativacao-empresa`, `ativar-empresa-mei`, `atualizar-contratos-empresa-queue`, `auditoria-das-queue`, `backup-kind-queue`, `backup-queue`, `bank-integration-first-of-month-run`, `bigquery-exporter-queue`, `cadastro-automatico-queue`, `call-back-obrigacao`, `carregar-notificar-faturamento-zero`, `carregarDados-queue`, `certificado-digital`, `cnae-queue`, `cnd-queue`, `cobranca-avulsa-jira`, `comunicacao-fechamento-balanco`, `conclusao-importacao-queue`, `correcao-movimentacao`, `criar-obrigacao`, `darf-pagamento`, `das-pagamento`, `das-queue`, `dte-queue`, `email-boas-vindas-csa`, `email-follow-certificado`, `emissao-nota-fiscal-contabilizei`, `empresa-queue`, `enviar-email-finalizacao-abertura-queue`, `escrituracao-processamento-evento`, `escrituracao-queue`, `execucao-importacao-queue`, `fast-obrigacao-queue`, `faturamento-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `fintech-criacao-contas`, `fintech-processos-consultas`, `firebase-callback-queue`, `fiscal-queue`, `folha-queue`, `gerar-arquivo-obrigacao`, `gerar-pdf-aceite-queue`, `gps-pagamento`, `importacao-auto-nfse-queue`, `importacao-ofx`, `importacao-queue`, `imposto-comercio-queue`, `iss-queue`, `jira-queue`, `limpar-mes-contabil`, `lucro-presumido-queue`, `mes-contabil-queue`, `modulo-impostos-queue`, `nfe-entrada-queue`, `notas-recorrentes`, `notificacao-queue`, `notificacao-worker-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacao-recibo-impostos-queue`, `obrigacoes-core-fast-queue`, `obrigacoes-core-queue`, `optimize-queue`, `pagamentos-service-queue`, `particionamento-notas-queue`, `pendencia-exclusao-simples-nacional-queue`, `processa-lancamento-contabil-bk-queue`, `processamento-impostos-queue`, `processar-recibo-obrigacao`, `processar-transmissao-queue`, `qc-queue`, `qc-queue-slow`, `recibo-queue`, `regime-tributario-queue`, `relatorio-contabil-queue`, `salvar-novo-onboarding-queue`, `sedex-queue`, `sincronizar-contabil-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `verificador-pendencias-queue`, `zendesk-queue`

### Bancos e dados

- Tabelas/datasets do BigQuery citados: `contabilizei-dataflow:dw_mgm.vw_empresas_com_cupom_promocional_nao_utilizado`

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/main/resources/filtered/parametro.desenv.properties:123`
- Meta (WhatsApp Cloud API / Graph): `graph.facebook.com` em `src/main/java/br/com/contabilizei/monolito/jersey/OAuth2Jersey.java:272`
- Zendesk: `contabilizei1595352016.zendesk.com` em `src/main/resources/filtered/parametro.desenv.properties:861`

<!-- deps:auto:fim -->
