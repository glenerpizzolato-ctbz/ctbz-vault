---
name: db-indice
description: "Índice dos bancos de dados (Cloud SQL Postgres) da CTBZ: quais existem por ambiente (dev/prd), em qual instância e porta de proxy, e como conectar via psql (dev leitura e escrita, prd só leitura)"
metadata:
  type: reference
tags:
  - db-indice
---

# Bancos de dados

Bancos Postgres no Cloud SQL acessados localmente pelos proxies de `~/dotfiles/ctbz/sql-proxies`, com as mesmas conexões configuradas no DBeaver. Senhas nunca ficam no vault: vivem no DBeaver e, exportadas, em `~/.pgpass`.

- [[como-conectar|Como conectar]] — subir os proxies, gerar `~/.pg_service.conf`/`~/.pgpass` a partir do DBeaver e consultar com `psql service=...` (dev leitura e escrita, prd só leitura)
- [[bancos-dev|Bancos de dev]] — serviços `dev_*` disponíveis, instância, porta, database e situação do acesso; leitura e escrita liberadas
- [[bancos-prd|Bancos de prod]] — serviços `prd_*`, **somente leitura**: nunca executar escrita em prod
- [[auto-grant-atendimento-canais|Auto grant no atendimento-canais]] — script de "auto elevação" (do Henrique) para se dar SELECT/UPDATE/DELETE em todos os bancos da instância como usuário IAM
- [[cloud-sql-alteracoes-com-restart|Alterações do Cloud SQL que reiniciam]] — habilitar HA (REGIONAL) e afins derrubam conexões (57P01) por minutos; como achar no audit log
- [[status-empresa-bigquery|Status da empresa (prod) pelo BigQuery]] — status, motivo de inatividade, plano e regime por CNPJ em `contabilizei-dataflow.saude_empresa.empresa` (snapshot mensal, só prod)
