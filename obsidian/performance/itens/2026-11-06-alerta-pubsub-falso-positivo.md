---
name: 2026-11-06-alerta-pubsub-falso-positivo
description: "Fim do falso-positivo recorrente do alerta de Pub/Sub do experts-prd: troca de volume médio por idade da mensagem, calibrada com backtest de 30 dias"
metadata:
  type: project
tags:
  - performance
titulo: "Alerta de Pub/Sub do experts-prd sem falso-positivo (idade da mensagem no lugar de volume)"
data: 2026-11-06
periodo: 2026QD3
categorias: [qualidade]
impacto: medio
fontes: ["[[alerta-pubsub-unacked-falso-positivo]]"]
---

# Alerta de Pub/Sub do experts-prd sem falso-positivo

## Contexto

O alerta "Cloud Pub/Sub Subscription - Unacked messages" do Cloud Monitoring (`contabilizei-experts-prd`) disparava quase todo dia no espaço Engenharia Canais | Alertas por causa das rajadas do `processar-guia-imposto`, que o consumidor drena em menos de 5 min. A investigação automática ainda leu o valor como 116 mil mensagens, quando eram 116,7.

## O que fiz

- Identifiquei a causa: a condição usava a média de 2h de `num_undelivered_messages` com limiar 100, e o valor aparece com 3 casas decimais.
- Levantei 30 dias das 64 assinaturas do projeto e separei os atrasos reais das rajadas.
- Troquei a condição para "mensagem mais antiga sem ack > 15 min por 10 min" e validei com backtest antes de aplicar.

## Resultado

- A regra antiga abriu 10 incidentes em 30 dias, e 6 deles eram falso-positivo. No backtest, a regra nova dispara nos 4 atrasos reais do guia-imposto e em nenhuma das rajadas.
- Ela passou a pegar 2 problemas que a antiga não via: mensagens presas por 4 dias no `plataforma-alteracao-plano` e um atraso de 29 min no `relatorio-faturamento`.

## Evidências

- [[alerta-pubsub-unacked-falso-positivo]]
- Policy `projects/contabilizei-experts-prd/alertPolicies/8855052505336933525`, alterada em 2026-11-06.
