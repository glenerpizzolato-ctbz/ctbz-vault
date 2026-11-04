---
name: api-gateway-bots-whatsapp
description: "Como obter a x-api-key do API gateway do atendimento (Kong) usada pelo bot de WhatsApp (Ultimate) via cloud function zendeskbot-config, e chamar as rotas de busca por telefone/CNPJ e autenticação (plataforma-crm-web e atendimento-zendesk)"
metadata:
  type: reference
tags:
  - apis
  - api-gateway
  - kong
  - ultimate
  - bruno
sistemas:
  - zendeskbot-functions
  - atendimento-api-gateway
  - plataforma-crm-web
  - atendimento-zendesk
  - experts-bruno
atualizado_em: 2026-10-27
---

# API gateway dos bots de WhatsApp (Ultimate)

As rotas que o bot de WhatsApp da Ultimate chama (plataforma-crm-web e atendimento-zendesk) passam pelo API gateway (Kong) do atendimento, autenticadas por `x-api-key`. Essa chave **não** é o token do SSO ([[sso-token-dev-prd]]): é a mesma que a Ultimate usa, e quem a fornece é a cloud function `zendeskbot-config`.

Skills que fazem isso sozinhas: `buscar-empresas-por-telefone` e `autenticar-empresa-whatsapp` (script `bots_api.py`). A chave fica salva em `~/dotfiles/docs/ai/skills/ctbz/empresas/buscar-empresas-por-telefone/bruno/.env` (gitignored, renovada pelo script quando o Kong a recusa; `bots_api.py credenciais --env todos` força), e a pasta `bruno/` da skill é uma collection Bruno com as três rotas usando essa autenticação. Ela substitui a pasta `glener-funcionando` da collection da plataforma-crm-web, que tinha a chave de prd fixa no `folder.bru` (em 2026-10-27 ainda igual à atual de prd; a de dev é outra).

## Como obter a x-api-key (o jeito certo)

Em vez de copiar a chave das integrações da Ultimate na mão, fazer o que o próprio bot faz:

1. **AUTH_TOKEN da function**: fica nas variáveis de ambiente da `zendeskbot-config` (gen2, `us-central1`, repositório `zendeskbot-functions`, deploy com `--env-vars-file .env.yaml`). Ver com `gcloud functions describe zendeskbot-config --project contabilizei-crm --region us-central1` (dev: `contabilizei-crm-dev`), em `serviceConfig.environmentVariables.AUTH_TOKEN`.
2. **Config do bot**: `GET <uri da function>?auth_token=<AUTH_TOKEN>` (ou `https://us-central1-contabilizei-crm.cloudfunctions.net/zendeskbot-config`). A resposta traz `config.app.services.apigateway.url` (prd `atendimento.ctbz.com.br`, dev `atendimento-dev.ctbz.com.br`) e `.token` (a `x-api-key`), além de tokens de functions e Sunshine. O config sai dos `environments/config-<env>.json` publicados com a function, então é sempre o que a Ultimate está usando.
3. **Chamar o gateway** com os headers que o Kong exige (`header-validation`): `x-api-key`, `x-cloud-trace-context` e `x-atendimento-id`. Os dois últimos aceitam qualquer valor no formato (`<32 hex>/<número>;o=1` e um id qualquer); `x-conversation-id` é opcional (só vai para o log).

### No Bruno

A collection `~/repositories/experts-bruno/ultimate-ai-bots` já faz esse fluxo: `bots/wpp-main/init/1 config` chama a function com `fn_token` (`{{process.env.functions_token_prod}}`/`functions_token_dev`) e grava `apigatewayUrl`/`apigatewayToken` nas variáveis; depois as requests de `id_empresa/` (`1 count cnpjs by phone`, `2 details cnpj by phone`) usam esses valores. Basta ter o `ultimate-ai-bots/.env` com `functions_token_prod`/`functions_token_dev` = `AUTH_TOKEN` da function de cada ambiente e rodar `1 config` antes.

A collection `docs/bruno` da plataforma-crm-web (pasta `bots`, env `dev03-libera_meu_ip`) usa a chave fixa em `apiGatewayTokenDev`/`apiGatewayTokenPrd` do `.env` dela, que quebra quando a chave muda ou alguém mexe na collection. A pasta `v2/` e `empresas/` dessa collection chamam o App Engine direto (`/crm/rest/auth/atendimento/...`) e aí o token é o do SSO no query param `auth_token` (o `script:pre-request` do `collection.bru` que fazia isso foi removido numa alteração local).

## Rotas no gateway

Definidas em `~/repositories/atendimento-api-gateway/config/kong-template-<env>.yaml` (`strip_path: true` + plugin `kong-path-allow`):

| Prefixo no gateway | Serviço | Paths liberados |
| --- | --- | --- |
| `/atendimento/zendesk/bots/whatsapp/plataforma` | plataforma-crm-web (`PLATAFORMA_CRM_WEB_URL`) | `/atendimento/v2/bots/whatsapp/dados-cliente` |
| `/atendimento/zendesk/bots/whatsapp/fluxo/interacao` | atendimento-zendesk (`ATENDIMENTO_ZENDESK_URL`) | `/api/v1`, `/api/v2`, `/api/v4/bots/whatsapp` |
| `/atendimento/zendesk/bots/whatsapp/fluxo/inicio` | atendimento-zendesk | início da conversa (gera `traceId`/`atendimentoId`) |

Rotas de empresa usadas pelo bot (todas `POST`, somente leitura):

- `.../plataforma/atendimento/v2/bots/whatsapp/dados-cliente/buscar-por-telefone` — body `{"telefone": "+55..."}`: CNPJs e `categoriaPlano` do telefone, em ativas/rascunho, inativas e qualquer status (cada um com `quantidades`, `listasCNPJs`, `listasEmpresas`).
- `.../plataforma/atendimento/v2/bots/whatsapp/dados-cliente/buscar-por-telefone-e-cnpj` — body `{"telefone", "cnpj"}`: `possuiTelefoneVinculadoEmpresa`, `empresaInativa`, acessos (`possuiAcessoBasicoPadraoMultibeneficios`, `possuiAcessoBank`, `possuiAcessoExperts`) e `empresaLogada` (razão social, status, plano, município, telefones, regime, assessor etc.).
- `.../fluxo/interacao/api/v1/bots/whatsapp/autenticacao/basico-padrao` — body `{"area": "CRM|BANK|EXPERT|ATIVACAO", "telefone", "cnpj"?, "cpf"?}`: `statusBot`, `categoriaPlano` etc. Regras em [[categoria-plano-autenticacao-whatsapp]].

No código: `DadosClienteGeralWhatsAppBotJersey.kt` (plataforma-crm-web, `@Path("auth/atendimento/v2/bots/whatsapp/dados-cliente")`, exige telefone começando com `+`) e `whatsapp-autenticacao-basico-padrao.controller.ts` (atendimento-zendesk).

## Armadilhas

- **403 em HTML (`<title>403</title>403 Forbidden`) com a chave certa**: o WAF na frente do gateway bloqueia o User-Agent `Python-urllib`. Mandar um User-Agent de cliente comum (ex: `curl/8.5.0`). Validado em 2026-10-27 (prd): mesma chamada passou de 403 para 200 só trocando o User-Agent.
- **400 do Kong**: faltou `x-cloud-trace-context` ou `x-atendimento-id`.
- **401 na `zendeskbot-config`** (`Unauthorized`): `auth_token` diferente do `AUTH_TOKEN` atual da function (vem do `.env.yaml` de cada deploy, então pode mudar); pegar de novo pelo `gcloud functions describe`.
- **dev**: mesmo fluxo com `contabilizei-crm-dev` (gateway `atendimento-dev.ctbz.com.br`, plataforma no `contabilizeiapp-dev-03`), validado em 2026-10-27 nas três rotas. A chave de dev é diferente da de prd.
- **500 em HTML (`Server Error`) em dev**: cold start do `crm-web` no App Engine (`Request was aborted after waiting too long` no log); repetir a chamada.
- **Log do App Engine expõe token**: a request que chega na plataforma tem o token do SSO no query param `auth_token` (o gateway injeta), então `gcloud logging read` com `protoPayload.resource` mostra o valor; ao consultar log, não imprimir esse campo.
