---
name: buscar-grupo-zendesk
description: Descobre o nome (e descrição, situação e membros) de um grupo do Zendesk de produção a partir do id, ou acha o id de um grupo pelo nome, pela API REST com as credenciais da coleção Bruno `~/repositories/experts-bruno/zendesk-api`. Somente leitura. Use quando o usuário perguntar qual é o grupo de um id do Zendesk (ex: "qual o nome do grupo 15262373080476"), quais agentes estão num grupo, ou qual o id de um grupo pelo nome.
argument-hint: "<id ou nome do grupo> [membros: sim|nao]"
---

# Buscar grupo do Zendesk (prd)

Os ids de grupo aparecem em tickets (`group_id`), triggers, logs dos bots e configs de roteamento, mas não dizem qual é o grupo. Esta skill resolve id → nome (e o inverso) direto no Zendesk de produção (`contabilizei.zendesk.com`).

- **Credenciais:** `user_email` e `personal_user_token_prod` do `.env` da coleção Bruno `~/repositories/experts-bruno/zendesk-api` (auth basic `email/token`, a mesma da coleção). Nunca exibir os valores. Se faltar o `.env`, pedir para o usuário criá-lo a partir do Bitwarden.
- **Rotas (as mesmas da coleção, pasta `Support API/groups`):** `GET /api/v2/groups/{id}` (request `fetch`), `GET /api/v2/groups` (request `groups/list`, paginado, para a busca por nome) e `GET /api/v2/groups/{id}/users` (membros).
- Somente leitura: o script só faz `GET`.

## Passo a passo

1. Por id (aceita vários):

    ```bash
    python3 ~/.claude/skills/buscar-grupo-zendesk/scripts/buscar_grupo.py 15262373080476
    ```

2. Por nome (trecho, sem diferenciar maiúsculas):

    ```bash
    python3 ~/.claude/skills/buscar-grupo-zendesk/scripts/buscar_grupo.py --name "ultimate bot"
    ```

3. Se o usuário quiser os agentes do grupo, acrescentar `--members`.
4. Responder com o id, o nome, se está excluído e o link do grupo no admin.

## Armadilhas

- 404 no `GET /groups/{id}` quer dizer que o id não existe em prd (pode ser do sandbox, ambiente `sandbox` da coleção, ou de outro objeto, como organização ou usuário).
- Grupo excluído ainda volta no fetch por id, com `deleted: true` (o script marca "EXCLUÍDO").
- Ids conhecidos: `15262373080476` = `Default Ultimate Bot - [Chat][WhatsApp] [BP]` (grupo do bot da Ultimate no chat/WhatsApp, criado em 2024-08-05).
