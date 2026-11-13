---
name: ultimate-dashboard-read-api
description: "Como ler bots, replies e integrações da Ultimate de prd pela API interna do dashboard (rotas POST read*/get*, autenticadas pela sessão do navegador), e as armadilhas"
metadata:
  type: reference
tags:
  - ultimate-as-a-code
  - ultimate
---

# Ler a Ultimate pela API do dashboard

O guia completo (rotas, corpos e ids de todos os bots de prd) está no repo, em `~/repositories/ultimate-as-a-code/docs/dashboard-read-api.md` (branch `docs/mapa-mensagem-ativa`, 2026-11-13).

- Rotas de leitura são **POST** (`readBotsBasicInfo`, `bot/get-bot`, `reply/read-partial-replies` com `{botId, languageId}`, `getReply` com `{botId, replyId}`, `integration/read-list` com `{botId}`). Só as de feature flag são GET.
- Autentica pelo cookie: com o dashboard aberto no Chrome, um `fetch` same-origin com `credentials: 'include'` funciona. A política de não chamar o Zendesk de prd por IA ([[zendesk-sunco-prod-politica]]) vale: só com aprovação do usuário na conversa, e só rotas de leitura.
- `integration/read-list` não traz a URL das integrações, e os `apiParams[].testValue` têm tokens reais: nunca copiar. Para saber qual `fluxo` um GET de ativo usa, contar `fluxo=` nos logs do `atendimento-zendesk` no GKE (`contabilizei-prod-01`).
- `fetch` da página para `http://127.0.0.1` falha (CSP do dashboard), e o `javascript_tool` do Chrome trunca a saída em ~1000 caracteres: paginar o texto renderizado.
- Os `Pointer | …` são replies `template` com `isActive: false`, mas funcionam quando referenciados. Há várias versões com o mesmo nome: vale a que o pointer referencia.
- Mapa do retorno de ativo nos bots main e fina + avisos: [[retorno-ativo-plano-sem-whatsapp]].
