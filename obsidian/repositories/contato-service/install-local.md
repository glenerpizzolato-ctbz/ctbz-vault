---
name: contato-service-install-local
description: "contato-service: pnpm install local exige token do registry @contabilizei-private e o origin/HEAD local apontava para um main que não existe (a base é master)"
metadata:
  type: reference
---

# Install local e base do contato-service

- A branch padrão é `master`. O clone local tinha `origin/HEAD → origin/main` (antigo, a `main` não existe mais no remoto), e o BahCode criou as worktrees da feature em cima desse `main` velho, sem `package.json`. Correção: `git -C ~/repositories/contato-service remote set-head origin -a` (volta para `master`) e acertar `base` no inventário da feature. Visto em 2026-11-19, no upgrade do Vitest 5 (MR !64).
- O `pnpm install`/`pnpm add` dá 401 em `@contabilizei-private/*` (`us-central1-npm.pkg.dev/contabilizei-tools-production/npm/`), porque o `.npmrc` do repo não tem token. Sem mexer no repo: gerar um npmrc temporário (permissão 600) com `//us-central1-npm.pkg.dev/contabilizei-tools-production/npm/:_authToken=$(gcloud auth print-access-token)`, rodar com `npm_config_userconfig=<arquivo>` e apagá-lo em seguida. Mesmo truque de [[atendimento-canais-admin/build-e-deploy|build-e-deploy do atendimento-canais-admin]].
- Testes: `pnpm test:coverage` (46 arquivos, 624 testes, thresholds de 90%).
