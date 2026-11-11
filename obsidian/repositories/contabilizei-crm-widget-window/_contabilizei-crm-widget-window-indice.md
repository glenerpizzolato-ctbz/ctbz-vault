---
name: contabilizei-crm-widget-window-indice
description: "Índice de notas do repositório contabilizei-crm-widget-window: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - contabilizei-crm-widget-window
repositorio: contabilizei-crm-widget-window
caminho: ~/repositories/contabilizei-crm-widget-window
---

# contabilizei-crm-widget-window

Repositório em `~/repositories/contabilizei-crm-widget-window`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[widget-tags-roteamento-ouvidoria]] — como as conversationTags (`helpdesk:routing-tags`) chegam ao ticket, o botão Reclamação/Elogio que manda `sys_grupo_ouvidoria` e o risco de tags velhas no localStorage, e por que o menu de canais não mostra o Chat para Experts
- [[autenticacao-chat-web-zendesk]] — como o chat web autentica o cliente no Zendesk Messaging (sessão no BFF, JWT do atendimento-zendesk via loginUser) e o que fica sem autenticação (tags do localStorage, WhatsApp, e-mail)
