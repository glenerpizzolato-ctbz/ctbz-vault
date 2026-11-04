---
name: 2025-04-01-ativo-guias-imposto-experts
description: "WhatsApp ativo e e-mail de guias de imposto para Experts"
metadata:
  type: project
tags:
  - performance
titulo: "WhatsApp ativo e e-mail de guias de imposto para Experts"
data: 2025-04-01
periodo: 2025QD1
categorias:
  - entrega
impacto: alto
fontes:
  - "[[PRD-101122]]"
  - "[[PRD-102707]]"
  - "[[PRD-101545]]"
  - "[[PRD-105806]]"
  - "[[PRD-105925]]"
  - "[[PRD-107706]]"
  - "[[PRD-108032]]"
  - "[[PRD-101120]]"
  - "[[PRD-94375]]"
---

# WhatsApp ativo e e-mail de guias de imposto para Experts

- **Período:** 2025QD1 · **Categorias:** entrega · **Impacto:** alto

## Contexto

Os clientes Experts não recebiam as guias de imposto de forma proativa.

## O que fiz

Implementei o envio das guias por WhatsApp ativo e e-mail, o ativo do empacotamento de guias e melhorias no task-scheduler; corrigi o `guia-imposto-notifier-consumer`, que consumia evento repetido, e as regras de envio do ativo.

## Resultado

As guias passaram a chegar aos clientes Experts por WhatsApp e e-mail, sem envios duplicados.

## Evidências

- [[PRD-101122]]
- [[PRD-102707]]
- [[PRD-101545]]
- [[PRD-105806]]
- [[PRD-105925]]
- [[PRD-107706]]
- [[PRD-108032]]
- [[PRD-101120]]
- [[PRD-94375]]
