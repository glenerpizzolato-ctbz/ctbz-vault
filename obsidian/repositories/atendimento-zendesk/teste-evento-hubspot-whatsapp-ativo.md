---
name: teste-evento-hubspot-whatsapp-ativo
description: "Como validar ponta a ponta o evento whatsapp_ativo do HubSpot (ativo → status → worker → hubspot-proxy → portal): tópicos, assinantes, containers de log, tabela no BigQuery e tokens"
metadata:
  type: reference
tags:
  - atendimento-zendesk
  - hubspot
  - testes
atualizado_em: 2026-11-11
---

# Testar o evento `whatsapp_ativo` do HubSpot

O contrato e os comandos de criar e conferir a definição do evento ficam no `docs/hubspot/README.md` do repo. Esta nota junta o caminho do evento e onde conferir cada etapa (levantado no PRD-176511/PRD-176513).

## Caminho

1. Um ativo entra pelo tópico `atendimento-zendesk.envio-whatsapp-ativo` (projeto `contabilizei-crm-dev` em dev), com o corpo `EnviarWhatsappAtivoDTO` (`template`, `destino`, `integracao`, `cnpj`, `autor`, `metadados`…).
2. Ao chegar a `ENTREGUE` ou `ERRO`, o `update-status.service.ts` publica no `atendimento-zendesk.whatsapp-ativo-status`. Mesmo em `ERRO` o evento sai, então o teste não depende da entrega.
3. O `evento-hubspot.worker.ts` (subscription `atendimento-zendesk.whatsapp-ativo-status.hubspot-sub`) chama o `EventoHubspotAtivoService`. O serviço publica no tópico `hubspot-proxy`, que a function `hubspot-pubsub` (`contabilizei-canais-xp-dev`) manda ao portal: sandbox 51348990 em dev, e 47852359 em prd.

## Onde conferir

- **Worker:** no Cloud Logging, os containers `atz-worker-whatsapp-ativo-dev` (projeto `contabilizei-dev-01`, cluster privado, ns `crm-dev`) e `atz-worker-whatsapp-ativo-prd` (`contabilizei-prod-01`). Não precisa de VPN. A linha é `evento hubspot publicado para o ativo <id>`. Filtrar pelo `container_name`: o mesmo texto aparece em outros serviços (ex: `fintech-collections`).
- **Function:** `gcloud functions logs read hubspot-pubsub --region us-central1 --gen2 --project contabilizei-canais-xp-dev`.
- **Banco:** dev em `dev_crm_atendimento_zendesk` (proxy `sql_crm_dev`, 5434). Prd no BigQuery `contabilizei-dataflow.dw_atendimento_zendesk.mensagem_ativa`, com `metadados` **STRING** (usar `JSON_EXTRACT_SCALAR`). O `contabilizei-data` não tem a tabela.
- **Portal:** `GET /events/v3/event-definitions/whatsapp_ativo` e as ocorrências em `GET /events/v3/events?eventType=pe<portal>_whatsapp_ativo&objectType=company&objectId=<idhub>`. Os dois precisam do private app token de cada portal. Em 2026-11-11 ele não estava salvo em lugar nenhum da máquina: nem no `.env` do dotfiles, nem na coleção `experts-bruno/hubspot-api`, que espera `token_prod` num `.env` inexistente.

## Config do HubSpot no k8s

As variáveis ficam no ConfigMap de cada serviço, no repo `ctbz/devops/recursos/k8s-configmap` (clone em `~/repositories/k8s-configmap`, ler a `origin/master`, não a branch local), em `<projeto>/<cluster>/<namespace>/<serviço>.yaml`. O worker do evento é o `atz-worker-whatsapp-ativo-*`, mas os outros `atz-worker-*` e o web têm as mesmas chaves:

- dev: `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atz-worker-whatsapp-ativo-dev.yaml`, com `APP_SERVICES_HUBSPOT_EVENTOS_ATIVO_WHATSAPP=pe51348990_whatsapp_ativo`, `..._SEND_SANDBOX=true` e `APP_SERVICES_HUBSPOT_TOKEN=gcp:secretmanager:projects/642208929799/secrets/atendimentozendeskdevcrmdevdvp_APP_SERVICES_HUBSPOT_TOKEN/versions/latest` (projeto `contabilizei-sm-dev`).
- prd: `contabilizei-prod-01/contabilizei-private-cluster-prod-01/crm-prd/atz-worker-whatsapp-ativo-prd.yaml`, com `pe47852359_whatsapp_ativo`, `false` e `gcp:secretmanager:projects/1046698394190/secrets/atendimentozendeskprdcrmprdpdp_APP_SERVICES_HUBSPOT_TOKEN/versions/latest` (projeto `contabilizei-sm-prod`).

O evento **não usa** o `APP_SERVICES_HUBSPOT_TOKEN`: ele sai pelo Pub/Sub (`hubspot-proxy`), e quem fala com o HubSpot é a function `hubspot-pubsub`. O token só é usado no `identificar-cliente-plano-de-saude.service.ts` (leitura de contacts no CRM v3), então provavelmente não tem o escopo `behavioral_events.event_definitions.read_write` que a definição do evento exige. Em 2026-11-11, a conta pessoal recebia `IAM_PERMISSION_DENIED` até no `gcloud secrets describe` desses secrets.

## Armadilhas

- **Assinantes do tópico de status:** em dev, o `atendimento-zendesk.whatsapp-ativo-status` tem 5 assinantes: `hubspot-sub`, `zendesk.status-whatsapp-message.ticket-assessor.v2` (experts-dev), `ms-agrupamento-guias.sub.send-wpp-callback`, `survey-service.sub.whatsapp-ativo-status` e `experts-service.sub.csat.whatsapp-ativo-status`. O catálogo `infra/` (de 2026-10-09) lista menos. Publicar uma mensagem forjada direto no tópico de status atinge todos eles, então é melhor disparar um ativo de verdade pelo tópico de envio.
- **Deploy em dev pela pipeline do master:** a pipeline do merge no master (ex: #1415) tem também `helm-deploy-gke-dev`. Quando ele roda, o código do master vai para dev sem passar pela `develop`. Ver [[deploy-dev-e-prd]].
- **CNPJ do teste:** precisa ter `idhub` em `db_integracao_hubspot.public.empresa` do ambiente, com match exato da string sem máscara. Senão a function loga `IdHub not found` e o evento some.

## Collection Bruno

A collection `~/repositories/experts-bruno/hubspot` (que absorveu a antiga `hubspot-api`, com o upload de arquivo em `files/submit`) tem o `get-definition` do evento `whatsapp_ativo` e um `create-<property>` para cada uma das 4 properties das parcelas, com os ambientes `sandbox` (51348990) e `prod` (47852359). Os tokens ficam em `hubspot/.env` (gitignored), nas variáveis `hubspot_token_sandbox` e `hubspot_token_prod`.

Confirmado em 2026-11-11: o token do `APP_SERVICES_HUBSPOT_TOKEN` volta `403 MISSING_SCOPES` (`requiredGranularScopes: behavioral_events.event_definitions.read_write`) no `GET /events/v3/event-definitions/whatsapp_ativo`. O escopo é do private app, não do usuário: só quem administra os private apps do portal (super admin) consegue incluí-lo, ou criar um app próprio para isso. A alternativa sem API é declarar as properties pela tela de eventos customizados do HubSpot, com um usuário que tenha permissão de editar eventos.
