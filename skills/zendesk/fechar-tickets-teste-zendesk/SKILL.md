---
name: fechar-tickets-teste-zendesk
description: Fecha (status closed) os tickets abertos no Zendesk de produção que foram abertos pelo usuário de teste do Glener (end-user 21878313229212, o telefone usado para testar os bots de WhatsApp/Ultimate). Use quando o usuário pedir para fechar/finalizar/limpar os atendimentos ou tickets de teste dele em prd. Só atua nesse requester; nunca em tickets de outros usuários.
---

# Fechar os tickets de teste no Zendesk (prd)

Os testes dos bots de WhatsApp em produção (Ultimate, clientes inativos etc.) abrem tickets reais no Zendesk em nome do usuário de teste do Glener, que ficam abertos nas filas dos times. Esta skill lista os tickets desse usuário que não estão `solved`/`closed` e os fecha.

- **Requester fixo:** `21878313229212` (end-user "Glener", tickets em https://contabilizei.zendesk.com/agent/users/21878313229212/requested_tickets). O script não aceita outro usuário e confere o `requester_id` de cada ticket antes de fechar. Se o usuário pedir para fechar tickets de outra pessoa, recusar e explicar que a skill é só para os tickets de teste dele.
- **Credenciais:** `user_email` e `personal_user_token_prod` do `.env` da coleção Bruno `~/repositories/experts-bruno/zendesk-api` (a mesma auth basic `email/token` da coleção). Nunca exibir os valores. Se faltar o `.env`, pedir para o usuário criá-lo a partir do Bitwarden.
- **Rotas (as mesmas da coleção):** `GET /api/v2/users/{id}/tickets/requested` (paginado) e `PUT /api/v2/tickets/update_many.json` com `status: closed` (assíncrono, o script acompanha o `job_status`).

## Passo a passo

1. Listar os abertos:

    ```bash
    python3 ~/.claude/skills/fechar-tickets-teste-zendesk/scripts/fechar_tickets.py list
    ```

2. Mostrar a lista ao usuário (id, status, data, assunto, link). Se a lista estiver vazia, avisar e parar.
3. Fechar. Invocar a skill já é a autorização para fechar todos os da lista; se o usuário pediu para fechar só alguns ou só ver, parar no passo 2.

    ```bash
    python3 ~/.claude/skills/fechar-tickets-teste-zendesk/scripts/fechar_tickets.py close
    ```

4. Reportar quantos foram fechados e os que deram erro (o `job_status` traz o motivo). Rodar `list` de novo para confirmar que não sobrou nenhum.

## Armadilhas

- Fechar com `closed` é definitivo: o ticket não pode ser reaberto (um novo contato abre outro ticket). Por isso o filtro rígido de requester.
- O `update_many` processa até 100 tickets por chamada; o script divide em lotes.
- Ticket de outro canal (ex: ligação) aberto pelo mesmo usuário também entra, já que o filtro é só o requester.
- Ticket de messaging (WhatsApp) com a conversa ainda ativa no bot (status `new`, sem grupo/assignee, audit com `ChatStartedEvent` do backend `ocb`) não muda de status pela API: o `update_many` volta `TicketNotFound` e o `PUT /tickets/{id}` responde 200 mas ignora o status (nem gera audit), mesmo atribuindo o ticket. Só dá para fechar depois que a conversa acaba (timeout de sessão do messaging, ou o bot transfere/encerra); até lá, rodar de novo mais tarde (visto em 2026-11-13, ticket 30314078).
