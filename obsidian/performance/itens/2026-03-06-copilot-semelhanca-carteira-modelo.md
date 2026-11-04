---
name: 2026-03-06-copilot-semelhanca-carteira-modelo
description: "Copilot: análise de semelhança, expansão para a carteira e troca de modelo"
metadata:
  type: project
tags:
  - performance
titulo: "Copilot: análise de semelhança, expansão para a carteira e troca de modelo"
data: 2026-03-06
periodo: 2026QD1
categorias:
  - ia
  - qualidade
impacto: medio
fontes:
  - "[[PRD-142382]]"
  - "[[PRD-142641]]"
  - "[[PRD-142787]]"
  - "[[PRD-143513]]"
  - "[[PRD-143679]]"
  - "[[PRD-143713]]"
  - "[[PRD-142944]]"
  - "[[PRD-144313]]"
  - "[[PRD-114331]]"
---

# Copilot: análise de semelhança, expansão para a carteira e troca de modelo

- **Período:** 2026QD1 · **Categorias:** ia, qualidade · **Impacto:** medio

## Contexto

Faltava gerar perguntas similares a partir dos tickets, e o Copilot precisava se preparar para a depreciação de modelos.

## O que fiz

Construí a análise de semelhança (prompt, front, observabilidade, processamento de 4.000 tickets) e corrigi suas ACRs; habilitei o Copilot para a carteira, revisei prompts de smalltalk e guardrails na troca de modelo e documentei como manter a qualidade quando um modelo for depreciado.

## Resultado

O Copilot chegou à carteira e ganhou um procedimento documentado de troca de modelo.

## Evidências

- [[PRD-142382]]
- [[PRD-142641]]
- [[PRD-142787]]
- [[PRD-143513]]
- [[PRD-143679]]
- [[PRD-143713]]
- [[PRD-142944]]
- [[PRD-144313]]
- [[PRD-114331]]
