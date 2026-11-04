---
name: 2026-10-15-padrao-pubsub
description: "Padrão de nomenclatura de Pub/Sub do time"
metadata:
  type: project
tags:
  - performance
titulo: "Padrão de nomenclatura de Pub/Sub do time"
data: 2026-10-15
periodo: 2026QD3
categorias:
  - processo
  - lideranca
impacto: medio
fontes:
  - "[[pubsub-nomenclatura]]"
---

# Padrão de nomenclatura de Pub/Sub do time

- **Período:** 2026QD3 · **Categorias:** processo, lideranca · **Impacto:** medio

## Contexto

Nomes de tópicos e subscriptions eram inconsistentes, e consumers locais disputavam mensagens com o pod de dev.

## O que fiz

Defini o padrão: tópico `<serviço>.p2p.<nome>`, subscription `<consumidor>.sub.<nome>` e sufixo `-local` para execução local (só no terraform de dev).

## Resultado

Convenção usada pelo catálogo GCP para deduzir consumidores e aplicada no `agrupamento-guias-service`.

## Evidências

- [[pubsub-nomenclatura]]
