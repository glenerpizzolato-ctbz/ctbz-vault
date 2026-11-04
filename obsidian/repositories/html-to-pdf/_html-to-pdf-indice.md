---
name: html-to-pdf-indice
description: "Índice de notas do repositório html-to-pdf: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - html-to-pdf
repositorio: html-to-pdf
caminho: ~/repositories/html-to-pdf
---

# html-to-pdf

Repositório em `~/repositories/html-to-pdf`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[build-e-imagem]] — imagem Docker (golang:1.23 + wkhtmltopdf), teste local e correção da libbrotli1 (CVE-2026-111497)
- [[cloud-run-gen2-container-threat-detection|Deploy falha por gen1 (Container Threat Detection)]] — desde 2026-10-30 o deploy em dev exige gen2; config em `pipeline/custom/ctbz/experts/backend/html-to-pdf.*.yml`
- [[smoke-test-dev]] — POST autenticado em dev para validar o deploy; o handler sempre devolve 200, então conferir o `%PDF`
- [[historico-mrs-html-to-pdf|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
