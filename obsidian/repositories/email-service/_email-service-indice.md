---
name: email-service-indice
description: "Índice de notas do repositório email-service: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - email-service
repositorio: email-service
caminho: ~/repositories/email-service
---

# email-service

Repositório em `~/repositories/email-service`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[alertas-de-envio]] — card no Google Chat, policies do Cloud Monitoring e subscriptions de inspeção dos envios com falha; plan de prd só na pipeline; erro de banco no validation worker dá ack e perde o envio (corrigido no #52: nack + DLQ na última tentativa).
- [[historico-mrs-email-service|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
- [[contrato-optout|Contrato de opt-out]] — `optout_purpose` + `cnpj` (sem máscara, maiúsculas) no envio; `failure_reason` (não `reason`) traz a classe da falha no callback
- [[testes-em-worktree|Testes em worktree]] — o `PORT` da worktree quebra o teste de env; rodar `env -u PORT pnpm test:coverage`
