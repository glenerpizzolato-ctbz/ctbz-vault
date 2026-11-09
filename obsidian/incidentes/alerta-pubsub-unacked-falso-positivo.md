---
name: alerta-pubsub-unacked-falso-positivo
description: "Por que o alerta do Cloud Monitoring 'Cloud Pub/Sub Subscription - Unacked messages' (contabilizei-experts-prd) dispara falso-positivo nas rajadas do processar-guia-imposto, como ler o valor (116.733 = 116,7, não 116 mil) e a proposta de trocar por idade da mensagem mais antiga > 15 min"
metadata:
  type: reference
tags:
  - incidentes
  - alertas
  - pubsub
  - experts-service
---

# Alerta "Cloud Pub/Sub Subscription - Unacked messages" (falso-positivo)

## Onde fica

- É uma policy do **Cloud Monitoring** (não do Grafana) no projeto `contabilizei-experts-prd`: `projects/contabilizei-experts-prd/alertPolicies/8855052505336933525`, severidade WARNING, criada e editada por último por Gabriel Ganassin (2026-05-20).
- Notifica o espaço **Engenharia Canais | Alertas** (`AAAA22umHGg`, seção "Alerts - prod") pelo app "Google Cloud Monitoring". O mesmo espaço recebe "GCP Alerts" (incidentes de memória do `experts-api-gateway` etc.) e o Henrique responde com a investigação automática (app "Alert Investigator", Claude).
- Existe uma irmã desligada, `...alertPolicies/13680671101102890422` ("- Error", média de 5 min > 100).
- A conta do Glener tem `monitoring.alertPolicies.update` no projeto (verificado em 2026-11-06).

## Regra atual e por que dá falso-positivo

- Condição: `pubsub.googleapis.com/subscription/num_undelivered_messages`, `ALIGN_MEAN` em **7200s**, `> 100`, `duration 0s`, sem filtro de assinatura (vale para todas as do projeto).
- **Leitura do valor:** a mensagem do Cloud Monitoring usa 3 casas decimais, então "threshold of 100.000 with a value of 116.733" é **116,7 mensagens** (média de 2h), não 116 mil. A investigação automática de 2026-11-06 leu como 116 mil.
- O tópico `processar-guia-imposto` (fintech) manda rajadas de 2 a 4 mil mensagens para `experts-service.sub.guia-imposto`. O consumidor drena em menos de 5 min (mensagem mais antiga ≤ 288 s), mas uma rajada de 3.872 já puxa a média de 2h acima de 100. Foi o caso de 05/11 (04:32 → 09:09) e 06/11 (07:23): sem atraso real para o cliente.

## Casos reais em 30 dias (07/10 a 06/11/2026)

Medindo a idade da mensagem mais antiga sem ack (`oldest_unacked_message_age`):

| Assinatura | Quando | Duração (idade > 10 min) | Idade máx. | Backlog máx. |
| --- | --- | --- | --- | --- |
| `experts-service.sub.guia-imposto` | 09/10 13:35 UTC | 35 min | 34 min | 25 mil |
| `experts-service.sub.guia-imposto` | 14/10 09:20 UTC | ~4 h | 2,7 h | 157 mil |
| `experts-service.sub.guia-imposto` | 01/11 10:35 e 16:05 UTC | 2 h e 1 h | 54 min | 98 mil |
| `experts-service.sub.plataforma-alteracao-plano` | 07/10 → 10/10 | 3,5 dias | 4 dias (retenção) | 2 |
| `relatorio-faturamento.p2p.processing-sub` | 28/10 21:25 UTC | ~15 min | 29 min | 2 |

O caso do `plataforma-alteracao-plano` (2 mensagens presas até expirar) passa batido pela regra atual, que só olha volume.

## Aplicado em 2026-11-06 12:46 UTC (Glener)

- A condição da policy `8855052505336933525` foi trocada para `oldest_unacked_message_age` `ALIGN_MAX` 300s `> 900` com `duration 600s` (nome da condição: "Cloud Pub/Sub Subscription - Mensagem mais antiga sem ack > 15 min"). O nome da policy, o canal (`notificationChannels/6388798739835665203`), a severidade WARNING e o `autoClose` 1800s foram mantidos. Antes, depois e a proposta: `policy-antes.json`, `policy-depois.json` e `policy-proposta.json` em `~/.local/share/bahcode/features/f1793965969214.doc/`. Para reverter: `gcloud alpha monitoring policies update ... --policy-from-file=policy-antes.json`.
- Com a regra antiga foram 10 incidentes em 30 dias, todos do `guia-imposto`. Só 4 coincidem com atraso real (09/10, 14/10, 01/11 manhã e tarde). Os outros 6 (10/10, 21/10, 25/10, 01/11 noite, 05/11, 06/11) foram rajadas que drenaram em minutos. Os incidentes ficam em `GET https://monitoring.googleapis.com/v3/projects/contabilizei-experts-prd/alerts?filter=policy.name="..."`.
- Logo depois de aplicar, nenhuma das 64 assinaturas estava com mensagem acima de 900 s (a máxima era 2 s), então nada abriu.

## Ocorrências com a regra nova

- **2026-11-09 15:39 BRT (18:39 UTC), `experts-service.sub.guia-imposto`, idade 1.244 s → máx. 2.056 s (34 min); normalizou às ~16:12 BRT.** Alerta verdadeiro, sem falha: o fintech publicou de uma vez ~63 mil guias `PENDENTE` (quase tudo `SIMPLES` e `DARF_UNIFICADO`, com `clock` entre 15:10 e 15:40 BRT, geração em massa da competência), e a entrada (~26 msg/s) passou da vazão do consumer. O backlog chegou a 31 mil às 15:35 BRT. O HPA subiu de 2 para 5 pods e a vazão foi de ~6 para ~23 msg/s, com CPU em ~10% do limite, sem nack relevante, sem DLQ e com só 3 ack deadlines expirados. O gargalo é o `flowControl` do `GuiaImpostoNotifierConsumer` (`maxMessages` = `CONSUMER_GUIA_IMPOSTO_NOTIFIER_MAX_MESSAGES`, padrão 3, `maxStreams: 1`): poucas mensagens em paralelo por pod num trabalho de I/O. O efeito para o cliente é um atraso de até ~34 min na notificação das guias Expert, e a maior parte da rajada nem é Expert ("is not experts plan").
- Ajuste do `maxMessages` registrado no work-item https://gitlab.com/ctbz/experts/backend/experts-service/-/work_items/18 (2026-11-09).
- Sem acesso às métricas do tópico em `fintech-228118` (403): a entrada é estimada como acks + crescimento do backlog da assinatura.

## Proposta (backtest em 30 dias)

- Trocar para `oldest_unacked_message_age`, `ALIGN_MAX` em 300s, `> 900` (15 min) com `duration 600s`. A policy original e a proposta ficam em `~/.local/share/bahcode/features/f1793965969214.doc/policy-antes.json` e `policy-proposta.json`. Aplicar com `gcloud alpha monitoring policies update projects/contabilizei-experts-prd/alertPolicies/8855052505336933525 --policy-from-file=policy-proposta.json`.
- No backtest dispara só nos casos reais acima (os 4 do guia-imposto, o plataforma-alteracao-plano e o relatorio-faturamento) e em nenhuma das rajadas que drenam sozinhas.
- Variações testadas: `> 600s por 10 min` acrescenta o `experts-nfs.sub.nfs-concluida` (08/10); `> 1800s por 5 min` perde o relatorio-faturamento.

Relacionado: [[abertura-automatica-ip-grafana]], [[notificacao-individual-guias-x-agrupamento]].
