---
name: prc-cadastro-telefone-internacional
description: PRC — cliente que mora fora do Brasil pede o cadastro de um telefone internacional (DDI diferente de +55); como resolver, ACR (Rotina PRD-172999) e campos para fechar
metadata:
  type: reference
tags:
  - prc
canal:
  - wpp
dominio:
  - atendimento
  - plataforma
sistemas:
  - atendimento-canais-admin
  - atendimento-zendesk
acr:
  - PRD-172999
ocorrencias:
  - PRC-153094
  - PRC-153204
  - PRC-154248
  - PRC-155742
qtd_ocorrencias: 4
ultima_ocorrencia: 2026-11-23
---

# Cadastro de telefone internacional

## Sintoma

- Cliente reside no exterior e pede para cadastrar um número internacional (ex: +39 Itália, +34 Espanha). A stack modela telefone como brasileiro (ver ACR arquivada PRD-162752, "Domínio telefone modelado como Brasil em toda a stack"), então o cadastro não é feito pela plataforma.

## Como resolver

- Cadastrar o telefone pelo CRUD de telefone internacional do front admin (`atendimento-canais-admin`, entregue no PRD-168230; listagem no `atendimento-zendesk`, PRD-168231) e comentar no PRC "Telefone adicionado" com o print.
- **Alternativa sem tela (pela API, usada no PRC-155742 em 2026-11-24):** a tela só repassa para o controller `bots/whatsapp/fluxos/experts/flags/tel-internacional` do `atendimento-zendesk`, então dá para cadastrar direto:
  - `POST https://api.contabilizei.com.br/zendesk/api/v1/bots/whatsapp/fluxos/experts/flags/tel-internacional`, body `{"cnpj": "<só dígitos>", "telefone": "+<DDI><número>"}` → `201`. Conferir com `GET .../tel-internacional/empresa/<cnpj>` (`quantidade`, `listaTelefones`). Remover: `DELETE .../empresa/<cnpj>` com body `{"telefone"}`.
  - Autenticação: header `x-ctbz-api-gateway-token` com a `ATENDIMENTO_ZENDESK_API_KEY` de prd do `.env` do `atendimento-canais-admin` (a mesma que a tela usa). O `kong_token` do env `prod` da collection `docs/bruno` do `atendimento-zendesk` (pasta `web_v1/bots_wpp/exp/flags/tel-internacional`) está desatualizado e dá **401**.
  - O serviço normaliza com `libphonenumber-js` e recusa número brasileiro ou inválido (400). Ele tira o `0` do prefixo nacional sozinho (ex: `+610466372466` vira `+61466372466`), mas o `create` **não** limpa o CNPJ: mandar só dígitos.
  - Evidência no PRC: a resposta do `GET` por CNPJ no lugar do print. No banco (`flags_telefone_internacional`), o `bahcode db-query` só aceita contar por CNPJ (`telefone` é dado pessoal e não entra nem no `WHERE`).

## ACR para vincular

[PRD-172999](https://contabilizeicontabilidade.atlassian.net/browse/PRD-172999) — Cadastro telefone internacional (tipo Rotina, fica aberta acumulando os PRCs; não encerrar).

## Como vincular e fechar o PRC

- Link `Problem/Incident` no `createJiraIssueLink`: `inwardIssue` = PRD-172999, `outwardIssue` = PRC (o PRC **is caused by** a ACR).
- Transição `Solved` (→ Concluído) com os campos usados nos PRCs anteriores (PRC-153094/153204):
  - Classificação do chamado (N3) (`customfield_18430`): Expert - Projetos (`31450`)
  - Devido ou Indevido? (`customfield_19805`): Devido (`22182`)
  - Funcionalidade (`customfield_18681`): Atendimento - WhatsApp (`28568`)
  - Grau do Impacto (`customfield_19493`): Altíssimo - Impactou Cliente (`20698`)
  - Ofensor do Chamado (`customfield_21097`, labels): `telefone_internacional`
  - Resolução do chamado (`customfield_18429`): Resolvido diretamente pela plataforma (`17922`)
  - Tipo de chamado (`customfield_18460`): Suporte a operação (`18048`)
