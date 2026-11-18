---
name: pipeline-sem-testes-sonar-agrupamento-guias-service
description: O agrupamento-guias-service não tem arquivo custom no repo de pipeline (ctbz/devops/recursos/pipeline), então a pipeline não roda build/lint/teste e o sonar-merge-request reprova todo MR que mexe em src/ por falta de cobertura
metadata:
  type: reference
tags:
  - agrupamento-guias-service
  - sonar
  - pipeline
---

# Pipeline sem testes: Sonar reprova por cobertura

Levantado em 2026-11-18, no MR !3.

- O `.gitlab-ci.yml` só inclui o componente `ctbz/devops/recursos/pipeline/ci-cd`. O que cada serviço roda (build, lint, teste, migration, terraform, deploy) vem do arquivo do serviço em `custom/ctbz/<grupo>/<repo>.yml` (mais `.dev.yml`/`.prd.yml`) no repo `ctbz/devops/recursos/pipeline` (clone em `~/repositories/pipeline`). **Não existe** `custom/ctbz/experts/atendimento-canais/agrupamento-guias-service*.yml`.
- Sem ele, a pipeline do MR só tem os jobs genéricos (`context`, `js-requirements`, `npm-access-token`, `sonar-project-properties-available`, `semgrep-sast`, `secret_detection`, `gemnasium-dependency_scanning`, `sonar-merge-request`). Não roda `pnpm test:coverage`, então o Sonar loga `No LCOV files were found using ./coverage/lcov.info` e o quality gate reprova o código novo por cobertura (`QUALITY GATE STATUS: FAILED`).
- Por isso o MR !1 (código) reprovou e o !2 (só dependências, sem código novo medido) passou. Retry não resolve: é preciso criar o arquivo custom.
- Modelo: `custom/ctbz/experts/atendimento-canais/contato-service.yml` (Node + pnpm + vitest: `CUSTOM_JOB_BUILD`, `CUSTOM_JOB_LINT` com `typecheck` + `lint:check`, `CUSTOM_JOB_TEST` com `CUSTOM_JOB_TEST_TYPE: vitest` e `npm run test:coverage`, `CUSTOM_JOB_DB_MIGRATION`, `TERRAFORM_RESOURCES_ENABLED`, namespace `atendimento-canais`), com `.dev.yml`/`.prd.yml` de projeto GCP, recursos e Cloud SQL proxy.
- O gate do PR pode ser consultado em `$SONARQUBE_URL/api/qualitygates/project_status?projectKey=agrupamento-guias-service&pullRequest=<id>` (token em `~/dotfiles/.env`), mas o SonarQube só responde com a VPN.

## Não dá para forçar o merge

- Desde que o grupo raiz `ctbz` passou a ter `only_allow_merge_if_pipeline_succeeds: true` (os subgrupos `ctbz/experts` e `ctbz/experts/atendimento-canais` e o projeto mostram `false` na API REST, mas o valor efetivo no GraphQL `project.onlyAllowMergeIfPipelineSucceeds` é `true`), o merge com pipeline falha volta `405` e o `mergeabilityChecks` mostra `CI_MUST_PASS: FAILED`. A regra cascateia do grupo: Maintainer do projeto não a desliga.
- O MR !1 foi mergeado em 2026-11-03 com a pipeline falhando, antes de a regra valer; o !3 (2026-11-18) já ficou bloqueado. Saída: criar o arquivo custom no repo de pipeline, para o teste rodar e o Sonar receber a cobertura.
- Correção em andamento: MR [!3503](https://gitlab.com/ctbz/devops/recursos/pipeline/-/merge_requests/3503) no repo de pipeline cria `custom/ctbz/experts/atendimento-canais/agrupamento-guias-service.yml` (build, lint e `test-vitest`, sem deploy). Só vale depois do merge e de uma nova versão do componente (`PIPE_COMPONENT_VERSION`, tags `1.18.x`).
