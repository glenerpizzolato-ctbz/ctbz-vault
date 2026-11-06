---
name: optout-registro-em-lote
description: "contato-service: registro de opt-out com purpose/companyCode em array (produto cartesiano) e a rota POST /api/v1/optouts/batch, tudo ou nada"
metadata:
  type: project
tags:
  - contato-service
  - opt-out
---

# Opt-out: registro em lote (PRD-175747)

Branch `feat/PRD-175747`, encadeada em `feat/PRD-175745` (ver [[optout-empresa-obrigatoria]]).

- `POST /api/v1/optouts`: `purpose` e `companyCode` aceitam string ou array (não vazio, sem repetidos, até 50 empresas). Grava uma linha por combinação finalidade × empresa (finalidade por fora, empresa por dentro).
- **Resposta (decisão):** entrada escalar mantém `{ optout }`; com array em qualquer um dos dois campos, `{ optouts: [...] }` (mesmo com array de 1 item). Motivo: o consumidor atual, o `atendimento-canais-admin` (`useRegistrarOptout.ts` e `useRegistrarOptoutEmLote.ts`, que hoje faz N POSTs com `Promise.allSettled`), lê `{ optout }`.
- `POST /api/v1/optouts/batch`: body `{ optouts: [...] }`, cada item no formato do registro (com arrays), até 100 itens e 500 combinações no total; resposta `{ optouts }`.
- **Tudo ou nada:** uma transação só. Empresas resolvidas numa consulta (`CompanyDAO.findByCodes`), 404 lista os códigos inexistentes; `personId` resolvido uma vez por endereço; cache invalidado uma vez por endereço depois do commit.
- **Canal único de `TAX` dentro do lote:** as linhas são gravadas em sequência na transação e a consulta `findOptedOutByPerson` roda na mesma `tx`, então cada combinação já enxerga o que o lote gravou antes. Não há estado em memória: o lote se comporta como chamadas seguidas (revogar WhatsApp e depois recusar e-mail no mesmo lote é aceito; recusar os dois dá 409 e desfaz tudo).
- Um mesmo recorte repetido no lote é gravado duas vezes (o último vence), como duas chamadas seguidas.
