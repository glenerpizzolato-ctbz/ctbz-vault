---
name: docker-build-local
description: "Como rodar o docker build do bots-api localmente: o .npmrc do repo não tem token e o pnpm 11 falha com 401 no Artifact Registry (ERR_PNPM_MINIMUM_RELEASE_AGE_VIOLATION)"
metadata:
  type: reference
tags:
  - bots-api
  - docker
---

# Docker build local do bots-api

O `Dockerfile` copia o `.npmrc` do repo para dentro da imagem, mas esse `.npmrc` só aponta o escopo `@contabilizei-private` para o Artifact Registry (`us-central1-npm.pkg.dev/contabilizei-tools-production/npm/`), sem token: no CI a autenticação é injetada. Por isso, um `docker build .` puro falha no `pnpm install --frozen-lockfile` com `ERR_PNPM_MINIMUM_RELEASE_AGE_VIOLATION` ("could not be checked against minimumReleaseAge ... Unauthorized - 401") nos pacotes `@contabilizei-private/*`. O erro parece de lockfile, mas é só falta de autenticação.

Para validar o build sem sujar a worktree, montar uma cópia do repo num diretório temporário com um token temporário do gcloud (o `.npmrc` é apagado no fim do Dockerfile, mas fica numa camada da imagem: apagar a imagem depois):

```sh
S=$(mktemp -d); git archive HEAD | tar -x -C $S; cp Dockerfile .npmrc $S/
echo "//us-central1-npm.pkg.dev/contabilizei-tools-production/npm/:_authToken=$(gcloud auth print-access-token)" >> $S/.npmrc
docker build -t bots-api:check $S && docker run --rm --entrypoint node bots-api:check -v
docker rmi -f bots-api:check; rm -rf $S
```

O `ENTRYPOINT` é o `/tmp/bin/secrets-init`, que não existe na imagem local: usar `--entrypoint` para rodar comandos nela.

Descoberto em 2026-11-19, ao voltar a imagem base para `node:24-alpine` (work-item #15, MR !161).

## Onde roda em prod

O deploy de prod do `bots-api` é pelo helm no GKE (`contabilizei-private-cluster-prod-01`, namespace `atendimento-canais-prd`, job `helm-deploy-gke-prd`). O Cloud Run `bots-api` em `atendimento-canais-prd` está parado desde 2026-04 (revisão `bots-api-00020-4q9`, imagem 1.0.44) e não reflete o que está em produção. Para conferir a imagem que subiu, ver [[deploy-saude-pos-deploy]].
