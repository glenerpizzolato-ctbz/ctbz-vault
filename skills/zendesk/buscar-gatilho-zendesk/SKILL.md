---
name: buscar-gatilho-zendesk
description: Mostra os detalhes de um gatilho (trigger) do Zendesk - título, situação, categoria, posição, condições (todas/qualquer) e ações em forma legível, com os ids de grupos, usuários, campos de ticket, formulários, marcas, webhooks e alvos traduzidos em nome - a partir do id, do link do admin ou de um trecho do nome. Somente leitura, pela API REST com as credenciais da coleção Bruno `~/repositories/experts-bruno/zendesk-api`; sandbox por padrão, produção só com aprovação explícita do usuário. Use quando o usuário pedir para ver/explicar/listar um gatilho do Zendesk (ex: "o que faz o gatilho 5138317000988", um link `.../admin/objects-rules/rules/triggers/<id>`, "quais gatilhos falam de ouvidoria").
argument-hint: "<id, link ou nome do gatilho> [env: sandbox|prod]"
---

# Buscar gatilho do Zendesk

Resolve um gatilho por id, link do admin (`https://<subdominio>.zendesk.com/admin/objects-rules/rules/triggers/<id>`) ou trecho do título, e imprime as condições e ações já traduzidas (ex: `group_id is 15262373080476` vira `Grupo is Default Ultimate Bot - [Chat][WhatsApp] [BP] (15262373080476)`, `custom_fields_<id>` vira o título do campo e o nome da opção, `notification_webhook` vira nome + método + endpoint do webhook e o corpo).

- **Credenciais:** `user_email` + `personal_user_token_sandbox` ou `personal_user_token_prod` do `.env` da coleção Bruno `~/repositories/experts-bruno/zendesk-api` (auth basic `email/token`). Nunca exibir os valores. Ler gatilhos exige token de um usuário admin.
- **Rotas (as da coleção, pasta `Support API/triggers`):** `GET /api/v2/triggers/{id}`, `GET /api/v2/triggers/search?query=` (busca por nome), `GET /api/v2/trigger_categories/{id}` e, para traduzir ids, `groups`, `users`, `ticket_fields`, `ticket_forms`, `brands`, `organizations`, `webhooks`, `targets`. Só `GET`.

> [!WARNING]
> **Produção:** existe a política de que IA não deve chamar a API de produção do Zendesk (ver `~/ctbz-vault/obsidian/apis/zendesk-sunco-prod-politica.md`). Por isso o padrão é o sandbox e o script recusa `--env prod` sem `--i-confirm-prod`. Antes de usar prod, perguntar ao usuário e só seguir com o "sim" dele **naquela conversa**. Sem aprovação, a alternativa é o usuário abrir o link e colar o gatilho (ou exportar o JSON pelo admin).

## Passo a passo

1. Por id ou link (aceita vários):

    ```bash
    python3 ~/.claude/skills/buscar-gatilho-zendesk/scripts/buscar_gatilho.py 5138317000988
    python3 ~/.claude/skills/buscar-gatilho-zendesk/scripts/buscar_gatilho.py https://contabilizei.zendesk.com/admin/objects-rules/rules/triggers/5138317000988
    ```

2. Por nome (trecho do título, sem diferenciar maiúsculas):

    ```bash
    python3 ~/.claude/skills/buscar-gatilho-zendesk/scripts/buscar_gatilho.py --name "ouvidoria"
    ```

3. O link de `contabilizei.zendesk.com` é de **prod**: perguntar ao usuário antes e, aprovado, acrescentar `--env prod --i-confirm-prod`. O sandbox é `contabilizei1637606740.zendesk.com` (ids diferentes dos de prod).
4. `--json` imprime o JSON cru do gatilho (para comparar versões ou montar um igual).
5. Responder com um resumo em português do que o gatilho faz (quando dispara e o que muda no ticket), seguido das condições e ações e do link.

## Armadilhas

- HTTP 401/403: token inválido/expirado ou sem permissão de admin. Em 2026-11-11 o `personal_user_token_sandbox` do `.env` da coleção estava dando 401: gerar outro no sandbox (Admin Center → Apps e integrações → API do Zendesk) e atualizar o `.env` (valor no Bitwarden).
- 404 por id: o gatilho não existe naquele ambiente (o id de prod não existe no sandbox e vice-versa) ou foi excluído.
- A busca por nome (`triggers/search`) usa o índice do Zendesk: se não achar por um trecho, tentar uma palavra inteira do título.
- Ids de grupo conhecidos: ver a skill `buscar-grupo-zendesk`.
