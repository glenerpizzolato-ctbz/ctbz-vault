---
name: dependencias-plataforma-crm-web
description: "Dependências do plataforma-crm-web: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - plataforma-crm-web
repositorio: plataforma-crm-web
---

# Dependências do plataforma-crm-web

O que o `plataforma-crm-web` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

- `atendimento-zendesk`: `GET /auth/atendimento/v2/bots/whatsapp/dados-cliente/basico-padrao` e `/experts`, `GET /auth/atendimento/processo/telefone`, `GET /auth/atendimento/v2/bots/core/dados-cliente/certificado/emissor`, `GET /auth/atendimento/v2/apps/gerenciamento-faqs/municipios` — `src/infra/clients/plataforma-crm-web/` do atendimento-zendesk; também vão alimentar o motor de regras de avisos e mensagens (PRD-179459)

<!-- deps:auto:inicio (gerado por mapear-dependencias; não editar à mão) -->

## Levantamento automático

Gerado em 2026-11-19 sobre `develop` @ `913fde46` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-impostos` (18×): `src/test/java/br/com/contabilizei/crm/domain/atendimento/v2/apps/diagnosticocliente/impostos/facade/MemoriaCalculoFacadeTest.kt:34`, `src/main/resources/filtered/parametro.desenv.properties:11`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:9`
- `contabilizei-abertura` (18×): `src/test/java/br/com/contabilizei/crm/infra/http/client/autoatendimento/certificado/CertificadoClientTest.kt:65`, `src/main/resources/filtered/parametro.desenv.properties:181`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:139`
- `experts-zendesk` (10×): `src/main/resources/filtered/parametro.desenv.properties:216`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:157`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:160`
- `emissor-whatsapp` (9×): `src/main/resources/filtered/parametro.desenv.properties:201`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:144`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:147`
- `contabilizei-pagamentos` (7×): `src/main/resources/filtered/parametro.desenv.properties:6`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:12`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:12`
- `contabilizei-guias` (7×): `src/main/resources/filtered/parametro.desenvolvimento-1.properties:88`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:93`, `src/main/resources/filtered/parametro.desenvolvimento-3.properties:10`
- `plataforma-web` (1×): `README.md:49`
- `contabilizei-back-core` (1×): `pom.xml:101`

### Repositórios que citam este

- `atendimento-zendesk` (274×): `.config.json:184`, `environments/_deprecated/config-dev.json:255`, `environments/_deprecated/config-local.json:255`
- `experts-twilio` (4×): `environments/.env-dev:32`, `environments/.env-local:27`, `environments/.env-prod:32`
- `plataforma-central-rotinas` (3×): `sonar-project.properties:10`
- `plataforma-web` (3×): `sonar-project.properties:10`
- `atendimento-api-gateway` (1×): `.env.example:17`
- `contabilizei-abertura` (1×): `contabilizei-abertura-core/src/main/java/br/com/contabilizei/abertura/core/service/ProcessoAberturaService.java:2365`
- `contabilizei-abertura-BB` (1×): `contabilizei-abertura-core/src/main/java/br/com/contabilizei/abertura/core/service/ProcessoAberturaService.java:2346`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-bruno`, `experts-drawio`, `experts-excalidraw`, `kong-config`

### Libs internas

- `br.com.contabilizei:contabilizei-back-core` (`pom.xml`)
- `br.com.contabilizei:contabilizei-back-parent` (`pom.xml`)
- `br.com.contabilizei:contabilizei-obrigacoes-firebase` (`pom.xml`)
- `br.com.contabilizei:contabilizei-sso-client` (`pom.xml`)
- `br.com.contabilizei:contabilizei-testes` (`pom.xml`)
- `br.com.contabilizei:contabilizei-utils` (`pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `audit-pagamentos-tfe`, `audit-parcelamento-especial`, `consultar-tfe`, `gerar-tfe`, `verificador-pendencias`, `verificador-pendencias-cnd`
- **Fila Cloud Tasks**: `acesso-simples-queue`, `agendamento-queue`, `ativacao-empresa`, `bigquery-exporter-queue`, `call-back-obrigacao`, `carregarDados-queue`, `certificado-digital`, `cnae-queue`, `criar-obrigacao`, `crm-custom`, `darf-pagamento`, `das-pagamento`, `das-queue`, `emissor-whatsapp`, `escrituracao-queue`, `fast-obrigacao-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `folha-queue`, `gerar-arquivo-obrigacao`, `gps-pagamento`, `importacao-queue`, `nfe-entrada-queue`, `notificacao-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacoes-core-queue`, `optimize-queue`, `particionamento-notas-queue`, `processar-recibo-obrigacao`, `recibo-queue`, `regime-tributario-queue`, `simulador-plano-saude`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `zendesk-queue`
- **Cloud Run / function**: `emissor-whatsapp`, `historico-atendimento`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/main/resources/filtered/parametro.desenv.properties:37`
- Zendesk: `contabilizei1637606740.zendesk.com` em `src/main/resources/filtered/parametro.desenv.properties:174`

<!-- deps:auto:fim -->
