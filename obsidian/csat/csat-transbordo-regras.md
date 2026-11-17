---
name: csat-transbordo-regras
description: "Mapa de todas as regras do CSAT Transbordo (segurar a pesquisa CSAT até o ticket off/Jira ser resolvido): gatilho, flag, atraso, regras do CSAT, regras do Jira (Experts) e da conversa paralela (BPMP), PENDING por CNPJ, FUP do ticket off/Jira fechado/SLA 16h, nos dois motores (experts-service legado e survey-service), com logs e tabelas para investigar"
metadata:
  type: reference
tags:
  - csat
  - transbordo
  - experts-service
  - survey-service
---

# CSAT Transbordo: regras

Quando o pedido do cliente num atendimento humano de WhatsApp vira um ticket off de acompanhamento (com Jira, em Experts, ou conversa paralela, em BPMP), a pesquisa CSAT do atendimento é **segurada**, e o cliente recebe a pesquisa (FUP) só quando o ticket off ou o Jira é resolvido. Épico [[PRD-147775]]; ajustes em [[PRD-158026]], [[PRD-167347]] e [[PRD-168550]].

Para analisar por que um ticket segurou ou não, usar a skill `analisar-csat-transbordo` (aceita N tickets e gera planilha com a causa).

## Motores (quem decide)

| Período | Motor | Onde | Logs |
|---|---|---|---|
| até ~12/11/2026 18h UTC | `experts-service` (legado) | `RunSurveyCsatEngineConsumer` → `FetchTranbordoUseCase` → `ProcessExpertsTransbordoStrategy` / `ProcessBpmpTransbordoStrategy` | GKE `experts-prd/experts-service`, `jsonPayload.flow="csat-engine"`, steps `engine`, `survey-limit-handler`, `fetch-transbordo`, `fetch-transbordo-experts`, `fetch-transbordo-bpmp`. Loga cada regra e cada Jira descartado com o motivo |
| depois do cutover | `survey-service` | `CsatSurveyConsumer` → job pg-boss `csat.request` → `prepareRequest` → janela de expediente → `TransbordoHold.prepare` → `DispatchEngine` | GKE `atendimento-canais-prd/survey-service`, `jsonPayload.name="csat.request"` com `ticketId`. Só o desfecho: `CSAT DISPATCHED`, `CSAT HELD`, `CSAT SKIPPED`, `CSAT ignorado: <motivo>`, `CSAT agendado para a abertura do expediente`, `CSAT descartado: <motivo>`. **Não loga quais Jiras viu nem o `enable_transbordo`** |

O `survey-service` espelha os envios e os transbordos no banco do `experts-service` (`survey_csat_sent` e `ticket_transbordo`, com `survey_service_id`), pelo job `csat.legacy-mirror` (5 min). O banco do próprio `survey-service` (`survey_service`, instância `atendimento-canais`) não tem grant para o usuário IAM (0 tabelas visíveis em 2026-11-17).

## Fluxo e regras, na ordem

1. **Gatilho do Zendesk** (ticket humano resolvido) chama `POST /v1/survey-csat/engine` do experts-service, que publica em `zendesk-trigger.p2p.csat-survey`. O corpo traz `id`, `source`, `organization_cnpj`, `assignee_email`, `group_id`, `tags`, `custom_fields` (com `requester_phone`) e **`enable_transbordo`**. A flag é decidida no gatilho do Zendesk (a antiga tabela `survey_csat_feature_flag` foi removida em 2026-09-24). O campo "Transbordos" do ticket não é lido em nenhum ponto.
2. **Origem com transbordo:** só `HUMAN_EXPERTS` (por Jira) e `HUMAN_BPMP` (por conversa paralela). No survey-service isso vem de `csat_source_config.transbordo_kind` (`JIRA` / `PARALLEL_CONVERSATION`).
3. **`enable_transbordo = true`**, senão a checagem é pulada e a pesquisa segue as regras normais. No survey-service, o `TransbordoHold.prepare` também exige um **CNPJ de 14 dígitos** em `organization_cnpj` (normalizado): sem ele (CPF, vazio), não há transbordo, porque Jira e conversa paralela são buscados pelo CNPJ.
4. **Atraso de 10 min** (`TRANSBORDO_DELAY_MS` no legado, `startAfter` no survey-service) só para `HUMAN_EXPERTS`/`JIRA` com a flag, para dar tempo de o Jira ser aberto. **`HUMAN_BPMP` decide na hora.**
5. **Regras do CSAT antes do transbordo** (se barrar aqui, a pesquisa nem sai):
    - Payload: `assignee_email`, identificador (tag `cnpj_zd:` → `cnpj:` → `organization_cnpj`), `requester_phone`.
    - Origem `CSAT_FUP_TRANSBORDO` vai para o fluxo do FUP.
    - Atendente conta genérica (`contabilizei*`, `contador.inteligente*`) não recebe pesquisa nas origens humanas.
    - Blocklist do CNPJ (legado) / opt-out do contato-service (survey-service).
    - Micro tema elegível (só legado, com `CSAT_APLICA_RESTRICAO_MICRO_TEMA`).
    - Janela de expediente (só survey-service): fora dela, agenda para a abertura (`csat.request-scheduled`) ou descarta.
    - Regras de envio: `LIMITE_NAO_ATINGIDO` (quarentena, ex: 1 pesquisa em 7 dias por CNPJ) e depois `ASSESSOR_PRIORITARIO` (e `MICRO_TEMA_PRIORITARIO` no legado). **O transbordo só é avaliado depois que uma regra casa**: um CSAT barrado pela quarentena não cria transbordo.
6. **Data de criação do ticket pai**, buscada no atendimento-zendesk (`/api/v1/tickets/:id`).
7. **Experts (Jira):** Jiras do CNPJ no ticketing-service (`GET /v2/company/:cnpj/tickets/jira?start_date=<criação do pai>`, tabela `ticketing.ticket_jira`). No legado, filtrados pelos projetos `NFEXP, EXPBKO, VAL, SDC, PREV, RHC, C20, SST, OBA, ATE, RTRAB, OPFIS, REG, ER, INV, ENQEXP, PROA`; o survey-service não tem essa lista, e o efeito é o mesmo, porque a regra de prazo abaixo já descarta tudo que não é NFEXP nem EXPBKO. Cada Jira é elegível se, nesta ordem:
    1. foi criado **depois** do ticket pai;
    2. **não** está `closed`;
    3. é **NFEXP** (sem regra de prazo) ou **EXPBKO** com **`due_date` preenchido e a no máximo 48h** do momento do motor. Qualquer outro projeto é descartado;
    4. o campo **"Demanda preventiva"** (`metadata.demanda_preventiva`) está **preenchido e diferente de "Sim"**. Vazio também descarta.
    - A regra do `id_ticket_atendimento` (Jira ligado ao ticket do atendimento) está desativada ([[PRD-163952]]).
    - Cada Jira elegível vira um `ticket_transbordo` `PENDING` (com `jira_ticket_id`), a chave `ticket_transbordo_issue:<issue>` no cache (7 dias) e o agendamento do aviso de SLA de 16h úteis.
8. **BPMP (conversa paralela):** tickets do atendimento-zendesk (`GET /api/v1/csat/tickets/transbordo`, tabela `tickets`) com `via = 'Conversa paralela'`, `organization_external_id` = CNPJ, status fora de `solved`/`closed` e `created_at >= criação do pai`. Cada um vira `ticket_transbordo` `PENDING` com `fup_ticket_id`.
9. **Segura se o CNPJ tiver qualquer `ticket_transbordo` `PENDING`**, inclusive de outro ticket (e os recém-criados no passo 7/8). Senão, a pesquisa sai.

## Depois de segurar (FUP)

- **Ticket off resolvido** (webhook `/v1/survey-csat/ticketoff` no legado; consumer de tickets do CRM no survey-service): acha o transbordo pelo Jira do campo "Jira issues" do ticket (Experts, status `PENDING` ou `CSAT_FUP_SLA_16H_EXPIRED_SENT`) ou pelo `fup_ticket_id` (BPMP). Ignora se houver mais de um transbordo para o pai (`IGNORED_MULTIPLE_TRANSBORDO`) ou CNPJ na blocklist (`IGNORED_BLOCKLISTED_CNPJ`). Exige que o último comentário público seja do agente (`web`/`api`), senão reabre o ticket com nota interna. Exige que o ticket off esteja ligado ao Jira raiz. Aí manda o FUP (`csat_fup`, regra `CSAT_FUP_TRANSBORDO_OFF_CLOSED`) e marca `CSAT_FUP_SENT`.
- **Jira fechado** (tópicos `ticketing.bcast{,.v2}.ticket-jira`, com atraso): se a issue está no cache e só há esse `PENDING` para o pai, manda o FUP intermediário (`csat_fup_intermediario`, regra `CSAT_FUP_JIRA_CLOSED`) e marca `CSAT_FUP_ALTERNATIVE_SENT`.
- **SLA de 16h úteis** com o transbordo ainda `PENDING`: aviso ao cliente e `CSAT_FUP_SLA_16H_EXPIRED_SENT`.
- **Ticket off mesclado** (tag `closed_by_merge`): `IGNORED_TICKET_MERGED`.
- Fora do expediente, no survey-service o FUP vai para `CSAT_FUP_SCHEDULED` e sai na abertura.

## Armadilhas que já causaram vazamento

- **`due_date` preenchido depois do motor (EXPBKO):** o `due_date` é preenchido pela automação de SLA do Jira (usuário "SVC - Experts", `[SLA] Retorno da automação` de `SEM_SLA` para `VIGENTE`) só depois que o BKO classifica o "Tipo de Solicitação" (o gatilho da automação; na criação ela grava `SEM_SLA`). A automação responde em segundos; quem demora é a classificação manual, que pode passar muito dos 10 min de atraso contados do solved do atendimento. Fluxo em [[automacao-sla-jira]]. Caso do [[PRC-155098 - CSAT sai mesmo com o atendimento transbordado|PRC-155098]]: Jira EXPBKO-241737 criado 11:46, motor às 12:03 com `due_date` nulo, `due_date` preenchido às 12:35 (BRT, 10/11/2026), e a pesquisa saiu.
- **Demanda preventiva vazia descarta o Jira**, assim como "Sim".
- **BPMP sem atraso:** se o ticket de conversa paralela é aberto depois do solved, o motor já decidiu.
- **Qualquer PENDING do CNPJ segura**, inclusive um transbordo antigo travado de outro ticket ([[PRD-167347]]).

## Onde olhar

- Logs: projeto `contabilizei-prod-01` (ver a tabela de motores). O horário do solved aparece no `zendesk-agents` (`crm-prd`, "ticket X is closed or solved").
- Bancos (prod, só leitura): `prd_experts_experts_service` (`survey_csat_sent`, `ticket_transbordo`), `prd_issue_ticketing` (`ticket_jira`: estado atual, sem histórico), `prd_crm_atendimento_zendesk` (`tickets`: `via`, `status`, `created_at`, `organization_external_id`, `group_name`, `tags`).
- Histórico de um Jira (quando o `due_date`/status mudou): changelog pelo MCP do Atlassian (`getJiraIssue` com `expand: "changelog"`).
- Código: `experts-service` em `src/consumers/survey-csat/run-survey-csat-engine/`, `src/domain/ticket-transbordo/`, `src/domain/survey-csat/csat-fup.service.ts`; `survey-service` em `src/modules/csat/` (`transbordo-hold.ts`, `csat-request.worker.ts`, `ticket.ts`, `ticket-off.service.ts`, `csat-jira-closed.worker.ts`, e o `AGENTS.md` do módulo).
