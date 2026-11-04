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
