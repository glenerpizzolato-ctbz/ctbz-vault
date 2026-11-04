---
name: 2026-07-22-migracao-agrupamento-guias-gcp
description: "Migração do ms-agrupamento-guias para o GCP de atendimento-canais"
metadata:
  type: project
tags:
  - performance
titulo: "Migração do ms-agrupamento-guias para o GCP de atendimento-canais"
data: 2026-07-22
periodo: 2026QD2
categorias:
  - entrega
  - qualidade
impacto: alto
fontes:
  - "[[PRD-154460]]"
  - "[[PRD-154929]]"
  - "[[PRD-153904]]"
  - "[[PRD-154082]]"
  - "[[PRD-155157]]"
  - "[[PRD-160018]]"
  - "[[PRD-155633]]"
  - "[[PRD-154281]]"
  - "[[PRD-151895]]"
---

# Migração do ms-agrupamento-guias para o GCP de atendimento-canais

- **Período:** 2026QD2 · **Categorias:** entrega, qualidade · **Impacto:** alto

## Contexto

O microsserviço de agrupamento de guias estava fora do projeto GCP do time.

## O que fiz

Migrei banco e Redis (dev e prd), Pub/Sub de notificação e agrupamento e crons para o projeto `atendimento-canais`, passei o Pub/Sub para Terraform e ajustei os consumidores (bots-api e a subscription processar-guia da fintech).

## Resultado

O serviço ficou no projeto do time, com a infraestrutura versionada em Terraform.

## Evidências

- [[PRD-154460]]
- [[PRD-154929]]
- [[PRD-153904]]
- [[PRD-154082]]
- [[PRD-155157]]
- [[PRD-160018]]
- [[PRD-155633]]
- [[PRD-154281]]
- [[PRD-151895]]
