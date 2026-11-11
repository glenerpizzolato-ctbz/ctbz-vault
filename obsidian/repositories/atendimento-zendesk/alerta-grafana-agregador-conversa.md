---
name: alerta-grafana-agregador-conversa
description: "Alerta do Grafana 'agregador-conversa-sub • atendimento-zendesk': subscription que ele mede, lote noturno, mensagem em loop sem ack e troca de backlog > 200 para idade da mensagem > 45 min (11/11/2026)"
metadata:
  type: reference
tags:
  - atendimento-zendesk
  - monitoria-ia
  - grafana
  - alertas
---

# Alerta Grafana do agregador de conversa (entrada da monitoria-ia)

O alerta "agregador-conversa-sub • atendimento-zendesk" ("Backlog count too high"), que chega no espaço do Google Chat "Engenharia Canais | Grafana", é uma **regra do Grafana** (não do Cloud Monitoring do GCP).

- Regra: https://grafana.ctbz.com.br/alerting/grafana/fej3urtlra3nka/view (pasta `Experts`, grupo `Experts (every 10m)`).
- Labels: `Contact=Goole Chat`, `Resource=pubsub`, `Team=Canais` (é por elas que a notification policy roteia para o chat).
- Query (datasource GCP Stackdriver, projeto `contabilizei-monitoramento`): `num_undelivered_messages` da subscription `zendesk-webhooks-tickets-atendimento-zendesk-agregador-conversa-sub` (projeto `contabilizei-crm`, tópico `zendesk-webhooks-tickets`), dispara acima de 200.

Fluxo: o consumer `AgregadorConversaConsumer` do `atendimento-zendesk` (`src/app/worker/worker-experts/consumers/agregador-conversa/`) lê essa subscription e publica a conversa agregada em `atendimento-zendesk-full-conversation`, que tem dois assinantes: `monitoria-ia-parser.sub.zendesk-full-conversation` (aida-prd, monitoria-ia) e `atendimento-zendesk-full-conversation-resumo-atendimento-sub` (resumo de atendimento do próprio atendimento-zendesk). Ou seja, o agregador não serve só à monitoria-ia.

As políticas `[AIDA] Cloud Pub/Sub ...` do Cloud Monitoring do `aida-prd` excluem subscriptions com "monitoria" no nome; não são elas que geram esse alerta.

## De quem é o alerta

A subscription e o consumer são do **atendimento-zendesk**, não do repositório monitoria-ia. O agregador foi criado em 22/05/2025 (commits `430f0928c` e `ca7f11dc1`) para alimentar a monitoria-ia. O resumo de atendimento (consumer de 04/2025) também lê `atendimento-zendesk-full-conversation` e está ativo: foram 738 acks em 6h, medidos em 11/11/2026. Por isso, migrar a monitoria-ia para outro time não torna o alerta desnecessário: sem ele, ninguém percebe se o resumo de atendimento parar.

## Armadilha: duas subscriptions com nome parecido

No `contabilizei-crm` existem duas subscriptions do agregador, e só uma delas é a do alerta:

- `zendesk-webhooks-tickets-atendimento-zendesk-agregador-conversa-sub` (tópico `zendesk-webhooks-tickets`) é a do alerta. Tem tráfego alto (~275–380 mil acks/dia em dias úteis) e picos de backlog de 2,5–4 mil por dia.
- `atendimento-zendesk-agregador-conversa-sub` (tópico `atendimento-zendesk-agregador-conversa`) é a do reprocessamento em lote (`AgregadorConversaLoteUsecase`, rota `atendimento/zendesk/agregador-conversa`). Fica sem eventos na maior parte do tempo.

Números medidos em 11/11/2026, últimos 7 dias.

## Padrão do backlog (medido em 11/11/2026, últimas 48h, horário de Brasília)

- Durante o dia o backlog fica em 5–100 mensagens, com ~12–14 mil acks a cada 30 min.
- Todo dia entre ~23:30 e ~00:30 chega um lote noturno (~6–7 mil eventos em 30 min). O backlog sobe para ~2,5 mil e a mensagem mais antiga chega a ~28 min, mas tudo é drenado em menos de 1h. Os disparos das 23:47 e das 01:47 são esse lote, não uma falha.
- A `oldest_unacked_message_age` fica parada em ~550–600 s o dia todo, igual ao `ackDeadlineSeconds` (600). Indício de que sempre há mensagem sendo puxada e não confirmada, voltando só quando vence o prazo (erro/nack ou ack perdido). Ainda não investigado.

## Alterado em 11/11/2026

- Regra trocada de "backlog (`num_undelivered_messages`, média) > 200" para "**mensagem mais antiga sem ack (`oldest_unacked_message_age`, máx.) > 2700 s (45 min)**", com pending (`for`) de 10m para **20m**. O summary também foi trocado para explicar o lote noturno. Mesmos labels e contato.
- Feito pela ruler API (`POST /api/ruler/grafana/api/v1/rules/<folderUID>` com o grupo `Experts (every 10m)` inteiro, que também tem a regra `Agents • Latência Média de Resposta` reenviada sem mudança). A API de provisioning (`PUT /api/v1/provisioning/alert-rules/<uid>`) volta 403 para a conta do Glener (falta `alert.provisioning:write`).
- Logo depois da mudança: valor 222 s, estado Normal.
- O limite ficou bem acima dos ~600 s de base por causa da mensagem que fica em loop sem ack. Investigação no work-item [atendimento-zendesk#1](https://gitlab.com/ctbz/atendimento/geral/atendimento-zendesk/-/work_items/1). Depois da correção, dá para baixar o limite.
- Faz parte da [[limpeza-alertas-canais|limpeza de alertas de Canais]].
