---
name: 2026-10-15-agrupamento-guias-service-redesenho
description: "Redesenho da notificação do agrupamento de guias (agrupamento-guias-service)"
metadata:
  type: project
tags:
  - performance
titulo: "Redesenho da notificação do agrupamento de guias (agrupamento-guias-service)"
data: 2026-10-15
periodo: 2026QD3
categorias:
  - entrega
  - qualidade
impacto: alto
fontes:
  - "[[arquitetura-e-migracao]]"
  - "[[historico-mrs-agrupamento-guias-service]]"
  - "[[notificacao-individual-guias-x-agrupamento]]"
---

# Redesenho da notificação do agrupamento de guias (agrupamento-guias-service)

- **Período:** 2026QD3 · **Categorias:** entrega, qualidade · **Impacto:** alto

## Contexto

A notificação (e-mail e WhatsApp) do `microsservico-agrupamento-guias` estava sendo portada para um serviço Node novo.

## O que fiz

Redesenhei o serviço em 8 segmentos (público × regime × canal), cada um com rota, tópico e consumer próprios, evento autocontido e banco próprio (substituindo `controle_notificacao`), sem lote nem scheduler; padronizei templates por ambiente. Antes da virada, mapeei os riscos com a notificação individual de guias do experts-service (duplicidade, buraco de silêncio, rota removida).

## Resultado

Desenho mais simples e riscos de migração documentados; primeiro MR aberto em 2026-11-03.

## Evidências

- [[arquitetura-e-migracao]]
- [[historico-mrs-agrupamento-guias-service]]
- [[notificacao-individual-guias-x-agrupamento]]
