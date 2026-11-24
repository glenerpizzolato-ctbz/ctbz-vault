---
name: experts-functions-indice
description: "Índice de notas do repositório experts-functions: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - experts-functions
repositorio: experts-functions
caminho: ~/repositories/experts-functions
---

# experts-functions

Repositório em `~/repositories/experts-functions`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[templates-mandrill-holerite-e-guias|Templates Mandrill de holerite e guias]] — `experts-envio-de-holerite` ativo (email-holerites, admin FOPAG); `experts-disponibiliza-o-de-guias` sem uso desde 21/09/2026
- [[e2e-holerite-dev|E2E do holerite em dev]] — script (só no vault) que publica no functions.email-holerites de dev e confere function, email_replications, PDFs, e-mail renderizado e status (FAILED esperado pelo 421 do SMTP de dev)
- [[build-e-imagem]] — Dockerfile da raiz compartilhado entre functions, tag de imagem por release
- [[historico-mrs-experts-functions|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
- [[dependencias-experts-functions|Dependências]] — o que consome (repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome
