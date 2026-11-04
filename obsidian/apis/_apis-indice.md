---
name: apis-indice
description: "Índice de notas sobre como chamar APIs internas: tokens, liberação de IP e requisições"
metadata:
  type: reference
tags:
  - apis-indice
---

# APIs

Como obter tokens, liberar IP e chamar APIs internas (Bruno, curl) em dev/prd. Uma nota por assunto. Nunca guardar valores de token ou cookie aqui, só o passo a passo.

## SSO

- [[sso-token-dev-prd|Token do SSO (dev/prd) para chamar APIs internas]] — gerar o token pelo Bruno, `.env` da collection, armadilhas de User-Agent/sistema e 401/403

## API gateway (Kong) dos bots

- [[api-gateway-bots-whatsapp|API gateway dos bots de WhatsApp (Ultimate)]] — obter a `x-api-key` pela cloud function `zendeskbot-config` (sem copiar da Ultimate), rotas de busca por telefone/CNPJ e autenticação, headers obrigatórios e 403 por User-Agent

## Sunshine Conversations

- [[sunshine-identificar-cliente|Identificar o cliente de uma conversa no Sunshine]] — do platformConversationId da Ultimate para telefone, CNPJ, ticket e sunshineUserId; BSUID (`BR.xxx`) no lugar do telefone
