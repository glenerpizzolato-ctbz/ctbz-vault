---
name: dependencias-plataforma-importacao-notas-worker
description: "Dependências do plataforma-importacao-notas-worker: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - plataforma-importacao-notas-worker
repositorio: plataforma-importacao-notas-worker
---

# Dependências do plataforma-importacao-notas-worker

O que o `plataforma-importacao-notas-worker` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `develop` @ `bbe1c372a` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-guias` (33×): `src/main/resources/filtered/parametro.desenv.properties:257`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:184`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:212`
- `contabilizei-impostos` (16×): `src/main/resources/filtered/parametro.desenv.properties:453`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:339`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:364`
- `experts-nfs` (9×): `src/main/resources/filtered/parametro.desenv.properties:656`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:450`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:491`
- `contabilizei-pagamentos` (7×): `src/main/resources/filtered/parametro.desenv.properties:10`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:15`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:15`
- `plataforma-web` (2×): `src/test/java/br/com/contabilizei/notafiscal/registro/facade/RegistroNotaFacadeOrquestradorTest.kt:582`
- `contabilizei-back-core` (1×): `pom.xml:159`

### Repositórios que citam este

- `atendimento-zendesk` (6×): `src/infra/clients/plataforma-notas-worker/notas-fiscais/notas-fiscais.service.ts:154`, `src/infra/clients/plataforma-notas-worker/tomadores/tomadores.service.ts:34`
- `experts-nfs` (1×): `src/modules/v3/confianca/usecases/registrar-desfecho/registrar-desfecho.usecase.ts:35`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-drawio`, `pipeline`

### Libs internas

- `br.com.contabilizei:contabil-eventos` (`pom.xml`)
- `br.com.contabilizei:contabilizei-back-core` (`pom.xml`)
- `br.com.contabilizei:contabilizei-back-parent` (`pom.xml`)
- `br.com.contabilizei:contabilizei-obrigacoes-firebase` (`pom.xml`)
- `br.com.contabilizei:contabilizei-sso-client` (`pom.xml`)
- `br.com.contabilizei:contabilizei-testes` (`pom.xml`)
- `br.com.contabilizei:contabilizei-utils` (`pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `alteracao-empresa`, `audit-inss`, `audit-pagamentos-tfe`, `audit-parcelamento-especial`, `audit-simples-ecac`, `comercio-20-topic-empresas-inativas`, `comercio-notify-evento-cancelamento`, `consulta-situacao-fiscal`, `consulta-situacao-fiscal-retorno`, `consultar-tfe`, `darf-entrada`, `darf-saida`, `dataflow-streaming-eventos-solicitacao-contas`, `empresa-alterada`, `empresa-ativada`, `eventos-solicitacao-contas-crm`, `gerar-tfe`, `mes-contabil-listener`, `notas-worker.bcast.nfs-concluida`, `notificar-alteracao-inss-darf`, `processar-guia-imposto`, `simular-transmissao-pgdas`, `update-empresa`, `update-integracao-conta-bancaria`, `verificador-pendencias`, `verificador-pendencias-cnd`, `verificador-pendencias-divida-ativa`, `verificador-pendencias-divida-ativa-dev`, `verificar-pagamento-darf`, `vinculo-certificado`
- **Fila Cloud Tasks**: `acesso-simples-queue`, `agendamento-queue`, `ativacao-empresa`, `atualizacao-cnae-anexo-massivo-queue`, `bigquery-exporter-queue`, `call-back-obrigacao`, `carregarDados-queue`, `cnae-queue`, `conclusao-importacao-queue`, `criar-obrigacao`, `darf-pagamento`, `das-pagamento`, `das-queue`, `escrituracao-queue`, `fast-obrigacao-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `folha-queue`, `gerar-arquivo-obrigacao`, `gps-pagamento`, `importacao-automatica-notas-tomadas-queue`, `importacao-queue`, `nfe-entrada-queue`, `notas-recorrentes`, `notificacao-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacoes-core-queue`, `optimize-queue`, `particionamento-notas-queue`, `processar-recibo-obrigacao`, `push-notification`, `recibo-queue`, `regime-tributario-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `zendesk-queue`

### Bancos e dados

- Tabelas/datasets do BigQuery citados: `contabilizei-dataflow.dw_contabilizeiapp.auditoriacsvnotasbhportoalegre`, `contabilizei-dataflow.dw_contabilizeiapp.auditoriacsvnotascuritiba`, `contabilizei-dataflow.dw_contabilizeiapp.auditoriacsvnotasrioniteroirecifeamericana`, `contabilizei-dataflow.dw_contabilizeiapp.auditoriacsvnotassp`, `contabilizei-dataflow.dw_contabilizeiapp.configuracao`, `contabilizei-dataflow.dw_contabilizeiapp.empresa`, `contabilizei-dataflow.dw_contabilizeiapp.grupoimportacao`, `contabilizei-dataflow.dw_contabilizeiapp.historicoimportacaonfse`, `contabilizei-dataflow.dw_contabilizeiapp.municipio`, `contabilizei-dataflow.dw_contabilizeiapp.notafiscal`

### Terceiros

- Zendesk: `contabilizei1595352016.zendesk.com` em `src/main/resources/filtered/parametro.desenvolvimento-1.properties:425`

<!-- deps:auto:fim -->
