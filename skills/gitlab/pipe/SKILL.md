---
name: pipe
description: Investiga e corrige uma pipeline (ou job) que falhou no GitLab - lê o log pelo glab, acha a causa (teste, lint, build, Sonar, deploy, infra), corrige o código quando o problema é do MR, commita e dá push, ou faz o retry quando a falha é intermitente. Use quando o usuário pedir para ver/corrigir a pipeline ou o CI do MR, ou quando o BahCode mandar `/pipe <link>` (botão da pipeline na aba MR).
argument-hint: "[link da pipeline ou do job]"
---

# Corrigir a pipeline

1. Descobrir a pipeline: o link dos argumentos (`$ARGUMENTS`, de pipeline `…/-/pipelines/<id>` ou de job `…/-/jobs/<id>`) ou a última da branch atual (`glab ci get`).
2. Listar os jobs que falharam (`glab api "projects/:id/pipelines/<id>/jobs?scope[]=failed"`) e ler o log de cada um (`glab ci trace <job_id>` ou `glab api "projects/:id/jobs/<job_id>/trace"`), indo direto ao primeiro erro de verdade.
3. Classificar a causa:
   - **do código do MR** (teste, lint, tipo, build, quality gate do Sonar): reproduzir localmente quando der, corrigir, rodar de novo, commitar com commit semântico e dar push;
   - **intermitente ou de infraestrutura** (timeout, runner, rede, registry, flaky já conhecido): `glab ci retry <job_id>` e acompanhar;
   - **fora do MR** (a base quebrada, variável de CI, permissão, ambiente): não mexer; explicar a causa e quem/como resolve.
4. Responder com a causa, o que foi feito (commit, retry) e o link da nova pipeline.

## Quality gate do Sonar

O log do job `sonar-merge-request` só diz `QUALITY GATE STATUS: FAILED - View details on https://sonarqube.ctbz.com.br/dashboard?id=<projectKey>&pullRequest=<id>`. Para saber o motivo, usar o **SonarQube CLI** (`sonar`), que já fica autenticado em `https://sonarqube.ctbz.com.br` (token no keychain) e responde **sem VPN**. O `curl` no `$SONARQUBE_URL` do `~/dotfiles/.env` só responde com VPN, e o token de lá dá 401 no `sonarqube.ctbz.com.br`; não pedir VPN por isso.

1. Conferir a sessão: `sonar auth status` (deve mostrar `Connected` e o servidor acima). Se não estiver autenticado, pedir ao usuário para rodar `! sonar auth login`.
2. Ler o `projectKey` e o `pullRequest` do link do log e ver as condições do gate:
   `sonar api get "/api/qualitygates/project_status?projectKey=<projectKey>&pullRequest=<id>"`
   Cada condição traz `metricKey`, `actualValue`, `errorThreshold` e `status` (`ERROR` = a que derrubou).
3. Ir ao detalhe da condição que falhou:
   - `new_violations`: `sonar api get "/api/issues/search?componentKeys=<projectKey>&pullRequest=<id>&resolved=false&ps=100"` (regra, severidade, arquivo, linha e mensagem de cada issue).
   - `new_coverage`/`new_line_coverage`/`new_branch_coverage`: `sonar api get "/api/measures/component_tree?component=<projectKey>&pullRequest=<id>&metricKeys=new_coverage,new_uncovered_lines&qualifiers=FIL&ps=100"`, e conferir se o arquivo não está fora do relatório do runner (ver a nota `ci/sonar-cobertura-excluida-no-runner` do vault).
   - `new_duplicated_lines_density`: `sonar api get "/api/measures/component_tree?component=<projectKey>&pullRequest=<id>&metricKeys=new_duplicated_lines_density&qualifiers=FIL&ps=100"` e `sonar api get "/api/duplications/show?key=<projectKey>:<arquivo>&pullRequest=<id>"`.
   - `new_security_hotspots_reviewed`: `sonar api get "/api/hotspots/search?projectKey=<projectKey>&pullRequest=<id>"`.
4. Corrigir e conferir localmente antes do push com `sonar analyze --file <arquivo> [--file <outro>]` (análise local das regras, sem cobertura).

Armadilhas já vistas (detalhes nas notas de `ci/` do vault): `typescript:S2699` (BLOCKER) em teste vitest cujas únicas asserções são `expect(mock).not.toHaveBeenCalled()` ou `await expect(...).rejects…`: o Sonar não as conta; usar `expect(mock).toHaveBeenCalledTimes(0)`. O gate de `new_violations` tem limite 0, então até issue INFO derruba (ex: `TODO` em comentário).
