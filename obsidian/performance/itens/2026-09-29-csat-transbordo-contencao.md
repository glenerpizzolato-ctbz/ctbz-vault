---
name: 2026-09-29-csat-transbordo-contencao
description: "CSAT Transbordo: regras de contenção e tickets travados"
metadata:
  type: project
tags:
  - performance
titulo: "CSAT Transbordo: regras de contenção e tickets travados"
data: 2026-09-29
periodo: 2026QD3
categorias:
  - entrega
  - incidente
impacto: alto
fontes:
  - "[[PRD-150920]]"
  - "[[PRD-151218]]"
  - "[[PRD-151592]]"
  - "[[PRD-155905]]"
  - "[[PRD-158026]]"
  - "[[PRD-163436]]"
  - "[[PRD-165982]]"
  - "[[PRD-167347]]"
  - "[[PRD-167666]]"
  - "[[PRD-168648]]"
  - "[[PRD-147775]]"
  - "[[PRD-124863]]"
---

# CSAT Transbordo: regras de contenção e tickets travados

- **Período:** 2026QD3 · **Categorias:** entrega, incidente · **Impacto:** alto

## Contexto

O épico criou regras de contenção de transbordo; depois, uma ACR mostrou tickets de Experts e BPMP travados em PENDING.

## O que fiz

Implementei as regras (formulário de Ticket OFF, ativo em cenário limite, demandas preventivas, feature-flag, integração com Jira) e corrigi os tickets travados, cenários de borda, o conflito da pesquisa CSAT com outros ativos e uma rotina do Zendesk que impedia resolver tickets de B&P.

## Resultado

O transbordo passou a ser controlado por regra e os tickets presos voltaram a dar baixa.

## Evidências

- [[PRD-150920]]
- [[PRD-151218]]
- [[PRD-151592]]
- [[PRD-155905]]
- [[PRD-158026]]
- [[PRD-163436]]
- [[PRD-165982]]
- [[PRD-167347]]
- [[PRD-167666]]
- [[PRD-168648]]
- [[PRD-147775]]
- [[PRD-124863]]
