---
name: email-service-contrato-optout
description: Como um consumidor liga o opt-out no email-service (optout_purpose + cnpj) e como ler o callback (status x failure_reason)
metadata:
  type: reference
tags:
  - email-service
  - optout
---

# Contrato de opt-out do email-service

Para o `email-service` consultar o opt-out de e-mail no `contato-service` antes de enviar, o payload de `email-service.p2p.send-email` precisa levar:

- `optout_purpose`: `MARKETING`, `TRANSACTIONAL`, `SURVEY` ou `TAX` (impostos e obrigações usam `TAX`).
- `cnpj`: obrigatório junto com a finalidade, validado por `^[0-9A-Z]{12}\d{2}$`, ou seja, 14 caracteres **sem máscara e em maiúsculas** (já aceita o CNPJ alfanumérico). Sem ele, o envio volta como `INVALID_PAYLOAD`. Ao montar, normalizar com `replace(/[^0-9A-Za-z]/g, '').toUpperCase()`.

No callback (`email-service.p2p.send-email-callback`):

- `status`: `SENT`, `FAILED`, `INVALID_PAYLOAD` ou `BLOCKED_OPTOUT` (todos os destinatários barrados; desfecho esperado, sem `failure_reason`). Com parte barrada, vem `SENT` com `blocked_recipients`.
- A classe da falha vem em `failure_reason` (não em `reason`, que é texto livre): `SMTP_UNAVAILABLE`, `REJECTED`, `REPLICATION_NOT_FOUND`, `TEMPLATE_NOT_FOUND`, `OPTOUT_UNAVAILABLE` (contato-service fora em todas as tentativas) ou `UNKNOWN` num `FAILED`, e `VALIDATION_HANDLER_ERROR` num `INVALID_PAYLOAD`.

Consumidores que já mandam: `agrupamento-guias-service` (PRD-174790, `EnvioEmailService.envia`, e guarda `EMAIL_INVALID_PAYLOAD`/`EMAIL_OPTOUT_UNAVAILABLE` no `errorReason`).
