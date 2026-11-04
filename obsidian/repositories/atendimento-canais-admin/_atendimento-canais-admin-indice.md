---
name: atendimento-canais-admin-indice
description: "Índice de notas do repositório atendimento-canais-admin: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - atendimento-canais-admin
repositorio: atendimento-canais-admin
caminho: ~/repositories/atendimento-canais-admin
---

# atendimento-canais-admin

Repositório em `~/repositories/atendimento-canais-admin`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[build-e-deploy|Build e deploy]] — antigo canais-bff; build local exige token do registry npm; build.sh faz deploy público sem --project (criou serviço avulso no aida-stg)
- [[dashboard-agrupamento-guias-bigquery|Dashboard Agrupamento de Guias e BigQuery]] — tabelas de dw_ms_agrupamento_guias, item_grupo_guia com pares repetidos e órfãos, armadilhas de rodar check/testes em worktree; front não leva coleção Bruno
- [[historico-mrs-atendimento-canais-admin|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
