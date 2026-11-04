---
name: 2026-03-12-copilot-acoes-emissao-nf
description: "Módulo de ações do Copilot: emissão de NF sugerida por IA"
metadata:
  type: project
tags:
  - performance
titulo: "Módulo de ações do Copilot: emissão de NF sugerida por IA"
data: 2026-03-12
periodo: 2026QD1
categorias:
  - ia
  - entrega
impacto: alto
fontes:
  - "[[PRD-132701]]"
  - "[[PRD-132702]]"
  - "[[PRD-137732]]"
  - "[[PRD-138560]]"
  - "[[PRD-134749]]"
  - "[[PRD-132704]]"
  - "[[PRD-142980]]"
  - "[[PRD-143664]]"
  - "[[PRD-143028]]"
  - "[[PRD-143919]]"
  - "[[PRD-143225]]"
  - "[[PRD-132126]]"
  - "[[PRD-117320]]"
---

# Módulo de ações do Copilot: emissão de NF sugerida por IA

- **Período:** 2026QD1 · **Categorias:** ia, entrega · **Impacto:** alto

## Contexto

O Copilot só respondia; a ideia era que ele também sugerisse e executasse ações.

## O que fiz

Construí o módulo de ações: sugestão de emissão de NF (inclusive parcial, com tool de busca de CEP), aceite e recusa pelo front, chamada da tool, callback da emissão, deduplicação de sugestões e registro do atendente; corrigi a sessão de ações que contaminava a de outros agentes.

## Resultado

O agente passou a emitir NF a partir de uma sugestão da IA, sem sair do Zendesk.

## Evidências

- [[PRD-132701]]
- [[PRD-132702]]
- [[PRD-137732]]
- [[PRD-138560]]
- [[PRD-134749]]
- [[PRD-132704]]
- [[PRD-142980]]
- [[PRD-143664]]
- [[PRD-143028]]
- [[PRD-143919]]
- [[PRD-143225]]
- [[PRD-132126]]
- [[PRD-117320]]
