---
name: dependencias-pipeline
description: "Dependências do pipeline: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - pipeline
repositorio: pipeline
---

# Dependências do pipeline

O que o `pipeline` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `fix/experts-functions-prd-terraform-import` @ `68c3ac7d7` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-abertura` (105×): `custom/ctbz/atendimento/geral/atendimento-zendesk.dev.yml:145`, `custom/ctbz/atendimento/geral/atendimento-zendesk.prd.yml:141`, `custom/ctbz/ativacao/geral/painel-diario-dos-robos.yml:10`
- `contabilizei-impostos` (74×): `custom/ctbz/excelencia/geral/contabilizei-gae-data-helper.yml:16`, `custom/ctbz/fiscal-impostos/geral/contabilizei-guias.dev.yml:2`, `custom/ctbz/fiscal-impostos/geral/contabilizei-guias.prd.yml:2`
- `aida-back` (42×): `custom/ctbz/atendimento/geral/atendimento-api-gateway.dev.yml:25`, `custom/ctbz/atendimento/geral/atendimento-api-gateway.prd.yml:29`, `custom/ctbz/atendimento/geral/atendimento-zendesk.dev.yml:164`
- `contabilizei-pagamentos` (36×): `custom/ctbz/billing/geral/contabilizei-ms-gateway-adyen.dev.yml:3`, `custom/ctbz/billing/geral/contabilizei-ms-gateway-adyen.prd.yml:3`, `custom/ctbz/billing/geral/contabilizei-ms-gateway-adyen.stg.yml:3`
- `atendimento-zendesk` (15×): `custom/ctbz/atendimento/geral/atendimento-api-gateway.dev.yml:25`, `custom/ctbz/atendimento/geral/atendimento-api-gateway.prd.yml:29`, `custom/ctbz/atendimento/geral/atendimento-zendesk-api-tests.dev.yml:4`
- `aida-classifier` (11×): `custom/ctbz/inteligencia-artificial/atendimento/aida-classifier.prd.yml:3`, `custom/ctbz/inteligencia-artificial/atendimento/aida-classifier.stg.yml:3`, `custom/ctbz/inteligencia-artificial/atendimento/aida-classifier.yml:3`
- `zendesk-agents` (8×): `custom/ctbz/atendimento/geral/atendimento-zendesk.dev.yml:167`, `custom/ctbz/atendimento/geral/atendimento-zendesk.prd.yml:156`, `custom/ctbz/experts/atendimento-canais/atendimento-canais-admin.dev.yml:24`
- `plataforma-web` (7×): `custom/ctbz/aquisicao/geral/contabilizei-site.yml:94`, `custom/ctbz/engajamento-experiencia/arquitetura/plataforma-web.yml:7`, `custom/ctbz/onboarding-retencao/mfa/multiusuarios.dev.yml:23`
- `experts-service` (7×): `custom/ctbz/atendimento/geral/atendimento-zendesk.dev.yml:163`, `custom/ctbz/atendimento/geral/atendimento-zendesk.prd.yml:152`, `custom/ctbz/experts/atendimento-canais/canais-adk.dev.yml:55`
- `bots-api` (7×): `custom/ctbz/atendimento/geral/atendimento-zendesk.dev.yml:168`, `custom/ctbz/atendimento/geral/atendimento-zendesk.prd.yml:157`, `custom/ctbz/experts/atendimento-canais/atendimento-canais-admin.dev.yml:23`
- `contato-service` (7×): `custom/ctbz/experts/atendimento-canais/atendimento-canais-admin.dev.yml:26`, `custom/ctbz/experts/atendimento-canais/atendimento-canais-admin.prd.yml:26`, `custom/ctbz/experts/atendimento-canais/contato-service.prd.yml:23`
- `canais-certificado-digital` (7×): `custom/ctbz/experts/atendimento-canais/canais-adk.dev.yml:40`, `custom/ctbz/experts/atendimento-canais/canais-adk.prd.yml:70`, `custom/ctbz/experts/atendimento-canais/canais-certificado-digital.dev.yml:31`
- `sentinela-atendimento` (7×): `custom/ctbz/inteligencia-artificial/atendimento/aida-back.dev.yml:83`, `custom/ctbz/inteligencia-artificial/atendimento/aida-back.prd.yml:84`, `custom/ctbz/inteligencia-artificial/atendimento/sentinela-atendimento.dev.yml:1`
- `atendimento-api-gateway` (6×): `custom/ctbz/atendimento/geral/atendimento-api-gateway.dev.yml:6`, `custom/ctbz/atendimento/geral/atendimento-api-gateway.prd.yml:29`, `custom/ctbz/atendimento/geral/atendimento-api-gateway.yml:35`
- `plataforma-central-rotinas` (5×): `custom/ctbz/atendimento/geral/atendimento-zendesk.dev.yml:151`, `custom/ctbz/atendimento/geral/atendimento-zendesk.prd.yml:145`, `custom/ctbz/engajamento-experiencia/geral/canais-xp-jobs.prd.yml:16`
- `experts-nfs` (5×): `custom/ctbz/experts/atendimento-canais/atendimento-canais-admin.dev.yml:21`, `custom/ctbz/experts/atendimento-canais/atendimento-canais-admin.prd.yml:21`, `custom/ctbz/experts/atendimento-canais/canais-adk.dev.yml:39`
- `email-service` (5×): `custom/ctbz/experts/atendimento-canais/atendimento-canais-admin.dev.yml:39`, `custom/ctbz/experts/atendimento-canais/atendimento-canais-admin.prd.yml:39`, `custom/ctbz/experts/atendimento-canais/email-service.prd.yml:23`
- `canais-adk` (5×): `custom/ctbz/experts/atendimento-canais/canais-adk.yml:1`, `custom/ctbz/experts/atendimento-canais/canais-certificado-digital.prd.yml:8`, `custom/ctbz/experts/atendimento-canais/canais-certificado-digital.yml:36`
- `contabilizei-front` (4×): `custom/ctbz/aquisicao/geral/contabilizei-site-nuxt3.yml:9`, `custom/ctbz/cross-sell/geral/contabilizei-front-simulador-ps.yml:5`, `custom/ctbz/engajamento-experiencia/frontend-plataforma/contabilizei-front-vue.yml:5`
- `monitoria-ia` (3×): `custom/ctbz/atendimento/geral/monitoria-ia.yml:11`, `custom/ctbz/experts/atendimento-canais/atendimento-canais-admin.dev.yml:40`, `custom/ctbz/experts/atendimento-canais/atendimento-canais-admin.prd.yml:40`
- `zendesk-proxy` (3×): `custom/ctbz/experts/atendimento-canais/atendimento-canais-admin.dev.yml:25`, `custom/ctbz/experts/atendimento-canais/atendimento-canais-admin.prd.yml:25`, `custom/ctbz/experts/atendimento-canais/zendesk-proxy.prd.yml:36`
- `contabilizei-agents` (3×): `custom/ctbz/experts/atendimento-canais/canais-adk.dev.yml:53`, `custom/ctbz/experts/atendimento-canais/canais-adk.prd.yml:83`, `custom/ctbz/experts/geral/contabilizei-agents.prd.yml:23`
- `emissor-whatsapp` (3×): `custom/ctbz/experts/atendimento-canais/canais-certificado-digital.dev.yml:25`, `custom/ctbz/experts/atendimento-canais/canais-certificado-digital.prd.yml:26`, `custom/ctbz/experts/backend/emissor-whatsapp-reports.yml:12`
- `emissor-whatsapp-reports` (3×): `custom/ctbz/experts/atendimento-canais/canais-certificado-digital.dev.yml:25`, `custom/ctbz/experts/atendimento-canais/canais-certificado-digital.prd.yml:26`, `custom/ctbz/experts/backend/emissor-whatsapp-reports.yml:12`
- `aida-front` (3×): `custom/ctbz/inteligencia-artificial/atendimento/aida-front.yml:4`
- `contabilizei-crm-webhooks` (2×): `custom/ctbz/atendimento/geral/atendimento-api-gateway.dev.yml:25`, `custom/ctbz/atendimento/geral/atendimento-api-gateway.prd.yml:29`
- `ticketing-service` (2×): `custom/ctbz/atendimento/geral/atendimento-zendesk.dev.yml:159`, `custom/ctbz/atendimento/geral/atendimento-zendesk.prd.yml:150`
- `agent-eval` (2×): `custom/ctbz/experts/atendimento-canais/canais-adk.dev.yml:57`, `custom/ctbz/experts/atendimento-canais/canais-adk.prd.yml:87`
- `file-transcriber` (2×): `custom/ctbz/experts/geral/file-transcriber.prd.yml:24`, `custom/ctbz/experts/geral/file-transcriber.stg.yml:24`
- `ms-relatorio-faturamento` (2×): `custom/ctbz/inteligencia-artificial/fiscal/tax-orchestrator.prd.yml:44`, `custom/ctbz/inteligencia-artificial/fiscal/tax-orchestrator.stg.yml:44`
- `atendimento-zendesk-cronjob` (1×): `custom/ctbz/atendimento/geral/atendimento-zendesk.prd.yml:16`
- `contabilizei-movimentacao-back` (1×): `custom/ctbz/contabil/geral/contabilizei-movimentacao-back.yml:13`
- `contabilizei-front-vue` (1×): `custom/ctbz/engajamento-experiencia/frontend-plataforma/contabilizei-front-vue.yml:5`
- `ultimateai-webhook` (1×): `custom/ctbz/experts/atendimento-canais/ultimateai-webhook.yml:7`
- `webhook-gitlab` (1×): `custom/ctbz/experts/atendimento-canais/webhook-gitlab.yml:7`
- `experts-alertas` (1×): `custom/ctbz/experts/backend/experts-alertas.yml:13`
- `experts-async-publisher` (1×): `custom/ctbz/experts/backend/experts-async-publisher.yml:19`
- `experts-zendesk` (1×): `custom/ctbz/experts/backend/experts-tarefas-assessor.yml:12`
- `html-to-pdf` (1×): `custom/ctbz/experts/backend/html-to-pdf.yml:13`
- `contabilizei-guias` (1×): `custom/ctbz/fiscal-impostos/geral/contabilizei-guias.yml:4`
- `plataforma-faturamento-worker` (1×): `custom/ctbz/fiscal-impostos/geral/plataforma-faturamento-worker.yml:71`
- `saude-empresa-pendencias` (1×): `custom/ctbz/fiscal-impostos/geral/saude-empresa-pendencias.yml:8`
- `oi-contabilizei-functions` (1×): `templates/ci-cd.yml:737`
- `plataforma-importacao-notas-worker` (1×): `templates/gae.yml:91`
- Configuração, CI e documentação citadas: `k8s-configmap`, `kong-config`, `vault-roleset`

### Repositórios que citam este

_O nome `pipeline` é comum demais para busca por token; procurar pelo host, rota ou tópico._

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `alarme-abertura-conta`, `alarme-autopilot`, `alarme-importacao-extrato`, `alarme-tickets-fintech`, `alarme-votos-nps`, `atendimento-zendesk-atualizar-ticket`, `ativar-collections`, `autopilot-desligamento-clientes-inelegiveis`, `autopilot-liberacao-novos-clientes`, `bs2-sync-conta`, `classificacao-atendimento`, `contabilizei-bank.webhook-dock`, `desativar-collections`, `financeiro-chat-payments`, `gerar-das`, `oferta-da-payments`, `oferta-da-payments-debito`, `twilio-webhooks-messages`, `twilio-webhooks-tasks`, `zendesk-webhooks-agents`, `zendesk-webhooks-capacidade-agentes`, `zendesk-webhooks-comments`, `zendesk-webhooks-conversations`, `zendesk-webhooks-events-tickets`, `zendesk-webhooks-notifications`, `zendesk-webhooks-pesquisa-satisfacao`, `zendesk-webhooks-retorno-desconexao-sem-interacao`, `zendesk-webhooks-tickets`, `zendesk-webhooks-tickets-new`, `zendesk-webhooks-users`
- **Subscription**: `contato-service.sub.on-message-event-meta`, `dados.buscar-baixa-das-anterior-dev`, `dados.buscar-baixa-das-anterior-prod`, `dados.buscar-baixa-das-dev`, `dados.buscar-baixa-das-prod`, `dataflow-batch-service`, `email-service.p2p.send-email.sub`, `experts-service.sub.desconexao.evalutate-message-ia`, `zendesk-agents.sub.tickets`, `zendesk-webhooks-tickets`
- **Fila Cloud Tasks**: `aida-classifier`, `aida-memoria-process`, `certificado-digital`, `experts-zendesk`, `simulador-plano-saude`
- **Cloud Run / function**: `aida-back-dev`, `aida-classifier-prd-api`, `aida-classifier-stg-api`, `arquivos-fator-r`, `atendimento-api-gateway`, `atendimento-api-gateway-dev`, `atendimento-api-gateway-prd`, `bots-api`, `contabilizei-agents`, `contabilizei-comprovante-rendimentos`, `contador-inteligente-dev-api`, `contador-inteligente-stg-api`, `emissor-whatsapp-reports`, `experts-alertas`, `experts-async-publisher`, `experts-nfs`, `experts-zendesk`, `find_situacao_voucher`, `html-to-pdf`, `notify-guias`, `sentinela-atendimento-dev`, `ultimateai-webhook`, `webhook-gitlab`, `zendeskbot-check-numerical-answer`, `zendeskbot-compare-values`, `zendeskbot-conditional`, `zendeskbot-config`, `zendeskbot-delay`, `zendeskbot-loop`, `zendeskbot-multiply-two-string-values`, `zendeskbot-parse-string-to-number`, `zendeskbot-request-delay`, `zendeskbot-return-element-at-index`, `zendeskbot-return-list-property`, `zendeskbot-validate-date`, `zendeskbot-validate-finantial-value`
- **Templates de CI** (`.gitlab-ci.yml`): `ctbz/devops/dummies/dummy-appengine-single-service`, `ctbz/devops/dummies/dummy-cloud-run`, `ctbz/devops/dummies/dummy-cloudrun-java`, `ctbz/devops/dummies/dummy-cloudrun-python`, `ctbz/devops/dummies/dummy-container`, `ctbz/devops/dummies/dummy-java-lib`, `ctbz/devops/dummies/dummy-js-lib`, `ctbz/devops/dummies/dummy-spring-boot-app`, `ctbz/devops/dummies/dummy-spring-boot-app-k8s-deployment`

### Bancos e dados

- Tabelas/datasets do BigQuery citados: `contabilizei-dataflow.joao_pedro.tabela_mock_comunicacao_regua_d30`

### Terceiros

- APIs públicas (CNPJ/CEP): `viacep.com.br` em `custom/ctbz/inteligencia-artificial/vendas/cia-back-closer.dev.yml:22`
- Datadog: `datadoghq.com` em `custom/ctbz/aquisicao/geral/contabilizei-site-nuxt3.prd.yml:31`
- GitLab API: `gitlab.com/api` em `custom/ctbz/ativacao/robos.yml:13`
- Google Chat: `chat.googleapis.com` em `custom/ctbz/inteligencia-artificial/contabil/accounting-orchestrator.prd.yml:82`
- HubSpot: `api.hubapi.com` em `custom/ctbz/cross-sell/integracoes/integracao-crm-hubspot.dev.yml:35`
- Jira / Confluence: `contabilizei.atlassian.net` em `custom/ctbz/atendimento/geral/atendimento-zendesk.dev.yml:161`, `contabilizeicontabilidade.atlassian.net` em `custom/ctbz/billing.yml:2`
- Zendesk: `contabilizei.zendesk.com` em `custom/ctbz/atendimento/geral/atendimento-zendesk-extensao-web.prd.yml:4`, `contabilizei1637606740.zendesk.com` em `custom/ctbz/atendimento/geral/atendimento-zendesk-extensao-web.dev.yml:4`

<!-- deps:auto:fim -->
