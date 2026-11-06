---
name: sonar-cobertura-excluida-no-runner
description: Arquivo excluído da cobertura no runner de testes (vitest/jest/jacoco) aparece com 0% no Sonar mesmo com teste; conferir as exclusões do runner antes de escrever mais teste
metadata:
  type: reference
tags:
  - sonar
  - cobertura
---

# Sonar com 0% de cobertura em código testado

Quando o quality gate do MR falha com `new_coverage` em **0.0** (e não num valor parcial), mesmo com testes para o código novo, a causa costuma ser o runner de testes não gerar cobertura para aquele arquivo: ele está nas exclusões do runner (`coverage.exclude` do vitest, `coveragePathIgnorePatterns` do jest, `excludes` do jacoco) e por isso não entra no relatório (lcov/xml) que o Sonar importa. O Sonar não faz a mesma exclusão (a dele é `sonar.coverage.exclusions`) e conta o arquivo como totalmente descoberto.

Como resolver: tirar do runner a exclusão que pega o arquivo (ou restringi-la aos arquivos que de fato não são do MR) em vez de escrever mais teste; depois conferir o gate pelo MCP do SonarQube.

Exemplo: [[cobertura-sonar-vitest|experts-service, MR !148]]. Ver também [[sonar-cobertura-branches-kotlin]] e [[sonar-duplicacao-codigo-novo]].
