---
name: zendesk-sunco-prod-politica
description: "Política: assistentes de IA não devem chamar a API de produção do Zendesk nem do Sunshine Conversations (aciona a renovação de tokens e quebra as integrações); dev/stg liberado"
metadata:
  type: reference
tags:
  - apis
  - zendesk
  - sunshine
  - seguranca
fonte: "Marketplace de IA do Canais Admin (contexto global de um colega do time, item A8ZV3J2IqTC4e4eowPKS), lido em 2026-11-11"
---

# Zendesk e Sunco: não chamar a API de produção por IA

Segundo o contexto global publicado por um colega no [Marketplace de IA](https://admin.ctbz.com.br/api/atendimento-canais/marketplace/A8ZV3J2IqTC4e4eowPKS), o time dono da integração pediu diretamente que assistentes de IA não chamem a API de produção do Zendesk nem a do Sunshine Conversations (Sunco): o uso por IA obriga a acionar a política de renovação de tokens, o que quebra as integrações de todo mundo. Dev/stg (sandbox do Zendesk, app do Sunco de não-produção) continuam liberados.

Abrange qualquer caminho em produção: `*.zendesk.com/api/*`, `*.zendesk.com/sc/*`, `api.smooch.io`, abrir no navegador, MCP, subagente, rotas internas que repassam com token de serviço (ex: proxies `/zendesk/api/...` do `atendimento-zendesk`, `tickets_service` do `zendesk-agents`) e rodar código dos repos apontando para credenciais de prd.

Para investigar ticket de prd sem a API: Firestore (`copilot_actions`, sessões), Cloud Logging, BigQuery e bancos em modo leitura; o que só o Zendesk tiver, pedir para alguém colar.

> [!WARNING]
> Conflita com skills e notas atuais que chamam a API de prd: `fechar-tickets-teste-zendesk`, `buscar-grupo-zendesk`, `mapear-erros-ultimate` (Sunshine) e [[sunshine-identificar-cliente]]. Confirmar com o time dono da integração se a regra vale para o nosso uso antes de seguir com essas skills.
