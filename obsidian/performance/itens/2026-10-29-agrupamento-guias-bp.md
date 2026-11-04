---
name: 2026-10-29-agrupamento-guias-bp
description: "Agrupamento de guias para o plano BP (e separação Experts SN/LP)"
metadata:
  type: project
tags:
  - performance
titulo: "Agrupamento de guias para o plano BP (e separação Experts SN/LP)"
data: 2026-10-29
periodo: 2026QD3
categorias:
  - entrega
  - outros-times
impacto: alto
fontes:
  - "[[PRD-170830]]"
  - "[[PRD-170836]]"
  - "[[PRD-170837]]"
  - "[[PRD-174490]]"
  - "[[PRD-174792]]"
  - "[[notificacao-agrupamento-experts-bp-lp]]"
  - "[[dashboard-agrupamento-guias-bigquery]]"
---

# Agrupamento de guias para o plano BP (e separação Experts SN/LP)

- **Período:** 2026QD3 · **Categorias:** entrega, outros-times · **Impacto:** alto

## Contexto

O agrupamento de guias só existia para Experts e precisava chegar ao BP com clientes LP.

## O que fiz

No `microsservico-agrupamento-guias`, passei a receber regime e plano, separei rotas e crons Experts e BP (Terraform) e implementei a notificação do BP por e-mail e WhatsApp; separei Experts SN/LP com template próprio (MR !90), um service por público. No dashboard do admin, mostrei as guias de cada agrupamento, tratando duplicatas e ~50 mil órfãos da réplica no BigQuery.

## Resultado

Clientes BP LP passaram a receber o agrupamento por e-mail e WhatsApp, em parceria com a cron de outro time (`contabilizei-importacao-notas-worker`).

## Evidências

- [[PRD-170830]]
- [[PRD-170836]]
- [[PRD-170837]]
- [[PRD-174490]]
- [[PRD-174792]]
- [[notificacao-agrupamento-experts-bp-lp]]
- [[dashboard-agrupamento-guias-bigquery]]
