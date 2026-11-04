---
name: 2026-09-17-clientes-inativos-whatsapp
description: "Atendimento de clientes inativos no WhatsApp do Zendesk"
metadata:
  type: project
tags:
  - performance
titulo: "Atendimento de clientes inativos no WhatsApp do Zendesk"
data: 2026-09-17
periodo: 2026QD3
categorias:
  - entrega
impacto: alto
fontes:
  - "[[PRD-153622]]"
  - "[[PRD-153625]]"
  - "[[PRD-153623]]"
  - "[[PRD-153624]]"
  - "[[PRD-166516]]"
  - "[[PRD-167692]]"
  - "[[PRD-153607]]"
  - "[[clientes-inativos-cnpjs-teste]]"
---

# Atendimento de clientes inativos no WhatsApp do Zendesk

- **Período:** 2026QD3 · **Categorias:** entrega · **Impacto:** alto

## Contexto

Clientes inadimplentes, cancelados e com CNPJ baixado não eram recebidos no canal de WhatsApp do Zendesk.

## O que fiz

Criei o endpoint de inativos e o motivo na autenticação por telefone e CNPJ, montei as intents na Ultimate, fiz rollout em ondas por feature-flag, criei horário de atendimento próprio (`schedule_flow` no `bots-api` e `experts-admin`) e removi a flag no fim. Levantei no BigQuery a massa de CNPJs de teste por cenário.

## Resultado

Os clientes inativos passaram a ser atendidos no WhatsApp, respeitando o horário.

## Evidências

- [[PRD-153622]]
- [[PRD-153625]]
- [[PRD-153623]]
- [[PRD-153624]]
- [[PRD-166516]]
- [[PRD-167692]]
- [[PRD-153607]]
- [[clientes-inativos-cnpjs-teste]]
