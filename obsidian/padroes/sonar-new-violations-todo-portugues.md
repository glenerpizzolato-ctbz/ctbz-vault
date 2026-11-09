---
name: sonar-new-violations-todo-portugues
description: "Quality gate do SonarQube com new_violations > 0 (limite 0): até issue INFO derruba o gate, e o \"Todo\" do português em comentário é lido como TODO (S1135)"
metadata:
  type: reference
tags:
  - padroes
  - sonar
---

# Sonar: new_violations e o "Todo" em português

O gate dos projetos da CTBZ tem `new_violations` com limite **0**: qualquer issue nova, inclusive de severidade INFO, derruba o job `sonar-merge-request`, mesmo com cobertura e duplicação OK.

## Diagnóstico

1. No log do job, a linha `QUALITY GATE STATUS: FAILED - ... pullRequest=<id>` dá a chave do PR no Sonar.
2. Pelo MCP: `get_project_quality_gate_status` (projectKey + pullRequest) mostra qual condição falhou, e `search_sonar_issues_in_projects` com o mesmo `pullRequest` e `issueStatuses: ["OPEN"]` lista as issues com arquivo e linha.

## Armadilhas comuns em TypeScript

- **`typescript:S1135` (TODO) em comentário em português**: a regra casa a palavra `todo` sem diferenciar maiúsculas, então frases como "Todo endereço consultado volta…" viram "Complete the task associated to this TODO comment". Reescrever sem a palavra solta (ex: "Cada endereço…"). "Todos", "toda" não casam.
- **`typescript:S3358` (ternário aninhado)**: o Biome do projeto não reclama, mas o Sonar sim. Extrair para uma função com `if`/`return`.

## Branch chaining

Quando a issue está num commit do MR de baixo da corrente, corrigir na branch dele (worktree temporária, para não trocar a branch da worktree do conjunto) e fazer `git merge` dessa branch na de cima, em vez de rebase com force push.

Visto em nov/2026 nos MRs !177/!178 do `atendimento-canais-admin` (opt-out em lote).
