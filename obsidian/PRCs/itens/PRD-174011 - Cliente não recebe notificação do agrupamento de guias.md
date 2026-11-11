---
name: prc-cliente-nao-recebe-notificacao-agrupamento-guias
description: PRC — cliente diz que parou de receber a notificação mensal do agrupamento (empacotamento) de impostos; conferir o status de cada grupo_guia e o controle_notificacao no ms_agrupamento_guias — em geral o grupo nunca chegou a SUCESSO_AGRUPAMENTO (sem guia ou guias emitidas depois do dia 15), e não uma falha de envio
metadata:
  type: reference
tags:
  - prc
canal:
  - email
  - wpp
dominio:
  - notificacoes
  - impostos
sistemas:
  - microsservico-agrupamento-guias
  - agrupamento-guias-service
acr:
  - "[[PRD-174011]]"
ocorrencias:
  - PRC-151642
qtd_ocorrencias: 1
ultima_ocorrencia: 2026-10-02
---

# Cliente não recebe notificação do agrupamento de guias

## Sintoma

Cliente (Expert) diz que não recebe mais as notificações de "empacotamento" dos impostos mensais (e-mail/WhatsApp com o PDF das guias agrupadas).

## Como investigar

Banco `prd_atendimento_canais_ms_agrupamento_guias` (proxy `sql_atendimento_prd`, porta 5443; ver [[_db-indice|db]]). Achar a empresa pelo nome do responsável ou pelo CNPJ:

```sql
-- empresa pelo nome do responsável (o contato do grupo é jsonb)
select id, id_empresa, cnpj, contato::text from grupo_guia where contato::text ilike '%<nome>%' limit 5;

-- status do agrupamento por competência
select id, periodo_apuracao, status, regime_tributario, plano_pagamento_empresa, created_at, updated_at, path is not null as tem_pdf
from grupo_guia where id_empresa = <id_empresa> order by periodo_apuracao;

-- o que foi notificado
select cn.id, gg.periodo_apuracao, cn.tipo_notificacao, cn.status, cn.motivo, cn.email, cn.celular, cn.data_envio_notificacao
from controle_notificacao cn left join grupo_guia gg on gg.id = cn.grupo_guia_id
where cn.cnpj = '<cnpj>' order by cn.created_at;

-- guias e vencimentos (o que entrou ou não no grupo)
select id, periodo_apuracao, imposto, status, data_para_pagamento::date, created_at, updated_at
from controle_guias where id_empresa = <id_empresa> order by periodo_apuracao, imposto;
```

Só é notificado o grupo da competência anterior em `SUCESSO_AGRUPAMENTO`. Ler o status de cada mês:

| status do grupo | o que significa para a notificação |
| --- | --- |
| `SUCESSO_AGRUPAMENTO` + `controle_notificacao` `SUCESSO` | foi enviado; checar entrega no email-service/WhatsApp ativo pelo `external_id` |
| `AGRUPAMENTO_SEM_GUIA` | nenhuma guia agrupável no dia 15 (ex: só `TFE`, ou nenhuma guia em `controle_guias`): não há o que notificar. Se a plataforma mostra guias naquele mês, o problema é a sincronização das guias com o microsserviço |
| `GUIAS_AGUARDANDO_GERACAO` | no dia 15 havia guia ainda sem PDF. Fica preso para sempre se a guia só sair depois do vencimento ou depois da virada do mês (ver causa) |
| `GUIAS_AGUARDANDO_GERACAO` com `path` preenchido | o grupo foi reprocessado (guia alterada dentro do vencimento) e o PDF chegou a ser gerado com as guias prontas, mas uma guia do grupo continua sem arquivo, então o status volta para aguardando. Procurar no `item_grupo_guia` a guia em `AGUARDANDO_EMISSAO`/sem `id_arquivo` (ex: duplicata órfã do mesmo imposto, ver abaixo) |
| `ERRO_GUIA_ALTERADA*` / `ERRO_NOVA_GUIA` | guias mudaram depois do agrupamento: não há nova notificação com as guias novas |

## Causa (PRC-151642, ELENA KATSORCHIS, CNPJ 03916262000199)

A hipótese do Bolt (controle em `FALHA` bloqueando reenvio pelo `NOT EXISTS` das queries de elegíveis) **não se confirmou**: a cliente não tinha nenhum controle com falha. Os dois envios que existem (202603 e 202609) estão `SUCESSO`. Nos demais meses o grupo nunca chegou a `SUCESSO_AGRUPAMENTO`:

- 202601, 202604, 202605, 202606, 202607: `AGRUPAMENTO_SEM_GUIA` (nenhuma guia agrupável; em 202606 só `TFE`).
- 202602 e 202608: `GUIAS_AGUARDANDO_GERACAO`. Em 202608, PIS/COFINS/DARF só ficaram `REGISTRADO` em 2026-10-02 (com vencimento recalculado para 10-02), já na competência seguinte.
- 202609: notificado em 2026-10-15 (e-mail e WhatsApp); em 10-22 as guias foram canceladas e reemitidas → `ERRO_GUIA_ALTERADA_RECORRENTE`, sem nova notificação.

Por que o grupo `GUIAS_AGUARDANDO_GERACAO` não é retentado (`microsservico-agrupamento-guias`):

- `AnalisaAlteracaoGuiaServiceImpl.possuiImpactoAgrupamento` só reprocessa o grupo quando a guia alterada é da competência atual (mês anterior) **e** hoje é antes do `data_para_pagamento` **e** o imposto é agrupável. Guia emitida depois do vencimento ou depois da virada do mês é ignorada.
- `ReprocessamentoErrosJobImpl` só olha `StatusAgrupamento.errosReprocessaveis()` = `ERRO_SISTEMA`, `ERRO_GERACAO_PDF_AGRUPAMENTO`: `GUIAS_AGUARDANDO_GERACAO` e `AGRUPAMENTO_SEM_GUIA` ficam de fora.

## Como resolver

- Não há data fix em `controle_notificacao` a fazer quando não existe controle com falha. Responder com o histórico por competência (o que foi enviado e por que os outros meses não tinham agrupamento).
- Melhorias possíveis (ACR): retentar `GUIAS_AGUARDANDO_GERACAO` durante o mês (incluir no reprocessamento ou relaxar a regra do vencimento) e decidir com Produto se guias reemitidas depois da notificação geram nova notificação.
- Encaminhamento usado no PRC-151642: comentar a ACR, finalizá-la (transição `Finalizar`, a partir de `Detalhamento`, com "Não foi identificado problema no produto" e Produto e Subproduto `Empacotamento Guias > Notificação guias agrupadas (E-mail/Whatsapp)`) e transferir o PRC para o squad `Fiscal` (na época foi pela transição `Transferido`; hoje a regra é não mudar o status, só trocar o **Assigned Squad**, ver "Transferir um PRC" em [[_prcs-indice]]). Squads de impostos disponíveis: `Fiscal`, `Fiscal Sustentação`, `Fiscal Faturamento (Notas)`, `Reforma Tributária` (não existe squad "Impostos").

## Variação: guia duplicada presa em AGUARDANDO_EMISSAO (empresa 6417390000930816, 202609, investigado em 2026-11-11)

Grupo `732155` (CNPJ 26120247000135, Experts SN) ficou em `GUIAS_AGUARDANDO_GERACAO` e nunca foi notificado, embora tenha `path`. O grupo tem 3 itens: `SIMPLES` (19455277) e `DARF_UNIFICADO` (19507039), ambos `REGISTRADO` com PDF e vencimento 10-27, e uma segunda `DARF_UNIFICADO` (19526831, `id_guia` 6551924603879424, mesmo principal de R$ 495, vencimento 10-20) em `AGUARDANDO_EMISSAO` sem `id_arquivo`, sem atualização desde 2026-10-07 e com `clock` anterior ao da DARF válida. O `EfetivaStatusAgrupamentoServiceImpl` exige que **todas** as guias do grupo estejam com PDF; a duplicata órfã (provavelmente substituída no sistema de impostos sem o evento de cancelamento chegar) trava o grupo. Os reprocessamentos de 10-21 e 10-23 (DARF/DAS recalculadas com multa) mantiveram o status. Correção: confirmar no sistema de impostos o status da guia `6551924603879424` (se cancelada, o evento precisa chegar ao microsserviço ou a guia sair do grupo) e reprocessar o grupo.
