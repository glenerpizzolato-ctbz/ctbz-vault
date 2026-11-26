---
name: teste-e2e-plataforma-crm-indice
description: "Índice de notas do repositório teste-e2e-plataforma-crm: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - teste-e2e-plataforma-crm
repositorio: teste-e2e-plataforma-crm
caminho: ~/repositories/teste-e2e-plataforma-crm
---

# teste-e2e-plataforma-crm

Repositório em `~/repositories/teste-e2e-plataforma-crm` (GitLab [`ctbz/excelencia/automacao-plataforma-cliente/teste-e2e-plataforma-crm`](https://gitlab.com/ctbz/excelencia/automacao-plataforma-cliente/teste-e2e-plataforma-crm), branch `master`). Testes E2E em Cypress 12.17.4, mantidos pelo time de Qualidade (QAS), do autoatendimento da Plataforma CRM: o widget do Fale Conosco (`contabilizei-crm-widget-window`) até a abertura do chat. Notas sobre ele, uma linha por nota.

- [[rodar-testes-e2e-plataforma-crm]] — como instalar (binário do Cypress versionado no repo), rodar local em stg/dev03 (precisa de VPN, sem ela stg responde 403) e como roda na pipeline (template `e2e-plataforma-crm` no post-staging de outros repos, filtro `@regression+@autoatendimento`, Currents)
- [[e2e-criticos-canais]] — métrica de E2E crítico do squad Canais no Metabase: quais `test_key` são do Canais, qual spec cobre cada uma e por que o #3 (finalizar atendimento via chat) não conta
- [[dependencias-teste-e2e-plataforma-crm|Dependências]] — o que consome (repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome
