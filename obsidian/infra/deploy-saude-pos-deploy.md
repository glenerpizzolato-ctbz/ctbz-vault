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
