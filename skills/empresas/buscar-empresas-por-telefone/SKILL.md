---
name: buscar-empresas-por-telefone
description: Lista as empresas (CNPJ e plano) vinculadas a um telefone na plataforma da Contabilizei, pela mesma rota que o bot de WhatsApp (Ultimate) usa, a buscar-por-telefone da plataforma-crm-web via API gateway do atendimento. Separa ativas/rascunho, inativas e qualquer status, e básico/padrão/multibenefícios x experts. Busca as credenciais do gateway sozinha (cloud function zendeskbot-config) e as salva na skill, junto com uma collection Bruno própria das rotas (substitui a glener-funcionando). Funciona em prd e dev. Use quando o usuário pedir as empresas/CNPJs de um telefone (ex: "quais empresas estão no telefone 11 98267-0672", "lista os CNPJs desse número em prd").
argument-hint: "[telefone] [ambiente: prd|dev]"
---

# Buscar empresas por telefone

Chama `POST /atendimento/v2/bots/whatsapp/dados-cliente/buscar-por-telefone` da **plataforma-crm-web** pelo API gateway (Kong) do atendimento, exatamente como o bot de WhatsApp da Ultimate faz no passo de identificação da empresa. Somente leitura.

## Como as credenciais são obtidas

O script não usa token fixo nem a collection do Bruno (que quebra quando alguém mexe nela). Ele repete o que a Ultimate faz a cada conversa:

1. Lê o `AUTH_TOKEN` das variáveis de ambiente da cloud function `zendeskbot-config` (`gcloud functions describe`, projeto `contabilizei-crm` em prd e `contabilizei-crm-dev` em dev). Precisa do `gcloud` logado com acesso a esses projetos.
2. Chama `zendeskbot-config?auth_token=...`, que devolve o host e a `x-api-key` do gateway (`config.app.services.apigateway`).
3. Chama a rota no gateway com `x-api-key`, `x-cloud-trace-context` e `x-atendimento-id` (os dois últimos são obrigatórios no Kong, mas aceitam qualquer valor no formato certo; o script gera).

A URL e a `x-api-key` de cada ambiente ficam salvas em `bruno/.env` dentro da skill (gitignored, `chmod 600`), como `api_gateway_url_<prd|dev>` e `api_gateway_token_<prd|dev>`. O script usa o valor salvo e, se o Kong recusar a chave (401/403 em JSON), busca de novo na `zendeskbot-config` e regrava o `.env` sozinho. Nenhum valor de credencial é impresso. Detalhes em `~/ctbz-vault/obsidian/apis/api-gateway-bots-whatsapp.md`.

## Collection Bruno da skill

A pasta `bruno/` da skill é uma collection Bruno com as três rotas (`plataforma-crm-web/buscar-por-telefone`, `plataforma-crm-web/buscar-por-telefone-e-cnpj`, `atendimento-zendesk/autenticar-basico-padrao`), ambientes `prd` e `dev` e os headers do Kong já preenchidos no `collection.bru`. Ela lê a mesma autenticação salva em `bruno/.env` (`{{process.env.api_gateway_token_<env>}}`), então substitui a pasta `glener-funcionando` (chave fixa) da collection da plataforma-crm-web.

- Para abrir no Bruno: *Open Collection* em `~/ctbz-vault/skills/empresas/buscar-empresas-por-telefone/bruno`, escolher o ambiente e ajustar `telefone`/`cnpj`/`area` nas vars do `collection.bru`.
- Se o `.env` não existir ou o Bruno receber 401/403 em JSON, gerar/renovar a autenticação e reabrir o ambiente no Bruno:

    ```bash
    python3 ~/.claude/skills/buscar-empresas-por-telefone/scripts/bots_api.py credenciais --env todos
    ```

- A chave salva também serve para qualquer outra rota do gateway do atendimento liberada para o grupo dos bots (ex: as collections `ultimate-ai-bots` e `atendimento-zendesk/(kong)` do experts-bruno), copiando `api_gateway_token_<env>` para a variável que elas usam.

## Passo a passo

1. Identificar o telefone e o ambiente. **Se o usuário não informar o telefone, usar o dele: `+555596981032`** (padrão do script quando o telefone é omitido). Identificar também o ambiente (padrão **prd**; dev só se o usuário pedir). O telefone pode vir em qualquer formato (`11982670672`, `+55 11 98267-0672`): o script normaliza para `+55...`.
2. Rodar:

    ```bash
    python3 ~/.claude/skills/buscar-empresas-por-telefone/scripts/bots_api.py telefone [telefone] [--env prd|dev] [--raw]
    ```

3. Mostrar em tabela os CNPJs com `categoriaPlano`, separando ativas/rascunho e inativas. O `--raw` traz o JSON inteiro (com `listasEmpresas` de cada grupo).

O mesmo script tem as rotas de telefone + CNPJ e de autenticação do bot, usadas pela skill `autenticar-empresa-whatsapp`.

## Resposta

`data` tem três grupos, `empresasAtivasOuRascunho`, `empresasInativas` e `empresasQualquerStatus`, cada um com:

- `quantidades`: `basicoPadraoMultibeneficios`, `experts`, `total`.
- `listasCNPJs`: as mesmas três listas, só com os CNPJs.
- `listasEmpresas`: `{cnpj, categoriaPlano}` (ex: `EXPERT_ESSENCIAL`, `BASICO`).

## Armadilhas

- **403 em HTML (`403 Forbidden`)** com credenciais certas: o WAF na frente do gateway barra o User-Agent padrão do Python (`Python-urllib`). O script manda `User-Agent: curl/...`; ao chamar por outro cliente, não usar o User-Agent de biblioteca.
- **400 do Kong (`header-validation`)**: faltou `x-cloud-trace-context` ou `x-atendimento-id`.
- **Telefone sem `+`**: a plataforma exige que comece com `+` (`ObjectValidator.startsWith`).
- **500 em HTML (`Server Error`) em dev**: cold start do App Engine (`Request was aborted after waiting too long` no log do `crm-web` de `contabilizeiapp-dev-03`). Repetir a chamada.
- **`gcloud functions describe` falhou**: `gcloud auth login` vencido ou sem acesso ao projeto `contabilizei-crm(-dev)`.
- São dados reais de clientes (em prd): usar só no contexto do trabalho.
