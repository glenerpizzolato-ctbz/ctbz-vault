---
name: zendesk-tickets-bigquery
description: "Onde ler tickets do Zendesk de prod pelo BigQuery, sem chamar a API: eventos (audits com tags e EscalationEvent) em sbox_bi_atendimento_zendesk.raw_tb_ticket_events, atualizados até D-1; comentários e Fivetran estão parados"
metadata:
  type: reference
tags:
  - db
  - bigquery
  - zendesk
---

# Tickets do Zendesk (prod) pelo BigQuery

Como IA não deve chamar a API de prod do Zendesk/Sunshine (ver [[zendesk-sunco-prod-politica]]), o BigQuery é o caminho para ler o histórico de um ticket.

- `contabilizei-dataflow.sbox_bi_atendimento_zendesk.raw_tb_ticket_events`: os audits do ticket, particionados por `created_at_date` e atualizados até D-1 (conferido em 2026-11-11, com dados até 10/11). O `child_event` é uma **string JSON** com a lista de eventos do audit: `Create` (com `added_tags` da criação e o `subject`, ex: `Conversation with Web User <sunshineUserId>`), `Change` (tags, grupo, campos), `Comment` (só a flag, sem o texto) e `EscalationEvent` (`escalation_type: ai_agent` = handoff da Ultimate). O `control_context` do `ChatStartedEvent` **não** vem nessa tabela.
- `raw_tb_ticket_comments` / `trusted_tb_ticket_comments`: texto dos comentários, mas **parados em 2026-02-11**.
- `dw_fivetran_zendesk_support.*`: parado em 2020, não usar.
- `dw_atendimento_zendesk.eventos`: telemetria nossa (desconexão etc.), não traz navegação do widget.
- O dataset `contabilizei-dataflow.mixpanel` é legado (2021–2022): os eventos atuais do widget não estão no BigQuery.

Exemplo:

```sql
SELECT ticket_id, created_at, child_event
FROM `contabilizei-dataflow.sbox_bi_atendimento_zendesk.raw_tb_ticket_events`
WHERE created_at_date BETWEEN "2026-11-01" AND "2026-11-10" AND ticket_id IN (30176681)
ORDER BY created_at
```

Canal do ticket: o `via` do evento `Create` dentro do `child_event` separa os canais. Chat web = `Native Messaging`; WhatsApp = `WhatsApp`; API = `Web service`; follow-up = `Closed Ticket`. Para extrair, `UNNEST(JSON_QUERY_ARRAY(child_event))` e `JSON_VALUE(ce,'$.via')` / `JSON_VALUE_ARRAY(ce,'$.added_tags')`. O `via_reference_id` de um `Change` com `via: Rule` é o id do gatilho que o fez.

Caso de uso: [[PRD-176094 - Ticket de chat web cai na Ouvidoria sem o cliente pedir]].
