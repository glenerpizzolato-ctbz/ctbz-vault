---
name: limpeza-alertas-canais
description: "Limpeza dos alertas ruidosos da Engenharia Canais (out–nov/2026): o que foi ajustado, por quê e como; registro único para acompanhar o que ainda falta"
metadata:
  type: project
tags:
  - incidentes
  - alertas
  - grafana
  - cloud-monitoring
---

# Limpeza de alertas da Engenharia Canais

Os espaços de alerta do time ("Engenharia Canais | Grafana" e "Engenharia Canais | Alertas") recebiam alertas quase todo dia sem problema real. Com isso, o time passava a ignorar o canal, e um incidente de verdade corria o risco de passar despercebido (no IP-4361 a abertura do IP foi manual). A limpeza segue um critério fixo:

1. **Medir antes de mexer:** puxar 30–40 dias da métrica pela API do Cloud Monitoring e o histórico de disparos (Grafana `/api/v1/rules/history`), e separar os problemas reais do padrão normal (rajadas, lotes noturnos).
2. **Alertar sobre sintoma, não sobre volume:** em fila, idade da mensagem mais antiga (`oldest_unacked_message_age`) em vez de backlog; ver [[alertas-pubsub-idade-da-mensagem]].
3. **Sustentar a condição** (`for`/duração) para descartar picos curtos.
4. **Validar com backtest** (a regra nova pega os casos reais e ignora o ruído) e registrar o porquê em nota.
5. **Remover o que duplica** outro aviso.

## Alertas ajustados

| Data | Alerta | Onde | Antes | Depois | Detalhes |
|---|---|---|---|---|---|
| out/2026 | `send_email_unrecorded` (envio recusado ou sem registro) | Cloud Monitoring, `atendimento-canais-prd` (terraform do email-service) | Policy duplicando o card de falha no Google Chat | Removida (work-item #50 do email-service) | [[alertas-de-envio]] |
| 06/11/2026 | Cloud Pub/Sub Subscription - Unacked messages | Cloud Monitoring, `contabilizei-experts-prd` | Média de 2h de `num_undelivered_messages` > 100: 10 incidentes em 30 dias, 6 falso-positivos | Mensagem mais antiga sem ack > 15 min por 10 min: no backtest pega os 4 atrasos reais, ignora as rajadas e acha 2 problemas novos | [[alerta-pubsub-unacked-falso-positivo]] |
| 09/11/2026 | Technical error da Ultimate abrindo IP | Grafana, pasta Experts | Só aviso no chat, por bot (≥10 em 5 min); o IP-4361 foi aberto à mão | 2 regras novas para o JSM Ops (3+ bots com erro, ou soma ≥100 em 5 min), fase 1 sem prioridade até 23/11 | [[proposta-ajuste-alerta-ultimate-ip]] |
| 11/11/2026 | `agregador-conversa-sub • atendimento-zendesk` | Grafana, pasta Experts | Backlog > 200: disparava quase todo dia útil no lote noturno (~23:30, ~2,5 mil mensagens, drena em < 1h) | Mensagem mais antiga sem ack > 45 min por 20 min; achado à parte de mensagem em loop sem ack ([atendimento-zendesk#1](https://gitlab.com/ctbz/atendimento/geral/atendimento-zendesk/-/work_items/1)) | [[alerta-grafana-agregador-conversa]] |

## Pendentes / candidatos

- `UltimateAI - Falha de integração backend por integração (≥10 em 5 min)`: 12 disparos desde 11/10, todos de 10 a 16 erros numa integração. Proposta: `for: 5m` ou limiar maior ([[proposta-ajuste-alerta-ultimate-ip]]).
- `Webhook respondendo erro (≥20 em 10 min)` do `ultimateai-webhook`: dispara quase todo dia entre 20:35 e 21:30. Investigar o padrão antes de mexer.
- Ultimate fase 2 (a partir de 23/11/2026): adicionar `og_priority` às regras novas e pausar a antiga `• OPSGENIE`.
- Agregador de conversa: baixar o limite de 45 min depois de corrigir a mensagem em loop (atendimento-zendesk#1).

## Como alterar regras do Grafana

A conta do Glener é `Viewer` na org, mas tem `alert.rules:write` na pasta Experts. Por isso, a API de provisioning volta 403, e a alteração precisa ser feita pela ruler API (`GET`/`POST /api/ruler/grafana/api/v1/rules/<folderUID>/<grupo>`), reenviando o grupo inteiro com só a regra alterada. Detalhes em [[proposta-ajuste-alerta-ultimate-ip]].
