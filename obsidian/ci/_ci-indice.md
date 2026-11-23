---
name: ci-indice
description: "Índice de armadilhas e diagnósticos de pipeline (GitLab CI) e do quality gate do Sonar"
metadata:
  type: reference
tags:
  - ci-indice
---

# CI e Sonar

Armadilhas e diagnósticos de pipeline e do quality gate do Sonar: por que o gate caiu e como resolver.

- [[sonar-duplicacao-codigo-novo|Sonar: duplicação em código novo]] — gate de 6% em código novo: diagnosticar pelo MCP (`search_duplicated_files`), mexer em arquivo antigo o torna código novo, literais não quebram duplicação; extrair o idêntico para um service comum
- [[pipeline-repo-novo-sem-variaveis-ci|Repo novo sem variáveis de CI]] — pipeline sem build/lint/test e Sonar do MR com cobertura 0%; copiar as variáveis de um repo do mesmo tipo
- [[sonar-cobertura-branches-kotlin|Sonar: cobertura de branches em Kotlin]] — gate de 90% de branches no código novo; safe calls, let/takeIf e lambdas inline geram ramos inalcançáveis; diagnosticar com jacoco.xml × git diff e trocar por orEmpty/!!
- [[sonar-cobertura-excluida-no-runner|Sonar: 0% em código testado]] — `new_coverage` 0.0 com teste existente: o arquivo está nas exclusões de cobertura do runner (vitest/jest/jacoco) e não entra no relatório importado pelo Sonar
- [[sonar-new-violations-todo-portugues|Sonar: new_violations e o "Todo" em português]] — gate com limite 0 cai até por issue INFO; "Todo" em comentário vira S1135, ternário aninhado vira S3358, complexidade > 15 vira S3776; diagnosticar pelo MCP com a chave do PR do log
