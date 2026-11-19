---
name: contato-service-indice
description: "Índice de notas do repositório contato-service: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - contato-service
repositorio: contato-service
caminho: ~/repositories/contato-service
---

# contato-service

Repositório em `~/repositories/contato-service`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[vincular-contato-empresa]] — como vincular um contato a uma empresa (POST /api/v1/contacts hoje; PUT /companies/:code/memberships/:personId no MR !53)
- [[optout-empresa-obrigatoria]] — opt-out sempre por empresa (companyCode obrigatório, PRD-175745), legado com company_id nulo (bloqueia mesmo com revogação da empresa) e sinal da Meta
- [[contato-service/install-local|Install local]] — token do registry @contabilizei-private para o pnpm e armadilha do origin/HEAD apontando para main (a base é master)
- [[historico-mrs-contato-service|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
- [[optout-registro-em-lote]] — rota `POST /optouts/batch` (array, segue nos erros com resultado por item, por que não `Promise.allSettled`, MR !58) e `purpose`/`companyCode` em array no `POST /optouts` (produto cartesiano, tudo ou nada), PRD-175747
- [[dependencias-contato-service|Dependências]] — o que consome (repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome; os consumidores (antes na seção Consumidores deste índice) ficam em Consumido por
