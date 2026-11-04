---
name: sso-token-dev-prd
description: "Como gerar o token do SSO de dev/prd para chamar APIs internas (ex: contabilizei-impostos) pelo Bruno, e como resolver 401/403"
metadata:
  type: reference
tags:
  - apis
  - sso
  - bruno
sistemas:
  - contabilizei-sso
  - contabilizei-impostos
  - experts-bruno
atualizado_em: 2026-10-08
---

# Token do SSO (dev/prd) para chamar APIs internas

## Onde está

Collection `contabilizei-impostos/` no repositório `experts-bruno` (memória de cálculo do Lucro Presumido). No Bruno: *Open Collection* apontando para essa pasta. Ambientes `dev` (homologação, projeto `contabilizei-impostos-teste`) e `prd`.

## Como gerar o token

1. Crie `contabilizei-impostos/.env` (ignorado pelo git) com:

   ```
   sso_cookie_dev="<cookie do SSO de homologação>"
   sso_cookie_prd="<cookie do SSO de produção>"
   sso_token_dev="<token gerado em dev>"
   sso_token_prd="<token gerado em prd>"
   ```

2. Faça login no SSO do ambiente (prd: `https://sso.contabilizei.com/sistema-admin/`; dev: `https://contabilizei-sso-teste.appspot.com/sistema-admin/` ou `https://sso-nonprod.contabilizei.com/sistema-admin/`, este atrás do IAP com login Google; a raiz `contabilizei-sso-teste.appspot.com/` dá 404, é preciso entrar pelo `/sistema-admin/`).
3. No DevTools, vá em **Application → Cookies** (ou copie o header `Cookie` de uma request na aba Network) e cole em `sso_cookie_prd`/`sso_cookie_dev`.
4. No Bruno, selecione o ambiente e rode `auth/gerar token sso`. Ela chama `/_ah/api/usuarioApi/v1/autorizarSistemaExterno` pedindo autorização para o sistema do serviço (`contabilizei-impostos` em prd, `contabilizei-impostos-teste` em dev) e o token já passa a valer nas próximas requests enquanto o Bruno estiver aberto.
5. Para deixar fixo, copie o token da resposta para `sso_token_prd`/`sso_token_dev` no `.env`.

Para outro serviço, o mesmo fluxo vale trocando o sistema autorizado pelo `sso.application.name` do serviço (fica em `application-<perfil>.properties`).

## Armadilhas

- **User-Agent preso ao token:** o `contabilizei-sso-client` (`AbstractUserServiceFacadeV2.getUser`) só aceita o token se o header `User-Agent` da chamada for idêntico ao usado na criação. Na collection, o `User-Agent` fixo do `collection.bru` precisa ser igual ao `userAgent` do body de `auth/gerar token sso`. Token copiado do navegador (cookie `oauth-token-admin` do admin) só funciona com o User-Agent do próprio navegador (`navigator.userAgent`).
- **Sistema autorizado:** token gerado para outros sistemas (plataforma, abertura, contabilizeiapp, como os que estão nos `.env` de outras collections do experts-bruno) dá 401 no impostos, mesmo válido.
- **dev ≠ prd:** token de produção não vale em homologação e vice-versa (SSOs diferentes). Em dev, se der 401 com token novo, testar o sistema `contabilizei-impostos-dev` (não está confirmado qual perfil roda no projeto `-teste`).

## Erros

- **Login com Google no SSO de teste não abre nada e o navegador mostra 401 em `/rest/usuario/autorizacoes`:** `oauth-token-admin` antigo no navegador (o log do SSO mostra `Token nao encontrado`). Limpar os cookies de `contabilizei-sso-teste.appspot.com` (ou usar janela anônima) e logar de novo.
- **400 `Sistema <nome> nao cadastrado`** no `autorizarSistemaExterno`: o sistema pedido em `sistemasAutorizados` não existe naquele SSO (ex: `contabilizeiapp` no SSO de teste). Tirar da lista.

- **401 `Token nao possui acesso ao sistema: <appId>`** (aparece no log do serviço, não na resposta): o token não tem o sistema do serviço em `sistemasAutorizados`. O `appId` é o `sso.application.name`/`monolito.sso.app.id` do ambiente (ex: `monolito-dev-03`); gerar o token de novo incluindo-o. Para descobrir, ler o log do App Engine do projeto com `gcloud logging read 'textPayload:"Token nao"' --project <projeto>`.

- **401 `{"status": 401, "message": "Nao autorizado"}`:** chegou na aplicação; token expirado, de outro sistema ou User-Agent diferente.
- **403 em HTML (`Error: Forbidden`):** firewall do App Engine bloqueando o IP, antes da aplicação. Liberar em `https://libera-meu-ip.ctbz.com.br/` (em dev, o projeto `contabilizei-impostos-teste`; a lista de PROD não inclui os projetos `-teste`). A VPN não resolve: o tráfego para `*.appspot.com` não passa por ela. A máquina pode sair por **IPv6** (Node/curl preferem IPv6), então o IP a liberar é o que de fato faz a chamada (`curl -s -o /dev/null -w "%{remote_ip}" <url>` mostra a família usada).

## Coleção contabilizeiapp (plataforma/monolito)

A coleção `~/repositories/experts-bruno/contabilizeiapp` lê o token de `.env` (`sso_token_prod`, `sso_token_dev`). Em 2026-10-27, prd funcionou com token atualizado e o `User-Agent` fixo da coleção `contabilizei-sso`. Em dev, o 401 vem de `Token nao possui acesso ao sistema: monolito-dev-03`: o token precisa ser gerado no SSO de teste com o `appId` do ambiente (`monolito-dev-0N`) em `sistemasAutorizados`. Validado em 2026-10-27: com `sistemasAutorizados: ["monolito-dev-03", "plataforma"]` (o sistema `contabilizeiapp` não existe no SSO de teste) e o `User-Agent` do navegador, o dev-03 respondeu 200. Rotas, tabela de `appId` e passo a passo em [[rotas-busca-empresa]].
