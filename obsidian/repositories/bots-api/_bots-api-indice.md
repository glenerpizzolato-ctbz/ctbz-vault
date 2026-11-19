---
name: bots-api-indice
description: "Índice de notas do repositório bots-api: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - bots-api
repositorio: bots-api
caminho: ~/repositories/bots-api
---

# bots-api

- [[corujao-fila-noturna-experts]] — quando o reroute (`re-route-ticket.usecase.ts`) manda o ticket direto para o Corujão ou volta para o grupo de origem
- [[docker-build-local]] — `docker build` local (o `.npmrc` do repo não tem token; o 401 aparece como `ERR_PNPM_MINIMUM_RELEASE_AGE_VIOLATION`) e onde roda em prod (GKE; o Cloud Run está parado)
Repositório em `~/repositories/bots-api`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[historico-mrs-bots-api|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
