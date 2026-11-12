---
name: super-ouvidoria-tags-observabilidade
description: "Tags sys_super_ouvidoria_* (analise_habilitada, tema_compativel, flag_transfer_on/off, transferido) são gravadas pelo sentinela-atendimento via API do Zendesk, não pela Ultimate nem por gatilho"
metadata:
  type: reference
tags:
  - sentinela-atendimento
  - ouvidoria
  - zendesk
---

# Tags de observabilidade da Super-Ouvidoria

Definidas em `sentinela_atendimento/infra/config/config.py` (`ZENDESK_TAG_SO_*`) e aplicadas por `super_ouvidoria/service/super_ouvidoria_evento_handler.py` (`_aplicar_tags`, idempotente, guarda o que já mandou em `super_ouvidoria_tags` no doc do ticket no Firestore):

- `sys_super_ouvidoria_analise_habilitada` → o ticket passou nos gates (estado, CNPJ, kill switch `is_enabled_for` por canal/plano/assignment) e o cliente está ativo na lista da Super-Ouvidoria (collections `super_ouvidoria_entradas` / `super_ouvidoria_lotes` do aida-back).
- `sys_super_ouvidoria_tema_compativel` → a classificação da mensagem casou com o macro/micro tema de um motivo do cliente.
- `sys_super_ouvidoria_flag_transfer_on` / `_off` → se a transferência estava habilitada (senão é shadow).
- `sys_super_ouvidoria_transferido` → transferido (`zendesk/service/ticket_transfer_service.py`).

O gatilho é o evento Pub/Sub de classificação concluída do aida-back (`POST /ticket/super-ouvidoria/classificado`), ou seja, roda **depois** que o ticket já está com humano. No audit do Zendesk aparece como `via: Web service`, logo depois da classificação de tema (ex: `sys_tema_mensalidade`).

**Não tem relação com as tags `sys_*_ouvidoria_exp`** do bot de WhatsApp: ver [[tags-ouvidoria-whatsapp-ultimate]].
