---
name: resultado-de-teste-na-subtask-e2e
description: "Resultados de teste (dev, prd, regressão) vão como comentário na sub-task de teste E2E do card, não no card principal (PRD)"
metadata:
  type: feedback
tags:
  - fluxo-de-trabalho
  - jira
  - testes
---

# Resultado de teste vai na sub-task de teste E2E

Ao documentar no Jira o resultado de um teste (smoke, rajada, regressão, validação em dev ou prd), comentar na **sub-task de teste E2E** do card (a do tipo `Qualidade e Testes`, com Envolvimento `Testes -> E2E`), e não no card principal (PRD).

**Why:** pedido do Glener em 23/11/2026 (PRD-178301): o comentário de testes foi movido do card principal para a sub-task de teste PRD-178304. O card principal fica para o contexto da demanda; as evidências de teste ficam junto da sub-task que as acompanha.

**How to apply:** antes de comentar, achar a sub-task de teste do card (`parent = <card> AND issuetype = "Qualidade e Testes"`). Se não houver, perguntar ao usuário em vez de comentar no card principal. O MCP do Atlassian não apaga comentário: para remover um, usar a tela do Jira (botão Excluir do comentário).
