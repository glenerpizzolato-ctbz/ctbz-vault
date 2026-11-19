---
name: dependencias-experts-drawio
description: "Dependências do experts-drawio: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - experts-drawio
repositorio: experts-drawio
---

# Dependências do experts-drawio

O que o `experts-drawio` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `e84458c` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `atendimento-zendesk` (42×): `experts-canal-wpp/arq_wpp_experts.drawio:624`, `ticketing-service/jira.drawio:40`, `zendesk/monitoria-ia-arq-PoC.drawio:771`
- `emissor-whatsapp` (15×): `emissor-wpp/individual-arq.drawio:44`, `emissor-wpp/massivo-wpp-arq.drawio:29`, `emissor-wpp/unificado-arq.drawio:53`
- `plataforma-crm-web` (7×): `cashflow-architeture.drawio:111`, `emissor-wpp/unificado-arq.drawio:18`, `experts-canal-wpp/arq_wpp_experts.drawio:197`
- `experts-api-gateway` (5×): `cashflow-architeture.drawio:53`, `emissor-wpp/individual-arq.drawio:55`, `emissor-wpp/massivo-wpp-arq.drawio:10`
- `plataforma-importacao-notas-worker` (5×): `emissor-wpp/individual-arq.drawio:66`, `emissor-wpp/unificado-arq.drawio:146`, `experts-canal-wpp/arq_wpp_experts.drawio:418`
- `atendimento-api-gateway` (3×): `ticketing-service/jira.drawio:415`, `zendesk/monitoria-ia-arq-fornecedor.drawio:415`, `zendesk/monitoria-ia-arq_bkp_3a_pag.drawio:415`
- `contabilizei-crm-webhooks` (3×): `ticketing-service/jira.drawio:434`, `zendesk/monitoria-ia-arq-fornecedor.drawio:434`, `zendesk/monitoria-ia-arq_bkp_3a_pag.drawio:434`
- `contabilizei-back-core` (2×): `Diag Seq Experts.drawio:623`, `experts-canal-wpp/arq_wpp_experts.drawio:641`
- `plataforma-web` (2×): `cashflow/tech.drawio:16`, `experts-canal-wpp/arq_wpp_experts.drawio:665`
- `contabilizei-movimentacao-back` (2×): `cashflow/tech.drawio:99`, `pendencias-oportunidades/architeture.drawio:81`
- `experts-twilio` (2×): `emissor-wpp/individual-arq.drawio:200`, `experts-canal-wpp/arq_wpp_experts.drawio:332`
- `contabilizei-abertura` (2×): `experts-canal-wpp/arq_wpp_experts.drawio:219`
- `experts-zendesk` (2×): `experts-zd/encerramento-tarefas-organicas.drawio:52`
- `plataforma-monolito` (1×): `Diag Seq Experts.drawio:531`
- `experts-contabil` (1×): `cashflow/tech.drawio:83`
- `experts-async-publisher` (1×): `emissor-wpp/individual-arq.drawio:255`
- `emissor-whatsapp-reports` (1×): `emissor-wpp/massivo-wpp-arq.drawio:175`
- `experts-alertas` (1×): `experts-canal-wpp/arq_wpp_experts.drawio:376`
- `experts-nfs` (1×): `experts-canal-wpp/arq_wpp_experts.drawio:540`
- `atendimento-zendesk-cronjob` (1×): `zendesk/monitoria-ia-arq_bkp_3a_pag.drawio:725`

### Repositórios que citam este

_Nenhum._

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `atendimento-zendesk-ticket-criado-atualizado-banco-de-dados`, `emissor-individual-emitir`, `emissor-massivo-check-issuance`, `emissor-massivo-processar`, `emissor-massivo-reports`, `expired-twilio-tasks`, `twilio-republish-evts-from-crm`, `twilio-webhooks-tasks`, `zendesk-tickets-callback`, `zendesk-tickets-upsert`, `zendesk-webhooks-tickets`
- **Subscription**: `emissor-individual-emitir`, `emissor-massivo-processar`, `emissor-massivo-reports`, `tw-tasks-republish-to-experts-sub`, `zendesk-webhooks-tickets`, `zendesk-webhooks-tickets-atendimento-zendesk-sub`
- **Fila Cloud Tasks**: `emissor-whatsapp`, `emissor-whatsapp-massivo`, `experts-zendesk`
- **Cloud Run / function**: `atendimento-api-gateway`, `contabilizei-crm-suporte-webhooks`, `contabilizei-crm-webhooks`, `emissor-whatsapp`, `emissor-whatsapp-massivo`, `emissor-whatsapp-reports`, `experts-alertas`, `experts-api-gateway`, `experts-async-publisher`, `experts-contabil`, `experts-nfs`, `experts-twilio-metrics`, `experts-zendesk`, `function-pendencias-oportunidades`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `Diag Seq Experts.drawio:618`
- Zendesk: `contabilizei.zendesk.com` em `zendesk/monitoria-ia-arq-PoC.drawio:7`

<!-- deps:auto:fim -->
