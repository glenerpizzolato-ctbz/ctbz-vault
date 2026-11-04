---
name: 2025-08-07-monitoria-ia
description: "Monitoria de atendimentos com IA"
metadata:
  type: project
tags:
  - performance
titulo: "Monitoria de atendimentos com IA"
data: 2025-08-07
periodo: 2025QD2
categorias:
  - ia
  - entrega
impacto: alto
fontes:
  - "[[PRD-109055]]"
  - "[[PRD-110566]]"
  - "[[PRD-115769]]"
  - "[[PRD-115947]]"
  - "[[PRD-117663]]"
  - "[[PRD-120452]]"
  - "[[PRD-120587]]"
  - "[[PRD-120750]]"
  - "[[PRD-122312]]"
  - "[[PRD-109054]]"
---

# Monitoria de atendimentos com IA

- **Período:** 2025QD2 · **Categorias:** ia, entrega · **Impacto:** alto

## Contexto

O objetivo era monitorar com IA o comportamento dos atendimentos.

## O que fiz

No `monitoria-ia`, construí a análise de comportamento e a transcrição de arquivos, um endpoint de erros para refinar os prompts e labels de billing nas chamadas à Vertex; corrigi a concorrência nas transcrições e um gargalo no endpoint de busca.

## Resultado

A monitoria com IA entrou em operação, com custo rastreável por label e transcrições sem duplicidade.

## Evidências

- [[PRD-109055]]
- [[PRD-110566]]
- [[PRD-115769]]
- [[PRD-115947]]
- [[PRD-117663]]
- [[PRD-120452]]
- [[PRD-120587]]
- [[PRD-120750]]
- [[PRD-122312]]
- [[PRD-109054]]
