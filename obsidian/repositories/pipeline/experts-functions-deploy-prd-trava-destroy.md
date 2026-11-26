---
name: pipeline-experts-functions-deploy-prd-trava-destroy
description: "O deploy-prd do experts-functions usa um script próprio na pipeline central que falha se o plan destruir ou recriar recurso; como liberar um destroy intencional"
metadata:
  type: reference
tags:
  - pipeline
  - experts-functions
  - terraform
criado_em: 2026-11-25
---

# Trava de destroy no deploy-prd do experts-functions

O `deploy-prd` do experts-functions não usa o `TERRAFORM_RESOURCES_SCRIPT` padrão de `custom/ctbz.yml`. Ele usa o `CUSTOM_JOB_DEPLOY_SCRIPT` de `custom/ctbz/experts/backend/experts-functions.prd.yml`, que faz o seguinte:

1. Salva o plan (`-out=tfplan`).
2. Falha **antes do apply** se o `terraform show` do plan tiver `will be destroyed`, `will be replaced` ou `must be replaced`.
3. Aplica o plan salvo e conferido.

## Sintoma

O job termina com `ERROR: Job failed: command terminated with exit code 1` logo depois de imprimir o plan, sem nenhum erro do Terraform. A última linha útil do log é o `# … will be destroyed`.

Isso aconteceu em 25/11/2026, no job `18375731122`, quando o experts-functions!14 removeu o trigger do Eventarc `email-holerites`.

## Como liberar um destroy intencional

- **Depois do pipeline!3568 (PRD-179355):** rodar o `deploy-prd` passando a variável `TF_ALLOW_DESTROY=true`, que libera a trava só naquela execução e registra isso no log.
- **Sem ele:** apagar o recurso fora do Terraform (ex: com `gcloud`). No próximo plan, o refresh tira o recurso do state sem acusar destroy.

## Imports one-off (removidos no !3568)

O script tinha `terraform state show X || terraform import X` para os recursos criados antes de o state existir. Depois do primeiro deploy, eles não fazem nada, e passam a **quebrar** o deploy assim que um recurso é apagado de propósito: o script tenta importar algo que não existe mais.

Relacionado: [[deploy-from-mr-e-version]], experts-functions PRD-178821.
