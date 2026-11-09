---
name: auto-grant-atendimento-canais
description: Script de "auto elevação" para se dar SELECT/UPDATE/DELETE em todos os bancos da instância Cloud SQL atendimento-canais (dev e prd) como usuário IAM
metadata:
  type: reference
---

# Auto grant nos bancos do atendimento-canais

Depois de ganhar acesso IAM à instância (usuário `cloud_iam_user` criado), o usuário ainda não enxerga as tabelas: elas pertencem aos roles das aplicações. O Henrique Aurelio mandou no chat (DM, 2026-10-05) um script que faz a "auto elevação" temporária, banco a banco: `GRANT <dono> TO <eu>` → `SET LOCAL ROLE <dono>` → `GRANT ...` → `REVOKE <dono> FROM <eu>`. Os grants ficam e a elevação é devolvida.

- Original (Henrique): só `SELECT`, instância **prd** (`sql_can_prd`, porta 5447), nome `canais-grant-leitura`.
- Versão dev com `SELECT, UPDATE, DELETE` (2026-11-09; DELETE incluído no mesmo dia): mesma estrutura, `ME=glener...`, `PORT=5433` (proxy `sql_atendimento_dev`, `--auto-iam-authn`), `GRANT SELECT, UPDATE, DELETE ON ALL TABLES` e `ALTER DEFAULT PRIVILEGES ... GRANT SELECT, UPDATE, DELETE ON TABLES`. Sequências continuam só com `SELECT`.
- `DRY_RUN=1` executa tudo e faz `ROLLBACK` no fim, bom para testar antes.
- Em prd o vault só permite leitura: nunca rodar a versão com UPDATE lá.

Estrutura do bloco `DO $$` (o essencial para refazer):

1. Eleva: para cada dono de banco/schema/tabela (fora `postgres`, `cloudsqladmin`, `cloudsqlsuperuser`, `pg_database_owner`) de que o executor ainda não é membro, `GRANT %I TO %I WITH SET TRUE`.
2. `GRANT USAGE ON SCHEMA` como dono de cada schema (`pg_database_owner` → dono do banco).
3. Por (schema, dono): `GRANT <privs> ON ALL TABLES`, `GRANT SELECT ON ALL SEQUENCES` e `ALTER DEFAULT PRIVILEGES FOR ROLE <dono>`.
4. `REVOKE` dos roles assumidos no passo 1.

O grantee é passado via `set_config('acesso.grantee', :'grantee', true)` porque variável do psql não entra dentro de `DO $$`.

## Armadilha: só funciona se o executor for membro de `cloudsqlsuperuser`

A elevação depende de o executor já ter poder sobre os roles donos das tabelas (na prática, ser membro de `cloudsqlsuperuser`). Um usuário IAM recém-criado na instância só entra em `cloudsqliamuser`, então o script devolve `sem permissão para assumir o role "contato_service"`, `elevação devolvida: {}` e nenhum grant é aplicado (2026-11-09, dev, instância `atendimento-canais-dev:us-central1:atendimento-canais`, Postgres 18). Sem `USAGE` no schema, `select * from person` responde `relation "person" does not exist`, mesmo que a tabela exista (`public.person`, dono `contato_service`).

Como resolver:

- Dar `cloudsqlsuperuser` ao usuário IAM: `gcloud sql users assign-roles <email> --instance=atendimento-canais --project=atendimento-canais-dev --type=CLOUD_IAM_USER --database-roles=cloudsqlsuperuser` (exige permissão de admin no Cloud SQL do projeto; quem não tem pede ao TL). Validado em 2026-11-09: depois disso a elevação `GRANT contato_service TO <eu> WITH SET TRUE` funciona e o script roda.
- Ou conectar como o dono (`contato_service`, senha no secret da aplicação) e rodar os `GRANT`s direto.

## Execução em dev (2026-11-09)

- O DBeaver quebra o bloco `DO $$ ... $$` nos `;` internos (`syntax error at or near "ELSE"`), mesmo trocando as opções. Rodar pelo `psql` com o usuário IAM: `psql -h 127.0.0.1 -p 5433 -U <email> -d <banco> -f auto-grant.sql`. Se uma tentativa falhar no DBeaver, a transação fica abortada (`25P02`) até um `ROLLBACK`.
- Aplicado nos 8 bancos da instância (`bots_api`, `canais_adk`, `contato_service`, `email_service`, `ms_agrupamento_guias`, `survey_service`, `zendesk_agents`, `zendesk_proxy`). Validado: `select count(*) from person` funciona e há UPDATE e DELETE (re-executado com DELETE no mesmo dia; INSERT não foi concedido).
- Em `ms_agrupamento_guias` o `public` pertence a `pg_database_owner` e o banco é do `postgres`, que o script não assume; o WARNING de USAGE é inofensivo porque `PUBLIC` já tem USAGE nesse schema.
- No zsh, rodar uma lista vinda de `$(...)` com `for DB in $DBS` não quebra por linha: usar a lista explícita ou `${(f)DBS}`.

## SQL completo (SELECT, UPDATE, DELETE)

Rodar pelo `psql` em cada banco da instância (`psql -h 127.0.0.1 -p 5433 -U <email> -d <banco> -f auto-grant.sql`), trocando o e-mail em `v_grantee`. Para só leitura, deixar apenas `SELECT` nas duas linhas de tabelas.

```sql
BEGIN;

DO $$
DECLARE
  v_grantee text := 'glener.pizzolato@contabilizei.com.br';
  v_me      text := current_user;
  v_dbowner text := (SELECT pg_get_userbyid(datdba) FROM pg_database WHERE datname = current_database());
  v_granted text[] := '{}';
  v_role    text;
  r         record;
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = v_grantee) THEN
    RAISE EXCEPTION 'Usuário "%" não existe na instância (criar como cloud_iam_user antes)', v_grantee;
  END IF;

  -- 1. eleva: vira membro temporário de todo dono de schema/tabela que ainda não é
  FOR r IN
    SELECT DISTINCT o AS owner FROM (
      SELECT v_dbowner AS o
      UNION SELECT pg_get_userbyid(nspowner) FROM pg_namespace
             WHERE nspname NOT LIKE 'pg\_%' AND nspname <> 'information_schema'
      UNION SELECT pg_get_userbyid(c.relowner) FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
             WHERE c.relkind IN ('r','p','v','m','f','S')
               AND n.nspname NOT LIKE 'pg\_%' AND n.nspname <> 'information_schema'
    ) x
    WHERE o NOT IN ('postgres','cloudsqladmin','cloudsqlsuperuser','pg_database_owner')
      AND NOT pg_has_role(v_me, o, 'MEMBER')
  LOOP
    BEGIN
      EXECUTE format('GRANT %I TO %I WITH SET TRUE', r.owner, v_me);
      v_granted := v_granted || r.owner::text;
    EXCEPTION WHEN insufficient_privilege THEN
      RAISE WARNING 'sem permissão para assumir o role "%"', r.owner;
    END;
  END LOOP;

  -- 2. USAGE nos schemas (como dono do schema; pg_database_owner => dono do banco)
  FOR r IN
    SELECT nspname, pg_get_userbyid(nspowner) AS owner FROM pg_namespace
     WHERE nspname NOT LIKE 'pg\_%' AND nspname <> 'information_schema'
  LOOP
    v_role := CASE WHEN r.owner = 'pg_database_owner' THEN v_dbowner ELSE r.owner END;
    BEGIN
      EXECUTE format('SET LOCAL ROLE %I', v_role);
      EXECUTE format('GRANT USAGE ON SCHEMA %I TO %I', r.nspname, v_grantee);
      EXECUTE 'RESET ROLE';
      RAISE NOTICE 'USAGE schema % (como %)', r.nspname, v_role;
    EXCEPTION WHEN insufficient_privilege THEN
      RAISE WARNING 'USAGE schema % falhou (dono %)', r.nspname, r.owner;
    END;
  END LOOP;

  -- 3. SELECT + UPDATE + DELETE nas tabelas existentes + default privileges para as futuras, por (schema, dono)
  FOR r IN
    SELECT DISTINCT n.nspname, pg_get_userbyid(c.relowner) AS owner
      FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
     WHERE c.relkind IN ('r','p','v','m','f','S')
       AND n.nspname NOT LIKE 'pg\_%' AND n.nspname <> 'information_schema'
  LOOP
    BEGIN
      EXECUTE format('SET LOCAL ROLE %I', r.owner);
      EXECUTE format('GRANT SELECT, UPDATE, DELETE ON ALL TABLES IN SCHEMA %I TO %I', r.nspname, v_grantee);
      EXECUTE format('GRANT SELECT ON ALL SEQUENCES IN SCHEMA %I TO %I', r.nspname, v_grantee);
      EXECUTE format('ALTER DEFAULT PRIVILEGES FOR ROLE %I IN SCHEMA %I GRANT SELECT, UPDATE, DELETE ON TABLES TO %I',
                     r.owner, r.nspname, v_grantee);
      EXECUTE 'RESET ROLE';
      RAISE NOTICE 'SELECT, UPDATE, DELETE %.* (dono %)', r.nspname, r.owner;
    EXCEPTION WHEN insufficient_privilege THEN
      RAISE WARNING 'SELECT/UPDATE/DELETE em %.* (dono %) falhou: sem acesso ao role', r.nspname, r.owner;
    END;
  END LOOP;

  -- 4. devolve a elevação (os grants acima permanecem)
  EXECUTE 'RESET ROLE';
  FOREACH v_role IN ARRAY v_granted LOOP
    EXECUTE format('REVOKE %I FROM %I', v_role, v_me);
  END LOOP;
  RAISE NOTICE 'elevação devolvida: %', v_granted;
END
$$;

COMMIT;
```
