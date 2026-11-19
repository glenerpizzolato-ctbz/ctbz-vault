---
name: deploy-saude-pos-deploy
description: "Como descobrir os deploys (quem, quando, onde) pela API do GitLab e verificar a saúde do serviço depois do deploy pelo Cloud Monitoring, sem VPN"
metadata:
  type: reference
tags:
  - infra
  - deploy
  - monitoring
---

# Deploys e saúde pós-deploy

Nota escrita à mão (não é gerada pela skill do catálogo). É a receita usada pela aba Monitoring do BahCode.

## Achar os deploys

- O componente de pipeline (`ctbz/devops/recursos/pipeline/ci-cd`, repo `~/repositories/pipeline`) declara `environment` do GitLab nos jobs de deploy: `dev`, `dev1…dev6`, `stg` e `prd` (stg e prd são manuais). Por isso a **API de deployments** do GitLab traz cada deploy com ambiente, autor (quem disparou o pipeline ou deu play no job manual), status, ref, sha e o job: `glab api "projects/<id>/deployments?status=success&order_by=updated_at&sort=desc&updated_after=<ISO>"`.
- Status `blocked` é job manual ainda não executado (ex.: `migrations-check-prd`); só `success` é deploy feito.
- **Armadilha:** o `last_activity_at` do projeto **não** muda com o deploy (o `bots-api` teve deploy às 20:27, mas a última atividade era das 19:31). Para achar deploys recentes de um grupo, listar os projetos com atividade nos últimos dias (`groups/<g>/projects?include_subgroups=true&last_activity_after=…`) e consultar os deployments de cada um.
- O GraphQL não ajuda: `environments` só pode ser pedido para um projeto por vez.

## Onde o deploy foi parar (log do job)

`glab api projects/<id>/jobs/<job>/trace` (tirar as cores ANSI):

- **Cloud Run via gcloud:** `Deploying container to Cloud Run service [S] in project [P] region [R]`.
- **Cloud Run via Terraform** (ex.: `experts-nfs`, `experts-functions`): linhas `google_cloud_run_v2_service…[id=projects/P/locations/R/services/S]`; os alterados têm `Modifications complete`/`Creation complete`. Um job pode atualizar vários serviços (o `experts-functions` tem quatro).
- **GKE via helm:** `kubeconfig entry generated for <cluster>.` e `helm upgrade --install … --namespace <ns> <release> … --set app=<app>`. O container tem o nome do app; o namespace é `<NAMESPACE>-<env>`. Clusters de prod ficam no projeto `contabilizei-prod-01`, e os de dev, em `contabilizei-dev-01`.

## Saúde sem VPN (Cloud Monitoring)

As métricas dos clusters privados estão no Cloud Monitoring, que não depende da VPN (o `kubectl` depende). REST com o token do `gcloud auth print-access-token`, `GET https://monitoring.googleapis.com/v3/projects/<p>/timeSeries?filter=…&interval.startTime=…&interval.endTime=…&aggregation.*` (o `gcloud` não lê séries temporais):

- **Pods vivos (GKE):** `kubernetes.io/container/uptime` com `resource.labels.namespace_name`/`container_name`, últimos minutos, um série por `pod_name`.
- **Restarts (GKE):** `kubernetes.io/container/restart_count` com `ALIGN_DELTA` desde o deploy.
- **Respostas (Cloud Run):** `run.googleapis.com/request_count` agrupado por `metric.labels.response_code_class` (2xx, 5xx…). A condição do serviço vem de `https://run.googleapis.com/v2/projects/P/locations/R/services/S` (`terminalCondition.state = CONDITION_SUCCEEDED`).
- **Logs de erro (os dois):** `logging.googleapis.com/log_entry_count` com `metric.labels.severity=one_of("ERROR","CRITICAL","ALERT","EMERGENCY")` e o recurso (`k8s_container` ou `cloud_run_revision`). Comparar com o mesmo tempo antes do deploy, porque vários serviços têm erro de fundo (ex.: o `experts-nfs` prd loga 404 do `microservico-cep` o tempo todo).

## Conferir a versão da imagem que subiu (ex: base Node depois de uma CVE)

Dá para provar qual runtime está rodando em prod sem VPN e sem acesso de leitura ao Artifact Registry de `contabilizei-tools-production` (o usuário não tem `artifactregistry.repositories.downloadArtifacts` lá):

1. No log do job `build-push-container`, a linha `FROM docker.io/library/node:<tag>@sha256:…` mostra o digest da base usada; comparar com `curl -s https://hub.docker.com/v2/repositories/library/node/tags/<tag-de-patch>`. O `CONTAINER_TAG` mostra a tag da imagem (ex: `registry.gitlab.com/ctbz/devops/recursos/containers/<repo>:<versão>`).
2. No log do `helm-deploy-gke-prd` (ou do deploy de Cloud Run), conferir que `deployment.image.tag=<versão>` é a mesma; no `release-artifact-registry`, o digest publicado.
3. Puxar a mesma tag do registry do GitLab, que aceita o token do glab (`glab config get token --host gitlab.com | docker login registry.gitlab.com -u oauth2 --password-stdin`), conferir que o `RepoDigests` bate com o do release e rodar `docker run --rm --entrypoint sh <imagem> -c 'node -v; cat /etc/alpine-release'` (o `--entrypoint` é necessário porque o `secrets-init` não existe fora do cluster). Fazer `docker logout registry.gitlab.com` no fim.
4. Rollout no GKE sem VPN: `gcloud logging read 'resource.type="k8s_container" AND resource.labels.namespace_name="<ns>" AND resource.labels.container_name="<app>"' --project contabilizei-prod-01` agrupando por ReplicaSet (o hash do meio do nome do pod). O ReplicaSet novo começa a logar logo depois do helm, e o antigo para.
4b. Em Cloud Run, a prova direta é o digest da revisão no ar: `gcloud run revisions describe <rev> --project <p> --region us-central1 --format='value(status.imageDigest)'` é idêntico ao `RepoDigests` da tag puxada do registry do GitLab (o `release-artifact-registry` só retagueia, não rebuilda). Para a brotli do SO: `apk info -v | grep brotli` (Alpine) ou `dpkg-query -W 'libbrotli*'` (Debian). Usado na evidência do PRD-178206 (2026-11-19), com 9 repos.
5. O container-scanning (Trivy) da pipeline também mostra se a CVE ainda aparece na imagem.
