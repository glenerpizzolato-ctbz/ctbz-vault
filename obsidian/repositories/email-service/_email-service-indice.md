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
- [[teste-banco-fora|Testar com o banco fora]] — retentativa da validação em dev: branch local + derrubar só o proxy local, com o pod de dev escalado a 0
- [[testes-em-worktree|Testes em worktree]] — o `PORT` da worktree quebra o teste de env; rodar `env -u PORT pnpm test:coverage`
- [[replicar-template-prd-para-dev|Replicar template de prd para dev]] — `\copy` de `email_templates` entre os bancos (mesmo HTML e variáveis, UUID novo gerado em dev)
- [[status-de-templates]] — soft delete de templates: coluna status, rotas activate/inactivate, bloqueio no envio (TEMPLATE_INACTIVE) e filtro na listagem. Deploy de dev manual e corrida de tag entre merges seguidos.
