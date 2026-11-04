---
name: colecao-contabilizeiapp
description: "Coleção contabilizeiapp do experts-bruno (plataforma-monolito/contabilizeiapp): ambientes, variáveis do .env e passo a passo para gerar o token do SSO de dev e de prd e fazer as chamadas funcionarem"
metadata:
  type: reference
tags:
  - experts-bruno
  - plataforma-monolito
  - sso
repositorio: experts-bruno
atualizado_em: 2026-10-27
---

# Coleção `contabilizeiapp` (plataforma/monolito)

Coleção Bruno em `~/repositories/experts-bruno/contabilizeiapp`, que chama o `plataforma-monolito` (app/projeto GCP `contabilizeiapp`). Pastas: `pltf-monolito` (ex: `Empresa/getByCnpj`), `pltf-back-worker`, `pendencias-rotinas`. Rotas de empresa e armadilhas em [[rotas-busca-empresa]].

## Ambientes e variáveis

| Ambiente Bruno | Base (`baseUrl_FqdnAppSpot`) | Token |
|---|---|---|
| `prod` | `https://contabilizeiapp.appspot.com` | `{{process.env.sso_token_prod}}` |
| `dev03-libera_meu_ip` | `https://contabilizeiapp-dev-03.appspot.com` | `sso_token_dev` no `.env` (o arquivo do ambiente ainda tem um token literal antigo; trocar por `{{process.env.sso_token_dev}}` ao usar) |
| `dev01`, `dev02` | `https://contabilizeiapp-dev-0N.appspot.com` | token literal antigo no arquivo |

`.env` da coleção (gitignored, nunca commitar): `sso_token_prod`, `sso_token_dev`, `sso_token_prod_exp` e, para gerar o token de dev, `sso_cookie_dev`. As chamadas mandam o token na query (`auth_token=...`).

## Pré-requisitos comuns

- **IP liberado** em `https://libera-meu-ip.ctbz.com.br/` para o projeto (`contabilizeiapp` em prd, `contabilizeiapp-dev-0N` em dev). Sem isso: **403 em HTML** (firewall do App Engine). A VPN não resolve; a chamada costuma sair por IPv6 (`curl -s -o /dev/null -w "%{remote_ip}" <url>`).
- **Mesmo `User-Agent`** na chamada e na geração do token: o `contabilizei-sso-client` só aceita o token com o `User-Agent` usado na criação.
- **Token com o sistema do serviço** em `sistemasAutorizados`: o monolito valida contra o `monolito.sso.app.id` do ambiente (`monolito` em prd, `monolito-dev-0N` em dev; tabela em [[rotas-busca-empresa]]). Sem isso, **401** e, no log do App Engine, `Token nao possui acesso ao sistema: <appId>`.

## Token de prd

1. Logar em `https://sso.contabilizei.com/sistema-admin/` e copiar o cookie da sessão.
2. Rodar `contabilizei-sso/criar token` do experts-bruno (já aponta para `https://contabilizei-sso.appspot.com/_ah/api/usuarioApi/v1/autorizarSistemaExterno`, com `User-Agent` fixo `Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36` no header e no body).
3. Copiar o `token` da resposta para `sso_token_prod` no `.env` da coleção e chamar com o mesmo `User-Agent` (Chrome/133).

Validado em 2026-10-27: `getByCnpj` e `auth/filtrarempresas` responderam 200 em prd.

## Token de dev (SSO de teste)

A request `contabilizei-sso/criar token` tem a URL de **prd** fixa e não serve para dev. Passo a passo validado em 2026-10-27 no dev-03:

1. Logar em `https://contabilizei-sso-teste.appspot.com/sistema-admin/` (a raiz do domínio dá 404). Se o login com Google não abrir nada e o navegador mostrar 401 em `/rest/usuario/autorizacoes`, há um `oauth-token-admin` antigo: limpar os cookies do domínio (ou usar janela anônima) e logar de novo.
2. No DevTools, **Application → Cookies**, copiar o **valor** do cookie `oauth-token-admin` para `sso_cookie_dev` no `.env` da coleção. Anotar o `navigator.userAgent` do navegador (a sessão do SSO é presa a ele).
3. Gerar o token:

    ```
    POST https://contabilizei-sso-teste.appspot.com/_ah/api/usuarioApi/v1/autorizarSistemaExterno
    Content-Type: application/json
    Cookie: oauth-token-admin=<sso_cookie_dev>
    User-Agent: <navigator.userAgent>

    {"nomeSistema": "Experts-Bruno", "sistemasAutorizados": ["monolito-dev-03", "plataforma"], "userAgent": "<navigator.userAgent>"}
    ```

    Trocar `monolito-dev-03` pelo `appId` do ambiente usado. **Não incluir `contabilizeiapp`**: não existe no SSO de teste (400 `Sistema contabilizeiapp nao cadastrado`).
4. Copiar o `token` da resposta para `sso_token_dev` e chamar o dev com o **mesmo `User-Agent` do navegador** (não o Chrome/133 fixo da coleção). No Bruno, ajustar o header `User-Agent` da coleção para esse valor.

## Erros comuns

| Erro | Causa | Solução |
|---|---|---|
| 403 HTML `Error: Forbidden` | IP não liberado no projeto | `libera-meu-ip` para o projeto certo |
| 401 HTML `Error: Unauthorized` | token expirado, `User-Agent` diferente ou sem o sistema do ambiente | ver o log do App Engine (`gcloud logging read 'textPayload:"Token nao"' --project <projeto>`) e gerar de novo |
| 401 `Não autorizado` ao gerar o token | cookie do SSO inválido/antigo ou `User-Agent` diferente do navegador | logar de novo (limpando cookies) e usar o `navigator.userAgent` |
| 400 `Sistema <nome> nao cadastrado` | sistema inexistente naquele SSO | tirar da lista |
| 400 `The offset <n> must be between 0 and 1000` | limite de paginação da listagem (Datastore) | não passar de offset 1000; particionar por `status`/`ramoAtividade` |
| 400 `No enum constant ...MotivoStatusEmpresa...` (dev) | empresa com dado inválido na página da listagem | paginar item a item pulando os que falham ([[rotas-busca-empresa]]) |

Mais contexto sobre o SSO em [[sso-token-dev-prd]].
