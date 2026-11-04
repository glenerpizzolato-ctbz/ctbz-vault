---
name: 2025-12-19-tickets-retidos-corujao
description: "Tickets retidos na transição Corujão → Default"
metadata:
  type: project
tags:
  - performance
titulo: "Tickets retidos na transição Corujão → Default"
data: 2025-12-19
periodo: 2025QD3
categorias:
  - incidente
impacto: medio
fontes:
  - "[[PRD-135472]]"
  - "[[PRD-135547]]"
  - "[[PRD-135769]]"
  - "[[PRD-103530]]"
---

# Tickets retidos na transição Corujão → Default

- **Período:** 2025QD3 · **Categorias:** incidente · **Impacto:** medio

## Contexto

Uma ACR mostrou tickets presos na passagem da fila Corujão para a Default.

## O que fiz

Tratei a ACR e reverti o commit que tinha tirado essa transferência da automação diária.

## Resultado

A transferência diária voltou a funcionar e os tickets deixaram de ficar retidos.

## Evidências

- [[PRD-135472]]
- [[PRD-135547]]
- [[PRD-135769]]
- [[PRD-103530]]
