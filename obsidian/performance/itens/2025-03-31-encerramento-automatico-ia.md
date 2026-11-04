---
name: 2025-03-31-encerramento-automatico-ia
description: "Encerramento automático de atendimentos com IA (Experts)"
metadata:
  type: project
tags:
  - performance
titulo: "Encerramento automático de atendimentos com IA (Experts)"
data: 2025-03-31
periodo: 2025QD1
categorias:
  - ia
  - entrega
  - incidente
impacto: alto
fontes:
  - "[[PRD-97120]]"
  - "[[PRD-106946]]"
  - "[[PRD-108132]]"
  - "[[PRD-109136]]"
  - "[[PRD-109417]]"
  - "[[PRD-105165]]"
  - "[[PRD-113494]]"
  - "[[PRD-107494]]"
  - "[[fluxo-encerramento-com-ia]]"
  - "[[uso-de-llm-openai]]"
---

# Encerramento automático de atendimentos com IA (Experts)

- **Período:** 2025QD1 · **Categorias:** ia, entrega, incidente · **Impacto:** alto

## Contexto

Atendimentos ficavam abertos sem necessidade. Depois da primeira versão surgiram ACRs: problemas no encerramento com IA e tickets que não voltavam para os agentes.

## O que fiz

Entreguei o encerramento automático com IA (Gemini decide se o cliente quer encerrar) e tratei as ACRs: reconexão do cliente (sair da tabela de encerramento de 4h), reatribuição de tickets e cadastro de grupos no encerramento e na classificação por IA. Em 2026-10 documentei o fluxo completo (estados no Redis, prompt, timeout, retentativas) com diagrama clicável e as fragilidades encontradas.

## Resultado

O encerramento com IA ficou estável, os tickets voltaram a ser reatribuídos e o uso foi estendido a novos grupos; o fluxo e seus riscos ficaram documentados.

## Evidências

- [[PRD-97120]]
- [[PRD-106946]]
- [[PRD-108132]]
- [[PRD-109136]]
- [[PRD-109417]]
- [[PRD-105165]]
- [[PRD-113494]]
- [[PRD-107494]]
- [[fluxo-encerramento-com-ia]]
- [[uso-de-llm-openai]]
