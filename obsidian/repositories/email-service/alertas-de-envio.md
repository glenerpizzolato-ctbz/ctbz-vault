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
