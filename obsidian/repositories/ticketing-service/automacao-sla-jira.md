---
name: automacao-sla-jira
description: "Como a automação de SLA preenche o due_date dos Jiras (EXPBKO etc.): regra do Jira Automation chama o ticketing-service (/trigger/dados-empresa), que calcula o SLA pela tabela de SLAs e grava due_date e campos [SLA] com o usuário SVC - Experts; quem é dono e quanto demora"
metadata:
  type: reference
tags:
  - ticketing-service
  - sla
  - jira
---

# Automação de SLA dos Jiras (due_date)

O `due_date` e os campos `[SLA] *` dos Jiras (ex: EXPBKO) são gravados pelo **ticketing-service**, não por uma regra nativa do Jira. Quem grava aparece no Jira como o usuário de aplicação **"SVC - Experts"**.

O ticketing-service fica no grupo do GitLab `ctbz/experts/backend` e roda no GKE, namespace `proc-auto-prd`. É mantido pela Engenharia Canais (Henrique Aurelio, Gabriel Ganassin, Glener). O cadastro de SLAs (tabela por projeto, tipo de item e subtipo) é editado pela tela de SLA do `atendimento-canais-admin` (`/v1/bff/slas`, `/v1/bff/sla-issuetypes`).

## Fluxo

1. Uma regra do **Jira Automation** ("Automation for Jira") dispara na criação do card e quando o subtipo é preenchido (ex: "[EXPBKO] Tipo de Solicitação Fiscal"). Ela chama `POST /trigger/dados-empresa` do ticketing-service (`src/routes/dados-ticket.router.ts`).
2. O ticketing-service enfileira e processa o pedido (`update-jira.mixin.ts`):
    - busca a configuração do tipo de item (`t_issuetype_config`, que diz qual campo é o subtipo);
    - resolve o SLA pelo `SlaJiraUsecase` (`src/modules/dados-ticket/services/sla-jira.usecase.ts`);
    - grava no Jira os dados da empresa e os campos de SLA.
3. **Sem subtipo preenchido, não há SLA:** grava `[SLA] Retorno da automação = SEM_SLA` e deixa o `due_date` vazio. Com o subtipo, grava `due_date`, `[SLA] Data prevista de entrega`, `[SLA] SLA`, `[SLA] Unidade SLA` (ex: 13 HU) e `VIGENTE` (ou `NAO_VIGENTE` se o SLA cadastrado já expirou).
4. Logs (projeto `contabilizei-prod-01`, container `ticketing-service`): "message enqueued", "atualizando issue <KEY>", "dados SLA do card <KEY> atualizados com sucesso", "dados gerais do card <KEY> atualizados".

## Latência medida (EXPBKO-241737, 10/11/2026, BRT)

- Criação 11:46:41 → automação na fila 11:47:06 → `SEM_SLA` gravado 11:47:08: **~27 s**.
- BKO (Rafaela Abreu) preenche o "Tipo de Solicitação Fiscal" 12:34:13 → fila 12:35:01 → `due_date` gravado 12:35:03: **~50 s**.

A automação é rápida. O que atrasa o `due_date` é a classificação humana do subtipo pelo BKO, neste caso 47,5 min depois da criação. Isso afeta o CSAT Transbordo, que descarta EXPBKO sem `due_date` ([[csat-transbordo-regras]], [[PRD-177601]]).

## Onde fica o cálculo no código

O cálculo da data de vencimento fica em `src/modules/sla/service/sla-service/calculate-sla.mixin.ts` (`calculate(sla, basedate)`), chamado pelo `SlaJiraUsecase`, que também define `VIGENTE`/`NAO_VIGENTE` comparando `sla.data_fim` com a hora atual de São Paulo. Os tipos de SLA:

- **DU** (dias úteis): soma N dias pulando fim de semana e feriado, e fecha no `hora_fim_du` do cadastro (padrão 22:00 BRT).
- **HU** (horas úteis): soma N horas dentro da janela `hora_inicio_du`–`hora_fim_du` (padrão 09–22 BRT), só em dia útil.
- **DC** (dias corridos): soma N dias e fecha no fim do dia.

Os feriados vêm do `feriadosService`. Além do caminho do Jira Automation, o SLA também é aplicado pelo consumer `src/consumers/sla/handler.ts` (subscription `ticketing.sub.v1.sla`), que chama `slaTicketService.updateJiraTicket`. Existe ainda `add-working-hours-to-date.usecase.ts`, com janela fixa 09–12/13–18 (horário comercial com almoço), separado do cálculo da tabela de SLAs.

## Observação

No mesmo fluxo, o `relacionamento-service` (`crm-prd`) tenta atualizar o relacionamento e comentar no Jira, e recebe 404 ("Issue does not exist or you do not have permission to see it"). A causa provável é que o usuário dele não tem permissão no projeto EXPBKO. Isso não afeta o SLA.
