---
name: cloud-run-servicos
description: "Lista de serviços Cloud Run, Cloud Run functions e jobs por projeto GCP, para localizar onde um serviço roda em dev/prod"
metadata:
  type: reference
tags:
  - infra
  - cloud-run
atualizado_em: 2026-10-09
---

# Cloud Run e functions

Fotografia de 2026-10-09. As Cloud Run functions (gen2) também aparecem como serviço Cloud Run; quando o nome coincide, é o mesmo serviço. Região `us-central1` salvo indicação. Entre parênteses no fim: repositórios que citam o nome.

## atendimento-canais-dev

Atendimento / canais, dev.

- **Serviços**: `agent-eval-dev`, `atalhos-engenharia`, `atendimento-canais-admin-dev` (atendimento-canais-admin), `bots-api` (atendimento-canais-admin, atendimento-zendesk, bots-api, canais-adk, contabilizei-agents, email-service, experts-admin, experts-service, js-libraries, k8s-configmap, kong-config, pipeline, zendesk-agents), `canais-adk-dev` (canais-adk), `pm-calls-dev` (hackaton), `team-kb` (southamerica-east1), `team-kb-ui` (southamerica-east1), `ultimateai-webhook` (pipeline), `webhook-gitlab` (pipeline, webhook-gitlab), `zendesk-proxy-dev`

## atendimento-canais-prd

Atendimento / canais, prod.

- **Serviços**: `agent-eval-prd`, `atendimento-canais-admin-prd`, `bots-api` (atendimento-canais-admin, atendimento-zendesk, bots-api, canais-adk, contabilizei-agents, email-service, experts-admin, experts-service, js-libraries, k8s-configmap, kong-config, pipeline, zendesk-agents), `canais-adk-prd`, `ultimateai-webhook` (pipeline), `webhook-gitlab` (pipeline, webhook-gitlab), `zendesk-proxy-prd`

## contabilizei-experts-dev

Experts, dev.

- **Serviços**: `emissor-whatsapp-reports` (emissor-whatsapp-reports, experts-api-gateway, experts-drawio, pipeline), `experts-alertas` (experts-alertas, experts-bruno, experts-drawio, experts-twilio, pipeline), `experts-api-gateway` (experts-api-gateway, experts-drawio), `experts-async-publisher` (experts-api-gateway, experts-async-publisher, experts-drawio, kong-config, pipeline), `experts-nfs` (aida-back, atendimento-canais-admin, atendimento-zendesk, bots-api, canais-adk, cnpj-alfanumerico, experts-api-gateway, experts-bruno, experts-drawio, experts-nfs, mcp-notas-fiscais, pipeline, zendesk-agents), `experts-zendesk` (experts-api-gateway, experts-drawio, experts-tarefas-assessor, experts-zendesk, pipeline), `function-email-holerites` (experts-dominios-functions, experts-excalidraw, experts-functions), `function-email-sender` (experts-dominios-functions, experts-functions), `function-experts-clientes-emails`, `function-html-to-pdf` (experts-dominios-functions, experts-functions), `html-to-pdf` (experts-dominios-functions, experts-excalidraw, experts-functions, html-to-pdf, ms-relatorio-faturamento, pipeline), `json-hero`

## contabilizei-experts-prd

Experts, prod.

- **Serviços**: `emissor-whatsapp-massivo` (atendimento-zendesk, emissor-whatsapp, experts-api-gateway, experts-drawio, experts-service, experts-twilio), `emissor-whatsapp-reports` (emissor-whatsapp-reports, experts-api-gateway, experts-drawio, pipeline), `experts-alertas` (experts-alertas, experts-bruno, experts-drawio, experts-twilio, pipeline), `experts-api-gateway` (experts-api-gateway, experts-drawio), `experts-async-publisher` (experts-api-gateway, experts-async-publisher, experts-drawio, kong-config, pipeline), `experts-contabil` (experts-contabil, experts-drawio, experts-twilio), `experts-nfs` (aida-back, atendimento-canais-admin, atendimento-zendesk, bots-api, canais-adk, cnpj-alfanumerico, experts-api-gateway, experts-bruno, experts-drawio, experts-nfs, mcp-notas-fiscais, pipeline, zendesk-agents), `experts-twilio-metrics` (experts-api-gateway, experts-drawio), `experts-zendesk` (experts-api-gateway, experts-drawio, experts-tarefas-assessor, experts-zendesk, pipeline), `function-email-holerites` (experts-dominios-functions, experts-excalidraw, experts-functions), `function-email-sender` (experts-dominios-functions, experts-functions), `function-experts-clientes-emails`, `function-html-to-pdf` (experts-dominios-functions, experts-functions), `function-pendencias-oportunidades` (experts-dominios-functions, experts-drawio, experts-functions), `function-zendesk-organizations-update`, `html-to-pdf` (experts-dominios-functions, experts-excalidraw, experts-functions, html-to-pdf, ms-relatorio-faturamento, pipeline)
- **Functions**: `emissor-whatsapp` (atendimento-api-gateway, atendimento-zendesk, canais-adk, cnpj-alfanumerico, contabilizei-agents, emissor-whatsapp, emissor-whatsapp-reports, experts-api-gateway, experts-drawio, experts-nfs, experts-twilio-flows, firestore-to-bigquery, mcp-notas-fiscais, plataforma-crm-web)
- **Jobs**: `emissor-ha-switch`

## aida-stg

AIDA, dev/stg.

- **Serviços**: `ai-pulse-stg`, `aida-back-dev` (pipeline), `aida-back-stg`, `aida-classifier-stg-api` (pipeline), `aida-memoria-stg`, `arquivos-fator-r` (aida-back, pipeline), `atendimento-canais-admin-dev` (atendimento-canais-admin), `central-disparos-stg`, `contabilizei-agents` (canais-adk, cnpj-alfanumerico, contabilizei-agents, k8s-configmap, mcp-notas-fiscais, pipeline, zendesk-agents), `contabilizei-agents-stg`, `contabilizei-armor-stg`, `contador-inteligente-dev-api` (pipeline), `contador-inteligente-off-dev`, `contador-inteligente-off-stg`, `contador-inteligente-stg`, `contador-inteligente-stg-adkweb`, `contador-inteligente-stg-api` (pipeline), `dados-no-op-service`, `file-transcriber` (file-transcriber, monitoria-ia, zendesk-agents), `file-transcriber-stg`, `inbound-outbound-ai-stg`, `knowledge-book-agent-stg`, `monitoria-ia-aggregator` (monitoria-ia), `monitoria-ia-executor` (monitoria-ia), `monitoria-ia-parser` (monitoria-ia), `monitoria-ia-web` (atendimento-canais-admin, monitoria-ia), `notify-guias` (pipeline), `public-file-stg`, `sentinela-atendimento-dev` (pipeline), `sentinela-atendimento-stg`, `upload-file-webhook` (europe-west1), `vector-search-api-stg`
- **Functions**: `arquivos-fator-r` (aida-back, pipeline), `notify-guias` (pipeline)

## aida-prd

AIDA, prod.

- **Serviços**: `ai-pulse-prd`, `aida-back-prd`, `aida-classifier-prd-api` (pipeline), `aida-functions`, `aida-memoria-prd`, `arquivos-fator-r` (aida-back, pipeline), `central-disparos-prd`, `contabilizei-armor-prd`, `contador-inteligente-off-prd`, `contador-inteligente-prd-api`, `dados-no-op-service`, `file-transcriber-prd`, `find-situacao-voucher`, `functions`, `inbound-outbound-ai-prd`, `knowledge-book-agent-prd`, `monitoria-ia-aggregator` (monitoria-ia), `monitoria-ia-executor` (monitoria-ia), `monitoria-ia-parser` (monitoria-ia), `monitoria-ia-web` (atendimento-canais-admin, monitoria-ia), `notify-guias` (pipeline), `public-file-prd`, `sentinela-atendimento-prd`, `vector-search-api-prd`
- **Functions**: `arquivos-fator-r` (aida-back, pipeline), `find_situacao_voucher` (aida-back, pipeline), `notify-guias` (pipeline)

## contabilizei-crm-dev

CRM, dev.

- **Serviços**: `atendimento-api-gateway` (experts-drawio, pipeline), `atendimento-api-gateway-dev` (pipeline), `atendimento-front` (atendimento-api-gateway), `check-numerical-answer` (experts-bruno, zendeskbot-functions), `compare-values` (experts-bruno, zendeskbot-functions), `contabilizei-comprovante-rendimentos` (kong-config, pipeline), `contabilizei-comprovante-rendimentos-dev`, `contabilizei-crm-desconexao-cliente-sem-interacao`, `contabilizei-crm-ingestor-streaming-webhooks` (us-east1), `contabilizei-crm-suporte-webhooks` (us-east1) (experts-drawio, monitoria-ia), `contabilizei-crm-webhooks` (atendimento-api-gateway, contabilizei-crm-webhooks, experts-drawio, kong-config), `contabilizei-crm-webhooks-dev`, `historico-atendimento` (atendimento-api-gateway, plataforma-crm-web), `multiply-two-string-values` (experts-bruno, zendeskbot-functions), `return-element-at-index` (experts-bruno, zendeskbot-functions), `return-list-property` (experts-bruno, zendeskbot-functions), `validate-date` (experts-bruno, zendeskbot-functions), `zendeskbot-check-numerical-answer` (pipeline), `zendeskbot-compare-values` (pipeline), `zendeskbot-conditional` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-config` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-delay` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-loop` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-multiply-two-string-values` (pipeline), `zendeskbot-parse-string-to-number` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-request-delay` (pipeline, zendeskbot-functions), `zendeskbot-return-element-at-index` (pipeline), `zendeskbot-return-list-property` (pipeline), `zendeskbot-validate-date` (pipeline), `zendeskbot-validate-finantial-value` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-validate-is-today`
- **Functions**: `check-numerical-answer` (experts-bruno, zendeskbot-functions), `compare-values` (experts-bruno, zendeskbot-functions), `conditional`, `loop`, `multiply-two-string-values` (experts-bruno, zendeskbot-functions), `parse_str_number`, `return-element-at-index` (experts-bruno, zendeskbot-functions), `return-list-property` (experts-bruno, zendeskbot-functions), `return_list_prop`, `validate-date` (experts-bruno, zendeskbot-functions), `validate_finantial_value`, `zendeskbot-check-numerical-answer` (pipeline), `zendeskbot-compare-values` (pipeline), `zendeskbot-conditional` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-config` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-delay` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-loop` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-multiply-two-string-values` (pipeline), `zendeskbot-parse-string-to-number` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-request-delay` (pipeline, zendeskbot-functions), `zendeskbot-return-element-at-index` (pipeline), `zendeskbot-return-list-property` (pipeline), `zendeskbot-validate-date` (pipeline), `zendeskbot-validate-finantial-value` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-validate-is-today`

## contabilizei-crm

CRM, prod.

- **Serviços**: `atendimento-api-gateway` (experts-drawio, pipeline), `atendimento-api-gateway-prd` (pipeline), `atendimento-front` (atendimento-api-gateway), `check-numerical-answer` (experts-bruno, zendeskbot-functions), `compare-values` (experts-bruno, zendeskbot-functions), `contabilizei-comprovante-rendimentos` (kong-config, pipeline), `contabilizei-comprovante-rendimentos-prd`, `contabilizei-crm-desconexao-cliente-sem-interacao`, `contabilizei-crm-ingestor-streaming-webhooks` (us-east1), `contabilizei-crm-suporte-webhooks` (us-east1) (experts-drawio, monitoria-ia), `contabilizei-crm-webhooks` (atendimento-api-gateway, contabilizei-crm-webhooks, experts-drawio, kong-config), `contabilizei-crm-webhooks` (us-east1) (atendimento-api-gateway, contabilizei-crm-webhooks, experts-drawio, kong-config), `contabilizei-crm-webhooks-prd`, `dados-no-op-service`, `historico-atendimento` (atendimento-api-gateway, plataforma-crm-web), `multiply-two-string-values` (experts-bruno, zendeskbot-functions), `return-element-at-index` (experts-bruno, zendeskbot-functions), `return-list-property` (experts-bruno, zendeskbot-functions), `validate-date` (experts-bruno, zendeskbot-functions), `zendeskbot-check-numerical-answer` (pipeline), `zendeskbot-compare-values` (pipeline), `zendeskbot-conditional` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-config` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-delay` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-loop` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-multiply-two-string-values` (pipeline), `zendeskbot-parse-string-to-number` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-request-delay` (pipeline, zendeskbot-functions), `zendeskbot-return-element-at-index` (pipeline), `zendeskbot-return-list-property` (pipeline), `zendeskbot-validate-date` (pipeline), `zendeskbot-validate-finantial-value` (experts-bruno, pipeline, zendeskbot-functions)
- **Functions**: `check-numerical-answer` (experts-bruno, zendeskbot-functions), `compare-values` (experts-bruno, zendeskbot-functions), `conditional`, `config`, `multiply-two-string-values` (experts-bruno, zendeskbot-functions), `parse_str_number`, `request_delay`, `return-element-at-index` (experts-bruno, zendeskbot-functions), `return-list-property` (experts-bruno, zendeskbot-functions), `validate-date` (experts-bruno, zendeskbot-functions), `zendeskbot-check-numerical-answer` (pipeline), `zendeskbot-compare-values` (pipeline), `zendeskbot-conditional` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-config` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-delay` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-loop` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-multiply-two-string-values` (pipeline), `zendeskbot-parse-string-to-number` (experts-bruno, pipeline, zendeskbot-functions), `zendeskbot-request-delay` (pipeline, zendeskbot-functions), `zendeskbot-return-element-at-index` (pipeline), `zendeskbot-return-list-property` (pipeline), `zendeskbot-validate-date` (pipeline), `zendeskbot-validate-finantial-value` (experts-bruno, pipeline, zendeskbot-functions)

## Sem acesso para listar

Sem permissão para listar Cloud Run/functions em: `contabilizei-abertura`, `contabilizei-dev-01`, `contabilizei-impostos`, `contabilizei-impostos-teste`, `contabilizei-issue`, `contabilizei-prod-01`, `contabilizeiapp`, `contabilizeiapp-dev-02`, `fintech-228118`. Serviços desses domínios em geral rodam no GKE (ver [[gke-workloads]]) ou no App Engine.
