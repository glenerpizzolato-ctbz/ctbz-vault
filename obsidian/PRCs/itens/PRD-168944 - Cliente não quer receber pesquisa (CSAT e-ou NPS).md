---
name: prc-cliente-nao-quer-receber-pesquisa-csat-nps
description: PRC — cliente pede para não receber mais pesquisa; separar CSAT (blocklist do experts-service) de CSAT+NPS (opt-out do contato-service via front admin)
metadata:
  type: reference
tags:
  - prc
canal:
  - wpp
  - email
dominio:
  - csat
  - notificacoes
sistemas:
  - experts-service
  - contato-service
  - atendimento-canais-admin
acr:
  - "[[PRD-168944]]"
  - "[[PRD-178071]]"
ocorrencias:
  - PRC-146015
  - PRC-148207
  - PRC-152662
  - PRC-154915
qtd_ocorrencias: 4
ultima_ocorrencia: 2026-11-11
---

# Cliente não quer receber pesquisa (CSAT e/ou NPS)

## Sintoma

Cliente reclama do volume de pesquisas recebidas e pede para ser retirado da
listagem ("retirar pesquisa de insatisfação").

- Exemplo: [PRC-146015](https://contabilizeicontabilidade.atlassian.net/browse/PRC-146015)
  — RETIRAR PESQUISA DE INSATISFAÇÃO
- Exemplo: [PRC-152662](https://contabilizeicontabilidade.atlassian.net/browse/PRC-152662)
  — Exclusão pesquisa CSAT (cliente questiona a quantidade de CSAT enviada em cada interação; só CSAT)

## Primeiro passo: separar CSAT de NPS

CSAT e NPS são ambos uma "pesquisa" para o cliente, então é preciso entender
**qual** ele não quer receber — a solução é diferente.

### Somente CSAT → `blocklist` do `experts-service`

- Inserir o CNPJ (ou `id_processo_abertura`) na tabela `blocklist` do repositório `experts-service`.
- O motor de CSAT (`RunSurveyCsatEngineConsumer`, em
  `src/consumers/survey-csat/run-survey-csat-engine`) consulta
  `BlocklistService.includes()` em `resolveContext()` e interrompe o envio
  quando o identificador está na tabela.
- Também é consultada nos fluxos de follow-up (`csat-fup.service.ts`) e
  transbordo (`process-ticket-jira-closed.usecase.ts`).

### CSAT **e** NPS → opt-out do `contato-service`

- Usar o opt-out pelo front admin:
  `https://admin.ctbz.com.br/api/atendimento-canais/contatos/empresas`
- É o opt-out do `contato-service`, consumido pelo `atendimento-zendesk`
  (envio de ativo WPP).

### Validação no código (2026-11-18)

- **WhatsApp — consome o opt-out.** Todo ativo passa pelo `VerificarOptoutWhatsappAtivoService` do `atendimento-zendesk` (no worker `enviar-ativo`, comum aos caminhos individual, zendeskapp, legacy e massivo), que consulta o `contato-service` por telefone + empresa. A finalidade é `SURVEY` quando o template é do squad `SURVEY` ou a `categoria` é `WORKER_CSAT`/`NPS` (`optout-purpose.ts`). Cobre o CSAT do `experts-service` (legado) e do `survey-service` (ambos mandam `categoria: 'WORKER_CSAT'`) e o NPS (templates do squad `SURVEY`). Bloqueado, o ativo termina com status `BLOQUEADA_OPTOUT`.
- **E-mail — preparado, mas sem envio hoje.** O `survey-service` monta o e-mail com `optout_purpose: 'SURVEY'` + `cnpj` e o `email-service` consulta o `contato-service` antes de enviar (ver [[contrato-optout]]), mas o canal está desligado de propósito (`EMAIL_PROFILE` nulo para CSAT e NPS). Exceção: pesquisa de processo de abertura (sem CNPJ) iria sem `optout_purpose`. O `experts-service` não envia CSAT por e-mail.
- Para valer, o opt-out precisa ser `SURVEY` no canal certo, com a empresa (ou legado sem empresa) e `scope` do contato (`ADDRESS`); o de grupo (`COMPANY`) é ignorado.

### Quem dispara o NPS (2026-11-18)

Não existe serviço "experts-nps" que envie pesquisa: o `experts-ms-nps` só grava a resposta (`nps.p2p.save` → plataforma) e o `invite-nps-whatsapp` só gera a base de disparo (scripts/Streamlit). O envio do NPS de Experts (`nps_exp_2025_03a`, squad `SURVEY`) é feito **à mão, em massa, pelo app do Zendesk** (autores como `bruno.magalhaes`, `lucas.amato`, `debora.pacanaro`), e o NPS de onboarding (`bp_nps_abertura_v1`, `experts_nps_migracao_v1` etc.) sai automático do monolito `contabilizei-back-core` (`NpsFacade` + `EnvioAtivoWhatsappNpsClient`, `autor: Onboarding`, `squad: ONBOARDING`, `integracao: SURVEY`, `categoria: NPS`, template por plano e momento: abertura, migração, transformação). A resposta volta pelo bot do Ultimate (`Wpp Survey | Pesquisas NPS Router`) → `atendimento-zendesk` (`whatsapp-fluxo-nps`, Cloud Task `pesquisa-nps-whatsapp`) → `experts-ms-nps` (`/v1/salvar/nps`) → `nps.p2p.save` → plataforma. Tudo passa pelo worker do `atendimento-zendesk`, então o opt-out `SURVEY` vale. Templates antigos de NPS do squad `EXPERTS` (ex: `experts_nps_novembro`) **não** seriam tratados como `SURVEY` (cairiam em `MARKETING`/`TRANSACTIONAL` pela categoria da Meta) se voltassem a ser usados pelo app.

### NPS que o opt-out `SURVEY` não bloqueia (levantamento 2026-11-18)

A finalidade sai do template (squad `SURVEY` ou categoria `NPS`/`WORKER_CSAT` → `SURVEY`; senão categoria Meta `MARKETING` → `MARKETING`; resto → `TRANSACTIONAL`). Dos ~492 mil envios de templates `%nps%` no `mensagem_ativa`, **13.673 não cairiam no opt-out `SURVEY`** (11.950 `MARKETING`, 1.723 `TRANSACTIONAL`), todos de templates do squad `EXPERTS` ou `CORRETORA`:

- `squad-crm-hubspot` (automação do HubSpot via atendimento-zendesk): `experts_npsguerilha_*`, `experts_nps_crm330`, `exp_crm1223_ativosnps`, `crm802_promotores_nps` (11/2025 a 07/2026) — outra origem de NPS além das três da seção acima.
- `quezia.martins` (corretora): `fideliza_d30_nps`, `fideza_d60_nps2` (até 09/10/2026).
- Contas manuais em 2024/início de 2025 (`contabilizei4`, `patricia.holtz`, `lorenzo.ferreira` etc.): `experts_nps_setembro/outubro/novembro/dezembro/auto`.

Ampliando para CSAT e outras pesquisas (nomes com `csat`, `pesquisa`, `satisfa`, `survey`, `feedback`, `avalia`): de ~1,07 mi envios, 14.431 ficam fora do `SURVEY` — além dos de NPS, `BANK` (`testebank_nf_pesquisa_quant`, `cbank_pesquisa_de_cancelamento_de_conta_br`), `CORRETORA` (`pesquisa_*` de benefícios, leticia.salgado) e CSAT manual com template `EXPERTS` (`tratativacsat`, marcio.silveira, 27/10/2026). Página com o relatório por time, autor e template: https://claude.ai/artifact/TNkJBn1NwdNBMTKnet2733. Na `mensagem_ativa`, `count(distinct destino)` com regex no template estoura o `statement_timeout` de 30 s de prod: filtrar por `template in (select nome from mensagem_ativa_template where nome ~* ...)` e agregar sem distinct.

Cruzando com os opt-outs de WhatsApp, nenhum desses envios furou um opt-out `SURVEY` que já existia na data. **Depois de a validação entrar em prod (19/08/2026, PR #772, release 0.698), houve 913 envios de pesquisa com template errado: 910 da corretora (quezia.martins, `fideliza_d30_nps` 767 e `fideza_d60_nps2` 143, até 09/10), mais 1 `tratativacsat` (marcio.silveira, 27/10), 1 `convite_pesquisa` (marrara.markevis, 06/10) e 1 `csat_experts_resolucao_1` (teste). As campanhas do HubSpot pararam antes (07/2026).** Para essas campanhas respeitarem o opt-out de pesquisa, o template precisa ir para o squad `SURVEY` (ou o disparo mandar `optoutPurpose: SURVEY`).

### Requisitos para o ativo cair no opt-out `SURVEY` (validado em 2026-11-18)

Finalidade, nesta ordem: `optoutPurpose: "SURVEY"` no payload (precedência; **não é gravado** na `mensagem_ativa`, então não dá para auditar pelo banco), ou squad do template cadastrado = `SURVEY`, ou `categoria` = `NPS`/`WORKER_CSAT`. `integracao`, `squad` do envio, `autor`, `tipo` e `fila` não influenciam. O opt-out é achado por `destino` (`+55…`) + `docTipo`/`docValor` (`cnpj` sem máscara ou `processo_abertura_id`); bloqueia manifestação `optedOut: true` com `scope: ADDRESS` → `BLOQUEADA_OPTOUT` / `OPTOUT_DO_TITULAR`. A checagem roda depois da validação do template (template inativo vira `ERRO` antes), é falha aberta (erro ou >3 s no contato-service → envia) e o contato-service tem cache de 5 min. Em prod, de 06/10 a 18/11/2026, os 16 `BLOQUEADA_OPTOUT` e os 63 envios para os 25 telefones com opt-out bateram com a regra (os avisos de guias barrados vêm do `optoutPurpose: TAX` do agrupamento).

### Armadilha: o opt-out é por par telefone + empresa

A consulta usa o `doc_valor` do envio como `companyCode`. Cliente com várias empresas e vários telefones precisa de **uma manifestação para cada par (telefone, CNPJ)** que já recebeu pesquisa, não só do telefone principal de cada empresa. Antes de fechar a PRC, levantar os pares no banco do atendimento-zendesk (`prd_crm_atendimento_zendesk`):

```sql
select m.destino, m.doc_valor, m.template, m.categoria, max(m.criado_em)
from mensagem_ativa m
where (m.doc_valor in ('<cnpj1>','<cnpj2>') or m.destino in ('+55<tel1>','+55<tel2>'))
  and (m.template ilike '%nps%' or m.template ilike '%csat%' or m.categoria in ('WORKER_CSAT','NPS') or m.squad = 'SURVEY')
group by 1,2,3,4 order by 5 desc;
```

Caso real: [PRC-154915](https://contabilizeicontabilidade.atlassian.net/browse/PRC-154915) (SHOWCALLERS, 2026-11-11), ACR [[PRD-178071]] (a PRC fica vinculada a ela, não à PRD-168944). O opt-out foi gravado para `+5521969095343`/`53848191000102` e `+5521981597842`/`09322027000175`, mas o NPS já tinha ido para `+5521981597842`/`53848191000102` e o CSAT para `+5521969095343`/`54337616000181`, pares que ficaram sem opt-out. Nenhuma pesquisa saiu depois do cadastro (13/11), e o email-service nunca enviou pesquisa (só guias).

## ACR para vincular

PRCs que caem nesse problema devem ser vinculadas à ACR:
[PRD-168944](https://contabilizeicontabilidade.atlassian.net/browse/PRD-168944)
— [ACR] Adicionar CNPJs à blocklist de CSAT de clientes que não querem receber

## Como vincular e fechar a PRC

- Link: tipo `Problem/Incident`, com a PRC **is caused by** a ACR do caso (PRD-168944, ou uma ACR específica como a PRD-178071) (no `createJiraIssueLink`: `inwardIssue` = PRD-168944, `outwardIssue` = PRC).
- Saindo de `To-do`, passar antes por `Started` (61, → Em Andamento); a `Solved` (121, → Concluído) só aparece depois e exige 7 campos. Valores usados nas PRCs desse problema (copiados da PRC-146015):
  - Classificação do chamado (N3) (`customfield_18430`): Experts - CRM → WhatsApp - Comportamento não esperado (`39474` / `41165`)
  - Devido ou Indevido? (`customfield_19805`): Devido (`22182`)
  - Funcionalidade (`customfield_18681`): Atendimento - WhatsApp (`28568`)
  - Grau do Impacto (`customfield_19493`): Alto - Impactou Operação (`20700`)
  - Ofensor do Chamado (`customfield_21097`, labels): `csat_zendesk`
  - Resolução do chamado (`customfield_18429`): Resolvido diretamente pela plataforma (`17922`)
  - Tipo de chamado (`customfield_18460`): Suporte a operação (`18048`)
