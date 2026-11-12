---
name: experts-service-como-testar-localmente
description: "Como rodar o experts-service localmente e testar um consumer Pub/Sub de ponta a ponta (ex: processar-guia-imposto) com Postgres e emulador do compose, plataforma de dev e publicação via REST do emulador, sem disparar nada real"
metadata:
  type: reference
tags:
  - experts-service
  - testes
  - pubsub
atualizado_em: 2026-11-12
---

# Como testar o experts-service localmente

## Subir

- `docker compose up -d database pubsub` na worktree (Postgres na 5432, emulador `messagebird/gcloud-pubsub-emulator` na 8681). O `redis` do compose usa a 6379 fixa: se ela já estiver ocupada (ex: `microsservico-agrupamento-guias-cache-1`), não subir o do compose e deixar o app usar esse (o `REDIS_HOST` padrão é `localhost`; a porta não é configurável).
- `pnpm db:migrate` (drizzle-kit, usa o `DATABASE_URL` do `.env`, `localhost:5432`).
- `PORT=<porta> PUBSUB_ENDPOINT=localhost:8681 pnpm dev`. O `--env-file=.env` do Node não sobrescreve variáveis já definidas. Com `NODE_ENV` diferente de `production`, `getPubsub` usa o emulador; com `GCLOUD_PROJECT=contabilizei-experts-dev` no `.env`, a `Config` é a de dev (plataforma `contabilizeiapp-dev-02`, agrupamento via `api-gateway-dev`).
- Os consumers criam o tópico e a subscription no emulador ao subir (`PubsubClient.getTopic/getSubscription`). Publicar depois que o app estiver de pé.

## Publicar no emulador

```bash
curl -s -X POST "http://localhost:8681/v1/projects/contabilizei-experts-dev/topics/<tópico>:publish" \
  -H 'Content-Type: application/json' \
  -d "{\"messages\":[{\"data\":\"$(base64 -w0 msg.json)\",\"attributes\":{\"clock\":\"$(date +%s%3N)\"}}]}"
```

O `GuiaImpostoNotifierConsumer` (`processar-guia-imposto`) lê `attributes.clock`; sem ele a mensagem vai para o catch (nack).

## Seguro por padrão

- As notificações de guia só viram linhas no `task_scheduler` local; quem publica as tasks é o `POST /v1/task-scheduler` (cron na nuvem), e localmente iria para o emulador. Nada chega a WhatsApp ou e-mail real.
- O `alreadySent(cnpj)` deduplica por CNPJ no dia: limpar `DELETE FROM task_scheduler WHERE cnpj = '...'` entre cenários.
- Limpeza: `docker compose down -v`.

## Armadilhas

- `getDadosEmpresa` chama `contabilizeiapp-dev-02.appspot.com` com `auth_token` em **query param**. Um 403 em HTML (`Error: Forbidden`) é o firewall do App Engine pelo IP: liberar em https://libera-meu-ip.ctbz.com.br/ no projeto `contabilizeiapp-dev-02`. A máquina sai por IPv6 para o appspot (ver [[sso-token-dev-prd]]).
- Empresa Experts Simples de dev ligada ao telefone de teste: `12996446000105` (2026-11-12). Para achar outras, skill `buscar-empresas-por-telefone --env dev`.
- Não há `faketime` instalado: regras que dependem do dia (ex: dia ≥ 15 do `shouldSchedule`) só dá para ver ao vivo na data certa; os testes unitários usam `vi.setSystemTime`.

Relacionado: [[notificacao-individual-guias-x-agrupamento]], [[deploy-e-variaveis-de-ambiente]].
