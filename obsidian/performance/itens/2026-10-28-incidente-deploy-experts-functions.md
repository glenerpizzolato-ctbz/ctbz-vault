---
name: 2026-10-28-incidente-deploy-experts-functions
description: "Incidente no deploy de prd do experts-functions e regressão do html-to-pdf"
metadata:
  type: project
tags:
  - performance
titulo: "Incidente no deploy de prd do experts-functions e regressão do html-to-pdf"
data: 2026-10-28
periodo: 2026QD3
categorias:
  - incidente
  - outros-times
  - seguranca
impacto: alto
fontes:
  - "[[experts-functions/build-e-imagem]]"
  - "[[cve-2026-111497-node2shell]]"
---

# Incidente no deploy de prd do experts-functions e regressão do html-to-pdf

- **Período:** 2026QD3 · **Categorias:** incidente, outros-times, seguranca · **Impacto:** alto

## Contexto

O deploy de prd do experts-functions (monorepo de outro grupo) falhava com 409 por recursos fora do state do Terraform, e a correção da CVE não chegava a prd.

## O que fiz

Fiz o import via override do `CUSTOM_JOB_DEPLOY_SCRIPT` na pipeline central (pipeline!3238). O deploy quebrou o `function-html-to-pdf` (perdeu o Chromium, 500): diagnostiquei, validei a correção numa imagem mínima e abri experts-functions!8.

## Resultado

html-to-pdf de volta às 21:40; as 51 falhas de holerites da janela foram reentregues pelo Pub/Sub e o backlog zerou às 21:45.

## Evidências

- [[experts-functions/build-e-imagem]]
- [[cve-2026-111497-node2shell]]
