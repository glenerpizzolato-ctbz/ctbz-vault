---
name: corujao-fila-noturna-experts
description: "Corujão (fila noturna do Experts no Zendesk): como os tickets entram e saem (crons do atendimento-zendesk e reroute do bots-api), critérios, horários, IDs de grupo e pontos frágeis"
metadata:
  type: reference
tags:
  - ultimate
  - corujao
  - atendimento-zendesk
  - bots-api
---

# Corujão: fila noturna do Experts

Mapeado em 2026-11-17, a partir da thread do Lucas Knabben no espaço Squad Engenharia Canais ("CSAT quando vai em quero atendimento fora do horário de expediente ele fica na fila do corujão? qual o esforço de colocar a fila do corujão para outros fluxos"). Código lido: `atendimento-zendesk` (4a0d8961a), `bots-api` (3398386), `ctbz_atendimento_geral_atendimento-zendesk-cronjob`.

## O que é

Um grupo do Zendesk (`Corujão`, prd `15341738418332`, dev `15341735769756`) para o atendimento humano Experts fora do expediente. Não tem relação com CSAT ou outro produto: tickets entram por roteamento direto ou por uma cron que move tickets que preenchem os requisitos, e saem de manhã por outra cron. Agenda EXPERTS em prd (bots-api, `business_hours` flow `EXPERTS`): aberto 09–22 de seg a sex; `NIGHT` (Corujão) de seg a qui; sexta fecha às 22 (fonte: `survey-service/src/modules/survey/business-hours-window.spec.ts`). Status possíveis: `OPEN_COMMON`, `OPEN_EXTENDED`, `NIGHT`, `CLOSED`.

## Grupos envolvidos (prd)

| Grupo | ID | Onde é configurado |
| --- | --- | --- |
| Corujão | `15341738418332` | `APP_SERVICES_ZENDESK_CORUJAO_GROUP_ID` / `bots-api src/infra/env/index.ts` |
| Default (destino da manhã) | `15320473247900` | `APP_SERVICES_ZENDESK_DEFAULT_GROUP_ID` |
| Assessores Hubs | `5318557219868` | bots-api `assessores_hubs` |
| Caixa Noite | `18170415225372` | bots-api `caixa_noite` (não é o Corujão) |
| RE_ROUTE_TICKET | `26995812838556` | bots-api `re_route_ticket` |

## Entradas

1. **Cron `transf-hub-corujao`** (`30 1 * * *` UTC = 22:30 BRT, **todo dia**, sem `time_zone` no params) → `atz-worker-transferencia-atendimento-prd` `GET /api/v1/atendimento/zendesk/schedule/transferencia-atendimento/hubParaCorujao`. Busca no **espelho local** (tabela `Ticket` do Postgres do atendimento-zendesk, não a API do Zendesk) tickets `status = novo`, `assignee_id = null`, `via = WhatsApp`, com a tag `sys_tema_assessoria_exp`, **sem filtro de grupo**. Move para o Corujão em um único update em lote (sem chunk), removendo `sys_tema_assessoria_exp`, `gatilho_acionado_ongoing_exp`, `sys_grupo_exp_hour_extended` e adicionando `sys_grupo_exp_hour_night`.
2. **Reroute do bots-api** (`re-route-ticket.usecase.ts`, ticket que cai no grupo RE_ROUTE_TICKET, inclusive retorno de CSAT com `sys_re_route_source=csat`). Vai direto ao Corujão (com a tag `sys_grupo_exp_hour_night`) só em dois casos, e só se o status EXPERTS for `NIGHT`/`CLOSED`:
   - fallback: ticket de origem não encontrado, ou origem sem assignee e fora da Caixa Noite, **e** cliente com plano Experts (não Experts vai para AIDA geral WhatsApp);
   - origem na Caixa Noite fora do `OPEN_EXTENDED` (em `OPEN_COMMON` vai para Assessores Hubs).
   Nos demais casos volta para o **grupo de origem** (com o mesmo agente se estiver disponível), sem olhar horário. `HUMAN_CP` vai para o contador parceiro.
3. **Ultimate**: os caminhos do bot que passam pela validação de horário comercial caem no Corujão fora do expediente (ver [[csat-quero-atendimento-ramificacoes]]).

## Saída

- **Cron `transf-corujao-default`** (`5 12 * * *` UTC = 09:05 BRT, **todo dia**) → `.../corujaoParaDefault`. Busca no espelho os tickets WhatsApp do grupo Corujão que não estão `closed/fechado/solved/resolvido`, sem filtrar assignee, e move em lotes de 100 para o grupo **Default**, adicionando `sys_tema_assessoria_exp` e `sys_grupo_exp_hour_common` e removendo `sys_grupo_exp_hour_night`. O grupo de origem não é guardado: tudo volta para o Default.
- Relacionada: **`exp-expediente-extend`** (`50 20 * * 1-5` UTC = 17:50 BRT) marca com `sys_grupo_exp_hour_extended` os mesmos tickets do critério da entrada 1.

Histórico: em 2025-12 um commit tirou o group_id Default dessa transferência e os tickets ficaram retidos; foi revertido (`f5fec7445`, [[PRD-135472]], [[PRD-135769]]). Os schedulers antigos do Twilio (`transfer-tasks-Hub-to-corujao`, `transfer-tasks-corujao*`, projeto Experts) estão pausados.

## Resposta às perguntas da thread

- **CSAT "Quero atendimento" fora do horário vai para o Corujão?** Depende. Pelo reroute, só vai direto se não achar o ticket de origem (ou ele estiver sem assignee) e o cliente for Experts, ou se a origem for a Caixa Noite. Se a origem tem assignee, volta para o grupo de origem mesmo à noite e só chega ao Corujão pela cron das 22:30, se o ticket ainda estiver `novo`, sem assignee e com a tag `sys_tema_assessoria_exp`. Retorno depois das 22:30 fica no grupo de origem até a manhã.
- **Esforço de pôr o Corujão em outros fluxos:** entrar é barato (o fluxo põe a tag `sys_tema_assessoria_exp` e deixa sem assignee, ou roteia direto com `group_id` do Corujão + `sys_grupo_exp_hour_night`, como o bots-api). O custo está na saída: a cron devolve tudo para o Default do Experts com `sys_tema_assessoria_exp`, então um fluxo de outro time cairia na fila errada. Para outros fluxos, guardar o grupo de origem (ex: tag `sys_corujao_origem_<id>` ou coluna no espelho) e devolver para ele, e decidir o calendário (hoje as crons rodam todo dia).

## Pontos frágeis

- Crons rodam todo dia (inclusive sex/sáb/dom), enquanto a agenda do Corujão é seg–qui; sábado 09:05 os tickets vão para o Default com `hour_common` num dia fechado. Confirmar se é intencional.
- Critério da entrada 1 sem filtro de grupo: qualquer ticket WhatsApp novo, sem assignee e com a tag, em qualquer grupo, vai para o Corujão.
- Tudo depende do espelho local estar em dia (webhooks de eventos de ticket); status desatualizado move ou deixa de mover ticket.
- `corujaoParaDefault` não filtra assignee: ticket atribuído a um agente da noite troca de grupo com o assignee, e o Zendesk pode recusar o update se ele não for membro do Default.
- Uma única janela às 22:30: o que ficar elegível depois disso só é tratado na noite seguinte.
