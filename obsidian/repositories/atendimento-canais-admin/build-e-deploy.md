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

## Imagem base e Node local

- O `Dockerfile` usa `node:24-alpine` nos estágios `build` e `runner`. Ficou fixado em `node:24.22.1-alpine` por causa da CVE-2026-111497 (PRD-174630) e voltou para a tag de linha em 2026-11-19 (MR !199, work-item #5), quando a `24-alpine` já resolvia para a 24.22.3. Antes de voltar uma tag de linha, comparar no Docker Hub o digest dela com o das tags de patch (`curl -s https://hub.docker.com/v2/repositories/library/node/tags/<tag>`).
- Com Node 22 local, o teste `importacao.arquivo.test.ts > DecodificadorDeTexto > preserva os caracteres exclusivos do Windows-1252` falha (o `TextDecoder('windows-1252')` do Node 22 devolve `\u0093` em vez de `“`). No Node 24 passa: não é regressão, é o Node local. Rodar os testes com Node 24.

## Terraform x vault-roleset (onde fica cada permissão)

- O repositório tem `terraform/{dev,prd}` (state no bucket `ctbz-terraform-state`, prefixo `atendimento-canais-admin/<ambiente>`), aplicado pelo pipeline, só para recursos do próprio admin e IAM neles (ex: bucket do marketplace). A SA do Cloud Run está na variável `runtime_service_account` (prd `852985851006-compute@…`, dev `410826691463-compute@…`).
- **Permissões da SA em projetos (inclusive de outros donos, como BigQuery no `contabilizei-data`) ficam no repositório `vault-roleset`**, em `gcp-roleset-default-user-managed/atendimento-canais-{prd,dev}/<sa>.json`, não no Terraform daqui. Ver [[_vault-roleset-indice|vault-roleset]]. O MR !203, que punha a leitura do dataset do CDC no Terraform, foi fechado por isso (e porque a permissão já existia).
