---
name: 2026-11-03-skill-mapear-erros-ultimate
description: "Levantamento de clientes afetados por incidente (skill mapear-erros-ultimate)"
metadata:
  type: project
tags:
  - performance
titulo: "Levantamento de clientes afetados por incidente (skill mapear-erros-ultimate)"
data: 2026-11-03
periodo: 2026QD3
categorias:
  - ia
  - incidente
impacto: alto
fontes:
  - "[[sunshine-identificar-cliente]]"
  - "[[eventos-de-erro-ultimate]]"
---

# Levantamento de clientes afetados por incidente (skill mapear-erros-ultimate)

- **Período:** 2026QD3 · **Categorias:** ia, incidente · **Impacto:** alto

## Contexto

O log do webhook da Ultimate não traz o telefone do cliente, e era preciso saber quem foi afetado no IP-4361 e que mensagem recebeu.

## O que fiz

Criei uma skill que cruza os eventos do `ultimateai-webhook` e os logs do `atz-worker-webhooks` com o Sunshine Conversations, detecta as versões da mensagem de erro e gera um CSV por bot com o cenário de cada conversa e como identificar o cliente.

## Resultado

6.904 conversas com erro mapeadas entre 09:00Z e 15:00Z, incluindo 866 do chat web e 87 de WhatsApp que o webhook não registrou; reutilizável em próximas instabilidades.

## Evidências

- [[sunshine-identificar-cliente]]
- [[eventos-de-erro-ultimate]]
- Jira: [IP-4361](https://contabilizeicontabilidade.atlassian.net/browse/IP-4361)
