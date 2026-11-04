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

- [[alertas-de-envio]] — card no Google Chat, policies do Cloud Monitoring e subscriptions de inspeção dos envios com falha; plan de prd só na pipeline.
- [[historico-mrs-email-service|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
- [[contrato-optout|Contrato de opt-out]] — `optout_purpose` + `cnpj` (sem máscara, maiúsculas) no envio; `failure_reason` (não `reason`) traz a classe da falha no callback
