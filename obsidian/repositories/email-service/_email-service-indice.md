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

- [[alertas-de-envio]] — card no Google Chat (inclui o caso "Template não existe" do super-app com UUID de dev, 26/11/2026), policies do Cloud Monitoring e subscriptions de inspeção dos envios com falha; plan de prd só na pipeline; erro de banco no validation worker dá ack e perde o envio (corrigido no #52: nack + DLQ na última tentativa); REPLICATION_NOT_FOUND em rajada (pool esgotado + record e dispatch em paralelo) deixa o e-mail PENDING sem envio, e o reprocess não pega PENDING (corrigido no #49: linha gravada antes do publish, replicate-record removida em dois deploys).
- [[historico-mrs-email-service|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
- [[contrato-optout|Contrato de opt-out]] — `optout_purpose` + `cnpj` (sem máscara, maiúsculas) no envio; `failure_reason` (não `reason`) traz a classe da falha no callback
- [[teste-banco-fora|Testar com o banco fora]] — retentativa da validação em dev: branch local + derrubar só o proxy local, com o pod de dev escalado a 0
- [[testes-em-worktree|Testes em worktree]] — o `PORT` da worktree quebra o teste de env; rodar `env -u PORT pnpm test:coverage`
- [[replicar-template-prd-para-dev|Replicar template de prd para dev]] — `\copy` de `email_templates` entre os bancos (mesmo HTML e variáveis, UUID novo gerado em dev)
- [[envios-no-hubspot|Envios na HubSpot]] — só SMTP API, sem tag/header/evento, um token para todos os apps; o envio fica no portal do token SMTP (47852359), não no 21138480 dos tokens de API; onde procurar
- [[smtp-dev-hubspot-dominio|SMTP de dev recusado pela HubSpot]] — 421 "connected email sending domain": o portal 51348990 de dev não tem ctbz.com.br conectado; não é código (último SENT 28/05, FAILED desde 20/08); evidências de DNS/DKIM por portal.
- [[status-de-templates]] — soft delete de templates: coluna status, rotas activate/inactivate, bloqueio no envio (TEMPLATE_INACTIVE) e filtro na listagem. Deploy de dev manual e corrida de tag entre merges seguidos.
- [[dados-no-bigquery|Dados no BigQuery]] — email_replications e email_templates no trusted do CDC: partição por created_at, cluster status/template_id/application, atraso D-1, completo vs Postgres, email_templates sem a coluna status
- [[migrar-template-do-mandrill|Migrar template do Mandrill]] — sem chave do Mandrill: HTML de um .eml real, desfazer o rastreamento (click/open), trocar valores por {{VAR}}, criar e testar pela API com o token do Bruno
- [[dependencias-email-service|Dependências]] — o que consome (repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome
