---
name: email-service-testes-em-worktree
description: "No email-service rodando numa worktree do BahCode, o teste de env falha por causa do PORT da worktree; rodar com env -u PORT"
metadata:
  type: reference
tags:
  - email-service
  - testes
---

# Testes do email-service numa worktree

As worktrees do BahCode exportam `PORT` próprio (ex: `3080`). O `src/infra/env/index.spec.ts` ("expõe o ambiente já validado, agrupado por dependência") espera a porta padrão `3000` e falha com `port: 3080`, sem relação com a mudança.

Rodar a suíte sem a variável: `env -u PORT pnpm test:coverage`.

O `pnpm lint:check` também mostra sempre 1 warning e 2 infos do próprio `biome.json` (schema 2.4.4 × CLI 2.5.12 e `recommended` depreciado); não bloqueiam.
