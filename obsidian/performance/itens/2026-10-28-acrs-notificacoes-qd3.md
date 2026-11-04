---
name: 2026-10-28-acrs-notificacoes-qd3
description: "Análise de ACRs de notificações e e-mail (QD3/2026)"
metadata:
  type: project
tags:
  - performance
titulo: "Análise de ACRs de notificações e e-mail (QD3/2026)"
data: 2026-10-28
periodo: 2026QD3
categorias:
  - incidente
  - qualidade
  - outros-times
impacto: medio
fontes:
  - "[[PRD-168171]]"
  - "[[PRD-168429]]"
  - "[[PRD-169004]]"
  - "[[PRD-168129]]"
  - "[[PRD-174011]]"
  - "[[PRD-168707]]"
  - "[[PRD-166692]]"
  - "[[alertas-de-envio]]"
---

# Análise de ACRs de notificações e e-mail (QD3/2026)

- **Período:** 2026QD3 · **Categorias:** incidente, qualidade, outros-times · **Impacto:** medio

## Contexto

Chegaram várias ACRs: falha na recepção de e-mails pelo Zendesk, notificações não enviadas por campo nulo, empacotamento com diagnóstico não suportado, aviso indevido de ISS e falta de idempotência no agrupamento.

## O que fiz

Analisei cada ACR; no PRD-174011 descartei a hipótese do Bolt, investiguei competência por competência no banco e achei por que `GUIAS_AGUARDANDO_GERACAO` nunca é retentado, encaminhando ao squad Fiscal com playbook. Aumentei a observabilidade do `email-service` para envios bloqueados, criei a ingestão sql2bq das notificações de guia avulsa e tirei um alerta duplicado (email-service!72).

## Resultado

ACRs fechadas com causa explicada e monitoração das notificações melhorada.

## Evidências

- [[PRD-168171]]
- [[PRD-168429]]
- [[PRD-169004]]
- [[PRD-168129]]
- [[PRD-174011]]
- [[PRD-168707]]
- [[PRD-166692]]
- [[alertas-de-envio]]
