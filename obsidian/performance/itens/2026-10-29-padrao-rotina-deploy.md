---
name: 2026-10-29-padrao-rotina-deploy
description: "Padrão de rotina separada para o deploy (cycle time)"
metadata:
  type: project
tags:
  - performance
titulo: "Padrão de rotina separada para o deploy (cycle time)"
data: 2026-10-29
periodo: 2026QD3
categorias:
  - processo
  - lideranca
impacto: medio
fontes:
  - "[[rotina-deploy-separada]]"
  - "[[jira-transicoes-passo-a-passo]]"
---

# Padrão de rotina separada para o deploy (cycle time)

- **Período:** 2026QD3 · **Categorias:** processo, lideranca · **Impacto:** medio

## Contexto

Cards ficavam parados em "Ready for Release" esperando janela de deploy, o que inflava o cycle time do time.

## O que fiz

Defini o processo: fechar a feature ao fim do desenvolvimento e validação e abrir uma Rotina só para o deploy no mesmo épico; mapeei as transições do Jira uma a uma.

## Resultado

Aplicado em PRD-170026/PRD-170272 e PRD-173035/PRD-174558.

## Evidências

- [[rotina-deploy-separada]]
- [[jira-transicoes-passo-a-passo]]
- Jira: [PRD-170026](https://contabilizeicontabilidade.atlassian.net/browse/PRD-170026), [PRD-170272](https://contabilizeicontabilidade.atlassian.net/browse/PRD-170272), [PRD-173035](https://contabilizeicontabilidade.atlassian.net/browse/PRD-173035), [PRD-174558](https://contabilizeicontabilidade.atlassian.net/browse/PRD-174558)
