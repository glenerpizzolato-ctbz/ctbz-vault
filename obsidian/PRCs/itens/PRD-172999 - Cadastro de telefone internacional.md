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
qtd_ocorrencias: 3
ultima_ocorrencia: 2026-11-04
---

# Cadastro de telefone internacional

## Sintoma

- Cliente reside no exterior e pede para cadastrar um número internacional (ex: +39 Itália, +34 Espanha). A stack modela telefone como brasileiro (ver ACR arquivada PRD-162752, "Domínio telefone modelado como Brasil em toda a stack"), então o cadastro não é feito pela plataforma.

## Como resolver

- Cadastrar o telefone pelo CRUD de telefone internacional do front admin (`atendimento-canais-admin`, entregue no PRD-168230; listagem no `atendimento-zendesk`, PRD-168231) e comentar no PRC "Telefone adicionado" com o print.

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
