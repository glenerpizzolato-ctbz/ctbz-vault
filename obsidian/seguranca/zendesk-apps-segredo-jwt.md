---
name: zendesk-apps-segredo-jwt
description: "Como o segredo do JWT dos apps Zendesk (e o token do zcli) chega na instalação: variável do GitLab -> envsub/zcli-config -> zcli apps:update -> parâmetro seguro do app; o Kong valida com o mesmo segredo vindo do Secret Manager. Riscos achados em 2026-11-26 (segredo igual em dev e prd, impresso no log do deploy, variáveis sem mask)"
metadata:
  type: reference
tags:
  - seguranca
  - zendesk-app
  - jwt
criado_em: 2026-11-26
---

# Segredo do JWT dos apps Zendesk

## Como funciona hoje (todos os zendeskapps do grupo `ctbz/atendimento/geral`)

Os 16 apps com arquivo no repo `pipeline` (`custom/ctbz/atendimento/geral/zendeskapp-*.yml`) seguem o mesmo fluxo, sem Vault nem Secret Manager do lado do app:

1. **Variáveis do projeto no GitLab** (UI, por ambiente `dev`/`prd`): `JWT_SECRET_KEY` e `ZENDESK_OAUTH_TOKEN` (o comentário "cadastradas direto na UI do GitLab" está em todos os `*.dev.yml`/`*.prd.yml`). Os ids de grupo (`PERMISSION_GP_*`) e outras chaves (Firebase, Mixpanel) vão do mesmo jeito.
2. **Deploy**: `npm run config:${ENV}` (`envsub`) troca os `${VAR}` de `environments/zcli.apps.config.<env>.json` e grava `dist/zcli.apps.config.json`.
3. **`zcli apps:update dist`** sobe o pacote e, em seguida, faz `PUT /api/support/apps/installations/<id>.json` com **todos os parâmetros** do config (`updateProductInstallation` do `@zendesk/zcli-apps`). Ou seja: a cada deploy a pipeline reescreve as configurações da instalação, inclusive o parâmetro seguro `jwtSecretKey`. Mexer à mão no Admin Center não dura: o próximo deploy sobrescreve. Parâmetro do manifest que não está no config o zcli tenta perguntar (no CI fica vazio).
4. **No Zendesk**: `jwtSecretKey` é `secure: true`, então o valor fica no Zendesk e não chega ao navegador; o proxy do ZAF assina o JWT HS256 (`{{setting.jwtSecretKey}}`, claim `iss` = `2a7ed7a5-…`).
5. **Validação**: o Kong do `atendimento-api-gateway` (consumer JWT com key `2a7ed7a5-…`) valida a assinatura com `ZENDESKAPP_JWT_SECRET`, que vem do **Secret Manager** (`SET_SECRETS` em `custom/ctbz/atendimento/geral/atendimento-api-gateway.{dev,prd}.yml`, segredo `<projeto>_APIGW_ZENDESKAPP_JWT_SECRET:latest`). O `ZendeskAppsGuard` do `atendimento-zendesk` **não confere a assinatura**: só decodifica o payload e compara `sub` com `x-zendesk-user-id`, confiando que a chamada passou pelo Kong.

O vault-roleset (`vault read gcp-roleset-…`) aparece na pipeline só para credenciais GCP (token do Artifact Registry no `npm-access-token`, chave de SA quando `SERVICE_ACCOUNT_KEY_FROM_VAULT_ENABLED`), que todos os zendeskapps deixam `false`. Nenhum app Zendesk busca segredo de app no Vault ou no Secret Manager.

## Riscos achados (2026-11-26)

- **Mesmo segredo em dev e prd, em todos os apps**: os 15 `zendeskapp-*` do grupo com `JWT_SECRET_KEY` no GitLab têm o mesmo valor (conferido por hash em 2026-11-26; alguns com escopo `*` em vez de `dev`/`prd`). É o secret do único consumer JWT de apps no Kong (`zendeskapp`), então não há como cada app ter o seu sem consumer novo. Um JWT assinado em dev vale no gateway de prd, e quem tem acesso a dev tem o segredo de prd.
- **Segredo impresso no log do deploy**: o `CUSTOM_JOB_DEPLOY_BEFORE_SCRIPT` de todos faz `cat dist/zcli.apps.config.json`. No `deploy-prd` de 2026-11-24 do whatsapp-ativo o `jwtSecretKey` aparece em claro (variável sem `masked`). Projetos privados, mas com `public_jobs: true` (qualquer membro lê o log).
- **Variáveis sem mask e algumas sem protect**: `JWT_SECRET_KEY`/`ZENDESK_OAUTH_TOKEN` com `masked=false` em todos; `ZENDESK_OAUTH_TOKEN` de prd sem `protected` em concierge, timeline e dados-basicos-cliente; `JWT_SECRET_KEY` de prd sem `protected` no timeline.
- O clone antigo do gateway no Bitbucket (`contabilizei-ninjas/atendimento-api-gateway`) tem um segredo literal no `kong-template-*.yaml` (diferente do atual).

## Correção sugerida

1. Tirar o `cat dist/zcli.apps.config.json` dos deploys (ou imprimir sem os parâmetros seguros) e marcar `JWT_SECRET_KEY`/`ZENDESK_OAUTH_TOKEN` como masked + protected (+ hidden).
2. Separar o segredo por ambiente e rotacionar: novo `ZENDESKAPP_JWT_SECRET` no Secret Manager de cada ambiente do gateway, mesmo valor no `JWT_SECRET_KEY` de cada app, redeploy de gateway e apps (todos de uma vez, ou o Kong aceitando dois consumers durante a troca).
3. Opcional: o deploy dos apps ler o segredo do Secret Manager (`gcloud secrets versions access`) em vez de copiar na variável de cada projeto, para ter fonte única.

No `zendeskapp-warnings-and-messages` o deploy já não faz `cat` do config (MR !3582 do `pipeline`).

Passo a passo para cadastrar ou rotacionar um secret: [[subir-secrets-em-apps-zendesk]].
