---
name: emissor-whatsapp-build-e-deploy
description: "emissor-whatsapp: código dos Cloud Run emissor-whatsapp e emissor-whatsapp-massivo; deploy era pelo Bitbucket Pipelines, hoje sem CI; 5 testes já falham"
metadata:
  type: reference
---

# Build e deploy

- O repositório (grupo `ctbz/experts/arquivo`) é o código do Cloud Run `emissor-whatsapp-massivo` (`contabilizei-experts-prd`; o `emissor-whatsapp` singular não existe mais no Cloud Run em 2026-10-26), publicado com `gcloud run deploy --source=.` a partir de `app/` (usa o `app/Dockerfile`).
- O deploy era feito pelo `bitbucket-pipelines.yml` (steps `deploy_singular`/`deploy_massivo`). No GitLab não há `.gitlab-ci.yml`, então hoje qualquer deploy é manual, seguindo esses steps (o bundle sai de `pnpm run build:prod:massivo`).
- O tráfego do `emissor-whatsapp-massivo` está fixado numa revisão (00104-c8l). Depois de um deploy, rodar `gcloud run services update-traffic emissor-whatsapp-massivo --to-latest` para a revisão nova receber tráfego.
- Para subir o container localmente, passar `ENVIRONMENT=CLOUD`, `SSO_APP_SECRET` e `SSO_HOST` (com valores fictícios ele sobe; sem eles quebra com "Invalid app credentials").
- Em 2026-10-26, 5 testes já falhavam também no Node 22.2.0 (validação de CNPJ, sanitização de strings e fallback de consulta da empresa).
- Ver [[cve-2026-111497-node2shell]].
