---
name: 2026-10-09-skill-prds-vault
description: "Sincronização das demandas do vault com o Jira (skill atualizar-prds-vault)"
metadata:
  type: project
tags:
  - performance
titulo: "Sincronização das demandas do vault com o Jira (skill atualizar-prds-vault)"
data: 2026-10-09
periodo: 2026QD3
categorias:
  - ia
  - processo
impacto: medio
fontes:
  - "[[_prds-indice]]"
---

# Sincronização das demandas do vault com o Jira (skill atualizar-prds-vault)

- **Período:** 2026QD3 · **Categorias:** ia, processo · **Impacto:** medio

## Contexto

A lista de demandas do vault, fonte da verdade do que foi entregue, saía de sincronia com o Jira.

## O que fiz

Criei uma skill com script (`prds.py`) que busca meus últimos cards, atualiza situação, título e datas, aponta cards novos, cancelados e com épico divergente e regenera as visões por épico, período e domínio.

## Resultado

Entregas rastreáveis por épico e quadrimestre sem edição manual (388 demandas, 46 épicos).

## Evidências

- [[_prds-indice]]
