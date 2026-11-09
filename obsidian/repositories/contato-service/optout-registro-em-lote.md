---
name: optout-registro-em-lote
description: "contato-service: rota POST /api/v1/optouts/batch (array de opt-outs, em sequência, segue nos erros com resultado por item, MR !58; por que não Promise.allSettled) e purpose/companyCode em array no POST /api/v1/optouts (produto cartesiano, tudo ou nada) — PRD-175747"
metadata:
  type: project
tags:
  - contato-service
  - opt-out
---

# Opt-out: registro em lote (PRD-175747)

- **Escopo decidido pelo Glener (2026-11-06):** só uma rota nova, `POST /api/v1/optouts/batch`, que recebe um array `[{...}, {...}]`, com cada item no formato do `POST /api/v1/optouts`, e cria N registros. A rota atual **não** passou a aceitar `purpose`/`companyCode` em array: essa versão (produto cartesiano, tudo ou nada numa transação, MRs !56 e !57) foi descartada e os MRs foram fechados (a parte dos arrays voltou depois, ver abaixo). O código dela ficou na branch `feat/PRD-175747` (remota) e no backup local da worktree `feature-8`.
- Implementação (MR !58, branch `feat/PRD-175747-optouts-batch`, alvo `master`): `RegisterOptoutsBatchUsecase` chama o `RegisterOptoutUsecase` para cada item, em sequência; aceita de 1 a 100 itens e responde um resultado por item, na ordem do array (ver abaixo).
- **Segue nos erros (desde o commit `e384ff5`, 2026-11-09):** cada item tem a sua transação e a falha de um não interrompe os demais. A resposta é `200 { results: [{ index, status: "fulfilled", optout } | { index, status: "rejected", error: { statusCode, message } }] }`, com 404/409 do item ou 500 genérico (logado). Só o body inválido dá 400, e aí nada é gravado.
- **Por que `for` sequencial e não `Promise.allSettled`:** o `allSettled` só coleta promises que já rodam em paralelo. Em paralelo: (1) a regra de canal único de `TAX` é ler e depois gravar, e em READ COMMITTED duas transações do mesmo titular não veem uma a outra, então WhatsApp e e-mail passariam juntos; (2) itens repetidos teriam o último a gravar imprevisível; (3) até 100 transações disputariam o pool de 10 conexões (`src/infra/database/index.ts`). O resultado no formato do `allSettled` é montado à mão, com `try/catch` por item.
- Consumidor potencial: `atendimento-canais-admin` (`useRegistrarOptoutEmLote.ts`, que hoje faz N POSTs com `Promise.allSettled`).
- A sub-task PRD-175747 do Jira já estava **Concluído**, com o título da entrega da PRD-175745 (empresa obrigatória), então não foi movida para este trabalho.

## purpose e companyCode em array (retomado em 2026-11-06)

- Branch `feat/PRD-175747-optouts-arrays`, empilhada sobre a do MR !58 (branch chaining). Traz também o `CompanyDAO.findByCodes` (uma consulta para várias empresas).
- `POST /api/v1/optouts`: `purpose` e `companyCode` aceitam string ou array (não vazio, sem repetidos, até 50 empresas). Grava uma linha por combinação finalidade × empresa (`expandOptoutInput`, finalidade por fora, empresa por dentro).
- **Resposta:** com os dois escalares continua `{ optout }` (compatível com os consumidores atuais); com array em qualquer um dos dois, `{ optouts }`, mesmo com um item só.
- `RegisterOptoutUsecase.execute(input)` passou a devolver `OptoutItem[]`: as combinações de um registro vão numa transação só (tudo ou nada), com 404 listando todos os códigos inexistentes antes de abrir a transação, titular resolvido uma vez e cache invalidado uma vez (todas as combinações são do mesmo endereço).
- Rota em lote: cada item aceita os arrays, a resposta junta as combinações na ordem, e o lote tem teto de 500 combinações (`OPTOUT_REGISTER_BATCH_MAX_COMBINATIONS`). Continua não atômica entre itens; dentro de um item é tudo ou nada. O conflito de `TAX` entre itens é pego porque o lote é sequencial e cada item enxerga o que os anteriores gravaram (testado em `register-optouts-batch.usecase.spec.ts` com o usecase real e uma transação fake com rollback).
- **2026-11-09:** o !58 foi mergeado com outro contrato: o lote responde `{ results }` por item, estilo `Promise.allSettled` (`{ index, status: "fulfilled", optout }` ou `{ index, status: "rejected", error: { statusCode, message } }`), sem parar no primeiro erro. O !59 (`findByCodes`) também foi mergeado e o !60 foi rebaseado no master: no lote, o item com `purpose`/`companyCode` em array devolve `{ index, status: "fulfilled", optouts: [...] }` (mesma regra da rota individual), e um 404/409 dentro do item vira um `rejected` sem gravar nenhuma combinação dele.
