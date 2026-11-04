---
name: 2026-08-21-explicacao-proativa-das
description: "Explicação proativa da variação de impostos (DAS)"
metadata:
  type: project
tags:
  - performance
titulo: "Explicação proativa da variação de impostos (DAS)"
data: 2026-08-21
periodo: 2026QD2
categorias:
  - entrega
  - outros-times
impacto: alto
fontes:
  - "[[PRD-146143]]"
  - "[[PRD-147596]]"
  - "[[PRD-147488]]"
  - "[[PRD-147619]]"
  - "[[PRD-148390]]"
  - "[[PRD-148930]]"
  - "[[PRD-149113]]"
  - "[[PRD-153118]]"
  - "[[PRD-163933]]"
  - "[[PRD-170696]]"
  - "[[PRD-142386]]"
---

# Explicação proativa da variação de impostos (DAS)

- **Período:** 2026QD2 · **Categorias:** entrega, outros-times · **Impacto:** alto

## Contexto

Os clientes não recebiam explicação quando o DAS aumentava.

## O que fiz

No `ms-agrupamento-guias`, implementei a notificação de diagnóstico por e-mail (novo `email-service`) e WhatsApp, com template por diagnóstico, callbacks, feature-flag, trava contra duplicidade, rota de cron para B&P e melhoria de performance; subi a base de 1.498 CNPJs Experts para o diagnóstico de AUMENTO_FATURAMENTO e depois removi a flag.

## Resultado

A explicação proativa ficou ativa para Experts e B&P.

## Evidências

- [[PRD-146143]]
- [[PRD-147596]]
- [[PRD-147488]]
- [[PRD-147619]]
- [[PRD-148390]]
- [[PRD-148930]]
- [[PRD-149113]]
- [[PRD-153118]]
- [[PRD-163933]]
- [[PRD-170696]]
- [[PRD-142386]]
