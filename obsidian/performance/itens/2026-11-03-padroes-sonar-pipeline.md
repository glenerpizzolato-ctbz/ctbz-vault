---
name: 2026-11-03-padroes-sonar-pipeline
description: "Padrões de diagnóstico de Sonar e pipeline"
metadata:
  type: project
tags:
  - performance
titulo: "Padrões de diagnóstico de Sonar e pipeline"
data: 2026-11-03
periodo: 2026QD3
categorias:
  - qualidade
  - processo
impacto: medio
fontes:
  - "[[pipeline-repo-novo-sem-variaveis-ci]]"
  - "[[sonar-cobertura-branches-kotlin]]"
  - "[[sonar-duplicacao-codigo-novo]]"
---

# Padrões de diagnóstico de Sonar e pipeline

- **Período:** 2026QD3 · **Categorias:** qualidade, processo · **Impacto:** medio

## Contexto

MRs batiam no gate de cobertura de branches em Kotlin e de duplicação, e um repositório novo tinha cobertura 0% sem explicação.

## O que fiz

Identifiquei que o repositório novo não tinha variáveis de CI (build, lint e test nunca rodavam) e documentei como diagnosticar pelo MCP do Sonar as armadilhas de branches em Kotlin e de duplicação em código novo.

## Resultado

Três notas genéricas de padrões, válidas para qualquer repositório do componente ci-cd.

## Evidências

- [[pipeline-repo-novo-sem-variaveis-ci]]
- [[sonar-cobertura-branches-kotlin]]
- [[sonar-duplicacao-codigo-novo]]
