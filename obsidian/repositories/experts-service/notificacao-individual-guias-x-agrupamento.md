---
name: experts-service-notificacao-individual-guias-x-agrupamento
description: "Como o experts-service notifica guias de imposto individualmente (consumer processar-guia-imposto + task_scheduler) e como isso convive com a notificação do agrupamento de guias (regras de dia 15, listas de impostos, ERRO_NOVA_GUIA, dependência da rota enviou-notificacao-agrupamento)"
metadata:
  type: reference
tags:
  - experts-service
  - microsservico-agrupamento-guias
  - notificacao
sistemas:
  - experts-service
  - microsservico-agrupamento-guias
  - agrupamento-guias-service
atualizado_em: 2026-11-12
---

# Notificação individual de guias (experts-service) x agrupamento

## Fluxo individual (experts-service)

`GuiaImpostoNotifierConsumer` (tópico `processar-guia-imposto`, sub `experts-service.sub.guia-imposto`) agenda WhatsApp (`experts_guia_imposto`, seg–sex 9h–18h) e e-mail ("Sua empresa tem uma nova guia de imposto disponível") no `task_scheduler` (`event_source_type = guia-imposto-notifier`). Filtros em ordem:

1. Status ≠ `PENDENTE` → cancela a task da guia e sai.
2. Só plano que contém "expert" e regime `LUCRO_PRESUMIDO` ou `SIMPLES`; precisa de telefone; `dataParaPagamento` no futuro.
3. Imposto "do agrupamento" pela lista do próprio experts-service (`handlerLucroPresumido`: COFINS, IRPJ, CSLL, IRPJ_16, IRPJ_32, FGTS, PIS, DARF_UNIFICADO, IRPJ_COMPL; `handlerSimplesNacional`: FGTS, SIMPLES, DARF_UNIFICADO). **ISS** (só o `ISS`; `ISS_FIXO`, `RETENCAO_FONTE_ISS` e `ISSQN` não) também conta como do agrupamento nos dois regimes quando `dataParaPagamento` ≥ dia 15 do mês seguinte à competência, 00:00 UTC (`isIssAgrupavel`, `src/domain/guia-imposto/services/iss-agrupamento/`, mesmo formato de `ElegibilidadeGuiaAgrupamento` do MR !98 do agrupamento); com vencimento antes do corte, é notificado na hora como avulso. Se for do agrupamento, `shouldSchedule`: competência ≠ atual → notifica; dia < 15 → não notifica; dia ≥ 15 → só notifica se `GET /agrupamento-guias/enviou-notificacao-agrupamento/WHATSAPP/idEmpresa/{id}` do microsservico-agrupamento-guias disser que o grupo da competência já foi notificado com sucesso.
4. `alreadySent(cnpj)`: não agenda se já existe task não enviada ou criada/enviada hoje para o CNPJ (dedup diário por empresa, não por guia).

## Como saber do que se trata cada disparo (qual guia é cada notificação)

Os disparos ficam na tabela `task_scheduler` do banco do experts-service, replicada no BigQuery em `contabilizei-dataflow.dw_experts_service.task_scheduler`. Cada guia gera **duas linhas** (uma de WhatsApp e uma de e-mail), com o mesmo `event_source_id`. Campos:

| Campo | O que é |
| --- | --- |
| `created_at` | Data de criação do registro (agendamento), **não** a data de envio |
| `sent_date` | Data de envio da notificação (no código, `sent_at`) |
| `id` | Id interno do agendamento (técnico, pode desconsiderar) |
| `data` | JSON com o conteúdo necessário para o envio (nome do cliente, e-mail, telefone, template etc.) |
| `is_sent` | Se já foi enviado (`true`/`false`) |
| `topic` | Tópico Pub/Sub em que o disparo é publicado (técnico): `atendimento-zendesk.envio-whatsapp-ativo` = WhatsApp, `email-service.p2p.send-email` = e-mail |
| `event_source_type` | Quem agendou; notificação avulsa de guia = `guia-imposto-notifier` (transbordo e outros usam outros valores) |
| `event_source_id` | **O mais importante: o id da guia.** Cruzando com a tabela de guias, dá o tipo de imposto, competência, vencimento etc. |
| `cnpj` | CNPJ da empresa |

Também existem `retry` e `error` (tentativas e último erro do envio) e `start_date`/`stop_date`/`start_time`/`stop_time` (janela em que o disparo pode sair: WhatsApp seg–sex 9h–18h, e-mail na hora, até 3 dias).

**Descobrir o imposto de cada disparo**: cruzar `event_source_id` com o `id` da guia em `contabilizei-dataflow.dw_contabilizei_impostos.Guia` (campos `imposto`, `tipoImposto`, `periodoApuracao_periodo`, `dataParaPagamento`, `valorPrincipal`, `status`, `guiaAvulsa`, `idEmpresa`). O `id` da `Guia` é INT64 e o `event_source_id` é STRING, então precisa de `CAST`:

```sql
SELECT t.cnpj, t.created_at, t.sent_date, t.is_sent,
       IF(t.topic LIKE '%whatsapp%', 'WHATSAPP', 'EMAIL') AS canal,
       g.id AS id_guia, g.imposto, g.periodoApuracao_periodo AS competencia, g.dataParaPagamento, g.valorPrincipal, g.status
FROM `contabilizei-dataflow.dw_experts_service.task_scheduler` t
LEFT JOIN `contabilizei-dataflow.dw_contabilizei_impostos.Guia` g ON CAST(g.id AS STRING) = t.event_source_id
WHERE t.event_source_type = 'guia-imposto-notifier'
  AND DATE(t.created_at) >= '2026-11-01'
  -- AND g.imposto = 'ISS'   -- ex: só as guias de ISS
```

Validado em 2026-11-12: de 01 a 12/11/2026 o ISS liderava (2.975 linhas), seguido de DARF_UNIFICADO (1.358) e SIMPLES (948); também aparecem RETENCAO_FONTE_ISS, ISS_FIXO, TFE, IRRF_RENDA, MAED_*, GUIA_ASSISTENCIAL e TRSS.

Atalho só para o WhatsApp: desde 2026-09-16 (PRD-167563, commit `543064a`) o `data` do WhatsApp traz `metadados` com `ids_guia`, `tipos_imposto` (ex: `;ISS;`), `competencia`, `vencimento` e `valor_total` (`JSON_VALUE(t.data, '$.metadados.tipos_imposto')`), sem precisar do join. O `data` do e-mail não tem o imposto: para ele, só pelo join.

## Lado do agrupamento (microsservico-agrupamento-guias)

- Agrupáveis em `ImpostoPermiteAgrupamento` (SIMPLES, INSS*, DARF_INSS, IRRF*, CSRF, PIS, COFINS, IRPJ*, CSLL, DARF_UNIFICADO, FGTS ≥ 202403, FGTS_CONSIGNADO). **ISS não é agrupável hoje.**
- Grupo notificado uma vez por canal (elegíveis excluem quem já tem `controle_notificacao` com sucesso).
- Guia nova/alterada depois do agrupamento (competência atual, antes do vencimento, imposto agrupável): grupo em `SUCESSO_AGRUPAMENTO` vira `ERRO_NOVA_GUIA`/`ERRO_GUIA_ALTERADA` (depois `ERRO_GUIA_ALTERADA_RECORRENTE`), sem reprocessar o PDF nem renotificar. Só grupo em erro de processamento ou `GUIAS_AGUARDANDO_GERACAO` é reprocessado (`grupoGuiaService.reprocessar`). Grupo `AGRUPAMENTO_SEM_GUIA` ignora a guia nova.

## Armadilhas da convivência (análise de 2026-10-28)

- **Listas divergentes**: o agrupamento inclui INSS*, IRRF*, CSRF, DARF_INSS e FGTS_CONSIGNADO, que o experts-service não considera "do agrupamento" → essas guias recebem notificação individual **e** entram no agrupamento (duplicidade).
- **Guia nova depois do envio do grupo**: experts-service notifica individualmente (porque o grupo já foi enviado) e o grupo vai para `ERRO_NOVA_GUIA` sem incluir a guia no PDF. Não há renotificação do grupo, mas também não há "adicionar ao agrupamento".
- **Buraco de silêncio**: imposto agrupável, dia ≥ 15, e grupo nunca notificado (`AGRUPAMENTO_SEM_GUIA`, `GUIAS_AGUARDANDO_GERACAO` preso, opt-out/falha no WhatsApp) → nenhum dos dois notifica a guia.
- **Migração**: o agrupamento-guias-service removeu `enviou-notificacao-agrupamento`; na virada, a chamada do experts-service quebra (erro → nack até 5 tentativas → ack), e as guias agrupáveis da competência atual a partir do dia 15 deixam de ser notificadas.
- **ISS por vencimento no agrupamento**: o experts-service (MR !152, PRD-176996, branch `feat/PRD-176996`) usa o corte no dia **15** do mês seguinte à competência (`dataParaPagamento`, UTC), mas o MR !98 do agrupamento (PRD-175884) ainda está com `diaMinimoVencimento = 20` (2026-11-12). Os dois lados precisam do mesmo dia: com cortes diferentes, o ISS entre os dois dias fica sem notificação (segurado aqui e fora do grupo) ou sai duplicado. O experts-service também só fica correto depois que o agrupamento estiver em produção com o ISS.

Relacionado: [[notificacao-agrupamento-experts-bp-lp]], [[arquitetura-e-migracao]].

## Opt-out (PRD-174790)

- O e-mail da notificação individual (`schedule-notification-email-task.service.ts`) leva `optout_purpose: 'TAX'` e `cnpj` no payload do `email-service`, normalizado com `normalizeCnpj` (`src/domain/utils/cnpjValidator.ts`), que tira a máscara e mantém as letras do CNPJ alfanumérico. Não usar `replace(/\D/g, '')`, que apaga as letras (ver [[contrato-optout]]). Com isso, o `email-service` consulta o opt-out de e-mail no `contato-service` e pode devolver `BLOCKED_OPTOUT`. O WhatsApp (`schedule-notification-wpp-task.service.ts`) já mandava `optoutPurpose: 'TAX'`.
- O repositório usa **pnpm** (`pnpm-lock.yaml`): numa worktree nova, rodar `pnpm install --frozen-lockfile` (o `npm ci` falha por falta de `package-lock.json`).
