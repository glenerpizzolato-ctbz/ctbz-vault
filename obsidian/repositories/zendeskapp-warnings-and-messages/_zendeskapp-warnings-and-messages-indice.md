---
name: zendeskapp-warnings-and-messages-indice
description: "Índice de notas do repositório zendeskapp-warnings-and-messages: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - zendeskapp-warnings-and-messages
repositorio: zendeskapp-warnings-and-messages
caminho: ~/repositories/zendeskapp-warnings-and-messages
---

# zendeskapp-warnings-and-messages

Repositório em `~/repositories/zendeskapp-warnings-and-messages`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[stack-e-execucao-local]] — stack (Node 26, Vite 8, TS 7, Biome, Vitest, Sentinela), rodar fora do Zendesk (client ZAF falso) e dentro (zcli), armadilhas
- [[dependencias-zendeskapp-warnings-and-messages]] — o que consome (atendimento-zendesk, sentinela-foundations, ZAF) e quem consome
- [[historico-mrs-zendeskapp-warnings-and-messages|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
- [[instalacao-e-grupos]] — instalação no Zendesk por ambiente (app_id prd 1321150, dev 1321165) e os grupos de permissão Leitor e Editor/Publicador com os ids
- [[plano-testes-e2e]] — plano de testes E2E da base (PRD-179547): pipelines dev/prd, permissões por grupo, chamada autenticada pelo Kong, e os pré-requisitos que faltavam
