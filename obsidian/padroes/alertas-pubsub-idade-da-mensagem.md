---
name: alertas-pubsub-idade-da-mensagem
description: "Padrão de alerta para fila Pub/Sub: idade da mensagem mais antiga sem ack, sustentada, em vez de quantidade de mensagens; como calibrar o limite"
metadata:
  type: reference
tags:
  - padroes
  - alertas
  - pubsub
---

# Alerta de Pub/Sub: idade da mensagem, não volume

O que importa numa fila é se a mensagem demora a ser processada, não quantas estão esperando. Rajadas e lotes (ex: o lote noturno dos webhooks do Zendesk, a rajada do `processar-guia-imposto`) enchem a fila e drenam em minutos. Alerta por `num_undelivered_messages` dispara nesses casos e vira ruído.

- **Métrica:** `pubsub.googleapis.com/subscription/oldest_unacked_message_age` (segundos), agregada com `max`.
- **Limite:** acima do maior atraso normal medido em 30 dias (incluindo os lotes), com folga. Exemplos: 15 min no experts-prd e 45 min no agregador de conversa.
- **Sustentação:** `for`/duração de 10–20 min, para descartar picos.
- **Armadilha:** se a idade fica parada perto do `ackDeadlineSeconds` da subscription o dia todo, há mensagem em loop sem ack (erro, nack ou lease perdida). O limite precisa ficar acima disso até a causa ser corrigida, e vale pôr dead-letter com `maxDeliveryAttempts`.
- **Opcional:** manter um alerta de volume com limite bem alto, como reforço para picos fora do comum.

Casos: [[alerta-pubsub-unacked-falso-positivo]], [[alerta-grafana-agregador-conversa]]. Contexto geral: [[limpeza-alertas-canais]].
