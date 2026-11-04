---
name: fechar-tickets-teste-zendesk
description: "Como fechar os tickets que os testes dos bots de WhatsApp em prd deixam abertos no Zendesk (skill fechar-tickets-teste-zendesk)"
metadata:
  type: reference
tags:
  - tests
  - zendesk
dominio:
  - atendimento
  - ultimate
repositorios:
  - experts-bruno
  - dotfiles
ambiente: prd
atualizado_em: 2026-10-26
---

# Fechar os tickets de teste no Zendesk (prd)

Testar os bots de WhatsApp em produção (Ultimate, clientes inativos etc.) abre tickets reais no Zendesk, que ficam nas filas dos times. Os tickets saem em nome do usuário de teste do Glener: end-user "Glener", id `21878313229212`, o telefone de teste ([tickets dele](https://contabilizei.zendesk.com/agent/users/21878313229212/requested_tickets)). Depois de cada rodada de testes, fechar os que ficaram abertos.

- **Skill:** `fechar-tickets-teste-zendesk`, versionada em `~/dotfiles/docs/ai/skills/ctbz/zendesk/fechar-tickets-teste-zendesk/`. Basta pedir ao Claude Code "fecha meus tickets de teste no Zendesk".
- **Script direto:** `python3 ~/.claude/skills/fechar-tickets-teste-zendesk/scripts/fechar_tickets.py list | close [--dry-run]`.
- **Escopo:** só atua nesse requester e confere o `requester_id` de cada ticket antes de fechar. `closed` é definitivo: o ticket não pode ser reaberto.
- **Credenciais:** `user_email` e `personal_user_token_prod` do `.env` da coleção Bruno `~/repositories/experts-bruno/zendesk-api`, com auth basic `email/token`.
- **Rotas:** `GET /api/v2/users/{id}/tickets/requested` (paginada, 100 por página) e `PUT /api/v2/tickets/update_many.json` com `status: closed`. A segunda é assíncrona e devolve um `job_status`, que precisa ser acompanhado.

Usado depois dos testes de [[clientes-inativos-cnpjs-teste]].
