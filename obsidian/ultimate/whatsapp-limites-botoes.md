---
name: whatsapp-limites-botoes
description: "Limites de caracteres de botões e listas no WhatsApp (Meta) e nos AI agents da Ultimate/Zendesk: botão de resposta 20, título de linha de lista 24"
metadata:
  type: reference
tags:
  - whatsapp
  - ultimate
  - zendesk
atualizado_em: 2026-10-28
---

# Limites de caracteres de botões no WhatsApp (Ultimate/Zendesk)

| Elemento | Limite |
| --- | --- |
| Botão de resposta (reply button, até 3 por mensagem) | **20** caracteres |
| Texto do botão que abre a lista | 20 caracteres |
| Botão CTA URL (texto exibido) | 20 caracteres |
| Título da linha da lista (até 10 linhas) | **24** caracteres |
| Título da seção da lista | 24 caracteres |

- O limite que vale para os botões do AI agent da Ultimate/Zendesk é **20**: o artigo de erros técnicos dos AI agents manda conferir se os botões não passam de 20 caracteres. Os 24 são da linha de lista (list message), e é daí que vem a confusão.
- Botões de quick reply em **template** aprovado na Meta aceitam 25 caracteres, mas isso não vale para os botões da conversa do bot.
- Fontes: Zendesk "Technical errors in AI agents" (artigo 8536904782106) e documentações de provedores do WhatsApp Cloud API (Exotel, 360dialog).
