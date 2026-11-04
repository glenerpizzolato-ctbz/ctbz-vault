---
name: rotas-busca-empresa-plataforma-monolito
description: "Rotas do plataforma-monolito para buscar empresas (por CNPJ e listagem por status/ramo com plano no retorno), autenticação por token do SSO e como chamar pela coleção contabilizeiapp do experts-bruno"
metadata:
  type: reference
tags:
  - plataforma-monolito
  - empresa
  - api
atualizado_em: 2026-10-27
---

# Rotas de busca de empresa (plataforma-monolito)

Rotas REST do monolito (App Engine, `contabilizeiapp`) que devolvem a empresa completa, incluindo o plano em `planoPagamentoEmpresa.pagtoPlano` (`categoria` e `categoriaV2.nome`: `BASICO`, `AVANCADO`, `PREMIUM`, `MULTIBENEFICIOS`, `EXPERT_ESSENCIAL`, `EXPERT_PRO`). Ao contrário do BigQuery ([[status-empresa-bigquery]]), é o dado em tempo real.

| Rota | Código | O que faz |
|---|---|---|
| `GET /rest/empresa/auth/getByCnpj?cnpj=<cnpj>&auth_token=<token>` | `EmpresaJersey.java` | Empresa completa por CNPJ |
| `GET /rest/empresa/auth/filtrarempresas?status=ATIVO&limite=<n>&cursor=<offset>&auth_token=<token>` | `EmpresaJersey.java:318` | Lista paginada filtrando só por `status`, `ramoAtividade` e `franquia`; **não filtra por plano** (filtrar do lado do cliente) |
| `GET /rest/empresa/filtrar` | `EmpresaJersey.java:291` | Mesma listagem com mais filtros (regime, UF, cidade etc.), mas `@AcessoRestrito` (sessão do admin) |

Resposta do `filtrarempresas`: `{serializedList, list, total, cursor}`. As empresas vêm em `serializedList`, uma **string JSON** que precisa de um segundo parse (`list` volta vazio). `cursor` é o offset numérico da paginação; `total` é o total do filtro (58.621 ativas em prd em 2026-10-27).

## Como chamar

Coleção Bruno `~/repositories/experts-bruno/contabilizeiapp` (pasta `pltf-monolito/Empresa`), token do SSO em `.env` (`sso_token_prod`, `sso_token_dev`), referenciado nos ambientes como `{{process.env.sso_token_prod}}`. Passo a passo do token (dev e prd) em [[colecao-contabilizeiapp]]; contexto do SSO em [[sso-token-dev-prd]].

- **Prd** (`https://contabilizeiapp.appspot.com`): funcionando em 2026-10-27 com token atualizado em `sso_token_prod` e o `User-Agent` fixo da coleção `contabilizei-sso` (`Mozilla/5.0 (X11; Linux x86_64) … Chrome/133.0.0.0 Safari/537.36`).
- **Dev** (`https://contabilizeiapp-dev-0N.appspot.com`): **funcionando no dev-03 desde 2026-10-27** com token gerado no SSO de teste para `monolito-dev-03` (passo a passo abaixo). Precisa de IP liberado no `libera-meu-ip` (sem isso, 403 em HTML) **e** de um token gerado no SSO de teste com o sistema do ambiente em `sistemasAutorizados`. Com o token da coleção (sistemas `plataforma`, `abertura`, `plataforma-crm-web`, `contabilizeiapp`), o dev-03 responde **401**.

## Por que o dev dá 401 (investigado em 2026-10-27)

O filtro do `contabilizei-sso-client` (`AppSSOAuthFilter` → `AppSSOService.verificarTokenSistemaExternoAutorizado`) chama o SSO do ambiente (`loginApi/v1/verificarSistemaExternoAutorizado`) e exige que o token tenha acesso ao `monolito.sso.app.id` daquele ambiente. O log do App Engine (`gcloud logging read ... --project contabilizeiapp-dev-03`) mostra:

```
POST https://contabilizei-sso-teste.appspot.com/_ah/api/loginApi/v1/verificarSistemaExternoAutorizado → 401
"Token nao possui acesso ao sistema: monolito-dev-03"
```

O `appId` de cada ambiente fica em `src/main/resources/filtered/parametro.<ambiente>.properties` (`monolito.sso.app.id`):

| Ambiente | Projeto | SSO | `appId` (sistema a autorizar) |
|---|---|---|---|
| prd | `contabilizeiapp` | `contabilizei-sso.appspot.com` | `monolito` |
| stg/homolog | — | `contabilizei-sso-teste.appspot.com` | `monolito-stg` |
| dev-01 … dev-06 | `contabilizeiapp-dev-0N` | `contabilizei-sso-teste.appspot.com` | `monolito-dev-0N` |

**Correção (validada em 2026-10-27 no dev-03):**

1. Logar em `https://contabilizei-sso-teste.appspot.com/sistema-admin/`. Se o botão do Google não abrir nada e aparecerem 401 em `/rest/usuario/autorizacoes`, é um `oauth-token-admin` antigo no navegador: limpar os cookies do domínio (ou usar janela anônima) e logar de novo.
2. Copiar o valor do cookie `oauth-token-admin` (Application → Cookies) para `sso_cookie_dev` no `.env` da coleção `contabilizeiapp`, e anotar o `navigator.userAgent` do navegador (a sessão do SSO é presa a ele).
3. `POST https://contabilizei-sso-teste.appspot.com/_ah/api/usuarioApi/v1/autorizarSistemaExterno` com header `Cookie: oauth-token-admin=<valor>`, `User-Agent: <navigator.userAgent>` e body `{"nomeSistema": "Experts-Bruno", "sistemasAutorizados": ["monolito-dev-03", "plataforma"], "userAgent": "<navigator.userAgent>"}`. **`contabilizeiapp` não existe no SSO de teste** (400 `Sistema contabilizeiapp nao cadastrado`), então não incluir.
4. Gravar o `token` da resposta em `sso_token_dev` e chamar o dev-03 com o **mesmo `User-Agent`** do navegador.

Referência anterior: gerar o token no SSO de **teste** (`POST https://contabilizei-sso-teste.appspot.com/_ah/api/usuarioApi/v1/autorizarSistemaExterno`, com o cookie da sessão logada em `https://contabilizei-sso-teste.appspot.com/sistema-admin/`) incluindo o sistema do ambiente, ex: `"sistemasAutorizados": ["monolito-dev-03", "plataforma", "contabilizeiapp"]`, e o mesmo `userAgent` que vai no header das chamadas. A request `contabilizei-sso/criar token` do experts-bruno tem a URL de **prod** fixa e não inclui os `monolito-*`, então não serve para dev sem ajuste. Também aparece no log o aviso `ACESSO DE API DESCONTINUADA - MIGRE PARA O MODULO CORRETO` para `/rest/empresa/...` no módulo default (não bloqueia).

## Armadilha: listagem em dev quebra por dado inválido

Em dev, `auth/filtrarempresas` devolve **400** com texto `Error loading Empresa(<id>): No enum constant br.com.contabilizei.enumeration.MotivoStatusEmpresa.Alteração manual para rascunho` quando a página contém uma empresa com `motivoStatus` fora do enum. A página inteira falha. Contorno: paginar com `limite` maior e, na página que der 400, buscar item a item (`limite=1`, `cursor=offset+i`) pulando os que falham. Em 2026-10-27, ~7% dos registros varridos no dev-03 falhavam assim (78 de 1.150), com 21.236 empresas ativas no total. A ordem da listagem parece ser alfabética por razão social, e empresas Expert são raras em dev (3 a cada ~1.150 ativas).

**Limite de paginação:** o `cursor` (offset) só aceita valores de 0 a 1000 (400 `The offset <n> must be between 0 and 1000`, limite do Datastore). Com a ordem alfabética, a listagem só alcança as ~1.050 primeiras empresas de cada filtro, então **não dá para varrer a base inteira** por essa rota. Para cobrir mais, particionar pelos filtros que a rota aceita (`status`, `ramoAtividade`, `franquia`), ainda limitado a ~1.050 por partição. Em 2026-10-27, a varredura do dev-03 achou só 3 empresas Expert nessa janela.
