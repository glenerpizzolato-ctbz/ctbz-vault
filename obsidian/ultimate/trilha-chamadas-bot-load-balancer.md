---
name: trilha-chamadas-bot-load-balancer
description: "Como ver por onde o bot da Ultimate passou numa conversa sem a API do Zendesk: os logs do load balancer de api.contabilizei.com.br (logs/requests em contabilizei-prod-01) registram cada GET do bot com telefone, conversa, processo ou CNPJ na URL; e a tabela tickets do prd_crm_atendimento_zendesk traz tags, telefone, conversa do Sunshine e transcrição"
metadata:
  type: reference
tags:
  - ultimate
  - debug
  - cloud-logging
---

# Trilha de chamadas do bot pelo load balancer

Descoberto em 2026-11-24, ao criar a skill `validar-drop-ativacao`.

## Logs do load balancer

Toda chamada que a Ultimate faz às nossas APIs passa pelo LB de `api.contabilizei.com.br`, que loga URL, método e status em `projects/contabilizei-prod-01/logs/requests` (retenção de 30 dias). Filtrando pelo telefone (só dígitos, com e sem o 9), pelo `conversationid`, pelo id do processo ou pelo CNPJ, sai a trilha da conversa:

```bash
gcloud logging read 'logName="projects/contabilizei-prod-01/logs/requests" AND timestamp>="<ini>" AND timestamp<="<fim>" AND (httpRequest.requestUrl:"5511999999999" OR httpRequest.requestUrl:"<conversationid>")' --project contabilizei-prod-01 --order asc --format='value(timestamp,httpRequest.requestMethod,httpRequest.status,httpRequest.requestUrl)'
```

- Início de sessão: o bot checa ativo pendente `GET /zendesk/api/v1/bots/whatsapp/mensagem/ativa?telefoneCliente=...&idConversation=...&fluxo=ESPECIAIS` (depois `EXPERTS` e `CORE`). É a melhor estimativa do horário em que a config sorteou o rollout da IA ([[rollout-ia-ativacao]]).
- Identificação de processo: `GET .../identificacao/processos/contagem/+55...` e `.../dados/{idProcesso}/telefone/+55...` ([[endpoints-autenticacao-bot]]).
- Empresa ativa: chamadas por CNPJ (`flags-empresas/{cnpj}`, `contabil-core`, `payments`, `aida/contador-parceiro/elegibilidade/{cnpj}` etc.).
- **POSTs não aparecem com o telefone** (buscar-por-telefone, consulta CNPJ): o dado vai no corpo.
- O Kong (`namespace kong`) loga o mesmo em `textPayload`, mas o LB é mais fácil de filtrar.

## Tabela tickets do atendimento-zendesk

`prd_crm_atendimento_zendesk.tickets` (proxy `sql_crm_prd`, 5444) é sincronizada quase em tempo real e tem `group_id`/`group_name`, `tags` (com `conversationid:`, `businessphone:`, `processo_id:`, `sys_template_ativo:`, `id_mensagem_ativa:`, `sys_grupo_*`, `escalated_to_ai`), `requester_phone`, `sunshine_conversation_id`, `organization_cnpj`/`organization_plano` e `comments_formatted` (transcrição com as mensagens do bot e do cliente). Buscar sempre por `id` ou `requester_phone` (índices): filtros por `group_name`/`created_at` dão timeout.

Uso: skill `validar-drop-ativacao`.
