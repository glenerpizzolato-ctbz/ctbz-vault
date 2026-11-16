---
name: logs-conversa-ultimate
description: "Como ver o que a Ultimate (Zendesk AI agents) fez numa conversa: URL dos conversation logs do dashboard, montada com o id do bot, o período e o id da conversa do Sunshine (pegável na tag conversationid: do ticket)"
metadata:
  type: reference
tags:
  - ultimate
  - zendesk
  - sunshine
  - debug
---

# Logs de conversa da Ultimate

Para saber por onde uma conversa passou no bot (replies, integrações, variáveis, escalonamento), use o monitoring do dashboard. Dica do Glener, 2026-11-16:

```
https://contabilizei.zendesk.com/ai-agents/dashboard/agent/<botId>/optimize/monitoring/conversation-logs/<logId>?endDate=<AAAA-MM-DD>+23%3A59&startDate=<AAAA-MM-DD>+00%3A00&platformConversationId=<sunshineConversationId>
```

Exemplo real: `https://contabilizei.zendesk.com/ai-agents/dashboard/agent/66c6220557465548f3ff0d6e/optimize/monitoring/conversation-logs/9b22a569-c512-4992-ac9f-d20b7c8ac09b?endDate=2026-11-16+23%3A59&startDate=2026-11-10+00%3A00&platformConversationId=68a7774b276b3b82574dff1a`

- **Trocar:** o `botId` (ids dos bots de prd em [[dashboard-read-api]]; o main é `66c6220557465548f3ff0d6e`), o período (`startDate`/`endDate`) e o `platformConversationId`, que é o id da conversa no Sunshine.
- **De onde tirar o `platformConversationId`:** da tag `conversationid:<id>` do ticket no Zendesk (o bot grava `businessphone:`, `conversationid:`, `cnpj:` etc. nas tags). Por exemplo, pelas audits do ticket (`GET /api/v2/tickets/{id}/audits.json`) ou pelo campo `tags`.
- O segmento depois de `conversation-logs/` é o id do log na Ultimate. Ao trocar só o `platformConversationId` e as datas, a tela filtra a conversa certa.
- É acesso ao Zendesk de prd pelo navegador: vale a política de [[zendesk-sunco-prod-politica]] (só com aprovação do usuário na conversa, só leitura).
- Usado nos testes de [[testes-roteamento-n1-ativacao]] para entender por que o ticket caiu na AIDA Ativação em vez do menu do bot.
