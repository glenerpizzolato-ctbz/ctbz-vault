---
name: autenticacao-kong-jwt
description: "Como os apps Zendesk chegam ao atendimento-zendesk: pelo Kong do atendimento-api-gateway (atendimento[-crm][-dev].ctbz.com.br), com JWT HS256 assinado pelo proxy do ZAF e validado pelo consumer zendeskapp (iss 2a7ed7a5-...); o que o parâmetro 'Chave do JWT' é, como testar e como plugar um app novo (service, route, allow_paths, consumer próprio)"
metadata:
  type: reference
tags:
  - zendesk-apps
  - kong
  - jwt
criado_em: 2026-11-26
---

# Apps Zendesk: autenticação pelo Kong

## Como funciona

Há dois gateways no caminho dos apps (conferido em 2026-11-26 pelos headers e pelas rotas que cada um responde):

| | Antigo: `atendimento-api-gateway` | Novo: `kong-config` (DevOps) |
| --- | --- | --- |
| Kong | 3.6.1 em Cloud Run, atrás do LB do Google (`34.111.146.51`) | 3.9.5, atrás da Azion |
| Hosts | `atendimento[-crm][-dev].ctbz.com.br` | `api[-dev].contabilizei.com.br` |
| Quem usa | whatsapp-ativo, concierge, timeline, dados-básicos, dashboard-métricas, diagnóstico | hub-eficiencia, esteiras-atendimento e o Avisos e Mensagens (**padrão para app novo**) |
| Caminho do app | `/atendimento/zendesk/apps/<app>/api/v1/...` | `/zendesk/atendimento/zendesk/apps/<app>/api/v1/...` (a Azion só repassa `/zendesk/...`; sem o prefixo dá 502) |
| Deploy | `master` quebrada desde 2026-10 (ver [[deploy-e-pipeline-gitlab]]); dev sai de branch com `DEPLOY=true` | pipeline do repo (decK): dev aplica no merge, prd é job manual |

App novo: `baseUrl` `https://api[-dev].contabilizei.com.br` e prefixo `zendesk/atendimento/zendesk/apps/<app>` no client (ex: `HUB_EFICIENCIA_API_PATH` do zendeskapp-hub-eficiencia).

### Gateway antigo

- Cada app tem um **service** no Kong (`config/kong-template-<dev|prd>.yaml`, no GitLab `ctbz/atendimento/geral/atendimento-api-gateway`; o clone em `~/repositories/atendimento-api-gateway` aponta para o Bitbucket antigo, desatualizado) com rota `/atendimento/zendesk/apps/<app>` (`strip_path: true`) apontando para `${ATENDIMENTO_ZENDESK_URL}` e os plugins:
  - `header-validation`: exige `x-zendesk-user-id` e `x-zendesk-user-role`;
  - `jwt`: header `Authorization`, `key_claim_name: iss`, `claims_to_verify: [exp]`, `maximum_expiration: 3600`;
  - `kong-jwt2header`, `kong-path-allow` (só os prefixos do back-end daquele app, ex: `/api/v1/zendeskapps/whatsapp-ativo`), `rate-limiting` e `request-transformer`.
- O JWT é validado pelo **consumer `zendeskapp`** (`jwt_secrets`: key `2a7ed7a5-bd7a-497c-9274-131f21ad9d5f`, que é o `jwtIss` dos apps, e secret `${ZENDESKAPP_JWT_SECRET}`, que vem do Secret Manager pelo `SET_SECRETS` do repo `pipeline`). Não há `acl` nesses services: qualquer consumer JWT válido passa em qualquer rota de app.
- O `ZendeskAppsGuard` do atendimento-zendesk não confere a assinatura: confia no Kong.

## "Chave do JWT" na instalação do app

É o parâmetro seguro `jwtSecretKey`: o **secret do consumer** do Kong (hoje o do `zendeskapp`, igual ao `JWT_SECRET_KEY` cadastrado no GitLab dos outros apps e ao `ZENDESKAPP_JWT_SECRET` do gateway). O proxy do ZAF assina o token com ele e o Kong confere. Valor errado dá `401 {"message":"Invalid signature"}`. Segredo atual é o mesmo em dev e prd (ver [[zendesk-apps-segredo-jwt]]).

## Testar (só leitura)

No gateway novo: `GET https://api[-dev].contabilizei.com.br/zendesk/atendimento/zendesk/apps/<app>/api/v1/...` com o JWT e os headers. Rota publicada e caminho inexistente no back-end → 404 em JSON do atendimento-zendesk; fora do `allow_paths` → 403 `path not allowed`; rota não publicada → 404 em HTML (gateway antigo, rota `/` do front) ou 502 (Azion).


Armadilha no teste por curl: o `ZendeskAppsGuard` compara `payload.sub !== x-zendesk-user-id` com igualdade estrita, então o `sub` do JWT de teste tem de ir como **texto** (`"1"`, igual ao header). Com `sub` numérico o back-end devolve 403 `Forbidden resource` mesmo com o Kong aceitando o token. No Zendesk de verdade o app manda `sub: currentUser.id` e passa (visto no hub-eficiencia e no Avisos e Mensagens em 2026-11-26).

No gateway antigo:

Assinar um HS256 com `{"iss": "<key do consumer>", "sub": 1, "email": "...", "role": "agent", "exp": agora+300}` e chamar, com `x-zendesk-user-id`, `x-zendesk-user-role` e `x-cloud-trace-context`:
`GET https://atendimento-dev.ctbz.com.br/atendimento/zendesk/apps/whatsapp-ativo/api/v1/zendeskapps/whatsapp-ativo/templates` → 200 com o secret certo, 401 com o errado (conferido em 2026-11-26).

## Dois Kongs

As rotas dos apps existem em dois gateways, e um app novo entra nos dois:

- **`atendimento-api-gateway`** (GitLab `ctbz/atendimento/geral/atendimento-api-gateway`, clone em `~/repositories/ctbz_atendimento_geral_atendimento-api-gateway`; o `~/repositories/atendimento-api-gateway` é o Bitbucket antigo): Kong em Cloud Run do time, que atende `atendimento[-crm][-dev].ctbz.com.br` hoje. Um service por app em `config/kong-template-<env>.yaml`.
- **`kong-config`** (GitLab `ctbz/devops/recursos/kong-config`, decK/GitOps do DevOps): em dev, a rota `atendimento-zendesk-web-zendeskapp-jwt.route` (`dev/heimdall_legado/atendimento/atendimento-zendesk-web/atendimento-zendesk-web.yaml`); em prd, a `atendimento-zendesk-apps.route` (`prd/heimdall_legado/atendimento/atendimento-zendesk/atendimento-zendesk.yaml`). Cada app entra como dois paths (`/atendimento/zendesk/apps/<app>` e `/zendesk/atendimento/zendesk/apps/<app>`) mais o prefixo do controller no `kong-path-allow`; `acl` `atendimento-zendesk-apps-acl-group` + `jwt`. O consumer dos apps é o `deck_atendimento_legacy_to_many_v1_zendeskapp` (`dev/atendimento/consumers.yaml`, key `2a7ed7a5-...`, secret `DECK_ZENDESKAPP_TO_ATENDIMENTO_ZENDESK_JWT_SECRET`). O validador local (`.devops/scripts/validate_kong_config.py <env>`) precisa do `deck` instalado.

Exemplo: Avisos e Mensagens em kong-config!595 (no ar em dev e prd em 2026-11-26) e atendimento-api-gateway!9 (mergeado, mas não publicado, porque a `master` desse repo não faz deploy).

## Plugar um app novo

1. No `atendimento-api-gateway` (dev e prd): service `backend-zendesk-apps-<app>-service` com `url: ${ATENDIMENTO_ZENDESK_URL}`, rota `/atendimento/zendesk/apps/<app>` e os mesmos plugins, com `kong-path-allow` só no prefixo do controller novo.
2. Consumer próprio (recomendado, isola o segredo): `consumers` + `jwt_secrets` com key nova (UUID, vira o `jwtIss` do app) e secret `${<APP>_JWT_SECRET}` vindo do Secret Manager (`SET_SECRETS` do `atendimento-api-gateway.<env>.yml` no repo `pipeline`), valor diferente por ambiente. Para que só ele entre na rota (e ele não entre nas outras), `acl` no service + grupo do consumer.
3. No app: `jwtIss` = key nova, `jwtSecretKey` = secret novo (GitLab `JWT_SECRET_KEY` por ambiente), `baseUrl` = host do Kong e o client chamando `atendimento/zendesk/apps/<app>/api/v1/...`.
