---
name: optout-registro-em-lote
description: "contato-service: rota POST /api/v1/optouts/batch (array de opt-outs, em sequência, não atômica, MR !58) e purpose/companyCode em array no POST /api/v1/optouts (produto cartesiano, tudo ou nada) — PRD-175747"
metadata:
  type: project
tags:
  - contato-service
  - opt-out
---

# Opt-out: registro em lote (PRD-175747)

- **Escopo decidido pelo Glener (2026-11-06):** só uma rota nova, `POST /api/v1/optouts/batch`, que recebe um array `[{...}, {...}]`, com cada item no formato do `POST /api/v1/optouts`, e cria N registros. A rota atual **não** passou a aceitar `purpose`/`companyCode` em array: essa versão (produto cartesiano, tudo ou nada numa transação, MRs !56 e !57) foi descartada e os MRs foram fechados (a parte dos arrays voltou depois, ver abaixo). O código dela ficou na branch `feat/PRD-175747` (remota) e no backup local da worktree `feature-8`.
- Implementação (MR !58, branch `feat/PRD-175747-optouts-batch`, alvo `master`): `RegisterOptoutsBatchUsecase` chama o `RegisterOptoutUsecase` para cada item, em sequência; aceita de 1 a 100 itens e responde `{ optouts }` na ordem do array.
- **Não é atômica:** cada item tem a sua transação; se um falhar (404 de empresa, 409 de `TAX`), o lote para e os anteriores ficam gravados. Reenviar o lote é seguro porque o registro é um upsert idempotente. Por ser sequencial, a regra de canal único de `TAX` de um item enxerga o que os itens anteriores gravaram.
- Consumidor potencial: `atendimento-canais-admin` (`useRegistrarOptoutEmLote.ts`, que hoje faz N POSTs com `Promise.allSettled`).
- A sub-task PRD-175747 do Jira já estava **Concluído**, com o título da entrega da PRD-175745 (empresa obrigatória), então não foi movida para este trabalho.

## purpose e companyCode em array (retomado em 2026-11-06)

- Branch `feat/PRD-175747-optouts-arrays`, empilhada sobre a do MR !58 (branch chaining). Traz também o `CompanyDAO.findByCodes` (uma consulta para várias empresas).
- `POST /api/v1/optouts`: `purpose` e `companyCode` aceitam string ou array (não vazio, sem repetidos, até 50 empresas). Grava uma linha por combinação finalidade × empresa (`expandOptoutInput`, finalidade por fora, empresa por dentro).
- **Resposta:** com os dois escalares continua `{ optout }` (compatível com os consumidores atuais); com array em qualquer um dos dois, `{ optouts }`, mesmo com um item só.
- `RegisterOptoutUsecase.execute(input)` passou a devolver `OptoutItem[]`: as combinações de um registro vão numa transação só (tudo ou nada), com 404 listando todos os códigos inexistentes antes de abrir a transação, titular resolvido uma vez e cache invalidado uma vez (todas as combinações são do mesmo endereço).
- Rota em lote: cada item aceita os arrays, a resposta junta as combinações na ordem, e o lote tem teto de 500 combinações (`OPTOUT_REGISTER_BATCH_MAX_COMBINATIONS`). Continua não atômica entre itens; dentro de um item é tudo ou nada. O conflito de `TAX` entre itens é pego porque o lote é sequencial e cada item enxerga o que os anteriores gravaram (testado em `register-optouts-batch.usecase.spec.ts` com o usecase real e uma transação fake com rollback).
