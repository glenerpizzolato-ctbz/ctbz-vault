---
name: atendimento-canais-admin-optout-tela-contato
description: "Como a tela de contato do atendimento-canais-admin grava e consulta opt-out no contato-service: POST /optouts individual, POST /optouts/batch (lote de até 100) e POST /optouts/search (até 1000 endereços por canal)"
metadata:
  type: reference
tags:
  - atendimento-canais-admin
  - contato-service
  - optout
---

# Opt-out na tela de contato (atendimento-canais-admin)

O front fala com o contato-service pelo proxy wildcard `/api/proxy/contato-service/*` (injeta o token e aponta para `CONTATO_SERVICE_BASE_URL`; repassa qualquer método e rota, então rotas novas não pedem ajuste nele). Desde nov/2026 (branch `feat/optout-batch-routes`) usa as rotas de lote:

- **Registro individual** (um switch): `POST /api/v1/optouts`.
- **Registro em lote** ("Recusar todas", "aplicar a todos"): `POST /api/v1/optouts/batch`, em pedaços de até 100 itens enviados em sequência (a regra de canal único de `TAX` de um item precisa enxergar o que os anteriores gravaram). Resposta 200 com `results[{ index, status: fulfilled|rejected, error: { statusCode, message } }]`; um 400 (ou falha de rede/proxy) recusa o pedaço inteiro. O backend também limita a 500 combinações (finalidades × empresas) por lote.
- **Consulta de vários endereços** (`hooks/useAddressesOptouts.ts`, regra de canal único e painel por empresa): `POST /api/v1/optouts/search`, uma chamada por canal em pedaços de até 1000. A resposta volta na forma canônica (`+…`, e-mail minúsculo) e deduplicada, então o front casa cada ponto por `canonicalOptoutAddress` (não `toOptoutAddress`, que põe 55 em número sem DDI). A chave do cache é `["contato-service","optouts-search",canal,empresa,endereços]`, e o registro invalida também essas consultas via `invalidateAddressOptouts` (predicate `isOptoutsSearchOf`), além do prefixo `optoutsAddressKey`.
- **Consulta de um endereço** (`useOptouts`): continua no `GET /api/v1/optouts`.

- Cada registro é a chave (canal + endereço + finalidade + empresa), com `companyCode` opcional. Sem `companyCode` = manifestação geral do endereço, vale para todas as empresas do titular.
- `src/routes/contatos/-OptoutPanel.tsx` (painel por endereço, na página do contato): tabela com uma linha por empresa do contato e uma coluna por finalidade. Switch = 1 POST com `companyCode` da linha. "Recusar todas" (coluna "Canal inteiro") = um POST por finalidade ainda aceita, **só daquela empresa**. Se o endereço não tem contato/empresa, a única linha é "Este endereço" e os POSTs vão sem `companyCode` (geral).
- `src/routes/contatos/-CompanyOptoutPanel.tsx` (painel por empresa): mesma finalidade aplicada a vários endereços dos contatos da empresa, um POST por endereço.
- O lote (`hooks/useRegistrarOptoutEmLote.ts`) não é transacional: cada item é gravado na sua transação no backend, uma falha (ex: regra de canal único de Impostos) não desfaz as outras e o toast diz quantos endereços falharam.
- No backend, `purpose` e `companyCode` aceitam valor único ou lista (produto cartesiano, tudo ou nada) e `companyCode` é obrigatório; a linha "Este endereço" sem `companyCode` é tratada na PRD-175745.
- Não há, na UI, ação que marque todas as empresas de uma vez com recorte por empresa: para isso seria N empresas × M finalidades POSTs, ou um `POST` com `companyCode` em lista.
