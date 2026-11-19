---
name: dependencias-plataforma-back-worker
description: "Dependências do plataforma-back-worker: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - plataforma-back-worker
repositorio: plataforma-back-worker
---

# Dependências do plataforma-back-worker

O que o `plataforma-back-worker` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `develop` @ `8421840` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-guias` (33×): `src/main/resources/filtered/parametro.desenv.properties:393`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:302`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:328`
- `contabilizei-impostos` (16×): `src/main/resources/filtered/parametro.desenv.properties:609`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:486`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:504`
- `contabilizei-abertura` (15×): `src/main/resources/filtered/parametro.desenv.properties:800`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:595`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:620`
- `experts-async-publisher` (10×): `src/main/resources/filtered/parametro.desenv.properties:924`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:690`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:711`
- `contabilizei-pagamentos` (7×): `src/main/resources/filtered/parametro.desenv.properties:11`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:17`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:17`
- `contabilizei-back-core` (2×): `pom.xml:38`

### Repositórios que citam este

- `experts-service` (1×): `src/domain/event/events/internal/empresa/updated-assessor-empresa.test.ts:28`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-bruno`

### Libs internas

- `br.com.contabilizei:contabilizei-back-core` (`pom.xml`)
- `br.com.contabilizei:contabilizei-back-parent` (`pom.xml`)
- `br.com.contabilizei:contabilizei-obrigacoes-firebase` (`pom.xml`)
- `br.com.contabilizei:contabilizei-sso-client` (`pom.xml`)
- `br.com.contabilizei:contabilizei-utils` (`pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `alteracao-empresa`, `audit-pagamentos-tfe`, `audit-parcelamento-especial`, `consultar-tfe`, `experts.empresa`, `gerar-tfe`, `verificador-pendencias`, `verificador-pendencias-cnd`
- **Fila Cloud Tasks**: `acesso-simples-queue`, `agendamento-queue`, `ativacao-empresa`, `bigquery-exporter-queue`, `call-back-obrigacao`, `carregarDados-queue`, `certificado-digital`, `cnae-queue`, `criar-obrigacao`, `darf-pagamento`, `das-pagamento`, `das-queue`, `escrituracao-queue`, `fast-obrigacao-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `folha-queue`, `gerar-arquivo-obrigacao`, `gps-pagamento`, `importacao-queue`, `nfe-entrada-queue`, `notificacao-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacoes-core-queue`, `optimize-queue`, `particionamento-notas-queue`, `processar-recibo-obrigacao`, `recibo-queue`, `regime-tributario-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `zendesk-queue`, `zendesk-sincronizar-organizacao-queue`, `zendesk-sincronizar-usuario-queue`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/main/resources/filtered/parametro.desenv.properties:123`
- Zendesk: `contabilizei1595352016.zendesk.com` em `src/main/resources/filtered/parametro.desenvolvimento-1.properties:636`, `contabilizei1637606740.zendesk.com` em `src/main/resources/filtered/parametro.desenv.properties:866`, `developer.zendesk.com` em `src/main/java/br/com/contabilizei/worker/zendesk/facade/ZendeskAPIFacade.java:53`

<!-- deps:auto:fim -->
