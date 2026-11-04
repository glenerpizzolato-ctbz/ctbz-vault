---
name: sunshine-identificar-cliente
description: "Como chegar no telefone, CNPJ, ticket e sunshineUserId de um cliente a partir do conversationId do Sunshine (platformConversationId da Ultimate), incluindo o caso do BSUID (BR.xxx) da Meta no lugar do telefone"
metadata:
  type: reference
tags:
  - apis
  - sunshine
  - ultimate
---

# Identificar o cliente de uma conversa no Sunshine

A Ultimate expõe dois IDs: o `conversationId` dela (UUID, o do link `contabilizei.zendesk.com/ai-agents/dashboard/bot/<botId>/conversations/<uuid>`) e o `platformConversationId`, que é o `conversationId` do Sunshine (24 hex). Para identificar o cliente, usar o do Sunshine.

Credenciais: `config.app.services.sunshine.appId` e `.token` da cloud function `zendeskbot-config` (prd, projeto `contabilizei-crm`), que podem ser obtidas com a função `gcloud_function` do script `~/.claude/skills/buscar-empresas-por-telefone/scripts/bots_api.py`. O token vem sem prefixo: no header `Authorization`, usar `Basic <token>` quando ele for um base64 de `key:secret` (sem o prefixo, a API devolve 401). Nunca exibir os valores.

- `GET https://api.smooch.io/v2/apps/{appId}/conversations/{id}`: o `metadata` traz quase tudo:
    - `userId`: o sunshineUserId.
    - `5359989415708`: o telefone (campo do Zendesk), confiável.
    - `15818063240348`: o CNPJ.
    - `ezvoice_zendesk_ticket_id`: o ticket.
    - `tags`: `telefone:`, `cnpj:`, `carteira:` etc. Pode vir só com `sys_clear_tags`.
    - `activeSwitchboardIntegration.name`: quem controla a conversa agora (ex: `ultimate`).
- `GET .../conversations/{id}/messages`: as últimas 100 mensagens em ordem crescente. Mensagens do bot têm `author.type=business` com `displayName` `Bot` ou vazio; com nome de pessoa, é um agente humano.
- `GET .../users/{userId}/clients`: o client `whatsapp`. Quando a Meta manda o BSUID (ID de usuário por empresa), o `externalId` e o `displayName` vêm como `BR.<número>`, e o telefone real fica em `additionalIdentifiers[key=phoneNumber]` e `raw.from`.

> [!WARNING]
> A tag `telefone:` pode vir com o BSUID (`+BR.2701...`) em vez do número. Usar primeiro o `metadata["5359989415708"]`.

A API tem rate limit: com 8 threads, o ritmo caiu de ~300 para ~100 conversas por minuto. Caso de uso: o mapeamento dos clientes afetados no incidente da Ultimate em 2026-11-03 (ver [[eventos-de-erro-ultimate]]).
