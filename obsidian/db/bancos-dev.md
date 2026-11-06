---
name: bancos-dev
description: "Bancos de dados de dev da CTBZ: serviço psql, instância Cloud SQL, porta do proxy, database, usuário e situação do acesso"
metadata:
  type: reference
tags:
  - db
  - dev
atualizado_em: 2026-10-09
---

# Bancos de dev

Como conectar: [[como-conectar]]. Uso: `psql -w service=<serviço> -c "..."`. **Leitura e escrita liberadas** (SELECT, INSERT, UPDATE, DELETE, DDL). Situação testada em 2026-10-09.

| Domínio | Serviço psql | Instância (projeto:região:instância) | Proxy | Porta | Database | Usuário | Tabelas | Acesso |
|---|---|---|---|---|---|---|---|---|
| AIDA | `dev_aida_monitoria_ia` | `aida-stg:us-central1:db-aida-stg` | `sql_aida_dev` | 5431 | monitoria_ia | monitoria_ia | 13 | ok |
| AIDA | `dev_aida_file_transcriber` | `aida-stg:us-central1:db-aida-stg` | `sql_aida_dev` | 5431 | file_transcriber | file_transcriber | 2 | ok |
| Atendimento / canais | `dev_atendimento_canais_bots_api` | `atendimento-canais-dev:us-central1:atendimento-canais` | `sql_atendimento_dev` | 5433 | bots_api | bots_api | 8 | ok |
| Atendimento / canais | `dev_atendimento_canais_email_service` | `atendimento-canais-dev:us-central1:atendimento-canais` | `sql_atendimento_dev` | 5433 | email_service | email_service | 3 | ok |
| Atendimento / canais | `dev_atendimento_canais_contato_service` | `atendimento-canais-dev:us-central1:atendimento-canais` | `sql_atendimento_dev` | 5433 | contato_service | e-mail do usuário | — | ok (2026-11-06, com o e-mail do usuário; antes falhava com `password authentication failed` até o acesso ser ajustado) |
| Atendimento / canais | `dev_atendimento_canais_ms_agrupamento_guias` | `atendimento-canais-dev:us-central1:atendimento-canais` | `sql_atendimento_dev` | 5433 | ms_agrupamento_guias | ms_agrupamento_guias | 7 | ok |
| CRM | `dev_crm_atendimento_zendesk` | `contabilizei-crm-dev:us-central1:contabilizei-crm-dev` | `sql_crm_dev` | 5434 | atendimento-zendesk | atendimento-zendesk | 82 | ok |
| Experts | `dev_experts_experts_service` | `contabilizei-experts-dev:us-central1:contabilizei-experts-dev` | `sql_exp_dev` | 5435 | experts_service | experts_service | 21 | ok |
| Experts | `dev_experts_experts_nfs` | `contabilizei-experts-dev:us-central1:contabilizei-experts-dev` | `sql_exp_dev` | 5435 | experts_nfs | notasfiscais | 15 | ok |
| Issue | `dev_issue_ticketing` | `contabilizei-issue:us-central1:contabilizei-issue` | `sql_issue_dev` | 5437 | ticketing_dev | ticketing_dev | 6 | ok |

Observações:

- **Issue**: dev e prod ficam na **mesma instância** (`contabilizei-issue`); dev é só o database `ticketing_dev`. Antes de escrever, conferir que o serviço é `dev_issue_ticketing`.
- **Impostos** (`sql_impostos_dev`, porta 5436, `contabilizei-impostos-teste:us-central1:impostos-dev-01`, database `db_agrupamento_guias`): conexão `[DEPRECATED]` no DBeaver, fora do `.pg_service.conf`. Usa o `cloud_sql_proxy` antigo, sem IAM.
- Porta 5432 é reservada ao Postgres local (`[LOCAL] postgres` no DBeaver).
- **Empresas da plataforma (plano, status etc.) não estão em nenhum banco acessível de dev:** a plataforma (`plataforma-crm-web`, Postgres via App Engine) não tem conexão no DBeaver/`.pg_service.conf`, e `experts_service.empresa` só tem `cnpj`, `id_processo_abertura` e `assessor_id` (3 linhas em 2026-10-27). Para achar empresa por plano em dev, usar o admin (`admin-dev-03`) ou conferir CNPJ a CNPJ pela API do bot (`categoriaPlano`); a listagem do monolito (`auth/filtrarempresas`) em dev só funciona com token do SSO de teste autorizado para `monolito-dev-0N` (ver [[rotas-busca-empresa]]). Em prd, usar a skill `buscar-empresas-por-plano` (BigQuery) ou a API do monolito ([[rotas-busca-empresa]]).
