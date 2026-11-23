---
name: whatsapp-ativo-finalidade-optout
description: "atendimento-zendesk: como o ativo de WhatsApp decide a finalidade do opt-out (SURVEY/MARKETING/TRANSACTIONAL/TAX) e consulta o contato-service antes de enviar"
metadata:
  type: reference
tags:
  - atendimento-zendesk
  - opt-out
---

# Finalidade do opt-out no WhatsApp ativo

Fluxo no worker `enviar-ativo` (comum a individual, app do Zendesk, legado e massivo): `validarWhatsappAtivoService.validar` (template ativo e aprovado) → `VerificarOptoutWhatsappAtivoService.verificar` → envio. Opt-out encontrado encerra com `BLOQUEADA_OPTOUT` e `id_erro = OPTOUT_DO_TITULAR`.

Finalidade (`verificar-optout/optout-purpose.ts`), nesta ordem:

1. `optoutPurpose` do payload, se vier preenchido (ex: o agrupamento de guias manda `TAX`). **Não é gravado** na `mensagem_ativa`: pelo banco não dá para saber se o chamador mandou.
2. `SURVEY` se o squad do template (`mensagem_ativa_template.squad`, modelo Prisma `WhatsappTemplate`) é `SURVEY` ou se a `categoria` do envio é `NPS`/`WORKER_CSAT`.
3. `MARKETING` se a categoria Meta do template é `MARKETING`; senão `TRANSACTIONAL`.

`integracao`, `squad` do envio, `autor`, `tipo` e `fila` não entram. A consulta ao contato-service é `GET /api/v1/optouts` com `channel=WHATSAPP`, `address=destino`, `purpose` e `companyCode` (de `docTipo`/`docValor`: `cnpj` sanitizado ou `processo_abertura_id`); só bloqueia `optedOut: true` com `scope: ADDRESS`. Falha aberta: erro ou timeout de 3 s → lista vazia → envia.

Templates de pesquisa de outros squads (HubSpot, corretora, bank) escapam do opt-out `SURVEY`: ver o playbook [[PRD-168944 - Cliente não quer receber pesquisa (CSAT e-ou NPS)]] e o relatório https://claude.ai/artifact/TNkJBn1NwdNBMTKnet2733.

Como testar em dev: [[testar-optout-whatsapp-ativo-dev]].

## Histórico

- **18/08/2026**: Gabriel Ganassin implementa a validação de opt-out no ativo, com a finalidade `SURVEY` quando o template é do squad `SURVEY` ou a categoria é `WORKER_CSAT` (commit `f85de4319`), e no mesmo dia inclui o `NPS` como pesquisa (`66a6be593`). Entrou pelo PR #772 (`feat/optout-whatsapp-ativo`), mergeado em 19/08/2026 e publicado na release `0.698.0`.
- **05/10/2026**: Glener refatora para tratar o opt-out como desfecho do envio (status `BLOQUEADA_OPTOUT`), e não mais como exceção (status `ERRO`). Nessa mudança a regra vai para o `optout-purpose.ts`, que passa a aceitar `optoutPurpose` na rota (incluindo `TAX`). O merge de `feature/optout-purpose` chegou a ser revertido (`2b06b77da`) e depois foi reaplicado.
- **19/11/2026**: MR !252 (draft, `feat/optout-survey-nome-template`) adiciona o guardrail pelo nome do template. Regra final: `optoutPurpose` do DTO; senão é pesquisa se o squad é `SURVEY`, a categoria é `NPS`/`WORKER_CSAT` ou, por último, o nome tem `nps`/`csat` (substring), e aí a finalidade é só `SURVEY` (log `warn` "opt-out de pesquisa pelo nome do template"); senão `MARKETING`/`TRANSACTIONAL` pela categoria da Meta. Decisão de produto: uma finalidade só (chegou a ser feita a soma `SURVEY` + finalidade da regra e foi desfeita). Efeito: 49 templates ativos fora do squad SURVEY entram na regra; 23 são MARKETING e deixam de consultar o opt-out de MARKETING, 26 são UTILITY (inclusive `upsell_csat`) e deixam de consultar TRANSACTIONAL. Em `contact_optout` (prd, contato-service, WhatsApp, escopo ADDRESS) em 19/11/2026: 15 SURVEY, 3 MARKETING, 2 TRANSACTIONAL e 2 TAX ativos, nenhum telefone com MARKETING sem SURVEY. A revisar com os donos: `tratativacsat`, `upsell_csat`, `contab_csat`, `crm802_promotores_nps`, `experts_resgate_contatonps(2)`.

## Armadilha: o squad do template também filtra a lista no app e define a integração

No `zendeskapp-whatsapp-ativo`, o envio individual e o massivo só listam templates com `template.squad === getSquad(atendimento escolhido)` (`constants/squadTemplate.ts`), e o `create-template` grava `squad = integration`. Mover um template para o squad `SURVEY` (para cair no opt-out de pesquisa) obriga quem dispara a escolher o atendimento `SURVEY`, o que troca a `integracao` do envio e, com ela, para onde a resposta do cliente vai (fila/bot de pesquisa em vez da fila do time, ex: `Plano de Saúde [WhatsApp] [Corretora]`). O squad acumula três papéis (visibilidade no app, roteamento e finalidade do opt-out); a correção estrutural é ter a finalidade como atributo próprio do template.

## Envio manual pelo app (zendeskapp-whatsapp-ativo): o que o campo "Atendimento" muda

O "Atendimento" do envio individual/massivo é a `integracao` (`TipoAtendimento`: CORE, EXPERTS, SURVEY "Pesquisas", CORRETORA…). Ele define, de uma vez: os templates listados (`squad === getSquad(atendimento)`), as filas oferecidas (`getFilas(atendimento)`), o número que envia (`app.modules.whatsapp-ativo.integrations.<integracao>` no configmap `atendimento-zendesk-prd`: SURVEY = "WhatsApp (Survey)" +55 11 95817-7006; CORRETORA/EXPERTS/CORE = "WhatsApp (Main)" +55 41 4101-0021) e exige o grupo de permissão da área (`permissionGpSurvey` etc.). No cadastro de template, o "projeto" vira a integração usada para criar o template na Meta (`sunshine.createTemplate(dto.integration)`) e o `squad`. O app não manda `categoria` nem `optoutPurpose`, e a rota do massivo (CSV, `massivo/`) não aceita `optoutPurpose` (só a rota de mensagem individual aceita). Sem código, o único jeito de um envio manual cair no opt-out `SURVEY` é template criado no projeto "Pesquisas" + envio com Atendimento "Pesquisas" (como o `nps_exp_2025_03a`).
