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
- [[optout-empresa-obrigatoria]] — opt-out sempre por empresa (companyCode obrigatório, PRD-175745), legado com company_id nulo e sinal da Meta
- [[historico-mrs-contato-service|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
- [[optout-registro-em-lote]] — rota `POST /optouts/batch` (array, não atômica, MR !58) e `purpose`/`companyCode` em array no `POST /optouts` (produto cartesiano, tudo ou nada), PRD-175747
