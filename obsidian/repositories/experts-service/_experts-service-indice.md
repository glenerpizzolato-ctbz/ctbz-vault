---
name: experts-service-indice
description: "Índice de notas do repositório experts-service: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - experts-service
repositorio: experts-service
caminho: ~/repositories/experts-service
---

# experts-service

Repositório em `~/repositories/experts-service`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[fluxo-encerramento-com-ia]] — Encerramento com IA (desconexão): validações, estados, IA, timeout, fora de horário, parâmetros e tempos
- [[notificacao-individual-guias-x-agrupamento|Notificação individual de guias x agrupamento]] — filtros do consumer `processar-guia-imposto`, regra do dia 15, listas de impostos divergentes e armadilhas de duplicidade/silêncio com o agrupamento
- [[auditoria-troca-assessor|Auditoria das trocas de assessor]] — autor via Keycloak (`resolveAuthor`), tabela `event`, BigQuery e a armadilha do `data` do `UPDATED_ASSESSOR_EMPRESA`
- [[cobertura-sonar-vitest|Cobertura do Sonar x exclusões do vitest]] — arquivo em `coverage.exclude` do vitest vira 0% no Sonar (caso do `src/infra/auth`)
- [[deploy-e-variaveis-de-ambiente|Deploy e variáveis de ambiente]] — variáveis de deploy e do app no repo `pipeline`, KEDA e concorrência do consumer de guias
- [[historico-mrs-experts-service|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
