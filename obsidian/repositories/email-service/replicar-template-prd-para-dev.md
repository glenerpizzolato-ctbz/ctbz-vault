---
name: replicar-template-prd-para-dev
description: Como copiar templates da tabela email_templates do email_service de prd para dev (mesmo HTML e variáveis, UUID novo), via \copy pelos proxies
metadata:
  type: reference
---

# Replicar template de prd para dev

A criação de template no email-service (`EmailTemplateDAO.create`) é só um INSERT em `email_templates` (`id` default `gen_random_uuid()`, `name` com índice único em `lower(name)`), sem efeito colateral. Então dá para copiar direto pelo banco, com os proxies `sql_atendimento_prd` (5443) e `sql_atendimento_dev` (5433) de pé:

1. Conferir que o nome ainda não existe em dev: `select name from email_templates where lower(name) in (...)` no `dev_atendimento_canais_email_service`.
2. Exportar de prd (só leitura): `psql -w service=prd_atendimento_canais_email_service -c "\copy (select name, html_content, variables, author from email_templates where id in (...)) to '<arquivo>'"`.
3. Importar em dev: `psql -w service=dev_atendimento_canais_email_service -v ON_ERROR_STOP=1 -c "\copy email_templates(name, html_content, variables, author) from '<arquivo>'"`. Dev gera o UUID novo.
4. Pegar os UUIDs novos pelo nome e conferir `md5(html_content)` igual nos dois bancos.

Usado em 2026-11-12 para os templates novos do agrupamento de guias ([[notificacao-agrupamento-experts-bp-lp]]).
