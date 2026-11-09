---
name: incidentes-indice
description: "Índice das notas sobre gestão de incidentes (projeto IP no Jira, post-mortem no Outline)"
metadata:
  type: reference
tags:
  - incidentes-indice
---

# Incidentes

- [[processo-incidentes-ip]] — onde vai o relato (descrição), template de post-mortem do Outline (QD3), campos obrigatórios da transição Resolver e automação de Plano de Ação
- [[abertura-automatica-ip-grafana]] — como um alerta do Grafana vira IP (contact point opsgenie → JSM Ops; só P1/P2 abre IP), quais contact points abrem IP, por que os alertas da Ultimate não abriram o IP-4361 e quem é o responsável (Gabriel Egydio)
- [[proposta-ajuste-alerta-ultimate-ip]] — qual alerta da Ultimate abre IP automático: dados de 40 dias, decisão de 09/11/2026 (3+ bots com Technical error ou soma ≥100 em 5 min) e as duas regras criadas no Grafana (fase 1, sem prioridade)
- [[alerta-pubsub-unacked-falso-positivo]] — alerta "Pub/Sub Unacked messages" do Cloud Monitoring (experts-prd) dispara falso-positivo nas rajadas do processar-guia-imposto (média de 2h > 100; "116.733" = 116,7); proposta de idade da mensagem > 15 min e casos reais em 30 dias
- [[causa-raiz-zendesk-ai-agents-2026-11-03]] — causa raiz da Zendesk para a queda dos AI Agents em 03/11/2026 (IP-4361): rotação de segredo que não propagou, HTTP 401 entre serviços, recuperação por região
