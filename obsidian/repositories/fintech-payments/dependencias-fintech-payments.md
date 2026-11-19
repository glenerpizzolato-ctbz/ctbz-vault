---
name: dependencias-fintech-payments
description: "Dependências do fintech-payments: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - fintech-payments
repositorio: fintech-payments
---

# Dependências do fintech-payments

O que o `fintech-payments` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `cc3b9a66` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-impostos` (22×): `src/main/catalog-model/resources/fintech-payments-pubsub-subscriptions-resource.yaml:19`, `src/main/kotlin/br/com/contabilizei/fintech/app/recorrencia/component/AtualizarStatusGuiaClient.kt:11`, `src/test/kotlin/br/com/contabilizei/fintech/app/recorrencia/component/AtualizarStatusGuiaClientServiceTest.kt:28`
- `contabilizei-pagamentos` (6×): `src/main/kotlin/br/com/contabilizei/fintech/app/task/service/FaturaDebitoAutomaticoCloudTaskService.kt:23`, `src/main/resources/application-stg.yml:43`, `src/main/resources/application.yml:123`
- `plataforma-web` (2×): `src/test/kotlin/br/com/contabilizei/fintech/app/externo/debitoautomatico/service/DebitoAutomaticoExternoServiceTest.kt:585`, `src/test/kotlin/br/com/contabilizei/fintech/app/infra/pubsub/worker/ProcessadorAlteracaoFormaPagamentoWorkerTest.kt:29`

### Repositórios que citam este

- `atendimento-zendesk` (21×): `.config.json:159`, `environments/_deprecated/config-dev.json:224`, `environments/_deprecated/config-local.json:224`
- `plataforma-web` (10×): `src/main/java/br/com/contabilizei/plataforma/impostos/facade/ImpostoPagarV3Facade.kt:316`, `src/main/resources/filtered/parametro.desenv.properties:874`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:645`
- `plataforma-central-rotinas` (9×): `src/main/resources/filtered/parametro.desenv.properties:872`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:640`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:664`
- `sql2bq` (3×): `cronjobs/params-prd.yaml:87`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-bruno`, `k8s-configmap`, `kong-config`

### Libs internas

- `br.com.contabilizei.fintech:fintech-payments` (`pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `contabilizei-bank.agendar-pagamento`, `contabilizei-bank.cancelar-agendamento`, `contabilizei-bank.hubspot-events-input`, `contabilizei-bank.retentativa-pagamento-imediato`, `fintech-crm.enviar-email`, `fintech-crm.enviar-google-chat`, `fintech-crm.enviar-push-notification`, `payments.criar-lote-pagamento-recorrente`, `payments.enviar-dados-lote-para-fintech-web`, `payments.notificacao-email-pagamento-recorrente`, `payments.pagar-lote-recorrente`
- **Subscription**: `atualizar-forma-pagamento-fintech-payments-sub`, `contabilizei-bank.atualizar-conta-alias-fintech-payments-sub`, `contabilizei-bank.notificar-agendamento-cancelado-sub`, `payments.criar-lote-recorrente-sub`, `payments.enviar-dados-lote-para-fintech-web-sub`, `payments.notificacao-email-pagamento-recorrente-sub`, `payments.pagar-lote-recorrente-sub`, `sub.processar-controle-debito-guia-payments`, `sub.processar-faturas-payments`, `sub.processar-guia-imposto-payments`, `sub.update-empresa-payments`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
