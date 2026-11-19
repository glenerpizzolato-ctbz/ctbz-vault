---
name: dependencias-kong-config
description: "Dependências do kong-config: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - kong-config
repositorio: kong-config
---

# Dependências do kong-config

O que o `kong-config` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

## Consome

### Repositórios internos

_Nada confirmado ainda._

### Libs internas

_Nada confirmado ainda._

### Infra GCP

_Nada confirmado ainda._

### Bancos e dados

_Nada confirmado ainda._

### Terceiros

_Nada confirmado ainda._

## Consumido por

Quem consome os contratos deste repositório; a revisão de MRs confere se o diff quebra algum deles.

_Nada confirmado ainda._

<!-- deps:auto:inicio (gerado por mapear-dependencias; não editar à mão) -->

## Levantamento automático

Gerado em 2026-11-19 sobre `feat/PRD-170316` @ `0530ace` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-movimentacao-back` (282×): `dev/heimdall_legado/contabil/contabilizei-movimentacao-back/contabilizei-movimentacao-back.yaml:9`, `dev/heimdall_legado/heimdall_consumers.yaml:12`, `prd/heimdall_legado/contabil/contabilizei-movimentacao-back/contabilizei-movimentacao-back.yaml:7`
- `atendimento-zendesk` (254×): `dev/atendimento-canais/bots-api/bots-api.yml:144`, `dev/atendimento-canais/contato-service/contato-service.yml:136`, `dev/atendimento/consumers.yaml:14`
- `contabilizei-abertura` (129×): `dev/heimdall_legado/onboarding/contabilizei-abertura-back/contabilizei-abertura-back.yaml:9`, `dev/heimdall_legado/onboarding/contabilizei-abertura-docs/contabilizei-abertura-docs.yaml:9`, `dev/onboarding/classificador-fiscal-cnae/classificador-fiscal-cnae.yaml:115`
- `experts-service` (90×): `dev/atendimento-canais/contato-service/contato-service.yml:178`, `dev/experts/experts-service/experts-service.yaml:6`, `prd/atendimento-canais/contato-service/contato-service.yml:184`
- `ticketing-service` (90×): `dev/proc-auto/ticketing-service/ticketing-service.yaml:6`, `prd/heimdall_legado/experts/ticketing/ticketing.yaml:59`, `prd/heimdall_legado/heimdall_consumers.yaml:402`
- `bots-api` (76×): `dev/atendimento-canais/bots-api/bots-api.yml:6`, `dev/atendimento-canais/contato-service/contato-service.yml:164`, `dev/heimdall_legado/atendimento-canais/microsservicos-agrupamentos-guias/microsservico-agrupamento-guias.yaml:107`
- `relacionamento-service` (74×): `dev/atendimento/relacionamento-service/relacionamento-service.yaml:6`, `dev/heimdall_legado/atendimento/relacionamento/relacionamento.yaml:127`, `dev/heimdall_legado/heimdall_consumers.yaml:86`
- `contato-service` (72×): `dev/atendimento-canais/contato-service/contato-service.yml:6`, `prd/atendimento-canais/contato-service/contato-service.yml:6`
- `mcp-notas-fiscais` (50×): `dev/experts/experts-service/experts-service.yaml:121`, `dev/heimdall_legado/fiscal/emissor-notas-fiscais/emissor-notas-fiscais.yaml:105`, `dev/ia/mcp-notas-fiscais/mcp-notas-fiscais.yaml:6`
- `fintech-payments` (44×): `dev/fintech/febraban-calendario/febraban-calendario.yaml:122`, `dev/heimdall_legado/fintech/fintech-payments/fintech-payments.yaml:7`, `dev/heimdall_legado/heimdall_consumers.yaml:15`
- `zendesk-agents` (44×): `dev/atendimento/zendesk-agents/zendesk-agents.yaml:6`, `dev/heimdall_legado/atendimento/atendimento-zendesk-web/atendimento-zendesk-web.yaml:395`, `dev/ia/mcp-notas-fiscais/mcp-notas-fiscais.yaml:106`
- `ms-relatorio-faturamento` (44×): `dev/experts/ms-relatorio-faturamento/ms-relatorio-faturamento.yml:6`, `prd/experts/ms-relatorio-faturamento/ms-relatorio-faturamento.yml:6`
- `email-service` (40×): `dev/atendimento-canais/contato-service/contato-service.yml:185`, `dev/atendimento-canais/email-service/email-service.yml:6`, `prd/atendimento-canais/contato-service/contato-service.yml:191`
- `experts-ms-nps` (40×): `dev/experts/experts-ms-nps/experts-ms-nps.yaml:6`, `prd/heimdall_legado/experts/experts-ms-nps/experts-ms-nps.yaml:6`, `prd/heimdall_legado/heimdall_consumers.yaml:126`
- `microsservico-agrupamento-guias` (40×): `dev/heimdall_legado/atendimento-canais/microsservicos-agrupamentos-guias/microsservico-agrupamento-guias.yaml:6`, `dev/heimdall_legado/heimdall_consumers.yaml:27`, `prd/heimdall_legado/atendimento-canais/microsservico-agrupamento-guias/microsservico-agrupamento-guias.yaml:6`
- `contabilizei-pagamentos` (39×): `dev/heimdall_legado/billing/contabilizei-pagamentos-cupom/contabilizei-pagamentos-cupom.yaml:9`, `dev/heimdall_legado/heimdall_consumers.yaml:13`, `prd/heimdall_legado/billing/contabilizei-pagamentos-cupom/contabilizei-pagamentos-cupom.yaml:7`
- `contabilizei-crm-webhooks` (31×): `dev/atendimento/consumers.yaml:63`, `dev/atendimento/contabilizei-crm-webhooks/contabilizei-crm-webhooks.yaml:7`, `prd/atendimento/contabilizei-crm-webhooks/contabilizei-crm-webhooks.yaml:7`
- `aida-back` (29×): `.devops/scripts/validate_kong_config.py:112`, `dev/atendimento-canais/bots-api/bots-api.yml:168`, `dev/heimdall_legado/contabil/contabil-pendencia-documental-web/contabil-pendencia-documental-web.yaml:328`
- `plataforma-crm-web` (29×): `dev/atendimento/consumers.yaml:27`, `dev/heimdall_legado/atendimento/atendimento-zendesk (pending)/atendimento-zendesk.bkp:875`, `dev/heimdall_legado/atendimento/atendimento-zendesk-web/atendimento-zendesk-web.yaml:174`
- `atendimento-canais-admin` (27×): `dev/atendimento-canais/atendimento-canais-admin/atendimento-canais-admin.yml:6`, `dev/atendimento-canais/bots-api/bots-api.yml:160`, `dev/atendimento-canais/email-service/email-service.yml:101`
- `plataforma-web` (23×): `dev/billing/billing-orchestration/billing-orchestration.yaml:115`, `dev/experts/experts-service/experts-service.yaml:129`, `dev/heimdall_legado/engajamento/contabilizei-central-documentos/contabilizei-central-documentos.yaml:105`
- `experts-async-publisher` (19×): `dev/experts/experts-async-publisher/experts-async-publisher.yaml:7`
- `experts-nfs` (10×): `dev/atendimento-canais/bots-api/bots-api.yml:176`, `dev/experts/experts-service/experts-service.yaml:145`, `dev/heimdall_legado/fiscal/emissor-notas-fiscais/emissor-notas-fiscais.yaml:113`
- `contabilizei-agents` (8×): `dev/atendimento-canais/bots-api/bots-api.yml:152`, `dev/experts/experts-service/experts-service.yaml:161`, `dev/heimdall_legado/atendimento/atendimento-zendesk (pending)/atendimento-zendesk.bkp:1002`
- `canais-adk` (6×): `dev/atendimento/relacionamento-service/relacionamento-service.yaml:234`, `dev/experts/experts-ms-nps/experts-ms-nps.yaml:114`, `dev/experts/experts-service/experts-service.yaml:209`
- `plataforma-faturamento-worker` (6×): `dev/reforma-tributaria/codigos-tributarios/codigos-tributarios.yaml:95`, `dev/reforma-tributaria/dados-fiscais-empresa/dados-fiscais-empresa.yaml:100`, `prd/reforma-tributaria/codigos-tributarios/codigos-tributarios.yaml:95`
- `oi-contabilizei-functions` (4×): `dev/aquisicao/whatsapp-integration/whatsapp-integration.yaml:150`, `dev/atendimento-canais/contato-service/contato-service.yml:157`, `prd/aquisicao/whatsapp-integration/whatsapp-integration.yaml:150`
- `contabilizei-guias` (4×): `dev/heimdall_legado/impostos/microservico-caixa-postal-ecac/microservico-caixa-postal-ecac.yaml:125`, `dev/impostos/contabilizei-robo-integrador/contabilizei-robo-integrador.yaml:161`, `prd/heimdall_legado/impostos/microservico-caixa-postal-ecac/microservico-caixa-postal-ecac.yaml:106`

### Repositórios que citam este

- `survey-service` (12×): `.env.example:12`, `.claude/skills/add-channel/SKILL.md:20`, `docs/PLAN.md:182`
- `atendimento-zendesk` (1×): `docs/whatsapp-ativo-messaging-api.md:23`
- `canais-certificado-digital` (1×): `src/certificado-digital/cenario/cenario.controller.ts:22`
- `monitoria-ia` (1×): `docs/validacao-ajuste-avaliacoes.md:29`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `pipeline`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `atendimento-zendesk-atualizar-ticket`, `zendesk-webhooks-agents`, `zendesk-webhooks-capacidade-agentes`, `zendesk-webhooks-comments`, `zendesk-webhooks-conversations`, `zendesk-webhooks-events-tickets`, `zendesk-webhooks-messages`, `zendesk-webhooks-notifications`, `zendesk-webhooks-pesquisa-satisfacao`, `zendesk-webhooks-retorno-desconexao-sem-interacao`, `zendesk-webhooks-tickets`, `zendesk-webhooks-tickets-new`, `zendesk-webhooks-users`
- **Subscription**: `dataflow-batch-service`, `zendesk-webhooks-tickets`
- **Cloud Run / function**: `bots-api`, `contabilizei-comprovante-rendimentos`, `contabilizei-crm-webhooks`, `experts-async-publisher`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
