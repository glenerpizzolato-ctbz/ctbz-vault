---
name: 2026-11-11-ativo-fim-de-semana-agrupamento
description: "Descoberta de que, quando o dia 15 cai em fim de semana, o WhatsApp do agrupamento de guias sai na segunda mas a resposta do cliente deixa de ser ligada ao ativo (validade de 24h conta da criação)"
metadata:
  type: project
tags:
  - performance
titulo: "WhatsApp do agrupamento em fim de semana perde o vínculo com a resposta do cliente"
data: 2026-11-11
periodo: 2026QD3
categorias: [qualidade]
impacto: medio
fontes: ["[[whatsapp-ativo-fora-do-horario-comercial]]", "[[notificacao-agrupamento-experts-bp-lp]]"]
---

# WhatsApp do agrupamento em fim de semana perde o vínculo com a resposta do cliente

## Contexto

O agrupamento de guias dispara o WhatsApp no dia 15. Em 2026-11-15 o dia 15 cai num domingo, e surgiu a dúvida do que acontece com o ativo e com a resposta do cliente fora do horário comercial.

## O que fiz

Li o fluxo do `atendimento-zendesk` (`debounceToBusinessHour`, retentativa por Pub/Sub, `createOrAddRetry`, busca do ativo pela resposta) e cruzei com os dados de prod dos dias 15 de jul. a out. de 2026.

## Resultado

O envio não se perde: fica em retentativa e sai a partir de segunda às 9h. Mas a validade de 24h conta da criação da linha (no sábado/domingo), então a resposta do cliente deixa de ser ligada ao ativo. Em 2026-08-15 (sábado) foram 2 respostas reconhecidas, contra ~4 mil nos dias 15 úteis (4046, 3996, 4286), com volume de envio parecido. Correções possíveis foram mapeadas antes do dia 15/11.

A correção (PRD-176856, MR !102) entrou em prod no mesmo dia, 11/11, quatro dias antes do domingo 15/11: o agrupamento manda `validadeEmMinutos = 4320`. Usei os dados de prod para responder ao review (98,6% dos ativos de 15/08 saíram na segunda às 9h, então 72h deixam pelo menos 24h de janela depois do envio). No teste E2E em DEV, o ativo criado há 50h foi reconhecido pelo bot e uma resposta real virou `RESPONDIDA`; o controle de 24h não foi reconhecido (PRD-176859).

## Evidências

- [[whatsapp-ativo-fora-do-horario-comercial]]
- [[notificacao-agrupamento-experts-bp-lp]]
- MR: https://gitlab.com/ctbz/experts/atendimento-canais/microsservico-agrupamento-guias/-/merge_requests/102
- Teste E2E: https://contabilizeicontabilidade.atlassian.net/browse/PRD-176859
