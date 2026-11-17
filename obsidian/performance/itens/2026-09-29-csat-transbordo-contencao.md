---
name: 2026-09-29-csat-transbordo-contencao
description: "CSAT Transbordo: regras de contenção e tickets travados"
metadata:
  type: project
tags:
  - performance
titulo: "CSAT Transbordo: regras de contenção e tickets travados"
data: 2026-09-29
periodo: 2026QD3
categorias:
  - entrega
  - incidente
  - ia
impacto: alto
fontes:
  - "[[PRD-150920]]"
  - "[[PRD-151218]]"
  - "[[PRD-151592]]"
  - "[[PRD-155905]]"
  - "[[PRD-158026]]"
  - "[[PRD-163436]]"
  - "[[PRD-165982]]"
  - "[[PRD-167347]]"
  - "[[PRD-167666]]"
  - "[[PRD-168648]]"
  - "[[PRD-147775]]"
  - "[[PRD-124863]]"
---

# CSAT Transbordo: regras de contenção e tickets travados

- **Período:** 2026QD3 · **Categorias:** entrega, incidente · **Impacto:** alto

## Contexto

O épico criou regras de contenção de transbordo; depois, uma ACR mostrou tickets de Experts e BPMP travados em PENDING.

## O que fiz

Implementei as regras (formulário de Ticket OFF, ativo em cenário limite, demandas preventivas, feature-flag, integração com Jira) e corrigi os tickets travados, cenários de borda, o conflito da pesquisa CSAT com outros ativos e uma rotina do Zendesk que impedia resolver tickets de B&P.

Em 2026-11-17, mapeei todas as regras do transbordo nos dois motores (experts-service legado e o survey-service, que assumiu o CSAT em ~12/11) e criei a skill de IA `analisar-csat-transbordo`: recebe N tickets do Zendesk e, cruzando os logs do Cloud Logging com os bancos de prod (ticketing, experts_service, atendimento-zendesk) só leitura e sem a API de prod do Zendesk, monta o checklist de regras de cada ticket e gera a planilha com a causa. Com ela, achei a causa do PRC-155098: corrida entre o atraso de 10 min do motor e a automação de SLA que preenche o `due_date` dos Jiras EXPBKO.

## Resultado

O transbordo passou a ser controlado por regra e os tickets presos voltaram a dar baixa. A investigação de "por que a pesquisa saiu" passou de análise manual de logs e Jira para uma execução da skill, em lote, com a causa por ticket.

- 17/11/2026: ACR [[PRD-177601]] do PRC-155098 encerrada sem defeito, com a causa provada por logs e pelo changelog do Jira. Medi o tamanho da lacuna: 643 liberações com EXPBKO sem `due_date` em ~25 dias, contra 781 transbordos segurados. Deixei 3 ações de prevenção (motor, origem no Jira e campo "Transbordos").

## Evidências

- [[PRD-150920]]
- [[PRD-151218]]
- [[PRD-151592]]
- [[PRD-155905]]
- [[PRD-158026]]
- [[PRD-163436]]
- [[PRD-165982]]
- [[PRD-167347]]
- [[PRD-167666]]
- [[PRD-168648]]
- [[PRD-147775]]
- [[PRD-124863]]
- [[csat-transbordo-regras]]
- [[PRC-155098 - CSAT sai mesmo com o atendimento transbordado]]
- Skill `~/ctbz-vault/skills/zendesk/analisar-csat-transbordo`
