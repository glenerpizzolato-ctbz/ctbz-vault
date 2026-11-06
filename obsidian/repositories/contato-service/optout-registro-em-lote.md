---
name: optout-registro-em-lote
description: "contato-service: rota POST /api/v1/optouts/batch (array de opt-outs, um registro por item, em sequência, não atômica) — PRD-175747, MR !58"
metadata:
  type: project
tags:
  - contato-service
  - opt-out
---

# Opt-out: registro em lote (PRD-175747)

- **Escopo decidido pelo Glener (2026-11-06):** só uma rota nova, `POST /api/v1/optouts/batch`, que recebe um array `[{...}, {...}]`, com cada item no formato do `POST /api/v1/optouts`, e cria N registros. A rota atual **não** passou a aceitar `purpose`/`companyCode` em array: essa versão (produto cartesiano, tudo ou nada numa transação, MRs !56 e !57) foi descartada e os MRs foram fechados. O código dela ficou na branch `feat/PRD-175747` (remota) e no backup local da worktree `feature-8`.
- Implementação (MR !58, branch `feat/PRD-175747-optouts-batch`, alvo `master`): `RegisterOptoutsBatchUsecase` chama o `RegisterOptoutUsecase` para cada item, em sequência; aceita de 1 a 100 itens e responde `{ optouts }` na ordem do array.
- **Não é atômica:** cada item tem a sua transação; se um falhar (404 de empresa, 409 de `TAX`), o lote para e os anteriores ficam gravados. Reenviar o lote é seguro porque o registro é um upsert idempotente. Por ser sequencial, a regra de canal único de `TAX` de um item enxerga o que os itens anteriores gravaram.
- Consumidor potencial: `atendimento-canais-admin` (`useRegistrarOptoutEmLote.ts`, que hoje faz N POSTs com `Promise.allSettled`).
- A sub-task PRD-175747 do Jira já estava **Concluído**, com o título da entrega da PRD-175745 (empresa obrigatória), então não foi movida para este trabalho.
