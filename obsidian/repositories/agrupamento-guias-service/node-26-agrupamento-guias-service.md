---
name: node-26-agrupamento-guias-service
description: "Migração do agrupamento-guias-service para Node 26 com TypeScript nativo (MR !8, work-item #9): o que mudou, armadilhas (ioredis no nodenext, noUncheckedIndexedAccess) e como validar a imagem localmente"
metadata:
  type: project
tags:
  - agrupamento-guias-service
  - nodejs
---

# Node 26 no agrupamento-guias-service

Validado em 2026-11-18 sobre `origin/master` (d63aa2b), num container `node:26` (v26.13.1). Modelo de referência: [[node-26-typescript-nativo]].

Hoje o repo usa Node 24 (`node:24-alpine` no Dockerfile e na pipeline), esbuild (`--target=node24`) gerando `dist/index.js`, `tsx` no dev, TypeScript 5.9 com `moduleResolution: bundler` e alias `src/*`.

## Node 26 mantendo o build: funciona

- `tsc --noEmit` OK; 37 arquivos / 146 testes do vitest passam com 100% de cobertura.
- O bundle do esbuild sobe no Node 26 até a validação de env (todas as dependências carregam).
- A pipeline já usa `node:26-alpine` no `CI_CONTAINER_IMAGE` (MR !3503 do repo pipeline, 2026-11-18). Falta, no próprio serviço: `node:26-alpine` no Dockerfile, `--target=node26` no `build`, `@types/node` 26 e `engines.node`.

## TypeScript nativo (sem build): ainda não

- `node src/index.ts` falha com `ERR_MODULE_NOT_FOUND` (`./app.js` não existe; o node não mapeia `.js` → `.ts` nem resolve import sem extensão).
- Dos 228 imports relativos, 222 são sem extensão (muitos de diretório, ex: `./clients`), 2 usam `.js` e 4 são JSON (já com `with { type: 'json' }`).
- 1 import pelo alias `src/model` (`src/infra/database/index.ts`).
- Sintaxe já é apagável: `tsc --erasableSyntaxOnly` passa (sem enum, namespace, parameter properties, decorators). A migração é mecânica: imports para `.ts`, alias para relativo, tsconfig `nodenext` + `rewriteRelativeImportExtensions`, tirar tsx/esbuild/vite-tsconfig-paths, Dockerfile copiando `src/`.

## Migração feita (MR !8, work-item #9, 2026-11-18)

Branch `feat/node-26-typescript-7`, em cima do TypeScript 7 que entrou pelo !7 (#7 e #8). Commits: imports `.ts` + tsconfig `nodenext`; `noUncheckedIndexedAccess`; Node 26 sem build (Dockerfile, `package.json`); docs.

- **Reescrita dos imports**: script que resolve cada especificador relativo (e o alias `src/`) para o arquivo `.ts` ou `<dir>/index.ts`, inclusive dentro de `vi.mock(...)` e `import(...)`; 86 arquivos, 245 especificadores. O `vi.mock` precisa do mesmo caminho do import (ex: `./domain/index.ts`).
- **ioredis no `nodenext`**: `import Redis from 'ioredis'` deixa de ser construível no typecheck (`TS2351`/`TS2709`); usar o export nomeado `import { Redis } from 'ioredis'`, e nos mocks devolver `{ Redis: MockRedis }` em vez de `{ default: MockRedis }`.
- **`noUncheckedIndexedAccess`**: o `const [row] = await db.insert(...).returning()` passa a ser `T | undefined`; adotado o padrão do survey-service (`if (!row) throw ...`, com teste). `Record<string, string>` indexado por um nome já validado vira `as const satisfies Record<string, string>` + type guard.
- **Teste de env falha na worktree do BahCode**: o `PORT` da worktree (ex: 3152) vaza para o `index.spec.ts` do env, que espera 3000; rodar com `env -u PORT pnpm test:coverage`.
- **`esbuild` continua no lockfile** (vem do `drizzle-kit` e do `vite`), então o `allowBuilds.esbuild` do `pnpm-workspace.yaml` fica.
- **Validar a imagem localmente**: o `.npmrc` do repo não tem token (vem do `~/.npmrc`), então o `docker build` direto dá `ERR_PNPM_FETCH_401`. Copiar o contexto (Dockerfile, `.dockerignore`, `package.json`, lock, `pnpm-workspace.yaml`, `telemetry.cjs`, `src`, `.npmrc`) para o scratchpad, acrescentar `//us-central1-npm.pkg.dev/contabilizei-tools-production/npm/:_authToken=$(gcloud auth print-access-token)` só na cópia, buildar e apagar a cópia. Para subir, Postgres e Redis numa rede docker própria (sem porta no host) e `--entrypoint node` (o `secrets-init` do ENTRYPOINT só existe no cluster). Saúde do zezu: `/livez` e `/healthz` (não `/health`).
