---
name: atendimento-api-gateway-indice
description: "Índice de notas do repositório atendimento-api-gateway: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - atendimento-api-gateway
repositorio: atendimento-api-gateway
caminho: ~/repositories/atendimento-api-gateway
---

# atendimento-api-gateway

Clone **antigo** (Bitbucket `contabilizei-ninjas`, parado em 2026-03) em `~/repositories/atendimento-api-gateway`; o repositório vivo é o do GitLab (`ctbz/atendimento/geral/atendimento-api-gateway`), clonado em `~/repositories/ctbz_atendimento_geral_atendimento-api-gateway`. Rotas dos apps Zendesk: [[autenticacao-kong-jwt]]. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[dependencias-atendimento-api-gateway|Dependências]] — o que consome (repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome
- [[deploy-e-pipeline-gitlab]] — a pipeline da master no GitLab falha na criação (cloudrun-deploy precisa de release-artifact-registry), então merge não publica o Kong; como conferir se uma rota está no ar
