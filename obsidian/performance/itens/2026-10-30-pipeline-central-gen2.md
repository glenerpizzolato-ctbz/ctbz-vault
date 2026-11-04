---
name: 2026-10-30-pipeline-central-gen2
description: "Correções na pipeline central de devops (DEPLOY_FROM_MR, Go, gen2)"
metadata:
  type: project
tags:
  - performance
titulo: "Correções na pipeline central de devops (DEPLOY_FROM_MR, Go, gen2)"
data: 2026-10-30
periodo: 2026QD3
categorias:
  - outros-times
  - qualidade
  - seguranca
impacto: medio
fontes:
  - "[[deploy-from-mr-e-version]]"
  - "[[html-to-pdf/build-e-imagem]]"
  - "[[cloud-run-gen2-container-threat-detection]]"
  - "[[historico-mrs-html-to-pdf]]"
---

# Correções na pipeline central de devops (DEPLOY_FROM_MR, Go, gen2)

- **Período:** 2026QD3 · **Categorias:** outros-times, qualidade, seguranca · **Impacto:** medio

## Contexto

A correção da CVE no html-to-pdf esbarrou em falhas da pipeline central: build de MR quebrando em repos Go sem `VERSION`, lint e testes em Go 1.20 e deploy recusado porque o Container Threat Detection exige Cloud Run gen2.

## O que fiz

Corrigi no repositório `ctbz/devops/recursos/pipeline` (pipeline!3271, !3276, !3282) e, no html-to-pdf, removi a `libssl1.1` sem uso e apliquei o upgrade da `libbrotli1`.

## Resultado

Pipeline do html-to-pdf!1 passou inteira (Sonar, SAST, secret detection), a 0.0.4 subiu em gen2 e as receitas ficaram documentadas para qualquer serviço gen1.

## Evidências

- [[deploy-from-mr-e-version]]
- [[html-to-pdf/build-e-imagem]]
- [[cloud-run-gen2-container-threat-detection]]
- [[historico-mrs-html-to-pdf]]
- Jira: [PRD-174638](https://contabilizeicontabilidade.atlassian.net/browse/PRD-174638)
