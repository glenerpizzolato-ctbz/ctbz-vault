---
name: 2026-11-03-incidente-ip-4361-ultimate
description: "Incidente IP-4361 nos bots de WhatsApp: diagnóstico e post-mortem"
metadata:
  type: project
tags:
  - performance
titulo: "Incidente IP-4361 nos bots de WhatsApp: diagnóstico e post-mortem"
data: 2026-11-03
periodo: 2026QD3
categorias:
  - incidente
  - outros-times
impacto: alto
fontes:
  - "[[processo-incidentes-ip]]"
  - "[[eventos-de-erro-ultimate]]"
  - "[[monitor-mensagens-sistema-indisponivel]]"
  - "[[abertura-automatica-ip-grafana]]"
---

# Incidente IP-4361 nos bots de WhatsApp: diagnóstico e post-mortem

- **Período:** 2026QD3 · **Categorias:** incidente, outros-times · **Impacto:** alto

## Contexto

Em 2026-11-03 os bots da Ultimate entraram em erro em massa: coincidiram um incidente da Zendesk nos AI Agents e o enum novo `PRECOS_2027` em 8 planos, que quebrava serviços do nosso lado.

## O que fiz

Separei as duas causas pelos eventos do `ultimateai-webhook` (`Technical Error` ~2.100 em 30 min da Zendesk; `Action Failed` de ~1/h para ~110/h nosso), mapeei as versões do texto de erro, registrei o relato, escrevi o post-mortem no Outline e resolvi o IP. Mostrei que o monitor de mensagens de erro pegava só 1 de 5 variantes e que o alerta do Grafana (08:18) não abriu o IP automaticamente por falha na integração do JSM Ops (aberto à mão às 08:59).

## Resultado

Incidente documentado e fechado, textos de contingência revertidos (PRD-175013) e dois gaps de monitoramento identificados com causa.

## Evidências

- [[processo-incidentes-ip]]
- [[eventos-de-erro-ultimate]]
- [[monitor-mensagens-sistema-indisponivel]]
- [[abertura-automatica-ip-grafana]]
- Jira: [PRD-175013](https://contabilizeicontabilidade.atlassian.net/browse/PRD-175013)
