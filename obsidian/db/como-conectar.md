---
name: como-conectar
description: "Como conectar nos bancos Cloud SQL da CTBZ via psql: proxies, exportação das credenciais do DBeaver para ~/.pg_service.conf e ~/.pgpass e consulta (dev leitura e escrita, prd só leitura)"
metadata:
  type: reference
tags:
  - db
  - psql
  - cloud-sql
sistemas:
  - dbeaver
  - cloud-sql-proxy
atualizado_em: 2026-10-09
---

# Como conectar nos bancos

## 1. Subir os proxies

Os aliases ficam em `~/dotfiles/ctbz/sql-proxies` (carregado pelo `ctbz/terminal`). Cada instância escuta numa porta local fixa (dev 543x, prd 544x).

- `sql_all_dev_s` / `sql_all_prd_s` — sobe todos os proxies do ambiente em background (logs e pids em `~/.cache/sql-proxy/`).
- `sql_all_dev` / `sql_all_prd` — sobe em primeiro plano; Ctrl+C derruba todos.
- `sql_all_dev_stop` / `sql_all_prd_stop` — derruba.
- Individuais: `sql_<dominio>_<dev|prd>` (ex: `sql_exp_dev`).

Conferir se estão de pé: `ss -ltn | grep -E ':54[3-4][0-9]'`. Sem proxy, o psql falha com "connection refused". Não precisa de VPN.

## 2. Credenciais (uma vez)

Apesar de os proxies usarem `--auto-iam-authn`, **não existe usuário IAM do usuário nas instâncias**: as conexões usam usuários `BUILT_IN` com senha (ex: `experts_service`, `bots_api`), salvos no DBeaver.

O script `~/dotfiles/ctbz/dbeaver-to-pgservice [DEV|PRD]` decifra as credenciais do DBeaver e gera:

- `~/.pg_service.conf` — um bloco por conexão (host, porta, database, usuário). Todos com `statement_timeout=30000`; os de **PRD** também com `default_transaction_read_only=on`, então qualquer escrita em prod é recusada pelo próprio banco.
- `~/.pgpass` — só as senhas, `chmod 600`.

O script deve ser rodado **pelo usuário**, uma vez por ambiente (`! ~/dotfiles/ctbz/dbeaver-to-pgservice DEV` e `! ~/dotfiles/ctbz/dbeaver-to-pgservice PRD`): o modo automático do Claude Code bloqueia o agente de decifrar credenciais. Rodar de novo só quando senha ou conexão mudar no DBeaver; ele troca apenas o bloco `# >>> dbeaver-<env>` do ambiente e preserva o resto dos arquivos. Conexões `[DEPRECATED]` são ignoradas.

Nome do serviço = nome da conexão no DBeaver em minúsculas com `_` (ex: `[DEV] EXPERTS_experts_service` → `dev_experts_experts_service`).

## 3. Consultar

```bash
psql -w service=dev_experts_experts_service -c "select ..."
psql -w service=dev_experts_experts_service -Atc "..."   # saída crua, sem cabeçalho
```

- Sessões `prd_*` abrem em só leitura: escrita é recusada pelo próprio banco (`cannot execute ... in a read-only transaction`). Sessões `dev_*` aceitam escrita.
- `-w` evita o prompt de senha travar o comando se faltar entrada no `.pgpass`.
- Erro `password authentication failed`: senha/usuário errado no DBeaver — corrigir lá e rodar o script de novo.

## Regras para o agente

- **Dev**: liberado para ler e escrever (SELECT, INSERT, UPDATE, DELETE, DDL), sempre via `service=dev_*`. Antes de escrita em massa ou DDL destrutivo, conferir o alcance (ex: `count(*)` com o mesmo `where`).
- **Prod: SOMENTE LEITURA.** Só SELECT/consultas via `service=prd_*`. Nunca executar INSERT, UPDATE, DELETE, DDL, `SET transaction_read_only`/`BEGIN READ WRITE` ou qualquer comando que altere dados ou estrutura, mesmo que seja pedido: se uma correção em prod for necessária, montar o SQL e entregar para o usuário executar pelo fluxo dele.
- Issue: dev (`ticketing_dev`) e prod (`ticketing`) ficam na mesma instância; conferir o serviço antes de escrever.
- **Proxy**: se não estiver de pé, o agente sobe só o necessário e derruba ao terminar: `zsh -ic '_sql_proxy_start_alias sql_<dominio>_<dev|prd>'` → esperar a porta (`ss -ltn | grep :<porta>`) → consultar → `zsh -ic '_sql_proxy_kill_alias sql_<dominio>_<dev|prd>'`. Proxies que já estavam de pé ficam como estão.
- Nunca ler `~/.pgpass`, `credentials-config.json` ou exibir senhas.

Bancos por ambiente: [[bancos-dev]] e [[bancos-prd]].
