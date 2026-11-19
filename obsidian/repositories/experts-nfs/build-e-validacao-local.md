---
name: experts-nfs-build-e-validacao-local
description: "Como instalar as dependências, buildar a imagem Docker e validar o Prisma contra o banco de dev no experts-nfs"
metadata:
  type: reference
tags:
  - experts-nfs
---

# experts-nfs: build e validação local

- **Dependências**: o pacote privado `@contabilizei-private/*` vem do Artifact Registry (`us-central1-npm.pkg.dev/contabilizei-tools-production/npm/`) e o `.npmrc` do repo não traz token. Usar o pnpm da Dockerfile (`npx -y pnpm@10.12.4`), porque o pnpm global mais novo volta 403 nesse registro, e passar um token temporário por um userconfig fora do repo: `echo "//us-central1-npm.pkg.dev/contabilizei-tools-production/npm/:_authToken=$(gcloud auth print-access-token)" > <tmp>; CI=true NPM_CONFIG_USERCONFIG=<tmp> npx -y pnpm@10.12.4 install --frozen-lockfile; rm <tmp>`. Com o `node_modules` desatualizado (ex: numa worktree), os testes e o typecheck quebram com `Cannot find package '@contabilizei-private/br-utils'` e `testcontainers`.
- **Build da imagem**: o `docker build` também precisa do token. Copiar o contexto para uma pasta temporária, acrescentar o `_authToken` ao `.npmrc` da cópia e buildar dela. O `COPY . .` guarda o `.npmrc` numa camada (o `rm .npmrc` vem num RUN depois), então apagar a imagem e o cache (`docker rmi …; docker builder prune -f`) ao terminar.
- **Validar o Prisma em dev**: subir `sql_exp_dev` (porta **5435**; o `DATABASE_URL` de dev comentado no `.env` aponta para a 5436, então trocar a porta) e rodar a imagem com `--network host -e DATABASE_URL=…`, executando `npx prisma migrate status` e uma consulta pelo `PrismaClient`. O Prisma 5.22 funciona no Node 24 (`node:24-alpine`, engine `linux-musl-openssl-3.0.x`), validado em 2026-11-19 (MR !335).
