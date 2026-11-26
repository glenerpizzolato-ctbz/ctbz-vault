---
name: sonar-repo-novo-sem-analise-da-branch-padrao
description: "Repo novo: sonar-merge-request falha com 'No branch exists in Sonarqube with the name main' porque o projeto nunca teve análise da branch padrão; é preciso uma análise da master antes do primeiro MR"
metadata:
  type: reference
tags:
  - ci
  - sonar
---

# Sonar: "No branch exists in Sonarqube with the name main"

Visto em 2026-11-26 no `zendeskapp-warnings-and-messages` (MR !1, o primeiro do repo).

**Sintoma:** o `sonar-merge-request` aborta em segundos, antes de analisar o código, com `ERROR No branch exists in Sonarqube with the name main` e `EXECUTION FAILURE`. Mesmo com `sonar.pullrequest.base=master` (o `CI_DEFAULT_BRANCH`), a mensagem cita `main`.

**Causa:** o projeto ainda não tem nenhuma análise de branch no SonarQube. A análise de MR (`sonar.pullrequest.*`) precisa que a branch base já exista lá; sem ela, o scanner cai na branch principal padrão do servidor (`main`), que também não existe. Num repo recém-criado, a `master` só tem o README do GitLab: não tem `sonar-project.properties` e nunca rodou pipeline, então o job `sonar` (que só roda na branch padrão e em tags) nunca criou o projeto.

**Correção que funcionou (2026-11-26): pipeline de tag, sem mexer na master.** O job `sonar` roda em `$CI_COMMIT_TAG || branch padrão`; uma tag no commit da branch do MR (que já tem `.gitlab-ci.yml`, `package.json`, `vitest.config`, `sonar-project.properties`) cria o projeto no Sonar:

```bash
git tag 0.1.0 HEAD   # mesma versão do package.json
git push origin 0.1.0 -o ci.variable="CUSTOM_JOB_DEPLOY=false" -o ci.variable="JOBS_BYPASS=increment-package-json-version"
# depois do job sonar verde:
git push origin --delete 0.1.0 && git tag -d 0.1.0
glab api -X POST "projects/<id>/merge_requests/<iid>/pipelines"   # nova pipeline do MR
```

- `CUSTOM_JOB_DEPLOY=false`: na tag o deploy de dev/prd fica manual, mas é melhor nem criar.
- `JOBS_BYPASS=increment-package-json-version`: na tag esse job clona a branch padrão e faz push do bump de versão **na master**; num repo novo isso ou falha (master sem `package.json`) ou suja a master.
- O Sonar registra a análise com o nome da tag (`branch=0.1.0`), mas o projeto passa a existir e a análise do MR volta a funcionar (aí aparecem as condições do gate de verdade).

Só subir o `sonar-project.properties` na master **não basta**: sem `.gitlab-ci.yml` a master nem roda pipeline, e com ele o `ctbz-check-test` e o build falham sem `package.json`/`vitest.config` e pulam o Sonar. Alternativa: pedir ao DevOps para criar o projeto no SonarQube.

Relacionado: [[pipeline-repo-novo-sem-variaveis-ci]] (sem os arquivos do repo `pipeline`, o MR também sai sem test/coverage e o quality gate cai em 0%).
