---
name: zendeskapp-warnings-and-messages-instalacao-e-grupos
description: "Instalação do app Avisos e Mensagens no Zendesk por ambiente (app_id, installation id, parâmetros) e os grupos de permissão Leitor e Editor (Publicador), com ids de prd e dev"
metadata:
  type: reference
tags:
  - zendeskapp-warnings-and-messages
  - zendesk-apps
  - permissoes
criado_em: 2026-11-26
---

# Instalação e grupos de permissão

## Prd (`contabilizei.zendesk.com`)

- App privado criado em 2026-11-26 por upload do .zip (ver [[criar-app-privado]]): **app_id `1321150`**, installation `32134995952540`, nome `zendeskapp-warnings-and-messages`.
- Grupos de permissão (criados em 2026-11-26):

| Papel no app | Parâmetro | Grupo | Id |
| --- | --- | --- | --- |
| Leitor (só lista e histórico) | `permissionGpLeitor` | Permissoes - zendeskapp-warnings-and-messages - Leitor | `32134932901532` |
| Publicador (cria, edita, ativa, inativa) | `permissionGpPublicador` | Permissoes - zendeskapp-warnings-and-messages - Editor | `32134947702940` |

O grupo se chama "Editor", mas no app (e na especificação do card) o papel é **Publicador**.

- Parâmetros conferidos pela API (`GET /api/v2/apps/installations.json`, 2026-11-26): `baseUrl` `https://api.contabilizei.com.br` (Kong novo, `kong-config`; trocado em 2026-11-26 do `atendimento-crm.ctbz.com.br` do gateway antigo, ver [[autenticacao-kong-jwt]]), `jwtIss` `2a7ed7a5-bd7a-497c-9274-131f21ad9d5f`, grupos acima. **`env` estava `localhost`**: em prd tem de ser `prd` (com `localhost` o app usa o JWT do `localStorage` e não assina pelo proxy). O primeiro deploy pela pipeline também grava `env` com o nome do ambiente.
- Sem restrição por grupo na instalação (`group_restrictions: []`): o ícone some pelo `client.invoke('hide')` para quem não tem papel; restringir aos dois grupos na aba Configurações deixa isso garantido.

## Dev (`contabilizei1637606740.zendesk.com`)

- App privado criado em 2026-11-26 com o mesmo nome (`zendeskapp-warnings-and-messages`). **app_id `1321165`** (owner `11721909`).
- Grupos de permissão, com os mesmos nomes de prd:

| Papel no app | Parâmetro | Grupo | Id |
| --- | --- | --- | --- |
| Leitor | `permissionGpLeitor` | Permissoes - zendeskapp-warnings-and-messages - Leitor | `32135065202332` |
| Publicador | `permissionGpPublicador` | Permissoes - zendeskapp-warnings-and-messages - Editor | `32135080911900` |

- Parâmetros: `env` `dev` (nunca `localhost` na instalação), `baseUrl` `https://api-dev.contabilizei.com.br` (Kong novo), `jwtIss` igual ao de prd.
- Os ids e a instalação de dev não foram conferidos pela API: o `personal_user_token_sandbox` da coleção `experts-bruno/zendesk-api` dá 401 em `contabilizei1637606740` (2026-11-26).

## Variáveis do GitLab

`ZENDESK_APP_ID` (prd `1321150`, dev `1321165`), `JWT_SECRET_KEY`, `ZENDESK_OAUTH_TOKEN`, `PERMISSION_GP_PUBLICADOR` (prd `32134947702940`, dev `32135080911900`) e `PERMISSION_GP_LEITOR` (prd `32134932901532`, dev `32135065202332`), por ambiente. A pipeline reescreve os parâmetros da instalação a cada deploy (ver [[subir-secrets-em-apps-zendesk]]).

## Achar o app_id

Na URL do app privado no Admin Center aparece o id da instalação, não o app_id. Com a sessão de admin aberta no navegador, `https://<subdomínio>.zendesk.com/api/v2/apps/owned.json` lista os apps privados da conta com o `id` (app_id); `/api/v2/apps/installations.json` traz a instalação com `app_id` e os parâmetros.
