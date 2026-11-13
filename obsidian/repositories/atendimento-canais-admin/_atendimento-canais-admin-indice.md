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
- [[envio-teste-template-email|Envio de teste de template de e-mail]] — aviso fixo pós-criação (SMTP da HubSpot quebra HTML que o preview mostra certo) e atalho `?enviar=<templateId>` na tela de envios
- [[historico-mrs-atendimento-canais-admin|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
- [[optout-tela-contato]] — como a tela de contato grava e consulta opt-out no contato-service (POST /optouts, /optouts/batch em pedaços de 100 e /optouts/search em pedaços de 1000)
- [[status-template-email|Status de template de e-mail]] — ativar/inativar templates, listagem por situação, bloqueio de envio com template inativo (o email-service só recusa no worker, após o 201) e as permissões por operação da área de e-mail; como montar o E2E local (.env aponta para o email-service de prd, perfis de permissão, override do Firestore, SMTP de dev quebrado)
