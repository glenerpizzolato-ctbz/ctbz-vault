---
name: ctbz-check-sonar-vitest
description: "Job ctbz-check-test (checker sonar-vitest) falha e pula build/lint/test: o vitest.config precisa ser export default defineConfig({...}) literal (sem mergeConfig) com globals/watch/coverage/reporters fixos, e o sonar-project.properties precisa de projectName, tests, test.inclusions e lcov em ./coverage/lcov.info"
metadata:
  type: reference
tags:
  - ci
  - sonar
  - vitest
---

# ctbz-check sonar-vitest

Com `CUSTOM_JOB_TEST_TYPE: vitest`, a pipeline roda no pre-build o `ctbz-check-test` (`ctbz-check sonar-vitest`, repo `ctbz/excelencia/ferramentas/ctbz-check`, `src/checkers/sonar-vitest.js`). Se ele falha, **build, lint, test e sonar ficam todos `skipped`**. Visto em 2026-11-26 no `zendeskapp-warnings-and-messages` (MR !1).

## O que ele exige

**`vitest.config.ts` (ou `.js`)**, lido por AST com `@babel/parser`, sem executar:

- `export default defineConfig({...})` com objeto literal, ou `defineConfig((env) => ({...}))`. **Não funciona** `defineConfig((env) => mergeConfig(viteConfig(env), {...}))` (o corpo é uma chamada, não um objeto): dá "Não foi possível encontrar configuração para defineConfig". Reaproveitar o `vite.config.ts` com `mergeConfig` derruba o check; repetir no vitest.config o que for preciso (ex: `plugins: [react()]`).
- `test.globals: true`, `test.watch: false`.
- `test.coverage.enabled: true`, `reportsDirectory: 'coverage'`, `reporter` com `cobertura`, `lcov`, `json` e `text`, `exclude` como array, e no Vitest >= 4 `include` como array não vazio de strings (`all`, se presente, `true`).
- `test.reporters` com `'verbose'` e `['junit', { outputFile: 'coverage/junit-coverage.xml' }]`.

**`sonar-project.properties`:**

- `sonar.projectKey` e `sonar.projectName` iguais ao nome do projeto no GitLab (`CI_PROJECT_NAME`).
- `sonar.sources`, `sonar.tests` e `sonar.test.inclusions` (não vazios), `sonar.sourceEncoding=UTF-8`.
- `sonar.javascript.lcov.reportPaths=./coverage/lcov.info` (com o `./`); `sonar.typescript.lcov.reportPaths` não pode existir.

## Validar antes de subir

```bash
glab repo clone ctbz/excelencia/ferramentas/ctbz-check -- --depth 1 /tmp/ctbz-check
(cd /tmp/ctbz-check && npm ci --ignore-scripts)
CI_PROJECT_NAME=<repo> node /tmp/ctbz-check/bin/ctbz-check.js sonar-vitest   # rodar na raiz do repo
```

Exemplo que passa: `vitest.config.ts` e `sonar-project.properties` do `zendeskapp-warnings-and-messages` (commit `ab93f0c`) e a fixture `test/__fixtures__/success/vitest.config.ts` do ctbz-check.
