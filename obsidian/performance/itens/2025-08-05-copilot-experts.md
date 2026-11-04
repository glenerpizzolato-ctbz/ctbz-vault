---
name: 2025-08-05-copilot-experts
description: "Copilot do Zendesk adaptado para o atendimento Experts"
metadata:
  type: project
tags:
  - performance
titulo: "Copilot do Zendesk adaptado para o atendimento Experts"
data: 2025-08-05
periodo: 2025QD2
categorias:
  - ia
  - outros-times
impacto: alto
fontes:
  - "[[PRD-118179]]"
  - "[[PRD-120864]]"
  - "[[PRD-120244]]"
  - "[[PRD-116735]]"
  - "[[PRD-121598]]"
  - "[[PRD-121950]]"
  - "[[PRD-121100]]"
  - "[[PRD-117443]]"
  - "[[PRD-118204]]"
  - "[[PRD-121167]]"
  - "[[PRD-114331]]"
---

# Copilot do Zendesk adaptado para o atendimento Experts

- **Período:** 2025QD2 · **Categorias:** ia, outros-times · **Impacto:** alto

## Contexto

O Copilot (Concierge) do Zendesk não atendia o cenário Experts; o épico tem mais de 100 demandas no vault.

## O que fiz

Criei funções novas para a IA (busca de impostos, recálculo, análise de situação de guia, agenda do assessor, transcrição de XML e XLSX), blocklist de funções de Experts, troca do modelo de embedding, histórico de perguntas e respostas e métrica de cópia; revisei os prompts das árvores de impostos e de NF.

## Resultado

O Copilot passou a atender os agentes Experts com funções e prompts próprios, com uso medido pela métrica de cópia.

## Evidências

- [[PRD-118179]]
- [[PRD-120864]]
- [[PRD-120244]]
- [[PRD-116735]]
- [[PRD-121598]]
- [[PRD-121950]]
- [[PRD-121100]]
- [[PRD-117443]]
- [[PRD-118204]]
- [[PRD-121167]]
- [[PRD-114331]]
