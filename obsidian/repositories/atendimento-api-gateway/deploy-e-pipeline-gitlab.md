---
name: atendimento-api-gateway-deploy-e-pipeline-gitlab
description: "atendimento-api-gateway no GitLab: a pipeline da master falha na criação desde pelo menos 2026-10-21 (cloudrun-deploy-* precisa de release-artifact-registry, que não existe), então merge no GitLab não publica o Kong; como conferir se uma rota nova está no ar"
metadata:
  type: reference
tags:
  - atendimento-api-gateway
  - kong
  - ci
criado_em: 2026-11-26
---

# Deploy do atendimento-api-gateway (GitLab)

- **A pipeline da `master` não cria jobs.** Desde pelo menos 2026-10-21 (iids 19, 38 e 41) ela termina `failed` na hora com: `'cloudrun-deploy-dev' job needs 'release-artifact-registry' job, but 'release-artifact-registry' does not exist in the pipeline` (o mesmo para `cloudrun-deploy-prd`). A API REST só mostra `failed` sem jobs; o motivo aparece no GraphQL (`pipelines { failureReason errorMessages { nodes { content } } }`). Pelo plano de migração (`docs/plano-migracao-gitlab.md`), o fluxo esperado é release → `increment-version` → `cloudrun-deploy-dev/prd` manuais; falta o job de release (ou o `needs` ficar `optional`) na config do repo `pipeline` (`custom/ctbz/atendimento/geral/atendimento-api-gateway*.yml`).
- Consequência: **merge no GitLab não publica o Kong**. As pipelines de MR passam (só checks), o que engana. Visto no !9 (rota do app Avisos e Mensagens, 2026-11-26): mergeado, mas a rota não estava no ar.
- O `gcloud run services describe atendimento-api-gateway --project contabilizei-crm[-dev] --region us-central1` não devolveu nada com o usuário do dev (sem permissão nesses projetos).

## Conferir se uma rota de app está no ar

Com um JWT HS256 do consumer `zendeskapp` (ver [[autenticacao-kong-jwt]]):

- rota publicada, caminho inexistente no back-end → 404 em **JSON** do atendimento-zendesk (`{"errors":[{"code":"404","title":"NOT_FOUND",...}]}`); fora do `allow_paths` → 403 `path not allowed`;
- rota **não** publicada → 404 em **HTML** do Next.js ("This page could not be found"): caiu na rota `/` do `atendimento-front`. Sem JWT, os dois casos dão 401.
