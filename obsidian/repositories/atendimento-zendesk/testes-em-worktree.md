---
name: testes-em-worktree
description: "Como rodar jest/eslint/prettier do atendimento-zendesk numa worktree (atendimento-zendesk.wt/*) sem node_modules"
metadata:
  type: reference
tags:
  - atendimento-zendesk
  - testes
---

# Testes em worktree do atendimento-zendesk

As worktrees em `~/repositories/atendimento-zendesk.wt/<nome>/` não têm `node_modules`. Com isso, o `npx jest` baixa um jest avulso e falha com "Module ts-jest in the transform option was not found". Ele ainda deixa uma pasta `node_modules/.cache` na worktree.

Para rodar os testes:

1. Apagar o `node_modules` que o npx tenha deixado (se existir) e criar um symlink **absoluto**: `ln -s ~/repositories/atendimento-zendesk/node_modules node_modules`. Se a pasta já existir, o `ln -s` cria o link dentro dela, sem dar erro.
2. Rodar `node_modules/.bin/jest --maxWorkers=10% <caminho>`. Para o lint, `node_modules/.bin/eslint <arquivos>`. Para a formatação, `node_modules/.bin/prettier --check <arquivos>`.
3. Remover o symlink ao terminar (`rm node_modules`) para não sujar o `git status`.

Falhas que já existem no master (em 2026-10-30, sem relação com mudanças): `notificacao-empresa-2fa-producer.service.spec.ts`, `marcar-ativos-workflow-recebidas.service.spec.ts` e `marcar-mensagem-ativa-recebido.service.spec.ts`.
