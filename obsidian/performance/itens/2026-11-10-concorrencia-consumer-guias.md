---
name: 2026-11-10-concorrencia-consumer-guias
description: "Causa e correção do atraso de até 34 min nas notificações de guias de clientes Expert (rajada de 63 mil guias no experts-service)"
metadata:
  type: project
tags:
  - performance
titulo: "Correção do atraso nas notificações de guias após rajada de 63 mil mensagens (experts-service)"
data: 2026-11-10
periodo: 2026QD3
categorias: [incidente, qualidade]
impacto: medio
fontes: ["[[PRD-176493]]", "[[deploy-e-variaveis-de-ambiente]]"]
---

# Correção do atraso nas notificações de guias após rajada de 63 mil mensagens

## Contexto

Em 2026-11-09 disparou o alerta "Mensagem mais antiga sem ack > 15 min" na subscription `experts-service.sub.guia-imposto`: o fintech publicou ~63 mil guias de uma vez, o backlog chegou a 31 mil mensagens e as notificações de guias de clientes Expert atrasaram até 34 min. O autoscaling subiu para 5 pods com a CPU em ~10%.

## O que fiz

- Identifiquei que o gargalo era a concorrência do consumer (`maxMessages` padrão 3 por pod), não recurso, e que a variável não estava definida no deploy (repo `pipeline` do devops).
- Subi o padrão para 10 (MR !151), depois de avaliar o impacto no pool do banco (as conexões não mudam), na API da plataforma e no fluxo de notificação.
- Medi a mudança com o consumer real contra o emulador do Pub/Sub e registrei a evidência no Jira. No teste, achei que o `flowControl` não é aplicado quando o próprio consumer cria a subscription.
- Abri o work-item #19 para um risco que a concorrência maior torna mais provável: notificação duplicada pela corrida no `alreadySent`.

## Resultado

- Vazão por pod ~3,35x maior no teste (7,4 → 24,8 msg/s, 200 mensagens com 300 ms cada). Pela vazão do incidente, 2 pods passam a dar conta de uma entrada como a de ontem (~26 msg/s) sem precisar escalar.
- Validação em prd fica para a próxima rajada.

## Evidências

- [[PRD-176493]] (Jira PRD-176493; sub-tasks PRD-176494 e PRD-176495, com a evidência no comentário)
- MR: https://gitlab.com/ctbz/experts/backend/experts-service/-/merge_requests/151
- Work-items #18 e #19 do experts-service
