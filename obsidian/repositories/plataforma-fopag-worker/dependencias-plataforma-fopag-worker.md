---
name: dependencias-plataforma-fopag-worker
description: "Dependências do plataforma-fopag-worker: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - plataforma-fopag-worker
repositorio: plataforma-fopag-worker
---

# Dependências do plataforma-fopag-worker

O que o `plataforma-fopag-worker` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `develop05` @ `cbf8faf7` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-impostos` (24×): `src/main/resources/filtered/parametro.desenv.properties:40`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:180`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:81`
- `contabilizei-abertura` (15×): `src/main/resources/filtered/parametro.desenv.properties:326`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:212`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:232`
- `contabilizei-guias` (12×): `src/main/resources/filtered/parametro.desenvolvimento-1.properties:186`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:192`, `src/main/resources/filtered/parametro.desenvolvimento-3.properties:180`
- `contabilizei-pagamentos` (7×): `src/main/resources/filtered/parametro.desenv.properties:5`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:13`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:14`
- `contabilizei-back-core` (2×): `pom.xml:26`

### Repositórios que citam este

_Nenhum._
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-excalidraw`

### Libs internas

- `br.com.contabilizei:contabil-eventos` (`pom.xml`)
- `br.com.contabilizei:contabilizei-back-core` (`pom.xml`)
- `br.com.contabilizei:contabilizei-back-parent` (`pom.xml`)
- `br.com.contabilizei:contabilizei-obrigacoes-firebase` (`pom.xml`)
- `br.com.contabilizei:contabilizei-sso-client` (`pom.xml`)
- `br.com.contabilizei:contabilizei-utils` (`pom.xml`)
- `br.com.contabilizei:feign-apis-guias` (`pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `alteracao-empresa`, `audit-inss`, `audit-pagamentos-tfe`, `audit-parcelamento-especial`, `audit-simples-ecac`, `comercio-20-topic-empresas-inativas`, `comercio-notify-evento-cancelamento`, `consulta-situacao-fiscal`, `consulta-situacao-fiscal-retorno`, `consultar-tfe`, `darf-entrada`, `darf-saida`, `dataflow-streaming-eventos-solicitacao-contas`, `eventos-solicitacao-contas-crm`, `functions.email-holerites`, `gerar-imposto-composicao-darf-unificado`, `gerar-imposto-folha-fgts`, `gerar-tfe`, `notificar-alteracao-inss-darf`, `processar-guia-imposto`, `simular-transmissao-pgdas`, `update-empresa`, `update-integracao-conta-bancaria`, `verificador-pendencias`, `verificador-pendencias-cnd`, `verificador-pendencias-divida-ativa`, `verificador-pendencias-divida-ativa-dev`, `verificar-pagamento-darf`, `vinculo-certificado`
- **Fila Cloud Tasks**: `acesso-simples-queue`, `agendamento-queue`, `ativacao-empresa`, `bigquery-exporter-queue`, `call-back-obrigacao`, `carregarDados-queue`, `cnae-queue`, `criar-obrigacao`, `darf-pagamento`, `das-pagamento`, `das-queue`, `escrituracao-queue`, `fast-obrigacao-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `folha-queue`, `gerar-arquivo-obrigacao`, `gps-pagamento`, `importacao-queue`, `nfe-entrada-queue`, `notificacao-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacoes-core-queue`, `optimize-queue`, `particionamento-notas-queue`, `processar-recibo-obrigacao`, `recibo-queue`, `regime-tributario-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `zendesk-queue`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/main/java/br/com/contabilizei/folha/cron/AtualizarTipoFolhaEmpresa.java:22`

<!-- deps:auto:fim -->
