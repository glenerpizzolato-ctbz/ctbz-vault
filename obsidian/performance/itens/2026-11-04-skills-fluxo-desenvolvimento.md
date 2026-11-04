---
name: 2026-11-04-skills-fluxo-desenvolvimento
description: "Automação do fluxo de MR com IA (skills mr, comentario, pipe)"
metadata:
  type: project
tags:
  - performance
titulo: "Automação do fluxo de MR com IA (skills mr, comentario, pipe)"
data: 2026-11-04
periodo: 2026QD3
categorias:
  - ia
  - processo
impacto: medio
fontes:
  - "[[jira-anexar-imagens-comentario]]"
  - "[[commit-push-automatico]]"
---

# Automação do fluxo de MR com IA (skills mr, comentario, pipe)

- **Período:** 2026QD3 · **Categorias:** ia, processo · **Impacto:** medio

## Contexto

Abrir MR com descrição, card e work-item, tratar comentários de review e corrigir pipelines eram tarefas repetitivas.

## O que fiz

Criei três skills disparadas pelo BahCode: `/mr` (pré-voo dos commits contra o card, MR completo, sub-task para Pull Request), `/comentario` (corrige, responde e resolve cada thread) e `/pipe` (lê o log, acha a causa e corrige ou dá retry); montei o fluxo de anexar evidências de teste no Jira pelo MCP da Atlassian.

## Resultado

Fluxo de MR padronizado e automatizado pelo agente; evidências de teste anexadas direto nos cards (ex: PRD-174797).

## Evidências

- [[jira-anexar-imagens-comentario]]
- [[commit-push-automatico]]
- Jira: [PRD-174797](https://contabilizeicontabilidade.atlassian.net/browse/PRD-174797)
