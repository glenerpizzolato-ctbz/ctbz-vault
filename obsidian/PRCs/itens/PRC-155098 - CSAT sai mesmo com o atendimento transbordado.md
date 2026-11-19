---
name: prc-csat-sai-mesmo-com-transbordo
description: PRC — a pesquisa CSAT sai para o cliente mesmo com o atendimento transbordado para ticket off/Jira; achar a regra que liberou com a skill analisar-csat-transbordo
metadata:
  type: reference
tags:
  - prc
canal:
  - wpp
dominio:
  - csat
sistemas:
  - experts-service
  - survey-service
  - ticketing-service
  - atendimento-zendesk
acr: "[[PRD-177601]]"
ocorrencias:
  - PRC-155098
qtd_ocorrencias: 1
ultima_ocorrencia: 2026-11-12
---

# CSAT sai mesmo com o atendimento transbordado

## Sintoma

O atendimento de WhatsApp foi transbordado (ticket off aberto, com Jira, campo "Transbordos" = Sim), mas a pesquisa CSAT saiu logo após o solved, em vez de esperar a resolução do ticket off.

## Como investigar

Rodar a skill `analisar-csat-transbordo` com os tickets do atendimento (não o ticket off nem o da resposta da pesquisa; se vier o da resposta, a skill aponta o ticket pai). Ela diz qual regra liberou a pesquisa. As regras estão em [[csat-transbordo-regras]].

## Causas encontradas

- **PRC-155098** (GLOK CONSULTORIA, CNPJ 53982049000153, atendimento 30257371, ticket off 30259457, resposta 30263828): `HUMAN_EXPERTS` com `enable_transbordo=true`. O motor rodou 10 min depois do solved (12:03 BRT de 10/11/2026) e achou o Jira EXPBKO-241737 (criado 11:46), mas ele estava **sem `due_date`** e foi descartado. O `due_date` só foi preenchido às 12:35 pela automação de SLA ("SVC - Experts"), depois que o BKO classificou o "Tipo de Solicitação" (12:34). Com o `due_date` (prazo em ~24h), o Jira teria segurado a pesquisa. Causa: corrida entre o atraso fixo de 10 min e a automação de SLA do Jira. Não tem relação com o campo "Transbordos" nem com a via do ticket off. Efeito colateral: quando o ticket off 30259457 foi resolvido (11/11 09:58 BRT), o fluxo do FUP procurou o transbordo pelo Jira EXPBKO-241737 e não achou ("parent ticket not found"), então o FUP também não saiu. Sem exceção nem falha de execução: o motor rodou uma vez, sem retentativa, e cada passo bate com a regra (os logs "já está sendo processado" são do fluxo de desconexão, não do CSAT). É uma lacuna na regra do EXPBKO, não um bug de execução. Análise documentada no comentário da ACR PRD-177601. Relatório dos 3 tickets gerado com a skill (o código `TICKET_OFF_DO_TRANSBORDO` reconhece o ticket off).

## Tamanho do problema

Levantamento de 18/10 a 17/11/2026 (planilha caso a caso em `~/Downloads/csat-transbordo-expbko-sem-due-date-2026-10-18-a-2026-11-17.csv`, com relatório `.md` ao lado):
- **767 atendimentos** tiveram a pesquisa liberada com um EXPBKO do CNPJ sem `due_date` no momento do motor: 643 no experts-service (exato, pelos logs) e 124 no survey-service (reconstruído). São cerca de 36 por dia útil.
- **280 (37%) teriam sido segurados** se o `due_date` existisse na hora. Os demais seriam liberados de todo jeito: 318 por prazo acima de 48h e 29 por demanda preventiva; outros 138 continuam sem `due_date` até hoje.
- No mesmo mês, o transbordo segurou 933 pesquisas.
- Da criação do EXPBKO até o `due_date` (classificação do "Tipo de Solicitação"): mediana de 2h53, p90 de 17h27; só 7 de 575 casos abaixo de 10 min.
- Uma reavaliação de até 2h pegaria 51% dos 280; até 8h, 81%.
- Método: no motor antigo, logs "as due_date is null" com a decisão; no survey-service, "CSAT DISPATCHED" com a flag inferida pelo atraso desde o solved, os EXPBKOs do CNPJ e o horário do `due_date` pelos logs de SLA do ticketing-service ([[automacao-sla-jira]]).

## Como resolver

- Caso pontual: não há o que desfazer (a pesquisa já saiu); responder à relatora com a causa.
- **PRC-155098 encerrado em 19/11/2026** (Concluído), com comentário à relatora; a ACR recebeu a conclusão final no mesmo dia. Campos de encerramento: N3 "Experts - CRM / WhatsApp - Comportamento não esperado", Grau "Alto - Impactou Operação", Ofensor `csat_zendesk`, `csat_transbordo`, Resolução "Envio de orientações (devido)", Devido.
- Causa resumida: o "Tipo de Solicitação" não é obrigatório em todos os tipos de Jira do EXPBKO, mas é o gatilho da automação de SLA que preenche o `due_date`, obrigatório para segurar a pesquisa.
- Soluções em avaliação (19/11/2026): (a) tornar o "Tipo de Solicitação" obrigatório em todos os tipos do EXPBKO, com limitações operacionais segundo Lucas Knabben; (b) aumentar os 10 min da validação quando o Jira ainda não tem `due_date`/SLA, com números sendo levantados por Lucas Knabben.
- Ações registradas na ACR PRD-177601 (comentário de 17/11/2026):
    1. Motor reavalia com limite quando o único candidato é um EXPBKO sem `due_date`, e segura se o limite acabar.
    2. Na origem, prazo provisório ou "Tipo de Solicitação" obrigatório no Jira, a cargo do time do Jira/BKO.
    3. "Transbordos = Sim" como sinal extra para reavaliar, ou comunicação à operação.
- Opções avaliadas antes: não descartar EXPBKO sem `due_date` (tratar como elegível, ou reavaliar depois), ou aumentar/condicionar o atraso para esperar o SLA do Jira. Hoje o motor é o survey-service (`isJiraEligible` em `src/modules/csat/transbordo-hold.ts`).
