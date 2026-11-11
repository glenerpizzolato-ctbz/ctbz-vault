---
name: agrupamento-guias-service-indice
description: "Índice de notas do repositório agrupamento-guias-service: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - agrupamento-guias-service
repositorio: agrupamento-guias-service
caminho: ~/repositories/agrupamento-guias-service
gitlab: https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service
---

# agrupamento-guias-service

Repositório em `~/repositories/agrupamento-guias-service`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[arquitetura-e-migracao|Arquitetura]] — notificação por segmento (exp/bp × simples/lp × email/wpp, rota + tópico + consumer cada), banco próprio só com `notifications`, evento autocontido, o que saiu do desenho original e armadilhas (Awilix, pnpm install)
- [[historico-mrs-agrupamento-guias-service|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
- [[replicar-features-no-agrupamento-guias-service|Features do microsservico a replicar]] — work-items abertos aqui para cada feature de notificação do microsservico-agrupamento-guias ainda não portada (nota na pasta do microsservico)
