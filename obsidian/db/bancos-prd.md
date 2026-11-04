---
name: bancos-prd
description: "Bancos de dados de produção da CTBZ mapeados no DBeaver: instância Cloud SQL, porta do proxy e database; acesso SOMENTE LEITURA"
metadata:
  type: reference
tags:
  - db
  - prd
atualizado_em: 2026-10-09
---

# Bancos de prod

Como conectar: [[como-conectar]].

**SOMENTE LEITURA.** Só consultas (SELECT). Nunca executar INSERT, UPDATE, DELETE, DDL ou qualquer ação que altere dados em prod. Os serviços `prd_*` abrem com `default_transaction_read_only=on`, e nunca se deve desligar isso (`SET transaction_read_only`, `BEGIN READ WRITE`).

Os serviços são gerados pelo usuário com `! ~/dotfiles/ctbz/dbeaver-to-pgservice PRD`. Situação testada em 2026-10-09 (só SELECT; todas as sessões abriram com `transaction_read_only=on`).

Diferente de dev, em prod há usuário IAM do usuário em algumas instâncias (CRM, `contato_service`).

| Domínio | Serviço psql | Instância (projeto:região:instância) | Proxy | Porta | Database | Usuário | Tabelas | Acesso |
|---|---|---|---|---|---|---|---|---|
| AIDA | `prd_aida_monitoria_ia` | `aida-prd:us-central1:db-aida` | `sql_aida_prd` | 5441 | monitoria_ia | — | — | **falha**: proxy recebe 403 `cloudsql.instances.get` em `aida-prd` (falta permissão IAM no projeto) |
| AIDA | `prd_aida_file_transcriber` | `aida-prd:us-central1:db-aida` | `sql_aida_prd` | 5441 | file_transcriber | — | — | **falha**: mesmo 403 do proxy em `aida-prd` |
| Atendimento / canais | `prd_atendimento_canais_bots_api` | `atendimento-canais-prd:us-central1:atendimento-canais` | `sql_atendimento_prd` | 5443 | bots_api | bots_api | 8 | ok |
| Atendimento / canais | `prd_atendimento_canais_email_service` | `atendimento-canais-prd:us-central1:atendimento-canais` | `sql_atendimento_prd` | 5443 | email_service | glener.pizzolato | 2 | ok |
| Atendimento / canais | `prd_atendimento_canais_contato_service` | `atendimento-canais-prd:us-central1:atendimento-canais` | `sql_atendimento_prd` | 5443 | contato_service | e-mail do usuário (IAM) | 9 | ok |
| Atendimento / canais | `prd_atendimento_canais_ms_agrupamento_guias` | `atendimento-canais-prd:us-central1:atendimento-canais` | `sql_atendimento_prd` | 5443 | ms_agrupamento_guias | ms_agrupamento_guias | 7 | ok |
| CRM | `prd_crm_atendimento_zendesk` | `contabilizei-crm:us-central1:atendimento-zendesk` | `sql_crm_prd` | 5444 | atendimento-zendesk | e-mail do usuário (IAM) | 82 | ok |
| Experts | `prd_experts_experts_service` | `contabilizei-experts-prd:us-central1:contabilizei-experts` | `sql_exp_prd` | 5445 | experts_service | experts_service | 21 | ok |
| Experts | `prd_experts_experts_nfs` | `contabilizei-experts-prd:us-central1:contabilizei-experts` | `sql_exp_prd` | 5445 | experts_nfs | notasfiscais | 15 | ok |
| Issue | `prd_issue_ticketing` | `contabilizei-issue:us-central1:contabilizei-issue` | `sql_issue_prd` | 5447 | ticketing | ticketing | 10 | ok |

Observações:

- **Issue**: mesma instância do dev (`contabilizei-issue`); prod é o database `ticketing`.
- **Impostos** (`sql_impostos_prd`, porta 5446, `contabilizei-impostos:us-central1:impostos-prod-01`, database `db_agrupamento_guias`): `[DEPRECATED]` no DBeaver, fora da exportação.
