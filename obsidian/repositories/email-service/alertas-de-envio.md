---
name: email-service-alertas-de-envio
description: "Como o email-service alerta envios com falha: card no Google Chat, policies do Cloud Monitoring que restam e subscriptions de inspeção"
metadata:
  type: reference
tags:
  - email-service
  - alertas
---

# Alertas de envio do email-service

- **Card no Google Chat** (`AlertSendFailureUsecase` + `src/domain/sender/helpers/send-alert-card.helper.ts`, webhook em `GCHAT_ALERTS_WEBHOOK`): cobre `INVALID_PAYLOAD`, `VALIDATION_HANDLER_ERROR` e `REPLICATION_NOT_FOUND`. É best-effort e deduplicado por janela de 10 minutos (só informa quantos casos iguais foram suprimidos).
- **Subscriptions de inspeção** em `terraform/prd/pubsub.sender.tf` (`email-service.p2p.send-email-callback.{invalid-payload,validation-error,replication-not-found}.sub`): sem consumidor, retenção de 24h. Como esses envios não têm linha em `email_replications`, o `gcloud pubsub subscriptions pull <sub> --project=atendimento-canais-prd --limit=10 --format=json` (sem ack, não consome) é o único lugar com cada envio individual (`messageId`, `application`, `status`, `reason`, `failure_reason`).
- **Policies do Cloud Monitoring** em `terraform/prd/monitoring.tf`, notificando o canal "GCP Alerts (CANAIS)": `smtp_unavailable`, `pubsub_oldest_unacked` e `pubsub_dlq`. A policy `send_email_unrecorded` ("envio recusado ou sem registro") foi removida no work-item #50 (out/2026) por duplicar o card.

## Armadilha

O `terraform plan` de prd usa o state no bucket `ctbz-terraform-state` (prefixo `email-service/production`), e o usuário não tem `storage.objects.list` nele: o plan só roda na pipeline. Localmente dá para validar com `terraform init -backend=false && terraform validate`.

## Armadilha: banco fora do ar vira "Falha ao validar o e-mail" e o envio é perdido

O `errorHandler` do `ValidationWorker` (`src/domain/sender/consumers/validation.worker.ts`) manda qualquer exceção para o `ValidationErrorUsecase`, que publica o callback `INVALID_PAYLOAD` com `failure_reason: VALIDATION_HANDLER_ERROR`, dispara o card e dá **ack**: não há retry. Então uma indisponibilidade do banco (ex: `Failed query: select ... from "email_templates" ...` com causa `Connection terminated due to connection timeout`) descarta o envio, sem linha em `email_replications`. O `CallbackWorker`, ao contrário, dá nack em erro não permanente e se recupera sozinho.

O experts-service (que publica no `email-service.p2p.send-email` a partir de `schedule-notification-email-task.service.ts`) não consome o callback, então também não reenvia. O callback não carrega o payload original (destinatário/variáveis): para reenviar, é preciso partir do experts-service.

Caso real em 09/11/2026 07:10 BRT: 2 envios do template `exp-email-guia-imposto-avulsa-v1` (messageIds `23323413534788818` e `23323087492834880`) perdidos durante a habilitação de HA na instância Cloud SQL (ver [[cloud-sql-alteracoes-com-restart]]). Correção sugerida: no `errorHandler`, dar nack em erro transitório (conexão/timeout) em vez de tratar como payload inválido.

**Como recuperar um envio do experts-service perdido assim:** o payload inteiro (destinatário, variáveis, template) fica na tabela `task_scheduler` do experts-service (`prd_experts_experts_service`, proxy `sql_exp_prd`), com `topic = 'email-service.p2p.send-email'` e `sent_date` = hora da publicação. Os logs do email-service não trazem o payload, e o tópico não tem retenção (`messageRetentionDuration` vazio, subscription sem `retainAckedMessages`), então seek não funciona. Para achar os perdidos, cruzar os `cnpj` das tarefas publicadas na janela com `email_replications` (`application = 'experts-service'`): o que não tiver linha se perdeu. No caso de 09/11/2026, eram as tarefas 522075 e 522077, publicadas às 10:10:11 UTC; as outras 52, de 10:00:33, ficaram SENT. Para reenviar, publicar o `data` da tarefa como está em `email-service.p2p.send-email` (`atendimento-canais-prd`), sem atributos: é o mesmo que o `ScheduledTasksPublisher` faz. Não reabrir a tarefa com `is_sent = false`, porque o banco de prd é só leitura. Feito assim em 09/11/2026 às 13:57 BRT (PRD-175908): os dois saíram SENT cerca de 5 s depois da publicação, com os novos messageIds 22541706733970787 e 22542033367926288.

**Corrigido no work-item #52** (branch `fix/validation-transient-retry`, nov/2026, aguardando MR/merge): o `errorHandler` só manda direto para o `ValidationErrorUsecase` (com ack) quando `data === undefined` ou `isPermanentFailure(error)`. O resto é nacado; a subscription `email-service.p2p.send-email.sub` tem `maxDeliveryAttempts: 5`, backoff 10s–600s e DLQ `email-service.p2p.send-email.dlq` (com `…dlq.inspect.sub`). Na última tentativa (`isLastDeliveryAttempt`, helper em `src/domain/sender/helpers/`) o usecase roda com `{ ack: false }` (callback + card) e a mensagem é nacada para ir à DLQ com o payload inteiro, que dá para republicar. Depois do merge, a armadilha acima só vale para indisponibilidade maior que as 5 tentativas.
