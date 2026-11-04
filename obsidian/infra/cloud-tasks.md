---
name: cloud-tasks
description: "Cloud Tasks: filas por projeto GCP com taxa, tentativas e repositórios que citam cada fila"
metadata:
  type: reference
tags:
  - infra
  - cloud-tasks
atualizado_em: 2026-10-09
---

# Cloud Tasks

Fotografia de 2026-10-09. Formato: fila · taxa máx. por segundo / concorrência · máx. tentativas · estado se não estiver rodando · roteamento App Engine se houver · repositórios que citam o nome da fila. O alvo de cada task é definido por quem cria a task (ver os repositórios).

## contabilizei-experts-dev

Experts, dev.

- `cashflow-generate` · 500/s, 1000 concorrentes · 3 tentativas · repos: experts-contabil
- `emissor-experts` · 500/s, 1000 concorrentes · tentativas ilimitadas · repos: experts-nfs
- `emissor-experts-pooler` · 10/s, 10 concorrentes · tentativas ilimitadas · **PAUSED** · repos: experts-nfs
- `emissor-whatsapp` · 500/s, 1000 concorrentes · 100 tentativas · **PAUSED** · repos: atendimento-api-gateway, atendimento-zendesk, canais-adk, cnpj-alfanumerico, contabilizei-agents, emissor-whatsapp, emissor-whatsapp-reports, experts-api-gateway, experts-drawio, experts-nfs, experts-twilio-flows, firestore-to-bigquery, mcp-notas-fiscais, plataforma-crm-web
- `emissor-whatsapp-massivo` · 500/s, 1000 concorrentes · tentativas ilimitadas · repos: atendimento-zendesk, emissor-whatsapp, experts-api-gateway, experts-drawio, experts-service, experts-twilio
- `emissor-whatsapp-massivo-check` · 500/s, 1000 concorrentes · 30 tentativas · **PAUSED**
- `experts-zendesk` · 500/s, 1000 concorrentes · 100 tentativas · repos: experts-api-gateway, experts-drawio, experts-tarefas-assessor, experts-zendesk, pipeline
- `feedback-hub` · 500/s, 1 concorrentes · 100 tentativas · repos: atendimento-zendesk, experts-bruno, experts-service, experts-twilio, experts-twilio-flows, js-libraries
- `notas-recorrentes` · 500/s, 1000 concorrentes · 100 tentativas · **PAUSED** · repos: atendimento-canais-admin, experts-nfs, experts-scripts, firestore-to-bigquery, plataforma-importacao-notas-worker, plataforma-monolito
- `one-by-one` · 500/s, 1 concorrentes · tentativas ilimitadas
- `pesquisa-nps-whatsapp` · 500/s, 1 concorrentes · tentativas ilimitadas · repos: atendimento-zendesk
- `teste` · 500/s, 1000 concorrentes · 100 tentativas · **PAUSED**
- `teste3` (us-east1) · 500/s, 1000 concorrentes · 100 tentativas · **PAUSED**

## contabilizei-experts-prd

Experts, prod.

- `cashflow-generate` · 500/s, 1000 concorrentes · 5 tentativas · repos: experts-contabil
- `emissor-experts` · 500/s, 5 concorrentes · 10000 tentativas · repos: experts-nfs
- `emissor-experts-pooler` · 10/s, 10 concorrentes · tentativas ilimitadas · **PAUSED** · repos: experts-nfs
- `emissor-whatsapp` · 500/s, 1000 concorrentes · tentativas ilimitadas · repos: atendimento-api-gateway, atendimento-zendesk, canais-adk, cnpj-alfanumerico, contabilizei-agents, emissor-whatsapp, emissor-whatsapp-reports, experts-api-gateway, experts-drawio, experts-nfs, experts-twilio-flows, firestore-to-bigquery, mcp-notas-fiscais, plataforma-crm-web
- `emissor-whatsapp-massivo` · 2/s, 5 concorrentes · tentativas ilimitadas · repos: atendimento-zendesk, emissor-whatsapp, experts-api-gateway, experts-drawio, experts-service, experts-twilio
- `feedback-hub` · 500/s, 1 concorrentes · tentativas ilimitadas · repos: atendimento-zendesk, experts-bruno, experts-service, experts-twilio, experts-twilio-flows, js-libraries
- `notas-recorrentes` · 500/s, 1000 concorrentes · 100 tentativas · repos: atendimento-canais-admin, experts-nfs, experts-scripts, firestore-to-bigquery, plataforma-importacao-notas-worker, plataforma-monolito
- `one-by-one` · 20/s, 5 concorrentes · tentativas ilimitadas
- `pesquisa-nps-whatsapp` · 500/s, 1 concorrentes · tentativas ilimitadas · repos: atendimento-zendesk
- `temp` · 1/s, 1 concorrentes · tentativas ilimitadas · **PAUSED**
- `temp-migr2-templates-tw-zd` · 1/s, 1 concorrentes · 100 tentativas · **PAUSED**

## aida-stg

AIDA, dev/stg.

- `aida-analise-mensagem-travada` · 500/s, 1000 concorrentes · 1 tentativas · repos: aida-back
- `aida-analise-transferencia` · 10/s, 10 concorrentes · 3 tentativas · repos: aida-back
- `aida-autopilot` · 10/s, 30 concorrentes · 1 tentativas · repos: aida-back
- `aida-autopilot-new-message` · 10/s, 10 concorrentes · 5 tentativas · repos: aida-back
- `aida-classifier` · 10/s, 10 concorrentes · 3 tentativas · repos: aida-back, aida-classifier, pipeline
- `aida-classifier-outbound` · 1/s, 3 concorrentes · 10 tentativas
- `aida-classifier-reprocessamento` · 10/s, 10 concorrentes · 10 tentativas
- `aida-classifier-tag` · 500/s, 10 concorrentes · 10 tentativas
- `aida-controle-ticket` · 60/s, 120 concorrentes · 3 tentativas · repos: aida-back
- `aida-despedida` · 30/s, 10 concorrentes · 3 tentativas · repos: aida-back
- `aida-encerramento` · 500/s, 1000 concorrentes · 100 tentativas · repos: aida-back
- `aida-extratos` · 500/s, 1000 concorrentes · 5 tentativas · repos: aida-back
- `aida-funcoes-agendadas` · 60/s, 120 concorrentes · 3 tentativas · repos: aida-back
- `aida-fup` · 5/s, 10 concorrentes · 5 tentativas
- `aida-instabilidade-emissao-notas` · 60/s, 120 concorrentes · 3 tentativas
- `aida-jobs-default` · 10/s, 10 concorrentes · 3 tentativas · repos: aida-back
- `aida-memoria-process` · 5/s, 20 concorrentes · 5 tentativas · repos: pipeline
- `aida-message-separator` · 500/s, 1000 concorrentes · 10 tentativas · repos: aida-back
- `aida-nf-emissao` · 10/s, 10 concorrentes · 3 tentativas · repos: aida-back
- `aida-nf-emissao-callback` · 10/s, 10 concorrentes · 3 tentativas · repos: aida-back
- `aida-processamento-msg` · 10/s, 10 concorrentes · 3 tentativas · repos: aida-back
- `aida-queue` · 10/s, 10 concorrentes · 3 tentativas · repos: aida-back
- `aida-router-fila` · 10/s, 10 concorrentes · 3 tentativas · repos: aida-back
- `aida-score` · 10/s, 10 concorrentes · 3 tentativas · repos: aida-back
- `aida-simulador` · 500/s, 1000 concorrentes · 1 tentativas · repos: aida-back
- `aida-temperature` · 10/s, 10 concorrentes · 3 tentativas · **PAUSED** · repos: aida-back
- `aida-transference` · 500/s, 1000 concorrentes · 100 tentativas · repos: aida-back
- `aida-update-ticket` · 60/s, 120 concorrentes · 3 tentativas · repos: aida-back
- `aida-ura-inteligente` · 10/s, 10 concorrentes · 3 tentativas · repos: aida-back
- `central-disparos-pos-evento` · 50/s, 40 concorrentes · 10 tentativas
- `contador-inteligente-off-jump-followup` · 5/s, 10 concorrentes · 5 tentativas
- `contador-inteligente-off-prepare` · 10/s, 10 concorrentes · 1 tentativas
- `contador-inteligente-off-process` · 10/s, 10 concorrentes · 5 tentativas
- `ext-bigquery-export-auto-queries-config-initBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas · **PAUSED**
- `ext-bigquery-export-auto-queries-config-setupBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas · **PAUSED**
- `ext-bigquery-export-auto-queries-config-syncBigQuery` · 100/s, 500 concorrentes · 5 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-all-documents-initBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-all-documents-setupBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-all-documents-syncBigQuery` · 100/s, 500 concorrentes · 5 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-chat-initBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-chat-setupBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-chat-syncBigQuery` · 100/s, 500 concorrentes · 5 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-fsimportexistingdocs` · 500/s, 1000 concorrentes · 15 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-initBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas
- `ext-firestore-bigquery-export-local-initBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-local-setupBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-local-syncBigQuery` · 100/s, 500 concorrentes · 5 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-pxwf-initBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-pxwf-setupBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-pxwf-syncBigQuery` · 100/s, 500 concorrentes · 5 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-setupBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas
- `ext-firestore-bigquery-export-syncBigQuery` · 100/s, 500 concorrentes · 5 tentativas
- `ext-firestore-bigquery-export-to-sandobox-initBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-to-sandobox-setupBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-to-sandobox-syncBigQuery` · 100/s, 500 concorrentes · 5 tentativas · **PAUSED**
- `ext-vai-porcao-initBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas
- `ext-vai-porcao-setupBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas
- `ext-vai-porcao-syncBigQuery` · 100/s, 500 concorrentes · 5 tentativas
- `file-transcriber-audio` · 500/s, 1000 concorrentes · 100 tentativas
- `file-transcriber-doc` · 500/s, 1000 concorrentes · 100 tentativas
- `file-transcriber-img` · 500/s, 1000 concorrentes · 100 tentativas
- `file-transcriber-v2` · 10/s, 10 concorrentes · 100 tentativas · repos: file-transcriber
- `inbound-outbound-event-aggregation` · 3/s, 3 concorrentes · 5 tentativas
- `monitoria-ia-aggregator-checker` · 10/s, 10 concorrentes · 10 tentativas
- `sentinela-default` · 50/s, 100 concorrentes · 10 tentativas
- `sentinela-orphan-messages` · 500/s, 500 concorrentes · 3 tentativas
- `sentinela-transfer` · 500/s, 1000 concorrentes · 100 tentativas
- `sentinela-transferred-ticket-review` · 5/s, 5 concorrentes · 3 tentativas
- `sentinela-validation` · 500/s, 100 concorrentes · 5 tentativas
- `monitoria-ia-agregador` (us-east1) · 10/s, 10 concorrentes · 10 tentativas · repos: monitoria-ia
- `monitoria-ia-executor` (us-east1) · 10/s, 10 concorrentes · 3 tentativas · repos: monitoria-ia

## aida-prd

AIDA, prod.

- `aida-analise-mensagem-travada` · 40/s, 120 concorrentes · 5 tentativas · repos: aida-back
- `aida-analise-temas-resposta` · 40/s, 240 concorrentes · 3 tentativas
- `aida-analise-transferencia` · 10/s, 10 concorrentes · 3 tentativas · repos: aida-back
- `aida-autopilot` · 30/s, 90 concorrentes · 3 tentativas · repos: aida-back
- `aida-autopilot-new-message` · 20/s, 120 concorrentes · 10 tentativas · repos: aida-back
- `aida-classifier` · 50/s, 150 concorrentes · 10 tentativas · repos: aida-back, aida-classifier, pipeline
- `aida-classifier-manutencao` · 5/s, 10 concorrentes · 10 tentativas
- `aida-classifier-outbound` · 1/s, 3 concorrentes · 10 tentativas
- `aida-classifier-reprocessamento` · 20/s, 20 concorrentes · 10 tentativas
- `aida-consulta-meu-cnpj` · 50/s, 100 concorrentes · 4 tentativas
- `aida-controle-ticket` · 60/s, 120 concorrentes · 3 tentativas · repos: aida-back
- `aida-despedida` · 30/s, 60 concorrentes · 3 tentativas · repos: aida-back
- `aida-encerramento` · 20/s, 120 concorrentes · 3 tentativas · repos: aida-back
- `aida-extratos` · 30/s, 90 concorrentes · 3 tentativas · repos: aida-back
- `aida-funcoes-agendadas` · 50/s, 120 concorrentes · 10 tentativas · repos: aida-back
- `aida-fup` · 5/s, 10 concorrentes · 5 tentativas
- `aida-instabilidade-emissao-notas` · 60/s, 120 concorrentes · 2 tentativas
- `aida-jobs-default` · 10/s, 10 concorrentes · 1 tentativas · repos: aida-back
- `aida-memoria-process` · 5/s, 20 concorrentes · 5 tentativas · repos: pipeline
- `aida-message-separator` · 500/s, 1000 concorrentes · 10 tentativas · repos: aida-back
- `aida-nf-emissao` · 10/s, 10 concorrentes · 3 tentativas · repos: aida-back
- `aida-nf-emissao-callback` · 10/s, 10 concorrentes · 3 tentativas · repos: aida-back
- `aida-processamento-msg` · 10/s, 10 concorrentes · 3 tentativas · repos: aida-back
- `aida-queue` · 60/s, 120 concorrentes · 3 tentativas · repos: aida-back
- `aida-router-fila` · 10/s, 10 concorrentes · 6 tentativas · repos: aida-back
- `aida-score` · 10/s, 10 concorrentes · 3 tentativas · repos: aida-back
- `aida-simulador` · 500/s, 1000 concorrentes · 100 tentativas · repos: aida-back
- `aida-tag` · 60/s, 120 concorrentes · 3 tentativas · repos: aida-back
- `aida-temperature` · 10/s, 10 concorrentes · 3 tentativas · repos: aida-back
- `aida-transference` · 20/s, 120 concorrentes · 10 tentativas · repos: aida-back
- `aida-update-ticket` · 60/s, 120 concorrentes · 3 tentativas · repos: aida-back
- `aida-ura-inteligente` · 50/s, 50 concorrentes · 3 tentativas · repos: aida-back
- `central-disparos-pos-evento` · 50/s, 40 concorrentes · 10 tentativas
- `contador-inteligente-off-jump-followup` · 5/s, 10 concorrentes · 5 tentativas
- `contador-inteligente-off-prepare` · 20/s, 50 concorrentes · 1 tentativas
- `contador-inteligente-off-process` · 20/s, 50 concorrentes · 5 tentativas
- `ext-firestore-bigquery-export-fsimportexistingdocs` · 500/s, 1000 concorrentes · 15 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-initBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-setupBigQuerySync` · 500/s, 1000 concorrentes · 15 tentativas · **PAUSED**
- `ext-firestore-bigquery-export-syncBigQuery` · 100/s, 500 concorrentes · 5 tentativas · **PAUSED**
- `file-transcriber-v2` · 500/s, 30 concorrentes · 100 tentativas · repos: file-transcriber
- `inbound-outbound-event-aggregation` · 3/s, 3 concorrentes · 5 tentativas
- `monitoria-ia-agregador` · 5/s, 5 concorrentes · 10 tentativas · repos: monitoria-ia
- `monitoria-ia-executor` · 5/s, 5 concorrentes · 10 tentativas · repos: monitoria-ia
- `sentinela-default` · 50/s, 100 concorrentes · 10 tentativas
- `sentinela-orphan-messages` · 500/s, 500 concorrentes · 3 tentativas
- `sentinela-transfer` · 500/s, 1000 concorrentes · 100 tentativas
- `sentinela-transferred-ticket-review` · 10/s, 10 concorrentes · 3 tentativas
- `sentinela-validation` · 500/s, 500 concorrentes · 100 tentativas
- `monitoria-ia-agregador` (us-east1) · 5/s, 5 concorrentes · 10 tentativas · repos: monitoria-ia
- `monitoria-ia-executor` (us-east1) · 20/s, 50 concorrentes · 3 tentativas · repos: monitoria-ia

## contabilizeiapp-dev-02

App Contabilizei, dev.

- `aceite-portabilidade-queue` · 10/s, 10 concorrentes · 3 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `acesso-simples-queue` · 1/s, 50 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `agendamento-importacao-notas-queue` · 20/s, 20 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `agendamento-queue` · 30/s, 30 concorrentes · 6 tentativas · repos: contabilizei-back-core, ctbzapp-utils, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `alterar-regime-empresa` · 10/s, 10 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `ativacao-contabil-histocio` · 40/s, 40 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `ativacao-empresa` · 10/s, 50 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `ativar-empresa-mei` · 10/s, 50 concorrentes · 8 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `atualizacao-cnae-anexo-massivo-queue` · 10/s, 10 concorrentes · 6 tentativas · App Engine `importacao-notas-worker` · repos: plataforma-app-config, plataforma-importacao-notas-worker
- `atualizar-campos-jira-processo-migracao-queue` · 3/s, 3 concorrentes · 1 tentativas · repos: contabilizei-back-core, plataforma-app-config
- `atualizar-contratos-empresa-queue` · 10/s, 10 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `audit-queue` · 5/s, 5 concorrentes · 6 tentativas · **PAUSED** · repos: contabilizei-back-core, contabilizei-pagamentos
- `auditoria-das-queue` · 10/s, 40 concorrentes · 3 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-faturamento-worker, plataforma-monolito
- `backup-kind-queue` · 5/s, 5 concorrentes · 4 tentativas · repos: plataforma-app-config, plataforma-monolito
- `backup-queue` · 10/s, 20 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `bank-integration-first-of-month-run` · 10/s, 20 concorrentes · 4 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `bigquery-exporter-queue` · 10/s, 5 concorrentes · 2 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `cadastro-automatico-queue` · 10/s, 50 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `calcular-grupo-nota-tomada-queue` · 30/s, 30 concorrentes · 11 tentativas · App Engine `importacao-notas-worker` · repos: contabilizei-back-core, plataforma-app-config
- `calculo-faturamento-queue` · 20/s, 20 concorrentes · 6 tentativas · App Engine `faturamento-worker` · repos: plataforma-app-config, plataforma-faturamento-worker
- `call-back-obrigacao` · 30/s, 48 concorrentes · 3 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `carregar-notificar-faturamento-zero` · 10/s, 10 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `carregarDados-queue` · 10/s, 10 concorrentes · 3 tentativas · repos: contabilizei-abertura, contabilizei-abertura-BB, contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `central-rotinas-queue` · 7/s, 15 concorrentes · 1 tentativas · App Engine `plataforma-central-rotinas` · repos: plataforma-app-config
- `certificado-digital` · 5/s, 50 concorrentes · 3 tentativas · repos: aida-back, atendimento-canais-admin, atendimento-zendesk, contabilizei-abertura, contabilizei-abertura-BB, contabilizei-back-core, contabilizei-crm-widget-window, contabilizei-front, contabilizei-front-vue, experts-scripts, pipeline, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-monolito, plataforma-web
- `cnae-queue` · 10/s, 2 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `cnd-queue` · 5/s, 2 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `cobranca-avulsa-jira` · 0.666666667/s, 50 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `comunicacao-fechamento-balanco` · 10/s, 10 concorrentes · 6 tentativas · repos: plataforma-app-config, plataforma-monolito
- `conciliador-escrituracao-reenvio-eventos` · 3/s, 2 concorrentes · 2 tentativas · App Engine `crm-web` · repos: plataforma-app-config
- `conclusao-importacao-comercio-queue` · 30/s, 30 concorrentes · 11 tentativas · App Engine `importacao-comercio-worker` · repos: contabilizei-back-core, plataforma-app-config
- `conclusao-importacao-queue` · 30/s, 30 concorrentes · 11 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `correcao-movimentacao` · 20/s, 10 concorrentes · 4 tentativas · repos: contabilizei-back-core, contabilizei-movimentacao-back, plataforma-app-config, plataforma-monolito
- `criar-obrigacao` · 30/s, 50 concorrentes · 3 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `criar-obrigacao-defis` · 15/s, 20 concorrentes · 4 tentativas · App Engine `obrigacoes-worker` · repos: plataforma-app-config
- `crm-custom` · 20/s, 50 concorrentes · 3 tentativas · App Engine `crm-web` · repos: plataforma-app-config, plataforma-crm-web
- `crm-default` · 20/s, 50 concorrentes · 3 tentativas · **PAUSED** · App Engine `crm-web`
- `darf-pagamento` · 5/s, 3 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `das-pagamento` · 0.333333333/s, 3 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `das-queue` · 20/s, 50 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `default` · 3/s, 2 concorrentes · tentativas ilimitadas
- `dte-queue` · 10/s, 10 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `email-boas-vindas-csa` · 1/s, 1 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `email-follow-certificado` · 10/s, 20 concorrentes · 3 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `emissao-nota-fiscal-contabilizei` · 0.666666667/s, 10 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `emissao-notas-async` · 0.666666667/s, 5 concorrentes · 6 tentativas · App Engine `importacao-notas-worker`
- `empresa-queue` · 10/s, 10 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `enviar-email-finalizacao-abertura-queue` · 0.166666667/s, 10 concorrentes · 2 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `escrituracao-processamento-evento` · 1/s, 1 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `escrituracao-queue` · 10/s, 40 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `ev-custom` · 20/s, 50 concorrentes · 3 tentativas · App Engine `escritorio-virtual` · repos: plataforma-app-config
- `execucao-importacao-comercio-queue` · 40/s, 40 concorrentes · 11 tentativas · App Engine `importacao-comercio-worker` · repos: contabilizei-back-core, plataforma-app-config
- `execucao-importacao-queue` · 40/s, 40 concorrentes · 11 tentativas · App Engine `importacao-notas-worker` · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `fast-obrigacao-queue` · 30/s, 48 concorrentes · 3 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `fator-r` · 5/s, 20 concorrentes · 3 tentativas · **PAUSED**
- `faturamento-queue` · 20/s, 20 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `fechamento-exercicio` · 10/s, 5 concorrentes · 6 tentativas · repos: contabilizei-back-core, contabilizei-front, contabilizei-front-admin, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `fechamento-exercicio-auto` · 40/s, 40 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `fintech-criacao-contas` · 5/s, 50 concorrentes · 3 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `fintech-processos-consultas` · 5/s, 20 concorrentes · 3 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito, plataforma-web
- `firebase-callback-queue` · 30/s, 5 concorrentes · 11 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `fiscal-queue` · 30/s, 30 concorrentes · 11 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `folha-atualizacao-colaborador` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-atualizacao-tipo-folha` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-cancelamento` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-coloca-em-calculo` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-criacao-movimento` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-criacao-novo-colaborador` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-dispara-integracoes` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-distribuicao-prolabore` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-empresa-persistencia` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-evento-finalizacao` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-executa-calculo` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-finalizacao` · 20/s, 40 concorrentes · 5 tentativas · repos: plataforma-app-config
- `folha-finalizacao-desmembramento` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-finalizacao-mes-atual` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-geracao` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-gerar-avulsa` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-historico-prolabore` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-importacao` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-movimentos` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-notificacao-data-limite-queue` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-notificacao-dissidio-fopag-queue` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-notificacao-ferias-fopag-queue` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-notificacao-holerite-queue` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-notificacao-queue` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-qualidade-cadastral` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-queue` · 20/s, 40 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `folha-totais-decimo-terceiro` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `folha-totalizacao` · 20/s, 40 concorrentes · 7 tentativas · repos: plataforma-app-config
- `gerar-arquivo-obrigacao` · 30/s, 20 concorrentes · 3 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `gerar-pdf-aceite-queue` · 10/s, 40 concorrentes · 3 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `gps-pagamento` · 5/s, 3 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `importacao-auto-nfse-queue` · 20/s, 20 concorrentes · 11 tentativas · **PAUSED** · repos: plataforma-monolito
- `importacao-automatica-nfse-queue` · 80/s, 80 concorrentes · 11 tentativas · App Engine `importacao-notas-worker` · repos: contabilizei-back-core, plataforma-app-config
- `importacao-automatica-notas-tomadas-queue` · 8/s, 8 concorrentes · 11 tentativas · App Engine `importacao-notas-worker` · repos: plataforma-app-config, plataforma-importacao-notas-worker
- `importacao-comercio-queue` · 30/s, 30 concorrentes · 11 tentativas · App Engine `importacao-comercio-worker` · repos: contabilizei-back-core, plataforma-app-config
- `importacao-ofx` · 20/s, 20 concorrentes · 1 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `importacao-queue` · 30/s, 30 concorrentes · 11 tentativas · App Engine `importacao-notas-worker` · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `imposto-comercio-queue` · 0.666666667/s, 10 concorrentes · 11 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `iss-queue` · 10/s, 10 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `jira-queue` · 5/s, 1 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `limpar-mes-contabil` · 10/s, 10 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `lucro-presumido-queue` · 30/s, 10 concorrentes · 7 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `mes-contabil-queue` · 3/s, 2 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `mobile-bff-default` · 5/s, 20 concorrentes · 3 tentativas · App Engine `plataforma-mobile-bff` · repos: plataforma-app-config
- `mobile-default` · 5/s, 20 concorrentes · 3 tentativas · repos: plataforma-app-config
- `mobile-init` · 5/s, 20 concorrentes · 3 tentativas · **PAUSED**
- `modulo-impostos-queue` · 20/s, 20 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `nfe-entrada-queue` · 10/s, 20 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `notificacao-queue` · 2/s, 10 concorrentes · 6 tentativas · repos: contabilizei-back-core, ctbzapp-utils, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `notificacao-worker-queue` · 4/s, 2 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `obrigacao-agendamento` · 30/s, 50 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `obrigacao-queue` · 30/s, 48 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `obrigacao-queue-manual` · 30/s, 48 concorrentes · 3 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `obrigacao-recibo-impostos-queue` · 10/s, 10 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `obrigacoes-core-fast-queue` · 30/s, 48 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `obrigacoes-core-queue` · 1/s, 10 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `obrigacoes-iss-poa-finalizacao-queue` · 5/s, 20 concorrentes · 2 tentativas · App Engine `obrigacoes-worker` · repos: plataforma-app-config
- `obrigacoes-iss-poa-transmissao-queue` · 0.2/s, 2 concorrentes · 2 tentativas · App Engine `obrigacoes-worker` · repos: plataforma-app-config
- `obrigacoes-iss-rj-queue` · 0.2/s, 2 concorrentes · 21 tentativas · App Engine `obrigacoes-worker` · repos: plataforma-app-config
- `optimize-queue` · 10/s, 40 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `pagamentos-service-queue` · 10/s, 50 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `particionamento-notas-queue` · 10/s, 20 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `pendencia-exclusao-simples-nacional-queue` · 10/s, 2 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `pesquisa-usuario-queue` · 20/s, 4 concorrentes · 2 tentativas · App Engine `pesquisa-usuario` · repos: plataforma-app-config
- `processa-lancamento-contabil-bk-queue` · 10/s, 10 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `processamento-dctfweb` · 30/s, 20 concorrentes · 3 tentativas · App Engine `obrigacoes-worker` · repos: plataforma-app-config
- `processamento-ecd` · 30/s, 20 concorrentes · 3 tentativas · App Engine `obrigacoes-worker` · repos: plataforma-app-config
- `processamento-impostos-queue` · 10/s, 20 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-faturamento-worker, plataforma-monolito
- `processamento-mit` · 30/s, 20 concorrentes · 3 tentativas · App Engine `obrigacoes-worker` · repos: plataforma-app-config
- `processamento-paginacao-dctfweb` · 30/s, 20 concorrentes · 3 tentativas · App Engine `obrigacoes-worker` · repos: plataforma-app-config
- `processamento-paginacao-ecd` · 30/s, 20 concorrentes · 3 tentativas · App Engine `obrigacoes-worker` · repos: plataforma-app-config
- `processamento-paginacao-mit` · 30/s, 20 concorrentes · 3 tentativas · App Engine `obrigacoes-worker` · repos: plataforma-app-config
- `processar-elegibilidade-defis` · 15/s, 20 concorrentes · 4 tentativas · App Engine `obrigacoes-worker` · repos: plataforma-app-config
- `processar-recibo-obrigacao` · 30/s, 48 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `processar-transmissao-queue` · 10/s, 40 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `push-notification` · 5/s, 20 concorrentes · 3 tentativas · repos: contabilizei-pagamentos, plataforma-app-config, plataforma-faturamento-worker, plataforma-importacao-notas-worker
- `qc-queue` · 10/s, 5 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `qc-queue-slow` · 1/s, 1 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `recibo-queue` · 0.5/s, 5 concorrentes · 2 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `regime-tributario-queue` · 0.016666667/s, 2 concorrentes · 3 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `relatorio-contabil-queue` · 10/s, 50 concorrentes · 11 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `salvar-novo-onboarding-queue` · 10/s, 10 concorrentes · 3 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `sedex-queue` · 1/s, 1 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `simulador-plano-saude` · 1/s, 1 concorrentes · 3 tentativas · App Engine `canais-xp-worker` · repos: pipeline, plataforma-app-config, plataforma-crm-web
- `simular-gatilho-processar-empresa-defis` · 15/s, 20 concorrentes · 4 tentativas · App Engine `obrigacoes-worker` · repos: plataforma-app-config
- `simular-gatilho-processar-lote-defis` · 15/s, 20 concorrentes · 4 tentativas · App Engine `obrigacoes-worker` · repos: plataforma-app-config
- `sincronizar-contabil-queue` · 10/s, 20 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `tarefas-depois-fechamento-queue` · 5/s, 5 concorrentes · 2 tentativas · App Engine `escrituracao-worker` · repos: plataforma-app-config
- `transmitir-obrigacao` · 30/s, 20 concorrentes · 3 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `upload-obrigacao` · 30/s, 48 concorrentes · 3 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `validacao-comercio-queue` · 0.333333333/s, 1 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `validacao-importacao-queue` · 30/s, 30 concorrentes · 11 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `validacao-queue` · 10/s, 5 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `verificador-pendencias-queue` · 10/s, 20 concorrentes · 6 tentativas · repos: contabilizei-back-core, plataforma-app-config, plataforma-monolito
- `verificar-prefeitura-queue` · 40/s, 10 concorrentes · 6 tentativas · repos: plataforma-app-config
- `zendesk-queue` · 10/s, 2 concorrentes · 4 tentativas · repos: contabilizei-abertura, contabilizei-abertura-BB, contabilizei-back-core, ctbzapp-utils, plataforma-app-config, plataforma-back-worker, plataforma-central-rotinas, plataforma-crm-web, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- `zendesk-sincronizar-organizacao-queue` · 2/s, 2 concorrentes · 4 tentativas · repos: plataforma-app-config, plataforma-back-worker
- `zendesk-sincronizar-usuario-queue` · 2/s, 2 concorrentes · 4 tentativas · repos: plataforma-app-config, plataforma-back-worker

## Sem acesso para listar

Sem permissão para listar Cloud Tasks em: `atendimento-canais-dev`, `atendimento-canais-prd`, `contabilizei-abertura`, `contabilizei-crm`, `contabilizei-crm-dev`, `contabilizei-dev-01`, `contabilizei-impostos`, `contabilizei-impostos-teste`, `contabilizei-issue`, `contabilizei-prod-01`, `contabilizeiapp`, `fintech-228118`.
