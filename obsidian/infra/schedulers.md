---
name: schedulers
description: "Cloud Scheduler: agendamentos por projeto GCP com cron, alvo (Pub/Sub, HTTP, App Engine) e repositórios que citam cada job"
metadata:
  type: reference
tags:
  - infra
  - scheduler
atualizado_em: 2026-10-09
---

# Cloud Scheduler

Fotografia de 2026-10-09. Formato: job · cron (fuso) · alvo · estado se não estiver ativo · repositórios que citam o nome do job.

## atendimento-canais-dev

Atendimento / canais, dev.

- `ms-agrupamento-guias-cron-notify-email` · `0 03,12 15,16,17,18,19 * *` (America/Sao_Paulo) · GET `api-dev.contabilizei.com.br/agrupamento-guias/notificacao/envia-lote/grupo-guia/experts/EMAIL` · repos: microsservico-agrupamento-guias
- `ms-agrupamento-guias-cron-notify-email-bp-lp` · `0 04,13 15,16,17,18,19 * *` (America/Sao_Paulo) · GET `api-dev.contabilizei.com.br/agrupamento-guias/notificacao/envia-lote/grupo-guia/bp-lp/EMAIL` · repos: microsservico-agrupamento-guias
- `ms-agrupamento-guias-cron-notify-wpp` · `0 09,15 15,16,17,18,19 * *` (America/Sao_Paulo) · GET `api-dev.contabilizei.com.br/agrupamento-guias/notificacao/envia-lote/grupo-guia/experts/WHATSAPP` · repos: microsservico-agrupamento-guias
- `ms-agrupamento-guias-cron-notify-wpp-bp-lp` · `0 10 15,16,17,18,19 * *` (America/Sao_Paulo) · GET `api-dev.contabilizei.com.br/agrupamento-guias/notificacao/envia-lote/grupo-guia/bp-lp/WHATSAPP` · repos: microsservico-agrupamento-guias
- `ms-agrupamento-guias-cron-reprocess-group` · `30 02 16,17,18,19 * *` (America/Sao_Paulo) · GET `api-dev.contabilizei.com.br/agrupamento-guias/agrupamento-guias/reprocessa-erros` · repos: microsservico-agrupamento-guias

## atendimento-canais-prd

Atendimento / canais, prod.

- `ms-agrupamento-guias-cron-notify-email` · `0 03,12 15,16,17,18,19 * *` (America/Sao_Paulo) · GET `api-gateway.contabilizei.com/agrupamento-guias/notificacao/envia-lote/grupo-guia/experts/EMAIL` · repos: microsservico-agrupamento-guias
- `ms-agrupamento-guias-cron-notify-email-bp-lp` · `0 04,13 15,16,17,18,19 * *` (America/Sao_Paulo) · GET `api-gateway.contabilizei.com/agrupamento-guias/notificacao/envia-lote/grupo-guia/bp-lp/EMAIL` · repos: microsservico-agrupamento-guias
- `ms-agrupamento-guias-cron-notify-wpp` · `0 09,15 15,16,17,18,19 * *` (America/Sao_Paulo) · GET `api-gateway.contabilizei.com/agrupamento-guias/notificacao/envia-lote/grupo-guia/experts/WHATSAPP` · repos: microsservico-agrupamento-guias
- `ms-agrupamento-guias-cron-notify-wpp-bp-lp` · `0 10 15,16,17,18,19 * *` (America/Sao_Paulo) · GET `api-gateway.contabilizei.com/agrupamento-guias/notificacao/envia-lote/grupo-guia/bp-lp/WHATSAPP` · repos: microsservico-agrupamento-guias
- `ms-agrupamento-guias-cron-reprocess-group` · `30 02 16,17,18,19 * *` (America/Sao_Paulo) · GET `api-gateway.contabilizei.com/agrupamento-guias/agrupamento-guias/reprocessa-erros` · repos: microsservico-agrupamento-guias
- `webhook-gitlab-canais-past-mr-reminder` · `0 10 * * 1,3,5` (America/Sao_Paulo) · POST Cloud Run `webhook-gitlab` /reminder · repos: webhook-gitlab
- `webhook-gitlab-canais-today-mr-needs-attention` · `0 12,16 * * 1-5` (America/Sao_Paulo) · POST Cloud Run `webhook-gitlab` /reminder/needs-attention · repos: webhook-gitlab
- `webhook-gitlab-canais-today-mr-reminder` · `0 11-17/2 * * 1-5` (America/Sao_Paulo) · POST Cloud Run `webhook-gitlab` /reminder · repos: webhook-gitlab

## contabilizei-experts-dev

Experts, dev.

- `cashflow-generate` · `0 4 * * 0` (America/Sao_Paulo) · GET Cloud Run `experts-contabil` /api/v1/cashflow/trigger-all/generate · **PAUSED** · repos: experts-contabil
- `cashflow-pre-routine` · `0 19 * * 6` (America/Sao_Paulo) · GET Cloud Run `experts-contabil` /api/v1/cashflow/trigger-all/pre-routine · **PAUSED**
- `executar_task_scheduler` · `*/10 * * * *` (America/Sao_Paulo) · GET `api-dev.contabilizei.com.br/experts-service/v1/task-scheduler` · **PAUSED** · repos: experts-service
- `experts-clientes-emails-scheduler` · `0 8 * * 5` (America/Sao_Paulo) · POST Cloud Run `function-experts-clientes-emails` /scheduler · **PAUSED**
- `experts-nfs-monitoring-check-queue` · `* * * * *` (America/Sao_Paulo) · POST Cloud Run `experts-nfs` /v3/monitoring/cloud-task · **PAUSED** · repos: experts-nfs
- `pendencias-oportunidades-scheduler` · `9 0 5-12 * *` (America/Sao_Paulo) · POST Cloud Run `function-pendencias-oportunidades` /scheduler · **PAUSED** · repos: experts-dominios-functions, experts-functions
- `tarefas-organicas` · `0 8 * * 1-5` (America/Sao_Paulo) · GET Cloud Run `experts-zendesk` /api/v1/autoclose-tickets/start-autoclose · **PAUSED** · repos: experts-tarefas-assessor, experts-zendesk

## contabilizei-experts-prd

Experts, prod.

- `cashflow-generate` · `0 8 * * 1` (America/Sao_Paulo) · GET Cloud Run `experts-contabil` /api/v1/cashflow/trigger-all/generate · **PAUSED** · repos: experts-contabil
- `cashflow-pre-routine` · `0 9 * * 0` (America/Sao_Paulo) · GET Cloud Run `experts-contabil` /api/v1/cashflow/trigger-all/pre-routine · **PAUSED**
- `cashflow-rotina-belvo` · `0 08 * * 0` (America/Sao_Paulo) · GET Cloud Run `experts-contabil` /api/v1/cashflow/importacao-semanal/bancos-externos/trigger-all · **PAUSED**
- `cashflow-rotina-extrato-bank` · `10 08 * * 0` (America/Sao_Paulo) · GET Cloud Run `experts-contabil` /api/v1/cashflow/importacao-semanal/bancos-externos/trigger-all · **PAUSED**
- `executar_task_scheduler` · `*/10 * * * *` (America/Sao_Paulo) · GET `api.contabilizei.com.br/experts-service/v1/task-scheduler` · repos: experts-service
- `experts-clientes-emails-scheduler` · `0 8 * * 5` (America/Sao_Paulo) · POST Cloud Run `function-experts-clientes-emails` /scheduler
- `experts-nfs-monitoring-check-queue` · `* 9-20 * * *` (America/Sao_Paulo) · POST Cloud Run `experts-nfs` /v3/monitoring/cloud-task · repos: experts-nfs
- `pendencias-oportunidades-scheduler` · `9 0 5-12 * *` (America/Sao_Paulo) · POST Cloud Run `function-pendencias-oportunidades` /scheduler · **PAUSED** · repos: experts-dominios-functions, experts-functions
- `scheduler-notas-recorrentes` · `0 10,14,18,22 * * *` (America/Sao_Paulo) · POST Cloud Run `experts-nfs` /v1/worker/notas-recorrentes/scheduler
- `tarefas-organicas` · `00 10 * * 1-5` (America/Sao_Paulo) · GET Cloud Run `experts-zendesk` /api/v1/autoclose-tickets/start-autoclose · repos: experts-tarefas-assessor, experts-zendesk
- `zendesk-organizations-update` · `0 8 * * *` (America/Sao_Paulo) · GET Cloud Run `function-zendesk-organizations-update` /trigger · **PAUSED**
- `transfer-tasks-Hub-to-corujao` (us-east1) · `30 22 * * 1-4` (America/Sao_Paulo) · GET `experts.contabilizei.com.br/api/twilio/v1/experts-gateway/task-transfer/fromHubToCorujao` · **PAUSED**
- `transfer-tasks-corujao` (us-east1) · `59 7 * * 1-5` (America/Sao_Paulo) · GET `experts.contabilizei.com.br/api/twilio/v1/experts-gateway/task-transfer/fromCorujaoToAnalistas` · **PAUSED**
- `transfer-tasks-corujao-remaining` (us-east1) · `1 8 * * 1-5` (America/Sao_Paulo) · GET `experts.contabilizei.com.br/api/twilio/v1/experts-gateway/task-transfer/fromCorujaoToAnalistas` · **PAUSED**

## contabilizei-impostos-teste

Impostos, dev.

- `Reexecucaomensaldosstatus` (southamerica-east1) · `0 6 24 * *` (America/Sao_Paulo) · Pub/Sub `reexecutar-status-pre-fator-r` · **PAUSED**
- `codigos-tributarios-confronto-diario` (southamerica-east1) · `0 2 * * *` (America/Sao_Paulo) · POST `api-dev.contabilizei.com.br/codigos-tributarios/auditoria/divergencias/executar`
- `gestao-eventos-snh-publicacao-modalidade` (southamerica-east1) · `*/5 * * * *` (America/Sao_Paulo) · Pub/Sub `snh-alteracao-modalidade-trigger`
- `reexecucao-diaria-pre-motor-fator-r` · `*/5 * * * *` (America/Sao_Paulo) · Pub/Sub `reexecutar-status-pre-fator-r` · **PAUSED**

## contabilizei-impostos

Impostos, prod.

- `codigos-tributarios-confronto-diario` (southamerica-east1) · `0 2 * * *` (America/Sao_Paulo) · POST `api.contabilizei.com.br/codigos-tributarios/auditoria/divergencias/executar`
- `gestao-eventos-snh-publicacao-modalidade` (southamerica-east1) · `*/5 * * * *` (America/Sao_Paulo) · Pub/Sub `snh-alteracao-modalidade-trigger`
- `reexecucao-diaria-pre-motor-fator-r` (southamerica-east1) · `0 4 * * *` (America/Sao_Paulo) · Pub/Sub `reexecutar-status-pre-fator-r`
- `reexecucao-mensal-pre-motor-fator-r` (southamerica-east1) · `0 6 24 * *` (America/Sao_Paulo) · Pub/Sub `reexecutar-status-pre-fator-r`

## Sem acesso para listar

Sem permissão para listar Cloud Scheduler em: `aida-prd`, `aida-stg`, `contabilizei-abertura`, `contabilizei-crm`, `contabilizei-crm-dev`, `contabilizei-issue`, `contabilizeiapp`, `fintech-228118`. Nesses domínios, agendamentos também podem ser CronJobs no GKE (ver [[gke-workloads]]).
