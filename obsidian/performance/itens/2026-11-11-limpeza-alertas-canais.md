---
name: 2026-11-11-limpeza-alertas-canais
description: "Limpeza dos alertas ruidosos da Engenharia Canais (out–nov/2026): critério baseado em dados, quatro alertas ajustados ou removidos, padrão documentado para o time e achados novos (mensagem em loop sem ack)"
metadata:
  type: project
tags:
  - performance
titulo: "Limpeza dos alertas ruidosos da Engenharia Canais"
data: 2026-11-11
periodo: 2026QD3
categorias: [qualidade, processo, incidente]
impacto: alto
fontes: ["[[limpeza-alertas-canais]]", "[[alerta-pubsub-unacked-falso-positivo]]", "[[proposta-ajuste-alerta-ultimate-ip]]", "[[alerta-grafana-agregador-conversa]]", "[[alertas-pubsub-idade-da-mensagem]]"]
atualizado_em: 2026-11-11
---

# Limpeza dos alertas ruidosos da Engenharia Canais

## Contexto

Os espaços de alerta do time recebiam disparos quase todo dia sem problema real (rajadas de fila, lotes noturnos, alertas duplicados). O canal perdia credibilidade, e um incidente real (IP-4361, queda dos AI Agents da Zendesk em 03/11/2026) teve o IP aberto à mão, 40 minutos depois do início.

## O que fiz

- Defini um critério para revisar cada alerta: medir 30–40 dias da métrica e do histórico de disparos, separar problema real de padrão normal, alertar sobre sintoma (atraso) e não volume, sustentar a condição e validar com backtest antes de aplicar.
- Ajustei ou removi quatro alertas:
  - out/2026: removi a policy duplicada `send_email_unrecorded` do email-service.
  - 06/11: troquei o alerta de Pub/Sub do `contabilizei-experts-prd` por idade da mensagem.
  - 09/11: criei as regras de abertura automática de IP para a Ultimate.
  - 11/11: troquei o alerta do agregador de conversa do atendimento-zendesk de backlog para idade da mensagem.
- Documentei o padrão para o time ([[alertas-pubsub-idade-da-mensagem]]), o registro da limpeza com os pendentes ([[limpeza-alertas-canais]]) e o caminho para alterar regras do Grafana sem permissão de admin (ruler API).

## Resultado

- Pub/Sub do experts-prd: 6 de 10 disparos em 30 dias eram falso-positivo. A regra nova pega os 4 atrasos reais, ignora as rajadas e achou 2 problemas que a antiga não via (mensagens presas por 4 dias no `plataforma-alteracao-plano` e atraso de 29 min no `relatorio-faturamento`).
- Ultimate: no IP-4361, as regras novas teriam aberto o IP 18–35 minutos antes da abertura manual, sem disparo fora do incidente em 35–40 dias.
- Agregador de conversa: o alerta deixou de disparar no lote noturno de todo dia útil (~2,5 mil mensagens, drenadas em < 1h). A análise revelou uma mensagem em loop sem ack, que virou work-item ([atendimento-zendesk#1](https://gitlab.com/ctbz/atendimento/geral/atendimento-zendesk/-/work_items/1)).

## Evidências

- [[limpeza-alertas-canais]] (tabela com antes/depois de cada alerta)
- [[2026-11-06-alerta-pubsub-falso-positivo]] (detalhe do Pub/Sub do experts-prd)
- [[proposta-ajuste-alerta-ultimate-ip]], IP-4383, post-mortem do IP-4361
- Regra do Grafana `fej3urtlra3nka` (agregador de conversa), alterada em 11/11/2026
- Work-item [atendimento-zendesk#1](https://gitlab.com/ctbz/atendimento/geral/atendimento-zendesk/-/work_items/1)
