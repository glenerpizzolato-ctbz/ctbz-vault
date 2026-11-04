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
atualizado_em: 2026-10-28
---

# Notificação individual de guias (experts-service) x agrupamento

## Fluxo individual (experts-service)

`GuiaImpostoNotifierConsumer` (tópico `processar-guia-imposto`, sub `experts-service.sub.guia-imposto`) agenda WhatsApp (`experts_guia_imposto`, seg–sex 9h–18h) e e-mail ("Sua empresa tem uma nova guia de imposto disponível") no `task_scheduler` (`event_source_type = guia-imposto-notifier`). Filtros em ordem:

1. Status ≠ `PENDENTE` → cancela a task da guia e sai.
2. Só plano que contém "expert" e regime `LUCRO_PRESUMIDO` ou `SIMPLES`; precisa de telefone; `dataParaPagamento` no futuro.
3. Imposto "do agrupamento" pela lista do próprio experts-service (`handlerLucroPresumido`: COFINS, IRPJ, CSLL, IRPJ_16, IRPJ_32, FGTS, PIS, DARF_UNIFICADO, IRPJ_COMPL; `handlerSimplesNacional`: FGTS, SIMPLES, DARF_UNIFICADO). Se for, `shouldSchedule`: competência ≠ atual → notifica; dia < 15 → não notifica; dia ≥ 15 → só notifica se `GET /agrupamento-guias/enviou-notificacao-agrupamento/WHATSAPP/idEmpresa/{id}` do microsservico-agrupamento-guias disser que o grupo da competência já foi notificado com sucesso.
4. `alreadySent(cnpj)`: não agenda se já existe task não enviada ou criada/enviada hoje para o CNPJ (dedup diário por empresa, não por guia).

## Lado do agrupamento (microsservico-agrupamento-guias)

- Agrupáveis em `ImpostoPermiteAgrupamento` (SIMPLES, INSS*, DARF_INSS, IRRF*, CSRF, PIS, COFINS, IRPJ*, CSLL, DARF_UNIFICADO, FGTS ≥ 202403, FGTS_CONSIGNADO). **ISS não é agrupável hoje.**
- Grupo notificado uma vez por canal (elegíveis excluem quem já tem `controle_notificacao` com sucesso).
- Guia nova/alterada depois do agrupamento (competência atual, antes do vencimento, imposto agrupável): grupo em `SUCESSO_AGRUPAMENTO` vira `ERRO_NOVA_GUIA`/`ERRO_GUIA_ALTERADA` (depois `ERRO_GUIA_ALTERADA_RECORRENTE`), sem reprocessar o PDF nem renotificar. Só grupo em erro de processamento ou `GUIAS_AGUARDANDO_GERACAO` é reprocessado (`grupoGuiaService.reprocessar`). Grupo `AGRUPAMENTO_SEM_GUIA` ignora a guia nova.

## Armadilhas da convivência (análise de 2026-10-28)

- **Listas divergentes**: o agrupamento inclui INSS*, IRRF*, CSRF, DARF_INSS e FGTS_CONSIGNADO, que o experts-service não considera "do agrupamento" → essas guias recebem notificação individual **e** entram no agrupamento (duplicidade).
- **Guia nova depois do envio do grupo**: experts-service notifica individualmente (porque o grupo já foi enviado) e o grupo vai para `ERRO_NOVA_GUIA` sem incluir a guia no PDF. Não há renotificação do grupo, mas também não há "adicionar ao agrupamento".
- **Buraco de silêncio**: imposto agrupável, dia ≥ 15, e grupo nunca notificado (`AGRUPAMENTO_SEM_GUIA`, `GUIAS_AGUARDANDO_GERACAO` preso, opt-out/falha no WhatsApp) → nenhum dos dois notifica a guia.
- **Migração**: o agrupamento-guias-service removeu `enviou-notificacao-agrupamento`; na virada, a chamada do experts-service quebra (erro → nack até 5 tentativas → ack), e as guias agrupáveis da competência atual a partir do dia 15 deixam de ser notificadas.
- **ISS pós dia 20 no agrupamento**: exige mudar os dois lados (regra por vencimento em `ImpostoPermiteAgrupamento` e nos handlers do experts-service), senão o ISS sai individual e no grupo.

Relacionado: [[notificacao-agrupamento-experts-bp-lp]], [[arquitetura-e-migracao]].

## Opt-out (PRD-174790)

- O e-mail da notificação individual (`schedule-notification-email-task.service.ts`) leva `optout_purpose: 'TAX'` e `cnpj` no payload do `email-service`, normalizado com `normalizeCnpj` (`src/domain/utils/cnpjValidator.ts`), que tira a máscara e mantém as letras do CNPJ alfanumérico. Não usar `replace(/\D/g, '')`, que apaga as letras (ver [[contrato-optout]]). Com isso, o `email-service` consulta o opt-out de e-mail no `contato-service` e pode devolver `BLOCKED_OPTOUT`. O WhatsApp (`schedule-notification-wpp-task.service.ts`) já mandava `optoutPurpose: 'TAX'`.
- O repositório usa **pnpm** (`pnpm-lock.yaml`): numa worktree nova, rodar `pnpm install --frozen-lockfile` (o `npm ci` falha por falta de `package-lock.json`).
