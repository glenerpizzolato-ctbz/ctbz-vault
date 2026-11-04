---
name: plataforma-monolito-indice
description: "Índice de notas do repositório plataforma-monolito: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - plataforma-monolito
repositorio: plataforma-monolito
caminho: ~/repositories/plataforma-monolito
---

# plataforma-monolito

Repositório em `~/repositories/plataforma-monolito`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[rotas-busca-empresa]] — `getByCnpj` e `auth/filtrarempresas` (listagem com plano no retorno), token do SSO pela coleção `contabilizeiapp`; dev-03 funcionando com token do SSO de teste para `monolito-dev-03` (passo a passo, `appId` por ambiente e listagem que quebra por enum inválido)
- [[colecao-contabilizeiapp]] — como chamar o monolito pela coleção `contabilizeiapp` do experts-bruno: IP, `User-Agent` e geração do token do SSO em dev e prd
