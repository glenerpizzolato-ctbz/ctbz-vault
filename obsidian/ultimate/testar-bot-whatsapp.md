---
name: testar-bot-whatsapp
description: "Receita para testar os bots de WhatsApp da Ultimate em prd com o WhatsApp do Glener: o Claude NÃO acessa o WhatsApp Web, pede ao Glener para enviar/responder e espera a confirmação; fugir do rollout da IA, achar o ticket e o grupo pela API do Zendesk, fechar sem CSAT e evidência no Jira"
atualizado_em: 2026-11-19
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

> [!IMPORTANT]
> **Não acessar o WhatsApp Web do Glener** (pedido dele em 2026-11-19). O Claude não abre o WhatsApp Web pelo claude-in-chrome, não lê as conversas e não envia mensagens por script. Em todo passo que envolve o WhatsApp, **pedir ao Glener** para enviar ou responder (dizendo exatamente o texto e, quando importar, o momento) e **ficar aguardando** a confirmação dele no chat ("enviei", "o bot respondeu X") antes de seguir. O resultado é conferido pelo lado do Zendesk e da Ultimate (scripts e logs abaixo), não pela tela do WhatsApp.

## Dados fixos

- Telefone de teste (Glener): `+555596981032`. End-user no Zendesk: `21878313229212` (tickets em https://contabilizei.zendesk.com/agent/users/21878313229212/requested_tickets).
- Bot: número `+55 41 4101-0021`, conversa `[prd] ctbz zendesk 41 41010021 main` no WhatsApp do Glener (botId `66c6220557465548f3ff0d6e`). Quem conversa é o Glener.
- O usuário do Zendesk está na organização de testes `5405377070236` ("Contabilizei - Squad Engenharia Canais - Testes"), cujas tags (`jira_finalizado`, `jira_não_finalizado`, `expert_essencial`…) entram em todo ticket.

## Ciclo por cenário

1. **Preparar o dado** (ex: status do SOCI pelo MCP do Jira) e conferir o que o bot vai ler: `python3 scripts/processos_bot.py +555596981032 <idProcesso>` (contagem e dados de processo pelo gateway, com as credenciais da skill `buscar-empresas-por-telefone`).
2. **Baseline de tickets:** `python3 scripts/zd_tickets.py 1` (último ticket do requester, com grupo e tags).
3. **Pedir a conversa ao Glener:** dizer o texto a enviar (ex: "Oi") para o bot `41 4101-0021` e perguntar antes se há **CSAT pendente** na conversa. Se houver, ele encerra: **o Claude não responde CSAT**, porque polui a métrica real. Depois do pedido, aguardar a confirmação dele; não seguir sem ela.
4. **Fugir do rollout da IA** de Ativação Experts ([[rollout-ia-ativacao]]): pedir que o Glener envie a mensagem com o relógio no segundo **:30** (o segundo é o mesmo em UTC e no horário local). Se o bot responder "Seu atendimento anterior já foi finalizado…", pedir para mandar de novo no próximo :30. Para saber o que o bot respondeu, perguntar ao Glener ou ler os comentários do ticket pela API do Zendesk.
5. **Grupo:** `python3 scripts/zd_tickets.py 3 --since-id <baseline>`.
6. **Fechar sem CSAT:** `python3 scripts/zd_fechar_sem_csat.py <ticketId>`. Ele confere o requester, grava `sys_csat_survey_sent` + `sys_csat_response_exp` **antes** de pôr `closed` (os gatilhos de CSAT Experts `27492316041500` e Ativação `29997958429596` não disparam quando o ticket já tem `sys_csat_survey_sent`; `sys_nao_oferecer_csat` só vale para o CSAT BP). Ticket atribuído a agente humano: fechar logo.
7. **Prints/GIF:** quem grava é o Glener, no WhatsApp dele (o Claude não captura a tela do WhatsApp). Se ele mandar um GIF com a lista de conversas aparecendo, recortar com `python3 scripts/crop_gif.py <raw.gif> <final.gif>` e **conferir a folha `.sheet.png` antes de subir**: as conversas pessoais não podem aparecer.
8. **Evidência no Jira:** `uploadAttachmentToJiraIssue` (fase 1) → rodar o `curl` → `addOrEditJiraIssueComment` com `contentFormat: html` + `inlineFileId`/`inlineFileCollection`. Ao trocar o GIF de um comentário (edição com outro `inlineFileId`), o Jira remove o anexo antigo.

## Para entender por onde a conversa passou

Logs de conversa do dashboard da Ultimate, com as variáveis setadas: [[logs-conversa-ultimate]]. Por que o bot foi para tal grupo/IA: [[endpoints-autenticacao-bot]], [[rollout-ia-ativacao]], [[menu-inic-experts-ramificacoes]].

## Armadilha: ativo especial pendente

Se o telefone tiver uma `mensagem_ativa` habilitada e dentro da validade (banco `prd_crm_atendimento_zendesk`, `destino = '+555596981032'`, `habilitado` e `criado_em + validade_em_minutos >= now()`), a conversa entra pelo retorno de ativo (`ativos especiais` → `URA_FLOW`) e não pelo fluxo de inbound. Os processos de teste da Abertura recebem ativos reais da operação. Antes de testar inbound, contar os ativos e consumir cada um com uma conversa (cada uma abre um ticket a fechar). Caso real em [[testes-roteamento-bp-n1-n2]].
