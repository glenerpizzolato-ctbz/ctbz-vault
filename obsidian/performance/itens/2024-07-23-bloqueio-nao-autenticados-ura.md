---
name: 2024-07-23-bloqueio-nao-autenticados-ura
description: "Bloqueio de atendimento a clientes não autenticados na URA do WhatsApp"
metadata:
  type: project
tags:
  - performance
titulo: "Bloqueio de atendimento a clientes não autenticados na URA do WhatsApp"
data: 2024-07-23
periodo: 2024QD2
categorias:
  - seguranca
impacto: alto
fontes:
  - "[[PRD-89849]]"
  - "[[PRD-89846]]"
---

# Bloqueio de atendimento a clientes não autenticados na URA do WhatsApp

- **Período:** 2024QD2 · **Categorias:** seguranca · **Impacto:** alto

## Contexto

No épico de alterações de segurança da URA do WhatsApp (na época na Twilio), clientes que não se autenticavam conseguiam seguir no atendimento.

## O que fiz

Implementei a trava na URA para não atender quem não está autenticado.

## Resultado

O atendimento pelo WhatsApp passou a exigir autenticação, fechando o acesso de terceiros a dados de empresas.

## Evidências

- [[PRD-89849]]
- [[PRD-89846]]
