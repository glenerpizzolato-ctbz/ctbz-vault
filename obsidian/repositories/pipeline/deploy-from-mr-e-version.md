---
name: deploy-from-mr-e-version
description: "Pipeline central: o DEPLOY_FROM_MR exige VERSION de um job *-requirements; repos sem isso (ex: Go) falham no build-push-container do MR"
metadata:
  type: reference
tags:
  - pipeline
---

# DEPLOY_FROM_MR e VERSION na pipeline central

- No `templates/ci-cd.yml`, a `VERSION` vem de um job de requisitos da linguagem (`java-requirements` pelo `pom.xml`, `js-requirements` pelo `package.json`, `python-requirements` pelo `pyproject.toml`) ou da tag git. O `go-requirements` aparece só como `needs` opcional e não existe.
- Com `DEPLOY_FROM_MR` ligado, o `version-validation` faz `VERSION="${VERSION}-${CI_COMMIT_SHORT_SHA}-dev"` no MR. Sem a `VERSION`, a tag fica `:-<sha>-dev` e o `build-push-container` quebra com `invalid reference format`.
- Correção por serviço: `DEPLOY_FROM_MR: "false"` no `custom/ctbz/<grupo>/<repo>.yml` (vários serviços já fazem, ex: `parser-nfse`), e o deploy passa a sair por tag. Exemplo: html-to-pdf, [pipeline!3271](https://gitlab.com/ctbz/devops/recursos/pipeline/-/merge_requests/3271) (2026-10-30).
- No clone local, usar uma worktree a partir do `origin/master` (`git worktree add -b <branch> ../pipeline.wt/<nome> origin/master`), porque o clone costuma estar em outra branch com trabalho em andamento.
- **Armadilha:** desligar o `DEPLOY_FROM_MR` pode mudar a imagem dos jobs de `lint`/`test`. No html-to-pdf, eles rodavam na `golang:1.23-bookworm` com o deploy de MR ligado e voltaram para o `CI_CONTAINER_IMAGE` do `custom/` (1.20) depois. Conferir a imagem do `custom/` contra a versão da linguagem do repositório ([pipeline!3276](https://gitlab.com/ctbz/devops/recursos/pipeline/-/merge_requests/3276)).
