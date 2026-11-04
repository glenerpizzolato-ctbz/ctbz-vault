---
name: 2025-12-22-copilot-envio-automatico-validador
description: "Envio automático de respostas do Copilot com validador de IA"
metadata:
  type: project
tags:
  - performance
titulo: "Envio automático de respostas do Copilot com validador de IA"
data: 2025-12-22
periodo: 2025QD3
categorias:
  - ia
  - entrega
impacto: alto
fontes:
  - "[[PRD-122785]]"
  - "[[PRD-123828]]"
  - "[[PRD-124140]]"
  - "[[PRD-126978]]"
  - "[[PRD-128221]]"
  - "[[PRD-130544]]"
  - "[[PRD-130970]]"
  - "[[PRD-131163]]"
  - "[[PRD-127521]]"
  - "[[PRD-131810]]"
  - "[[PRD-135974]]"
  - "[[PRD-114331]]"
---

# Envio automático de respostas do Copilot com validador de IA

- **Período:** 2025QD3 · **Categorias:** ia, entrega · **Impacto:** alto

## Contexto

O Copilot Experts passaria a enviar respostas sozinho, o que exige avaliar a qualidade antes de cada envio.

## O que fiz

Criei o avaliador/validador de respostas (RAGAS com contextual recall, guardrails), com métricas, categorias elegíveis (CNAE, impostos), envio em partes, tempo de espera dinâmico por agente e tema e bloqueio quando há transferência; adicionei observabilidade e labels das chamadas de IA via LiteLLM (PoC).

## Resultado

O envio automático entrou em produção com barreira de qualidade e métricas de cancelamento e de envio por categoria.

## Evidências

- [[PRD-122785]]
- [[PRD-123828]]
- [[PRD-124140]]
- [[PRD-126978]]
- [[PRD-128221]]
- [[PRD-130544]]
- [[PRD-130970]]
- [[PRD-131163]]
- [[PRD-127521]]
- [[PRD-131810]]
- [[PRD-135974]]
- [[PRD-114331]]
