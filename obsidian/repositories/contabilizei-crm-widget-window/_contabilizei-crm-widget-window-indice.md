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

Repositório em `~/repositories/contabilizei-crm-widget-window`. A fonte atual é o GitLab, [`ctbz/atendimento/geral/contabilizei-crm-widget-window`](https://gitlab.com/ctbz/atendimento/geral/contabilizei-crm-widget-window) (branch padrão `master`, pipeline com deploy dev/stg/prd): o `origin` do clone local ainda aponta para o Bitbucket, que parou em 29/04/2026, por isso o clone tem o remote `gitlab` (usar `git fetch gitlab` e ler de `gitlab/master`). Ex: em 11/11/2026 o MR !3 (PRD-176807) trocou a opção "Contabilizei Bank" do menu inicial por "Conta PJ", o que não aparece no Bitbucket. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[widget-tags-roteamento-ouvidoria]] — como as conversationTags (`helpdesk:routing-tags`) chegam ao ticket, o botão Reclamação/Elogio que manda `sys_grupo_ouvidoria` e o risco de tags velhas no localStorage, e por que o menu de canais não mostra o Chat para Experts, e de onde vem a `sys_canal_chat` (não é só chat web)
- [[autenticacao-chat-web-zendesk]] — como o chat web autentica o cliente no Zendesk Messaging (sessão no BFF, JWT do atendimento-zendesk via loginUser) e o que fica sem autenticação (tags do localStorage, WhatsApp, e-mail); a corrida do loginUser que faz o bot responder erro de autenticação (caso ticket 30176681, evidência da ACR [[PRD-176094]])
