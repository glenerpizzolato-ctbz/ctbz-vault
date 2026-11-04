---
name: autenticar-empresa-whatsapp
description: Consulta a autenticação de um telefone + CNPJ (ou CPF) no bot de WhatsApp (Ultimate) da Contabilizei, pelas mesmas rotas que o bot usa via API gateway do atendimento - a buscar-por-telefone-e-cnpj da plataforma-crm-web (vínculo do telefone, plano, status, acessos, assessor, dados da empresa) e a autenticacao/basico-padrao do atendimento-zendesk (statusBot, statusAutenticacao, categoriaPlano, fluxos habilitados por área CRM/BANK/EXPERT/ATIVACAO). Busca as credenciais do gateway sozinha (cloud function zendeskbot-config). Use quando o usuário pedir para autenticar/validar um telefone com um CNPJ, ver por que o bot não reconhece ou não libera um cliente, ou conferir o plano/statusBot de uma empresa no bot.
argument-hint: "<telefone> [cnpj-ou-cpf] [area: CRM|BANK|EXPERT|ATIVACAO] [ambiente: prd|dev]"
---

# Autenticar empresa (telefone + CNPJ) no bot de WhatsApp

Duas rotas, ambas somente leitura, chamadas pelo API gateway (Kong) do atendimento como a Ultimate faz:

| Comando | Serviço | Rota | Para quê |
| --- | --- | --- | --- |
| `telefone-cnpj` | plataforma-crm-web | `POST /atendimento/v2/bots/whatsapp/dados-cliente/buscar-por-telefone-e-cnpj` | Dados da empresa logada: telefone vinculado, status, plano, acessos (básico/bank/experts), assessor, telefones cadastrados |
| `autenticar` | atendimento-zendesk | `POST /api/v1/bots/whatsapp/autenticacao/basico-padrao` | Decisão do bot: `statusBot`, `statusAutenticacao`, `status2FA`, `categoriaPlano`, fluxos habilitados |

O script é o mesmo da skill `buscar-empresas-por-telefone`: a `x-api-key` vem da cloud function `zendeskbot-config`, fica salva em `~/.claude/skills/buscar-empresas-por-telefone/bruno/.env` (gitignored) e é renovada sozinha quando o Kong a recusa. As duas rotas também estão na collection Bruno dessa skill (pasta `bruno/`), que usa a mesma autenticação salva. Detalhes em `~/dotfiles/docs/ai/obsidian/ctbz/apis/api-gateway-bots-whatsapp.md`.

## Passo a passo

1. Identificar telefone, CNPJ (ou CPF, no fluxo de ativação), área e ambiente (padrão **prd**). Telefone e documento podem vir formatados: o script normaliza.
2. Para os dados da empresa:

    ```bash
    python3 ~/.claude/skills/buscar-empresas-por-telefone/scripts/bots_api.py telefone-cnpj <telefone> <cnpj> [--env prd|dev] [--raw]
    ```

3. Para a decisão do bot (o que a Ultimate recebe na autenticação):

    ```bash
    python3 ~/.claude/skills/buscar-empresas-por-telefone/scripts/bots_api.py autenticar <telefone> [--cnpj CNPJ | --cpf CPF] [--area CRM|BANK|EXPERT|ATIVACAO] [--env prd|dev] [--raw]
    ```

    `--area` padrão `CRM`. Sem `--cnpj`/`--cpf`, a busca é só pelo telefone (como no início da conversa).
4. Resumir: se o telefone está vinculado, status e plano, e o `statusBot`/fluxos para a área pedida. Quando o usuário quer saber "por que o bot não liberou", usar a regra abaixo.

## Como ler o `autenticar`

Regras completas em `~/dotfiles/docs/ai/obsidian/ctbz/repositories/atendimento-zendesk/categoria-plano-autenticacao-whatsapp.md`. Em resumo:

- `categoriaPlano`: `AVANCADO`, `BASICO`, `EXPERT` (qualquer plano com "EXPERT"), `PREMIUM`, `MULTIBENEFICIOS` ou `NAO_IDENTIFICADO`.
- `statusBot`: `BLOQUEADO` (telefone bloqueado), `SEM_AUTORIZACAO`, `AUTENTICADO`, `AUTENTICADO_VERIFICADO` (2FA ok), `EMPRESA_INATIVA`, `EVENTUAL`, `ONBOARDING`.
- Fluxo `CRM` só para ativo/rascunho com plano `AVANCADO`/`PREMIUM`/`MULTIBENEFICIOS` (`BASICO` só com autopilot ou ramo `COMERCIO`). **Cliente Expert com `--area CRM` sempre volta `SEM_AUTORIZACAO`**: usar `--area EXPERT`.
- 2FA `NAO_VERIFICADO` quando a busca é por CNPJ e o telefone não está vinculado à empresa (`possuiTelefoneVinculadoEmpresa: false` no `telefone-cnpj`).

## Armadilhas

- As mesmas da `buscar-empresas-por-telefone` (403 em HTML pelo User-Agent, headers obrigatórios do Kong, `gcloud` logado).
- **400 `Atributo área inválido`**: `area` fora de `ATIVACAO`, `BANK`, `CRM`, `EXPERT`.
- **400 de CNPJ inválido** no `telefone-cnpj`: a plataforma valida o dígito verificador.
- São dados reais de clientes (em prd), inclusive CPF e e-mail de sócios: mostrar só o necessário para a pergunta.
