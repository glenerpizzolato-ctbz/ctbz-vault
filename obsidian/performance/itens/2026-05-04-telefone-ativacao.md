---
name: 2026-05-04-telefone-ativacao
description: "Padronização do telefone na Ativação (outro time)"
metadata:
  type: project
tags:
  - performance
titulo: "Padronização do telefone na Ativação (outro time)"
data: 2026-05-04
periodo: 2026QD2
categorias:
  - outros-times
impacto: medio
fontes:
  - "[[PRD-150122]]"
  - "[[PRD-150809]]"
  - "[[PRD-146077]]"
---

# Padronização do telefone na Ativação (outro time)

- **Período:** 2026QD2 · **Categorias:** outros-times · **Impacto:** medio

## Contexto

O telefone enviado pela Ativação ao Zendesk não seguia um padrão.

## O que fiz

Fiz o MR de padronização no fluxo da Ativação e destravei a pipeline, que dependia de uma correção do Sonar no `contabilizei-abertura`.

## Resultado

O telefone passou a chegar padronizado ao Zendesk.

## Evidências

- [[PRD-150122]]
- [[PRD-150809]]
- [[PRD-146077]]
