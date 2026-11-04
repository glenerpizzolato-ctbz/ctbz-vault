---
name: vault-roleset-secrets-e-permissoes
description: "vault-roleset: onde ficam os acessos de uma SA aos secrets do contabilizei-sm-prod/dev e como o nome completo do secret é montado"
metadata:
  type: reference
---

# Secrets e permissões

- Os bindings de SAs já existentes ficam em `gcp-roleset-default-user-managed/<projeto>/<email-da-sa>.json`: uma entrada por projeto com `roles`; a entrada de `contabilizei-sm-prod` (ou `-dev`) lista em `secrets` os nomes curtos a que a SA tem `roles/secretmanager.secretAccessor`.
- O `create_update_roles.sh` monta o nome real como `<projeto-de-origem>_<SECRET>` (ex: `contabilizei-experts-prd_MANDRILL_KEY`), cria o secret vazio se ele não existir e faz `gcloud secrets add-iam-policy-binding` por secret. O caminho final é `projects/<número>/secrets/<nome>`, com `1046698394190` = `contabilizei-sm-prod` e `642208929799` = `contabilizei-sm-dev`. O valor é inserido à parte pelo `create_secret_value.sh` (branch `create-secret-value`).
- Esse é o mesmo padrão do `SM_PREFIX` do módulo `cloud_run` do experts-functions (`projects/${sm_project_id}/secrets/${project_id}_${secret_name}`).
- Exemplo: a SA de runtime do Cloud Run em `contabilizei-experts-prd` (`754947058455-compute@developer.gserviceaccount.com`) tem acesso ao `MANDRILL_KEY` desde a3cabaa9 (2025-11-05, Gabriel Ganassin).
- Para ler direto do Git sem mexer no checkout local (que pode estar em branch de trabalho), usar `git show origin/master:<arquivo>`.
- O state de Terraform dos repositórios fica no bucket compartilhado `gs://ctbz-terraform-state` (um prefixo por repo/ambiente, ex: `experts-functions/prd`). As SAs das pipelines ganham acesso pelo roleset (`resource "buckets/ctbz-terraform-state"` com `roles/storage.objectAdmin`, ou `roles/storage.objectAdmin` em `contabilizei-tools-production`). O Glener não tem nenhuma permissão nele (testPermissions vazio em 2026-10-28), e o projeto dono do bucket não aparece para ele; o mais provável é `contabilizei-tools-production`, mas não foi confirmado.
