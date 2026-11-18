---
name: node-26-typescript-nativo
description: "Modelo Node 26 do survey-service (TypeScript rodando direto no node, sem build) - pipeline, Dockerfile, tsconfig - e o que um repo precisa mudar para adotar"
metadata:
  type: reference
tags:
  - padroes
  - nodejs
  - pipeline
---

# Node 26 com TypeScript nativo (modelo survey-service)

Levantado em 2026-11-18 no `survey-service` (master, v0.1.78), o repo Node mais atual do time.

## Como o survey-service está

- **Node 26** (`engines.node: ">=26"`), imagem `node:26-alpine` no Dockerfile (dois estágios: `deps` com `.npmrc` descartado e final) e na pipeline (`CI_CONTAINER_IMAGE: node:26-alpine` em `custom/ctbz/experts/atendimento-canais/survey-service.yml`, usado por build, lint e test).
- **Sem build**: o node roda `src/index.ts` direto (type stripping nativo). `start`: `node --require ./telemetry.cjs src/index.ts`; `dev`: `node --watch --env-file-if-exists=.env ...`. Sem `tsx`, `esbuild`, `dist/` nem `vite-tsconfig-paths`; scripts de tooling também são `.ts` rodados pelo node.
- **tsconfig**: `module`/`moduleResolution: nodenext`, `erasableSyntaxOnly`, `verbatimModuleSyntax`, `allowImportingTsExtensions`, `rewriteRelativeImportExtensions`, `noUncheckedIndexedAccess`, `noEmit`. Imports relativos com extensão `.ts` explícita, sem alias de paths.
- **Ferramentas**: pnpm 11.2.2, TypeScript 7 (`^7.0.2`), vitest 5, biome 2, `@types/node` 26.
- Pipeline: o job de migration ainda usa `contabilizeidevops/node:22` (imagem própria com gcloud), destoando do resto.

## O que um repo precisa para adotar

1. **Só subir para o Node 26** (mantendo esbuild): trocar a imagem na pipeline e no Dockerfile, `--target=node26` no esbuild e `@types/node` 26. Baixo risco.
2. **TypeScript nativo (sem build)**: código só com sintaxe apagável (sem `enum`, `namespace`, parameter properties, decorators - conferir com `tsc --noEmit --erasableSyntaxOnly`), todos os imports relativos com `.ts` explícito (o node não resolve import sem extensão nem de diretório/`index`), sem alias de `paths`, JSON com `with { type: 'json' }`, tsconfig `nodenext` + `rewriteRelativeImportExtensions`, e Dockerfile copiando `src/` em vez de `dist/`.

## Armadilhas da migração

- `import X from 'pacote-cjs'` que funcionava no modo `bundler` pode deixar de ser construível no `nodenext` (ex: ioredis: usar `import { Redis } from 'ioredis'` e mockar `{ Redis: ... }`).
- Ligar `noUncheckedIndexedAccess` junto: `const [row] = await ....returning()` vira `T | undefined` (tratar com `if (!row) throw`), e specs com `mock.calls[0][0]`/`queries[0].text` precisam de `?.`.
- O `vi.mock` usa o mesmo especificador do import, então a reescrita para `.ts` tem que pegar os `vi.mock(...)` e `import(...)` também.
- Sem build, a imagem copia `src`: tirar specs e `test-utils` pelo `.dockerignore` (allowlist com `src/**/*.spec.ts` negado).

Situação do agrupamento-guias-service (migração feita no MR !8): [[node-26-agrupamento-guias-service]].

## Armadilha do TypeScript 7

O TS 7 removeu a opção `baseUrl` (`TS5102: Option 'baseUrl' has been removed`) e não aceita caminho não relativo em `paths` (`TS5090`). Repo que usa alias (ex: `src/*`) só precisa tirar o `baseUrl` e prefixar o destino com `./` (`"src/*": ["./src/*"]`): os caminhos passam a ser relativos ao tsconfig, e isso funciona igual no TS 5, no `vite-tsconfig-paths`, no `tsx` e no esbuild. Visto no agrupamento-guias-service (MR !7, 2026-11-18).
