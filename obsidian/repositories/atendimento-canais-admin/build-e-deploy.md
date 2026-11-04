---
name: atendimento-canais-admin-build-e-deploy
description: "atendimento-canais-admin: antigo canais-bff; build exige token do registry npm privado; build.sh faz deploy manual público e criou um serviço avulso no aida-stg"
metadata:
  type: reference
---

# Build e deploy

- O repositório se chamava `canais-bff` (ainda aparece no `.cta.json`, no `.planning/` e no `build.sh`). Imagens `gcr.io/contabilizei-tools-production/canais-bff:*` são deste repositório.
- O deploy oficial é pelo CI (componente `ctbz/devops/recursos/pipeline/ci-cd`), para o Cloud Run `atendimento-canais-admin-dev` no projeto `atendimento-canais-dev` (e `-prd` em `atendimento-canais-prd`).
- **Armadilha:** o `build.sh` faz build local e `gcloud run deploy atendimento-canais-admin-dev --allow-unauthenticated` **sem `--project`**, então publica no projeto gcloud default de quem roda. Foi assim que nasceu o serviço avulso `atendimento-canais-admin-dev` no `aida-stg` (abril/2026, Gabriel Ganassin), público e esquecido, que o Wiz apontou como P2 grau A na CVE-2026-111497. Ver [[cve-2026-111497-node2shell]].
- **Build local da imagem:** o `pnpm install` do Dockerfile falha com 401 no registry `@contabilizei-private` (`us-central1-npm.pkg.dev/contabilizei-tools-production/npm/`), porque o `.npmrc` do repo não tem token (o CI injeta). Para testar, buildar numa cópia temporária com `//us-central1-npm.pkg.dev/contabilizei-tools-production/npm/:_authToken=$(gcloud auth print-access-token)` no `.npmrc`; o estágio final só copia `.output`, mas apagar a imagem e rodar `docker builder prune` no fim. O container sobe na porta 3000 (`/` responde 307).
