---
name: pipeline-repo-novo-sem-variaveis-ci
description: Repo novo no componente ci-cd sem variáveis de CI no projeto não gera build/lint/test, e o Sonar do MR falha com cobertura 0% (não é falta de revision)
metadata:
  type: reference
tags:
  - padroes
  - gitlab-ci
  - sonar
---

# Repo novo: Sonar do MR com cobertura 0%

Todos os repos usam o mesmo `.gitlab-ci.yml` (`include: component: $CI_SERVER_FQDN/ctbz/devops/recursos/pipeline/ci-cd@$PIPE_COMPONENT_VERSION`). O que liga cada job são as **variáveis de CI do projeto no GitLab** (Settings → CI/CD → Variables), não o arquivo.

Sintoma num repo recém-criado (ex: `agrupamento-guias-service`, MR !1 em 2026-11-03):

- A pipeline do MR só tem `context`, `js-requirements`, `npm-access-token`, `sonar-project-properties-available`, os scans de segurança e `sonar-merge-request`. Faltam `ctbz-check-test`, `build`, `lint`, `test-vitest`, `version-validation` e `build-push-container`.
- O `sonar-merge-request` loga `No LCOV files were found using ./coverage/lcov.info` e o quality gate falha em `new_coverage`/`new_line_coverage` = 0.0 (mínimo 80). O scan acha a revision normalmente: não é problema de SCM.
- O MR fica `ci_must_pass` e o merge pela API volta 405, mesmo com `only_allow_merge_if_pipeline_succeeds: false` no projeto.

Causa: o projeto não tem nenhuma variável (`glab api "projects/:id/variables"` devolve `[]`). Um Node/Zezu que funciona (ex: `email-service`) tem `APP_TYPE`, `CUSTOM_JOB_TEST`/`_IMAGE`/`_SCRIPT`/`_TYPE`, `CUSTOM_JOB_LINT*`, `CUSTOM_JOB_BUILD*`, `CUSTOM_JOB_DB_MIGRATION*`, `CI_CONTAINER_IMAGE`, `DEPLOYMENT_*`, `SCALEDOBJECT_*`, `GCLOUD_PROJECT*`, `NAMESPACE` etc. Correção: copiar as variáveis de um repo do mesmo tipo e ajustar os valores.

Contorno usado quando o dev decidiu fazer o merge mesmo assim: como Maintainer, merge `--no-ff` local de `origin/master` com a branch e `git push origin HEAD:master`. O GitLab marca o MR como `merged` sozinho.
