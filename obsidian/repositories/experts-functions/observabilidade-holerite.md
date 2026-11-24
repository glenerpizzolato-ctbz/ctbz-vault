---
name: experts-functions-observabilidade-holerite
description: "Erros possíveis no fluxo do e-mail de holerite (function-email-holerites → html-to-pdf → email-service), o que já é visível e propostas de alerta no Google Chat; inclui o ackDeadline de 10 s da sub push que reentrega 8% das requisições (holerite duplicado)"
metadata:
  type: reference
tags:
  - experts-functions
  - email-service
  - observabilidade
  - alertas
analisado_em: 2026-11-24
---

# Observabilidade do e-mail de holerite

Levantamento de 24/11/2026 (PRD-178571), com o fluxo novo pelo email-service.

## Achados medidos em prd (30 dias até 24/11/2026)

- `POST /rhc/folha/notificar` da `function-email-holerites`: 2.301 requisições, sendo 202 = 2.004, **503 = 243** e **500 = 54** (os 500 são da regressão do html-to-pdf em 28/10, ver [[build-e-imagem]]).
- Latência: p50 1,9 s, p90 7,7 s, p99 22,9 s, máximo 99,9 s. **8% (177) passam de 10 s.**
- A subscription push `eventarc-us-central1-email-holerites-sub-224` tem `ackDeadlineSeconds: 10`, backoff de 10 a 600 s, retenção de 24 h e **nenhuma DLQ**. Em push, o ack deadline é o prazo da resposta: quem passa de 10 s é reentregue enquanto ainda processa, e o responsável recebe o holerite **em dobro**. É uma causa provável de parte dos ~40% de empresas que receberam mais de uma vez. Com o email-service, a duplicata também vira dois envios.
- Canais de notificação existentes:
  - `contabilizei-experts-prd`: `[chat] Alertas - GCP Experts` (tipo `google_chat`, nativo), além de webhooks como "Google Chat Experts Alerts" e "#Experts - GCP Alerts".
  - `atendimento-canais-prd`: "GCP Alerts (CANAIS)", com as policies do email-service (DLQ, mensagem antiga sem ack, SMTP indisponível).

## Mapa de falhas

| Salto | Falha | Comportamento hoje | Visível? |
|---|---|---|---|
| fopag-worker → tópico | publish falha / worker não publica | admin não recebe erro do e-mail | não |
| Pub/Sub → function | 503 (instância/escala), resposta > 10 s | reentrega (duplica quando > 10 s) | não alertado |
| Pub/Sub → function | falha permanente (payload ruim, config, permissão) | reentrega por 24 h e depois some | não (sem DLQ) |
| function → html-to-pdf | 5xx/timeout | rethrow, 500, reentrega | log ERROR, sem alerta |
| function → file-upload / send-email | PERMISSION_DENIED, tópico, env faltando, PDF > 10 MB (Buffer.toJSON infla ~3,5x) | `EmailServicePublishError`, 500, reentrega 24 h | log ERROR, sem alerta |
| email-service validação | template inativo/inexistente, variáveis, payload | callback INVALID_PAYLOAD + card no chat CANAIS | sim (card CANAIS) |
| email-service opt-out | responsável com opt-out TRANSACTIONAL | BLOCKED_OPTOUT, holerite não sai | não (desfecho "esperado") |
| email-service dispatch | anexo ausente, SMTP 421/5xx, REJECTED | retry ou FAILED; card só para alguns motivos | parcial |
| entrega | bounce, spam | só no painel SMTP da HubSpot (portal 47852359) | não |

## Propostas (ordem de prioridade)

1. **Subscription própria com `ack_deadline_seconds = 600` e DLQ**: tirar a dependência da sub do Eventarc e ter `dead_letter_policy` com `max_delivery_attempts`.
2. **Alerta de DLQ e mensagem velha**: `subscription/num_undelivered_messages` > 0 na DLQ e `oldest_unacked_message_age` > 30 min na sub de trabalho, para o canal `[chat] Alertas - GCP Experts`. Mesmo padrão do email-service.
3. **Alerta por log** (log-based alert, com o texto do log no card): `ERROR [function-email-holerites]` no `function-email-holerites`, com CNPJ e período, e erro no `function-html-to-pdf`. Limitar a 1 notificação a cada 30 min.
4. **5xx do Cloud Run**: `run.googleapis.com/request_count` com `response_code_class=5xx` para `function-email-holerites` e `function-html-to-pdf`, acima de X% em 10 min.
5. **Desfecho no email-service** (FAILED, BLOCKED_OPTOUT e PENDING > 1 h com `application = function-email-holerites`). Duas saídas:
   - genérica: o card do email-service passa a cobrir FAILED por aplicação;
   - local: resumo diário no chat, a partir da cópia CDC do `email_replications` no BigQuery (D-1), por scheduled query ou job.
6. **Resumo semanal no chat** (opcional): enviados, falhas, opt-out e reenvios por empresa. Hoje a métrica só sai dos logs.

Grafana: painel com volume diário, latência p90/p99, 5xx e status por `email_replications` (fonte Cloud Monitoring + BigQuery). Serve para acompanhar a tendência, mas o aviso de falha fica melhor no chat.

Relacionado: [[templates-mandrill-holerite-e-guias]], [[e2e-holerite-dev]], [[alertas-de-envio]], [[PRD-178571]].
