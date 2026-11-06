---
name: 2026-11-06-nexts-fila-priorizada
description: "Fila do que fazer a seguir priorizada por IA (aba Nexts do BahCode), juntando GitLab, vault, PRCs e Jira"
metadata:
  type: project
tags:
  - performance
titulo: "Fila do que fazer a seguir priorizada por IA (Nexts)"
data: 2026-11-06
periodo: 2026QD3
categorias:
  - ia
  - processo
impacto: medio
fontes:
  - "[[2026-11-05-opportunities-scan]]"
  - "[[2026-08-24-playbooks-prc]]"
---

# Fila do que fazer a seguir priorizada por IA (Nexts)

- **Período:** 2026QD3 · **Categorias:** ia, processo · **Impacto:** medio

## Contexto

O trabalho em aberto ficava espalhado em quatro lugares: work-items do GitLab, próximas tarefas anotadas no vault, PRCs que já têm playbook conhecido e os cards em TODO/BACKLOG do board do time no Jira. Decidir o próximo passo exigia abrir tudo e comparar à mão.

## O que fiz

Criei no BahCode a aba Nexts (grupo Scanning): lê as quatro fontes sem IA (GitLab pela API, vault pelos arquivos, PRCs pelo mapeamento contra os playbooks, Jira pelo MCP do Atlassian) e o Claude, só leitura, dá a cada item prioridade e esforço, com o porquê e o primeiro passo; a lista sai do mais prioritário e mais fácil para o menos, com filtro por fonte e destaque dos ganhos rápidos. Prompt, modelo, board, status, pastas e a avaliação automática (desligada por padrão) ficam nas Configurações.

## Resultado

A primeira avaliação juntou 48 itens (17 work-items, 12 tarefas, 19 cards do board) em ~1 minuto, por US$ 0,14, e pôs no topo um card de rotina meu de prioridade alta e esforço baixo, seguido de ajustes pontuais (troca de token provisório, monitor no Uptime Kuma) à frente de itens grandes atribuídos a outras pessoas.

## Evidências

- Commit `865fea5` do ide-bahcode (`feat(nexts)`)
- [[2026-11-05-opportunities-scan]]
