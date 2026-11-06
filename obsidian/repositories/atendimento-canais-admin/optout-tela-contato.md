---
name: atendimento-canais-admin-optout-tela-contato
description: "Como a tela de contato do atendimento-canais-admin grava opt-out: um POST /api/v1/optouts do contato-service por (endereço × finalidade × empresa), sem rota de lote"
metadata:
  type: reference
tags:
  - atendimento-canais-admin
  - contato-service
  - optout
---

# Opt-out na tela de contato (atendimento-canais-admin)

Não existe rota de lote no contato-service: o front dispara um `POST /api/v1/optouts` por registro, via proxy `/api/proxy/contato-service/api/v1/optouts` (o proxy injeta o token e aponta para `CONTATO_SERVICE_BASE_URL`).

- Cada registro é a chave (canal + endereço + finalidade + empresa), com `companyCode` opcional. Sem `companyCode` = manifestação geral do endereço, vale para todas as empresas do titular.
- `src/routes/contatos/-OptoutPanel.tsx` (painel por endereço, na página do contato): tabela com uma linha por empresa do contato e uma coluna por finalidade. Switch = 1 POST com `companyCode` da linha. "Recusar todas" (coluna "Canal inteiro") = um POST por finalidade ainda aceita, **só daquela empresa**. Se o endereço não tem contato/empresa, a única linha é "Este endereço" e os POSTs vão sem `companyCode` (geral).
- `src/routes/contatos/-CompanyOptoutPanel.tsx` (painel por empresa): mesma finalidade aplicada a vários endereços dos contatos da empresa, um POST por endereço.
- O lote (`hooks/useRegistrarOptoutEmLote.ts`) é `Promise.allSettled` de `postOptout`: chamadas independentes, não é transacional; uma falha (ex: regra de canal único de Impostos) não desfaz as outras e o toast diz quantos endereços falharam.
- Não há, na UI, ação que marque todas as empresas de uma vez com recorte por empresa: para isso seria N empresas × M finalidades POSTs, ou um POST geral sem `companyCode`.
