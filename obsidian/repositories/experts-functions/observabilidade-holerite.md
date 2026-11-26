---
name: experts-functions-observabilidade-holerite
description: "Erros possíveis no fluxo do e-mail de holerite (function-email-holerites → html-to-pdf → email-service), o que já é visível e propostas de alerta no Google Chat; inclui o ackDeadline de 10 s da sub push que reentrega 8% das requisições (holerite duplicado)"
metadata:
  type: reference
tags:
  - experts-functions
  - email-service
  - observabilidade
  - alertas
analisado_em: 2026-11-24
---

# Observabilidade do e-mail de holerite

Levantamento de 24/11/2026 (PRD-178571), com o fluxo novo pelo email-service.

## Achados medidos em prd (30 dias até 24/11/2026)

- `POST /rhc/folha/notificar` da `function-email-holerites`: 2.301 requisições, sendo 202 = 2.004, **503 = 243** e **500 = 54** (os 500 são da regressão do html-to-pdf em 28/10, ver [[build-e-imagem]]).
- Latência: p50 1,9 s, p90 7,7 s, p99 22,9 s, máximo 99,9 s. **8% (177) passam de 10 s.**
- A subscription push `eventarc-us-central1-email-holerites-sub-224` tem `ackDeadlineSeconds: 10`, backoff de 10 a 600 s, retenção de 24 h e **nenhuma DLQ**. Em push, o ack deadline é o prazo da resposta: quem passa de 10 s é reentregue enquanto ainda processa, e o responsável recebe o holerite **em dobro**. É uma causa provável de parte dos ~40% de empresas que receberam mais de uma vez. Com o email-service, a duplicata também vira dois envios.
- Canais de notificação existentes:
  - `contabilizei-experts-prd`: `[chat] Alertas - GCP Experts` (tipo `google_chat`, nativo), além de webhooks como "Google Chat Experts Alerts" e "#Experts - GCP Alerts".
  - `atendimento-canais-prd`: "GCP Alerts (CANAIS)", com as policies do email-service (DLQ, mensagem antiga sem ack, SMTP indisponível).

## Mapa de falhas

| Salto | Falha | Comportamento hoje | Visível? |
|---|---|---|---|
| fopag-worker → tópico | publish falha / worker não publica | admin não recebe erro do e-mail | não |
| Pub/Sub → function | 503 (instância/escala), resposta > 10 s | reentrega (duplica quando > 10 s) | não alertado |
| Pub/Sub → function | falha permanente (payload ruim, config, permissão) | reentrega por 24 h e depois some | não (sem DLQ) |
| function → html-to-pdf | 5xx/timeout | rethrow, 500, reentrega | log ERROR, sem alerta |
| function → file-upload / send-email | PERMISSION_DENIED, tópico, env faltando, PDF > 10 MB (Buffer.toJSON infla ~3,5x) | `EmailServicePublishError`, 500, reentrega 24 h | log ERROR, sem alerta |
| email-service validação | template inativo/inexistente, variáveis, payload | callback INVALID_PAYLOAD + card no chat CANAIS | sim (card CANAIS) |
| email-service opt-out | responsável com opt-out TRANSACTIONAL | BLOCKED_OPTOUT, holerite não sai | não (desfecho "esperado") |
| email-service dispatch | anexo ausente, SMTP 421/5xx, REJECTED | retry ou FAILED; card só para alguns motivos | parcial |
| entrega | bounce, spam | só no painel SMTP da HubSpot (portal 47852359) | não |

## Propostas (ordem de prioridade)

1. **Subscription própria com `ack_deadline_seconds = 600` e DLQ**: tirar a dependência da sub do Eventarc e ter `dead_letter_policy` com `max_delivery_attempts`.
2. **Alerta de DLQ e mensagem velha**: `subscription/num_undelivered_messages` > 0 na DLQ e `oldest_unacked_message_age` > 30 min na sub de trabalho, para o canal `[chat] Alertas - GCP Experts`. Mesmo padrão do email-service.
3. **Alerta por log** (log-based alert, com o texto do log no card): `ERROR [function-email-holerites]` no `function-email-holerites`, com CNPJ e período, e erro no `function-html-to-pdf`. Limitar a 1 notificação a cada 30 min.
4. **5xx do Cloud Run**: `run.googleapis.com/request_count` com `response_code_class=5xx` para `function-email-holerites` e `function-html-to-pdf`, acima de X% em 10 min.
5. **Desfecho no email-service** (FAILED, BLOCKED_OPTOUT e PENDING > 1 h com `application = function-email-holerites`). Duas saídas:
   - genérica: o card do email-service passa a cobrir FAILED por aplicação;
   - local: resumo diário no chat, a partir da cópia CDC do `email_replications` no BigQuery (D-1), por scheduled query ou job.
6. **Resumo semanal no chat** (opcional): enviados, falhas, opt-out e reenvios por empresa. Hoje a métrica só sai dos logs.

Grafana: painel com volume diário, latência p90/p99, 5xx e status por `email_replications` (fonte Cloud Monitoring + BigQuery). Serve para acompanhar a tendência, mas o aviso de falha fica melhor no chat.

## P1 implementada: subscription própria com DLQ (2026-11-24)

- [experts-functions!11](https://gitlab.com/ctbz/experts/backend/experts-functions/-/merge_requests/11) (branch `feat/PRD-178821`, sub-task PRD-178822, draft): `function-email-holerites-sub` (push com OIDC da `var.eventrc_sa`, ack 600 s, backoff 10–600 s, DLQ com 10 tentativas, sem expiração), tópico `functions.email-holerites.dlq` + pull `functions.email-holerites.dlq-sub` (7 dias), IAM do service agent do Pub/Sub e remoção do `google_eventarc_trigger.trigger_email_holerites` no mesmo MR. Variável nova `project_number` (prd `754947058455`, dev `416872398669`).
- O handler lê `request.body.message`, o push padrão com wrapper: trocar o Eventarc por push próprio não exige mudança de código.
- Armadilha: a SA de deploy do repo (vault-roleset `gcp-roleset-bb_pipelines/contabilizei-experts-{dev,prd}/pipeline-container.hcl`) tem `roles/pubsub.editor`, que **não** tem `setIamPolicy` em tópico/subscription; os `google_pubsub_*_iam_member` falham com 403 até liberar (ex: `roles/pubsub.admin`). Em prd ela já tem `roles/monitoring.alertPolicyEditor` e `notificationChannelViewer` (base da P2–P4); em dev, não. Em prd o service agent do Pub/Sub já tem `roles/pubsub.editor` no projeto; em dev só `roles/pubsub.serviceAgent`.
- Em dev, aplicado em 2026-11-24 (pipeline 3109977522): `function-email-holerites-sub` ativa (ack 600 s, DLQ 10), DLQ criada, trigger removido; os 2 IAM falharam com 403 (`Error retrieving IAM policy`), então o encaminhamento para a DLQ não funciona em dev até liberar a permissão. Solução: os bindings saíram do Terraform (commit `e11fc72`) e a permissão vai no próprio service agent pelo vault-roleset ([vault-roleset!728](https://gitlab.com/ctbz/devops/recursos/vault-roleset/-/merge_requests/728), PRD-178846, só dev; prd já tem `roles/pubsub.editor`), sem `roles/pubsub.admin` na SA de deploy.
- Armadilha: criar a sub nova e destruir o trigger no mesmo apply roda em paralelo, sem ordem garantida; rodar o `deploy-prd` fora do horário de liberação de folha.

Relacionado: [[templates-mandrill-holerite-e-guias]], [[e2e-holerite-dev]], [[alertas-de-envio]], [[PRD-178571]].

## P1 em prd (2026-11-25)

- `deploy-prd` da pipeline 3110577602 (experts-functions!11) criou `function-email-holerites-sub` (ack 600 s, DLQ `functions.email-holerites.dlq` com 10 tentativas) e `functions.email-holerites.dlq-sub`. O trigger do Eventarc continua até o MR de remoção.
- Primeiro envio depois do deploy (19:48 UTC): 1 evento virou **3 e-mails**. A sub nova entregou 1 vez (`push_request_count` ack=1, ~10,5 s, sem reentrega); a do Eventarc deu `deadline_exceeded` (>10 s) e reentregou 23 s depois.
- Como validar qual subscription entregou: o log da function não diz (User-Agent `APIs-Google` nas duas); usar a métrica `pubsub.googleapis.com/subscription/push_request_count` por `subscription_id` e `response_class` (atraso de 2 a 4 min). Script de monitor usado: logs "Holerites enviados por email" + essa métrica + `num_undelivered_messages` da DLQ.
- Até remover o trigger, todo holerite em prd sai no mínimo em dobro (em triplo quando a function passa de 10 s).

## Duplicados medidos em prd (26/10 a 25/11/2026)

- 1.913 e-mails para 1.377 folhas (CNPJ + período); **267 duplicados técnicos (14%) em 211 folhas (15,3%)**, mediana de 14 s entre o envio e a cópia. Out (26–31): 8,5% das folhas; nov (1–25): 21,6%.
- Duplicado técnico = nova cópia da mesma folha até 15 min depois (reentrega); >15 min = reenvio posterior (nova liberação, fora da conta).
- Como refazer (ex: para medir depois da remoção do trigger): exportar `gcloud logging read '... "Holerites enviados por email"' --freshness=31d --format=json`, rodar `scripts/holerite_duplicados_classifica.py <json> <dir>` e `uv run --with openpyxl --with matplotlib python scripts/holerite_duplicados_planilha.py <dir>` (planilha + gráfico semanal). Os logs só guardam 30 dias.
- Planilha, gráfico e PDF dos alertas anexados no PRD-178821.

## Como testar o alerta de DLQ em prd sem impacto (PRD-178824)

Validado em 25/11/2026, com evidências no comentário 30045804 da PRD-178827.

1. Publicar a mensagem de teste **direto no tópico da DLQ**, nunca no `functions.email-holerites`. Ela não chama a function nem envia e-mail:
   `gcloud pubsub topics publish functions.email-holerites.dlq --project contabilizei-experts-prd --attribute=teste=PRD-178824 --message='{"TESTE":"não reprocessar"}'`
2. Em ~3 min, a `num_undelivered_messages` da `dlq-sub` vai a 1. Em ~11 min, o incidente "holerite na DLQ" abre e notifica o `[chat] Alertas - GCP Experts`.
3. Fazer o pull e o ack **só da mensagem de teste**, filtrando pelo atributo `teste`. Antes, conferir se a DLQ tem folha real. Em ~10 min, o incidente fecha.

O alerta "folha parada na fila há mais de 30 min" não se testa em prd: exigiria segurar folhas reais mais de 30 min. Valida-se pela configuração e pela métrica `oldest_unacked_message_age`, que fica em 0 s no dia a dia.

## Como testar os alertas de log ERROR e de 5xx em prd (PRD-178825)

Validado em 25/11/2026, com evidências no comentário 30048729 da PRD-178827.

**Log ERROR**
- Gravar pela API `logging.googleapis.com/v2/entries:write` uma entrada `severity: ERROR` com `resource.type=cloud_run_revision`. Os labels são `service_name=function-email-holerites`, a `revision_name` atual, `location` e `configuration_name`. O `logName` é próprio, ex: `teste-prd-178825`.
- A mensagem segue o formato `… De "<nome> (<cnpj>)", período "<ano>/<mês>"`. Nenhum serviço é chamado.
- O incidente abre em ~20 s, com os labels `cnpj` e `periodo` extraídos.
- **Fechar à mão no console:** alerta por log só fecha sozinho em 1 dia, e enquanto está aberto segura novos incidentes com os mesmos labels.

**Taxa de 5xx**
- Fazer 6 POSTs autenticados (`gcloud auth print-identity-token`) ao `function-html-to-pdf` com um HTML cuja `<img>` aponta para `10.255.255.1`. O puppeteer estoura o timeout de 30 s e o serviço responde 500, sem afetar cliente.
- Ocupa até 6 instâncias por ~40 s.
- O incidente abre em ~5 min e fecha sozinho uns 10 min depois da janela limpar.
- Os `TimeoutError` também abrem o alerta de log ERROR para o `html-to-pdf`.

**Armadilhas**
- O alerta de log abre um incidente por combinação de recurso e labels: abriram 2 em 83 s na mesma policy.
- Logs de auditoria de deploy com ERROR (`UpdateService` "Internal error encountered") também casam com o filtro.
