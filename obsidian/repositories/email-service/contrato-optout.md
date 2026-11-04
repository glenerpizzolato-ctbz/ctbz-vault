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

## Armadilha: 401 do contato-service em prd (2026-11-04)

No primeiro envio real com `optout_purpose` em prd (agrupamento de guias, PRD-174790), o `email-service` recebeu `401` do Kong ao consultar o opt-out (`OptoutLookupError: Failed to check recipients opt-out in contato-service: Request failed with status code 401`). O e-mail fica retentando no BullMQ (10 tentativas, backoff exponencial, ~21 min) e depois volta `FAILED` com `OPTOUT_UNAVAILABLE`.

- URL em prd: `CONTATO_SERVICE_BASE_URL=http://api-gateway.ctbz.prd/contato-service` (a mesma do `bots-api`, que funciona).
- Consumer no Kong: `email-service-to-contato-service` em `kong-config/prd/atendimento-canais/contato-service/contato-service.yml` (deploy prd ok).
- Token: secret `emailserviceatendimentocanaisprdpdp_CONTATO_SERVICE_API_KEY` (projeto `1046698394190`), referenciado em `k8s-configmap/.../atendimento-canais-prd/email-service.yaml`. O 401 indica que o valor desse secret não bate com o `keyauth_credentials` do consumer no Kong de prd. O dev não tem permissão de listar/ler o secret.
- A key do consumer **não** está no `kong-config`: o YAML só tem a referência `'${{ env "DECK_EMAIL_SERVICE_TO_CONTATO_SERVICE" }}'`. O valor real (64 caracteres, gerado pela própria pipeline do `kong-config` quando o consumer é criado) fica na variável de CI/CD `DECK_EMAIL_SERVICE_TO_CONTATO_SERVICE` do projeto `kong-config` no GitLab, no escopo de prd. Copiar a linha do YAML para o secret mantém o 401.
- **Causa (resolvido em 2026-11-04 ~15:30 UTC):** o token tem `$`. O job `create-secret-value` do `vault-roleset` gravou o `$` de um jeito diferente do valor que o Kong tem, então o pod mandava outra key e levava 401, enquanto o mesmo token pelo Bruno passava (200). Correção: rodar o `create-secret-value` de novo **duplicando cada `$` do valor (`$` → `$$`)** e reiniciar o `email-service`. Detalhes em [[create-secret-value-cifrao]].
- Diagnóstico sem expor o valor: os logs do Kong (`namespace kong`, container `proxy`, `SEARCH("optouts/search")`) mostram o status por chamada; a prova negativa com token `xxx` no Bruno confirma que o teste usa o header certo; o log do job `create-secret-value` mostra qual secret e versão foram gravados (`Created version [N]`), mas não o valor.
- Logs: `labels."k8s-pod/app_kubernetes_io/name"="email-service"` no `contabilizei-prod-01`, `SEARCH("OptoutLookupError")`. No agrupamento, o log usa o `idControle` da notificação, não o id do grupo (`Notificação <idControle> ...`).
