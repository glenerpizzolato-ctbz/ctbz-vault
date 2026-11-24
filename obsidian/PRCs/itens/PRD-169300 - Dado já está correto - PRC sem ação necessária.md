---
name: prc-sem-acao-necessaria
description: PRC — pedido já atendido ou problema já normalizado quando chega a nós (ex: nome do cliente na Zendesk já atualizado); comentar com evidência, vincular à ACR PRD-169300 e arquivar
metadata:
  type: reference
tags:
  - prc
canal:
  - wpp
dominio:
  - atendimento
sistemas:
  - zendesk
acr:
  - "[[PRD-169300]]"
ocorrencias:
  - PRC-155237
qtd_ocorrencias: 1
ultima_ocorrencia: 2026-11-13
---

# Dado já está correto - PRC sem ação necessária

## Sintoma

O chamado pede um ajuste (ex: trocar o nome do cliente/sócio na Zendesk após alteração contratual, label `eng_canais_dados_zendesk_desatualizados`), mas ao conferir o dado já está correto ou o atendimento do cliente já se normalizou. Nenhuma ação nossa é necessária.

## Como resolver

1. Conferir o dado na fonte (ex: usuário/organização na Zendesk) e tirar um print como evidência.
2. Comentar no PRC explicando que o dado já está correto, com o print embutido no comentário (upload pelo `uploadAttachmentToJiraIssue` fase 1 + `addOrEditJiraIssueComment` com `inlineFileId`).
3. Vincular à ACR **PRD-169300** ("[ACR] PRCs sem problema identificado - atendimento do cliente já normalizado"), link `Problem/Incident` com o PRC *is caused by* PRD-169300 (`createJiraIssueLink` com `inwardIssue: PRD-169300`, `outwardIssue: <PRC>`).
4. Atribuir ao Glener (no `editJiraIssue`, passar `assignee` como `{"accountId": "..."}`: a string pura voltou sem gravar) e arquivar com a transição `Archived` (201), que sai direto de `Backlog`/`To-do` sem tela.

## Ocorrências

- PRC-155237 (ONCO HEALTH SOLUTIONS LTDA): pedido para trocar o nome na Zendesk para "Igor Andrade de Castro", que já estava assim.
