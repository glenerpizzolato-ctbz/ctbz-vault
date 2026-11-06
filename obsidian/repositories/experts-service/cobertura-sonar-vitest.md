---
name: cobertura-sonar-vitest-experts-service
description: No experts-service, arquivos fora do coverage.include/exclude do vitest aparecem com 0% de cobertura no Sonar mesmo com spec; src/infra/auth já caiu nisso
metadata:
  type: reference
tags:
  - experts-service
  - sonar
  - vitest
---

# Cobertura do Sonar x exclusões do vitest

O Sonar do experts-service lê a cobertura do `coverage/lcov.info` gerado pelo vitest (`sonar.javascript.lcov.reportPaths`). Se o arquivo estiver em `coverage.exclude` do `vitest.config.ts`, ele não entra no lcov e o Sonar conta todas as linhas como **0% de cobertura**, mesmo que exista `*.spec.ts` testando o arquivo. O `sonar.coverage.exclusions` do `sonar-project.properties` é outra lista e não cobre esses casos.

- Sintoma no MR: job `sonar-merge-request` falha com `QUALITY GATE STATUS: FAILED`, e o gate mostra `new_coverage` = `new_line_coverage` = 0.0, sem nenhuma issue de código.
- Caso real (MR !148, PRD-175691): `src/infra/auth/**/*` estava em `coverage.exclude`, e o `keycloak.ts` novo ficou com 0%. A correção foi restringir a exclusão a `src/infra/auth/helpers.ts` e completar os testes.
- Para conferir localmente a cobertura de um arquivo sem os thresholds globais: `npx vitest run <spec> --coverage --coverage.include='<pasta>/**' --coverage.thresholds.lines=0 --coverage.thresholds.functions=0 --coverage.thresholds.statements=0 --coverage.thresholds.branches=0`.
- Para ver o gate e as linhas descobertas do MR: MCP do SonarQube (`get_project_quality_gate_status` / `get_file_coverage_details` com o `pullRequest` do link do log).

Regra genérica em [[sonar-cobertura-excluida-no-runner]].
