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
3. Imposto "do agrupamento" pela lista do próprio experts-service (`handlerLucroPresumido`: COFINS, IRPJ, CSLL, IRPJ_16, IRPJ_32, FGTS, PIS, DARF_UNIFICADO, IRPJ_COMPL; `handlerSimplesNacional`: FGTS, SIMPLES, DARF_UNIFICADO). **ISS** (todos os tipos: `ISS`, `ISS_FIXO`, `ISSQN` e `RETENCAO_FONTE_ISS`, lista `IMPOSTOS_ISS`, decisão de 2026-11-12) também conta como do agrupamento nos dois regimes quando `dataParaPagamento` ≥ dia 20 do mês seguinte à competência, 00:00 UTC (`isIssAgrupavel`, `src/domain/guia-imposto/services/iss-agrupamento/`, espelho de `ElegibilidadeGuiaAgrupamento` do MR !98 do agrupamento); com vencimento antes do corte, é notificado na hora como avulso. Se for do agrupamento, `shouldSchedule`: competência ≠ atual → notifica; dia < 15 → não notifica; dia ≥ 15 → só notifica se `GET /agrupamento-guias/enviou-notificacao-agrupamento/WHATSAPP/idEmpresa/{id}` do microsservico-agrupamento-guias disser que o grupo da competência já foi notificado com sucesso.
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
- **ISS por vencimento no agrupamento**: experts-service (MR !152, PRD-176996, branch `feat/PRD-176996`) e agrupamento (MR !98, PRD-175884, `diaMinimoVencimento = 20`) usam o mesmo corte: dia **20** do mês seguinte à competência, `dataParaPagamento`, UTC (chegou a ir para 15 e voltou para 20 em 2026-11-12). Se um lado mudar o dia, o outro tem que acompanhar: com cortes diferentes, o ISS entre os dois dias fica sem notificação ou sai duplicado. A exigência de competência atual vem do `shouldSchedule`, não da regra do ISS. O experts-service só fica correto depois que o agrupamento estiver em produção com o ISS. ⚠️ O experts-service aplica a regra aos 4 tipos de ISS, mas o MR !98 (em 2026-11-12) agrupa só o `ISS` e tem teste garantindo que `ISS_FIXO`, `ISSQN` e `RETENCAO_FONTE_ISS` não agrupam: até o agrupamento incluí-los, essas guias com vencimento ≥ 20 da competência atual ficam sem notificação.

## ISS: quando o cliente não recebe a guia nem no grupo nem avulsa (análise de 2026-11-12, MR !152 + MR !98)

Premissas: o !98 vai para prod antes do !152 e agrupa os 4 tipos de ISS (`ISS`, `ISS_FIXO`, `ISSQN`, `RETENCAO_FONTE_ISS`) com corte no dia 20; os `grupo_guia` são montados **sempre na madrugada do dia 15** (informado pelo Glener em 2026-11-12; o disparo vem do `plataforma-faturamento-worker` via `agrupar-guias-empresa` e não está no catálogo `infra/schedulers.md`).

Fatos conferidos no código (branch do !98):

- O experts-service **não reavalia** guia segurada: dá ack e só volta a olhar se chegar outro evento da mesma guia.
- Crons de notificação só **dos dias 15 a 19**: e-mail Exp SN 03h e 12h, Exp LP 05h e 14h; WhatsApp 09h e 15h. Só pegam grupo em **`SUCESSO_AGRUPAMENTO`** (`GrupoGuiaRepository.buscarGruposGuiaElegiveisNotificacao*`).
- Guia agrupável nova da competência atual com o grupo já em `SUCESSO_AGRUPAMENTO` → grupo vira **`ERRO_NOVA_GUIA`** (`AnalisaAlteracaoDocumento`), sem refazer o PDF. O `reprocessa-erros` só pega `ERRO_SISTEMA` e `ERRO_GERACAO_PDF_AGRUPAMENTO`: grupo em `ERRO_NOVA_GUIA` nunca mais é notificado.
- Grupo `AGRUPAMENTO_SEM_GUIA` ignora guia nova (`controleGuiaAlterado` devolve null).
- `enviou-notificacao-agrupamento/WHATSAPP` só é true com `controle_notificacao` de WhatsApp em SUCESSO (o SUCESSO vem do callback do atendimento-zendesk, não do envio).

Janela segura e janela de risco:

- ISS gerado **até a montagem** (dias 1 a 15 de madrugada): o experts-service segura e o grupo montado no dia 15 já inclui a guia. Sem buraco.
- ISS gerado **depois do WhatsApp do grupo com SUCESSO** (dia 15 a partir de ~09h): o experts-service notifica como avulsa. Sem buraco.
- **Janela de risco: entre a montagem (madrugada do dia 15) e o SUCESSO do WhatsApp do grupo.**

Buracos de silêncio:

1. **ISS gerado no dia 15 entre a montagem e o e-mail das 03h (LP: 05h)**: grupo vira `ERRO_NOVA_GUIA` e não sai em nenhum canal; o experts-service segura (grupo não enviado). O cliente perde o ISS **e o grupo inteiro**.
2. **ISS gerado no dia 15 entre o e-mail e o WhatsApp das 09h**: o e-mail do grupo já saiu sem o ISS, o WhatsApp não sai mais (`ERRO_NOVA_GUIA`) e o experts-service segura (sem WhatsApp com SUCESSO). O cliente recebe só o e-mail, sem o ISS.
3. **ISS gerado entre o disparo do WhatsApp e o callback de SUCESSO** (minutos; ou horas, com `debounceToBusinessHour`): o grupo já foi notificado, vira `ERRO_NOVA_GUIA` sem renotificar; o experts-service segura porque o controle ainda está `AGUARDANDO_NOTIFICACAO`.
4. **WhatsApp do grupo falhou ou opt-out** e ISS chega depois do dia 15 de madrugada: o experts-service segura para sempre (nunca há WhatsApp com SUCESSO) e o grupo, já enviado por e-mail, não renotifica.
5. **Grupo `AGRUPAMENTO_SEM_GUIA`** (sem guia agrupável na madrugada do dia 15) e ISS chega depois: o grupo ignora; o experts-service segura.
6. **Grupo preso em `GUIAS_AGUARDANDO_GERACAO` até depois do dia 19**: as crons não rodam mais; o experts-service segura todas as agrupáveis.
7. **Guia sem `idEmpresa` a partir do dia 15**: `shouldSchedule` segura.
8. **Rota `enviou-notificacao-agrupamento` removida** na migração para o agrupamento-guias-service: erro → nack 5x → ack.

Todos já existiam para os outros impostos agrupáveis; o ISS passa a estar sujeito a eles. Fechar de vez exige o experts-service perguntar se **aquela guia** entrou num grupo notificado (em vez de só "o grupo foi enviado?"), ou o agrupamento incluir/renotificar a guia nova em vez de travar em `ERRO_NOVA_GUIA`.

Sem buraco: vencimento antes do corte (sempre avulsa), competência anterior (notifica na hora), fuso e campo de data (mesmo `dataParaPagamento` e corte UTC nos dois lados).

## `periodoApuracao.periodo` é a competência, não o mês de geração

Conferido em 2026-11-12 na `contabilizei-dataflow.dw_contabilizei_impostos.Guia`: as guias de ISS com `periodoApuracao_periodo = 202610` vencem (`dataParaPagamento`) em 2026-11 e foram criadas entre 2026-10 e 2026-11; as de 202609 vencem em 2026-10 (e uma minoria, recalculada, em 2026-11). Ou seja, o período é o mês de apuração (competência) e o vencimento cai no mês seguinte. É por isso que o corte do ISS é "dia 20 do mês **seguinte** ao `periodo`" (`isIssAgrupavel` no experts-service e `ElegibilidadeGuiaAgrupamento` no agrupamento fazem a mesma conta), e o `shouldSchedule` compara o `periodo` com `getCurrentCompetence()` (mês anterior ao atual).

Distribuição na competência 202610 (prod, 2026-11-12): `ISS` 3.563 guias, 384 com vencimento ≥ dia 20 (~11%); `RETENCAO_FONTE_ISS` 241, 38 ≥ 20; `ISS_FIXO` 40, 1 ≥ 20; `ISSQN` sem volume relevante. A maior parte do ISS continua avulsa.

## Notificação duplicada: guia agrupável de competência futura (2026-11-12)

O `shouldSchedule` libera a notificação avulsa para **qualquer** competência diferente da atual (`periodo !== getCurrentCompetence()`), o que só é correto para competência **passada**. Uma guia agrupável gerada antes de o mês virar (competência futura, ex: ISS de 10/2026 gerado em 16/10, quando a atual ainda é 09/2026) é notificada como avulsa na hora **e** entra no grupo da competência dela, montado na madrugada do dia 15 do mês seguinte. O cliente recebe duas vezes.

Volume em prod (competência 10/2026, guias criadas em outubro com `dataParaPagamento` ≥ 20/11): `ISS` 5 de 384, `RETENCAO_FONTE_ISS` 24 de 44, `ISS_FIXO` 2 de 2. Já acontecia com os outros impostos agrupáveis gerados antes da virada; com o ISS no agrupamento, o `RETENCAO_FONTE_ISS` é o mais afetado.

Correção possível: segurar quando `periodo > competência atual` (só a competência passada notifica na hora). Afeta todos os agrupáveis e herda os riscos de guia segurada (se o grupo falhar, o cliente fica sem a guia).

Relacionado: [[notificacao-agrupamento-experts-bp-lp]], [[arquitetura-e-migracao]].

## Opt-out (PRD-174790)

- O e-mail da notificação individual (`schedule-notification-email-task.service.ts`) leva `optout_purpose: 'TAX'` e `cnpj` no payload do `email-service`, normalizado com `normalizeCnpj` (`src/domain/utils/cnpjValidator.ts`), que tira a máscara e mantém as letras do CNPJ alfanumérico. Não usar `replace(/\D/g, '')`, que apaga as letras (ver [[contrato-optout]]). Com isso, o `email-service` consulta o opt-out de e-mail no `contato-service` e pode devolver `BLOCKED_OPTOUT`. O WhatsApp (`schedule-notification-wpp-task.service.ts`) já mandava `optoutPurpose: 'TAX'`.
- O repositório usa **pnpm** (`pnpm-lock.yaml`): numa worktree nova, rodar `pnpm install --frozen-lockfile` (o `npm ci` falha por falta de `package-lock.json`).
