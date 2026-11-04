---
name: prc-cliente-nao-quer-receber-pesquisa-csat-nps
description: PRC — cliente pede para não receber mais pesquisa; separar CSAT (blocklist do experts-service) de CSAT+NPS (opt-out do contato-service via front admin)
metadata:
  type: reference
tags:
  - prc
canal:
  - wpp
  - email
dominio:
  - csat
  - notificacoes
sistemas:
  - experts-service
  - contato-service
  - atendimento-canais-admin
acr:
  - "[[PRD-168944]]"
ocorrencias:
  - PRC-146015
  - PRC-148207
  - PRC-152662
qtd_ocorrencias: 3
ultima_ocorrencia: 2026-10-14
---

# Cliente não quer receber pesquisa (CSAT e/ou NPS)

## Sintoma

Cliente reclama do volume de pesquisas recebidas e pede para ser retirado da
listagem ("retirar pesquisa de insatisfação").

- Exemplo: [PRC-146015](https://contabilizeicontabilidade.atlassian.net/browse/PRC-146015)
  — RETIRAR PESQUISA DE INSATISFAÇÃO
- Exemplo: [PRC-152662](https://contabilizeicontabilidade.atlassian.net/browse/PRC-152662)
  — Exclusão pesquisa CSAT (cliente questiona a quantidade de CSAT enviada em cada interação; só CSAT)

## Primeiro passo: separar CSAT de NPS

CSAT e NPS são ambos uma "pesquisa" para o cliente, então é preciso entender
**qual** ele não quer receber — a solução é diferente.

### Somente CSAT → `blocklist` do `experts-service`

- Inserir o CNPJ (ou `id_processo_abertura`) na tabela `blocklist` do repositório `experts-service`.
- O motor de CSAT (`RunSurveyCsatEngineConsumer`, em
  `src/consumers/survey-csat/run-survey-csat-engine`) consulta
  `BlocklistService.includes()` em `resolveContext()` e interrompe o envio
  quando o identificador está na tabela.
- Também é consultada nos fluxos de follow-up (`csat-fup.service.ts`) e
  transbordo (`process-ticket-jira-closed.usecase.ts`).

### CSAT **e** NPS → opt-out do `contato-service`

- Usar o opt-out pelo front admin:
  `https://admin.ctbz.com.br/api/atendimento-canais/contatos/empresas`
- É o opt-out do `contato-service`, consumido pelo `atendimento-zendesk`
  (envio de ativo WPP).

> [!warning] Ponto em aberto
> Não sabemos se o opt-out do `contato-service` é utilizado pelo
> `email-service` — ou seja, pode não bloquear pesquisas enviadas por e-mail.

## ACR para vincular

PRCs que caem nesse problema devem ser vinculadas à ACR:
[PRD-168944](https://contabilizeicontabilidade.atlassian.net/browse/PRD-168944)
— [ACR] Adicionar CNPJs à blocklist de CSAT de clientes que não querem receber

## Como vincular e fechar a PRC

- Link: tipo `Problem/Incident`, com a PRC **is caused by** PRD-168944 (no `createJiraIssueLink`: `inwardIssue` = PRD-168944, `outwardIssue` = PRC).
- A transição `Solved` (→ Concluído) exige 7 campos. Valores usados nas PRCs desse problema (copiados da PRC-146015):
  - Classificação do chamado (N3) (`customfield_18430`): Experts - CRM → WhatsApp - Comportamento não esperado (`39474` / `41165`)
  - Devido ou Indevido? (`customfield_19805`): Devido (`22182`)
  - Funcionalidade (`customfield_18681`): Atendimento - WhatsApp (`28568`)
  - Grau do Impacto (`customfield_19493`): Alto - Impactou Operação (`20700`)
  - Ofensor do Chamado (`customfield_21097`, labels): `csat_zendesk`
  - Resolução do chamado (`customfield_18429`): Resolvido diretamente pela plataforma (`17922`)
  - Tipo de chamado (`customfield_18460`): Suporte a operação (`18048`)
