---
name: dependencias-microsservico-agrupamento-guias
description: "Dependências do microsservico-agrupamento-guias: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - microsservico-agrupamento-guias
repositorio: microsservico-agrupamento-guias
---

# Dependências do microsservico-agrupamento-guias

O que o `microsservico-agrupamento-guias` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `fix/whatsapp-validade-fim-de-semana` @ `16aa7506` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-guias` (28×): `src/main/resources/application-dev.yml:74`, `src/main/resources/application-local.yml:85`, `src/main/resources/application-prod.yml:80`
- `contabilizei-impostos` (20×): `src/main/catalog-model/resources/microsservico-agrupamento-guias-resource.yaml:5`, `src/main/resources/application-dev.yml:62`, `src/main/resources/application-prod.yml:67`
- `email-service` (18×): `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/integrations/dto/EnviarEmailRequestDTO.kt:14`, `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/integrations/impl/EnvioEmailAgrupamentoServiceImpl.kt:32`, `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/services/EmailTemplateService.kt:7`
- `atendimento-zendesk` (14×): `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/integrations/MetadadosGuiaFactory.kt:24`, `src/main/resources/application-dev.yml:67`, `src/main/resources/application-local.yml:56`
- `contato-service` (5×): `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/integrations/dto/EnviarEmailRequestDTO.kt:16`, `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/integrations/dto/EnvioEmailCallbackDTO.kt:9`, `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/integrations/dto/WhatsAppRequestDTO.kt:48`
- `experts-service` (2×): `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/integrations/MetadadosGuiaFactory.kt:16`
- `impostos-scheduler` (1×): `docs/architecture.drawio:42`
- `contabilizei-back-core` (1×): `src/main/kotlin/br/com/contabilizei/agrupamentoGuias/enums/TipoParcelamento.kt:4`

### Repositórios que citam este

- `experts-service` (7×): `src/domain/guia-imposto/services/index.ts:10`, `src/domain/guia-imposto/services/schedule-notification-wpp-task/schedule-notification-wpp-task.service.ts:20`, `src/domain/guia-imposto/services/should-schedule/should-schedule.service.ts:6`
- `agrupamento-guias-service` (4×): `src/model/enums.ts:10`, `src/shared/notificacao/constants/parcelamento.constants.ts:2`, `docs/bruno/notifica/bp-simples-wpp.bru:37`
- `email-service` (3×): `src/domain/sender/dispatch-priority.integration.spec.ts:114`, `src/domain/sender/helpers/send-alert-card.helper.spec.ts:87`
- `atendimento-canais-admin` (1×): `src/server/domains/controle-notificacao/controle-notificacao.status.ts:5`
- `atendimento-zendesk` (1×): `docs/hubspot/README.md:69`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `k8s-configmap`, `kong-config`

### Libs internas

- `br.com.contabilizei:agrupamentoGuias` (`pom.xml`)
- `br.com.contabilizei:contabilizei-sso-client` (`pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `agrupar-guias-empresa`, `agrupar-guias-empresa-retry`, `atendimento-zendesk.envio-whatsapp-ativo`, `atendimento-zendesk.whatsapp-ativo-status`, `email-service.p2p.file-upload`, `email-service.p2p.send-email`, `email-service.p2p.send-email-callback`, `ms-agrupamento-guias.p2p.agrupar-guias-retry`, `ms-agrupamento-guias.p2p.notificacao-diagnostico-bp`, `ms-agrupamento-guias.p2p.notifies-email`, `ms-agrupamento-guias.p2p.notifies-wpp`, `notificacao-grupo-guia-email`, `notificacao-grupo-guia-whatsapp`, `notificacao-guia-email`, `processar-guia-imposto`
- **Subscription**: `ms-agrupamento-guias.sub.agrupar-guias`, `ms-agrupamento-guias.sub.agrupar-guias-retry`, `ms-agrupamento-guias.sub.notificacao-diagnostico-bp`, `ms-agrupamento-guias.sub.notificacao-diagnostico-bp-local`, `ms-agrupamento-guias.sub.notifies-email`, `ms-agrupamento-guias.sub.notifies-wpp`, `ms-agrupamento-guias.sub.processar-guia`, `ms-agrupamento-guias.sub.send-email-callback`, `ms-agrupamento-guias.sub.send-wpp-callback`, `sub.agrupar-guias-empresa`, `sub.agrupar-guias-empresa-retry`, `sub.notificacao-grupo-guia-email`, `sub.notificacao-grupo-guia-whatsapp`, `sub.processar-guia-imposto-impostos`
- **Scheduler**: `ms-agrupamento-guias-cron-notify-email-bp-lp`, `ms-agrupamento-guias-cron-notify-email-exp-lp`, `ms-agrupamento-guias-cron-notify-email-exp-sn`, `ms-agrupamento-guias-cron-notify-wpp-bp-lp`, `ms-agrupamento-guias-cron-notify-wpp-exp-lp`, `ms-agrupamento-guias-cron-notify-wpp-exp-sn`, `ms-agrupamento-guias-cron-reprocess-group`

### Bancos e dados

- Tabelas/datasets do BigQuery citados: `contabilizei-dataflow.dw_cloudsql_impostos.controle_guias`, `contabilizei-dataflow.dw_cloudsql_impostos.controle_notificacao`, `contabilizei-dataflow.dw_cloudsql_impostos.grupo_guia`

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
