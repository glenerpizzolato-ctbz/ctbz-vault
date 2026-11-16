---
name: testar-bot-whatsapp
description: "Receita para testar os bots de WhatsApp da Ultimate em prd com o WhatsApp do Glener: abrir a conversa pelo claude-in-chrome, fugir do rollout da IA, achar o ticket e o grupo pela API do Zendesk, fechar sem CSAT, GIF sem vazar conversas e evidência no Jira"
metadata:
  type: reference
tags:
  - ultimate
  - testes
  - whatsapp
  - zendesk
---

# Testar o bot de WhatsApp em prd (receita)

Montada nos testes de 2026-11-16 ([[testes-roteamento-n1-ativacao]]). Scripts em `~/ctbz-vault/obsidian/ultimate/scripts/`.

## Dados fixos

- Telefone de teste (Glener): `+555596981032`. End-user no Zendesk: `21878313229212` (tickets em https://contabilizei.zendesk.com/agent/users/21878313229212/requested_tickets).
- Bot no WhatsApp Web: buscar `41010021` → conversa `[prd] ctbz zendesk 41 41010021 main` (botId `66c6220557465548f3ff0d6e`).
- O usuário do Zendesk está na organização de testes `5405377070236` ("Contabilizei - Squad Engenharia Canais - Testes"), cujas tags (`jira_finalizado`, `jira_não_finalizado`, `expert_essencial`…) entram em todo ticket.

## Ciclo por cenário

1. **Preparar o dado** (ex: status do SOCI pelo MCP do Jira) e conferir o que o bot vai ler: `python3 scripts/processos_bot.py +555596981032 <idProcesso>` (contagem e dados de processo pelo gateway, com as credenciais da skill `buscar-empresas-por-telefone`).
2. **Baseline de tickets:** `python3 scripts/zd_tickets.py 1` (último ticket do requester, com grupo e tags).
3. **Conversar:** WhatsApp Web pelo claude-in-chrome. Antes, ler as últimas mensagens (`#main div[role="row"]` via `javascript_tool`) para ver se há **CSAT pendente**. Se houver, pedir ao Glener para encerrar: **não responder CSAT pelo Claude**, porque polui a métrica real.
4. **Enviar no segundo :30 UTC** para fugir do rollout da IA de Ativação Experts ([[rollout-ia-ativacao]]): digitar "Oi" e clicar em Enviar por script quando `new Date().getUTCSeconds()===30`. A espera tem que caber em 40 s (o `javascript_tool` corta em 45 s); se voltar `retry`, chamar de novo. Se o bot responder "Seu atendimento anterior já foi finalizado…", mandar de novo no próximo :30.
5. **Grupo:** `python3 scripts/zd_tickets.py 3 --since-id <baseline>`.
6. **Fechar sem CSAT:** `python3 scripts/zd_fechar_sem_csat.py <ticketId>`. Ele confere o requester, grava `sys_csat_survey_sent` + `sys_csat_response_exp` **antes** de pôr `closed` (os gatilhos de CSAT Experts `27492316041500` e Ativação `29997958429596` não disparam quando o ticket já tem `sys_csat_survey_sent`; `sys_nao_oferecer_csat` só vale para o CSAT BP). Ticket atribuído a agente humano: fechar logo.
7. **GIF:** `gif_creator` (start → ações → stop → export com download) e depois `python3 scripts/crop_gif.py <raw.gif> <final.gif>`, que tira a lista de conversas do WhatsApp. **Conferir a folha `.sheet.png` antes de subir**: as conversas pessoais não podem aparecer.
8. **Evidência no Jira:** `uploadAttachmentToJiraIssue` (fase 1) → rodar o `curl` → `addOrEditJiraIssueComment` com `contentFormat: html` + `inlineFileId`/`inlineFileCollection`. Ao trocar o GIF de um comentário (edição com outro `inlineFileId`), o Jira remove o anexo antigo.

## Para entender por onde a conversa passou

Logs de conversa do dashboard da Ultimate, com as variáveis setadas: [[logs-conversa-ultimate]]. Por que o bot foi para tal grupo/IA: [[endpoints-autenticacao-bot]], [[rollout-ia-ativacao]], [[menu-inic-experts-ramificacoes]].
