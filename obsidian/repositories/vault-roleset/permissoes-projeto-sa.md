---
name: vault-roleset-permissoes-projeto-sa
description: "vault-roleset: onde ficam as roles de uma SA em outros projetos GCP (ex: BigQuery no contabilizei-data) e como conferir antes de pedir ou abrir MR"
metadata:
  type: reference
---

# Permissões de uma SA em projetos

- Cada SA já existente tem um JSON em `gcp-roleset-default-user-managed/<projeto-da-sa>/<email-da-sa>.json`, com uma entrada `{project, roles}` por projeto onde ela recebe roles. O `create_update_roles.sh` aplica cada uma com `gcloud projects add-iam-policy-binding` no **projeto inteiro** (não por dataset ou bucket).
- É aqui (e não no Terraform do serviço) que entra, por exemplo, BigQuery de outro projeto. As SAs de runtime do `atendimento-canais-admin` (`852985851006-compute@…` em prd, `410826691463-compute@…` em dev) têm `roles/bigquery.dataViewer` e `roles/bigquery.jobUser` em `contabilizei-dataflow`, `contabilizei-data` e `contabilizei-contabilake` desde 07/08/2026 (`2f3beb5a`, Gabriel Ganassin).
- Antes de pedir acesso ou abrir MR, conferir: `git show origin/master:gcp-roleset-default-user-managed/<projeto>/<sa>.json` e, para saber se foi aplicado, `gcloud projects get-iam-policy <projeto> --flatten="bindings[].members" --filter="bindings.members:<sa>" --format="table(bindings.role)"` (o Glener consegue ler a política do `contabilizei-data`).
- O checkout local costuma estar em branch de trabalho de outra demanda; para mudanças, usar uma worktree a partir do `origin/master`.
- Publicar em tópico de outro projeto (ex: os do `email-service` em `atendimento-canais-prd`) também entra aqui: uma entrada `{"project": "atendimento-canais-prd", "roles": ["roles/pubsub.publisher"]}` no JSON da SA (padrão do `super-app-bff`). Foi o caso da SA de runtime do Cloud Run do `contabilizei-experts` (`754947058455-compute`/`416872398669-compute`), vault-roleset!723 (PRD-178571, 24/11/2026). O dev não tem `pubsub.topics.getIamPolicy` nesses tópicos, então a conferência é pelo `get-iam-policy` do projeto.
- DLQ de subscription Pub/Sub (2026-11-24, vault-roleset!728): o service agent `service-<n>@gcp-sa-pubsub.iam.gserviceaccount.com` precisa publicar no tópico DLQ e consumir a subscription de origem. Como a SA de deploy das pipelines (`pipeline-container` etc.) só tem `roles/pubsub.editor`, sem `setIamPolicy`, o binding por recurso no Terraform falha com 403. O caminho sem `roles/pubsub.admin` é dar `roles/pubsub.publisher` + `roles/pubsub.subscriber` ao service agent no JSON dele em `gcp-roleset-default-user-managed/<projeto>/` (em `contabilizei-experts-prd` ele já tinha `roles/pubsub.editor`).
- A pipeline (componente central `ctbz/devops/recursos/pipeline`) aplica só no merge para a `master` (diff `CI_COMMIT_SHA^1..CI_COMMIT_SHA`): não dá para aplicar a partir da branch.
