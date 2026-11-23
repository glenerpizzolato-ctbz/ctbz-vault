---
name: testar-optout-whatsapp-ativo-dev
description: "Como testar o opt-out do WhatsApp ativo em dev: rota de envio pelo gateway heimdall (o Kong de dev recusa o token da coleção), telefone de teste no formato com o 9, opt-outs já existentes dele no contato-service (alternar por UPDATE, sem INSERT), templates de dev com nps/csat, consultas de status e logs do worker"
metadata:
  type: reference
tags:
  - atendimento-zendesk
  - whatsapp-ativo
  - opt-out
  - testes
atualizado_em: 2026-11-23
---

# Testar o opt-out do WhatsApp ativo em dev

Levantado no plano de teste do PRD-178305 (MR !252, guardrail de `nps`/`csat` no nome). Regra da finalidade em [[whatsapp-ativo-finalidade-optout]]; deploy em [[deploy-dev-e-prd]].

## Envio

- `POST https://api-gateway-dev.contabilizei.com/zendesk/api/v1/whatsapp-ativo/messaging` com `client_id: experts` e `access_token` = `access_token_exp_dev` (`docs/bruno/.env`, ambiente `dev heimdall` da coleção). Responde `202` com `{ message: 'ENFILEIRADO_SUCESSO', pubsubId }`; o `pubsubId` é o `mensagem_ativa.id_message_broker`. A rota já roda a validação (template, telefone, empresa) antes de publicar no tópico.
- Em 2026-11-23 o ambiente `dev kong` (`api-dev.contabilizei.com.br/zendesk`, `DECK_BRUNO_EXPERTS_TO_ATENDIMENTO_ZENDESK_dev`) voltava **401**.
- Payload mínimo: `template`, `destino`, `integracao`, `cnpj`, `autor`, `furaAtendimento: true` (não depende de ticket aberto) e `debounceToBusinessHour: false`. Empresa que não é Expert só recebe em dia útil.

## Telefone e opt-outs de teste

- O telefone de teste do Glener fica gravado em `mensagem_ativa.destino` como `+5555996981032` (com o 9; é o que o `TelefoneUtil.formatar` devolve). O `+555596981032` é o do end-user do Zendesk.
- No contato-service de dev, esse telefone já tem as quatro manifestações da empresa `12996446000105` (`SURVEY`, `MARKETING`, `TAX`, `TRANSACTIONAL`), gravadas em 2026-11-09 com `opted_out = true`.
- No banco `dev_atendimento_canais_contato_service`, o usuário tem **UPDATE e DELETE** em `contact_optout`, mas **não INSERT**. A API do contato-service em dev (`api-dev…/contato-service`, `kong_token_bruno_dev` da coleção do contato-service) voltava **401** em 2026-11-23, e o heimdall não roteia o contato-service (502). Para montar o cenário, alternar o `opted_out` das linhas existentes e restaurar no fim:

```sql
update contact_optout o set opted_out = (o.purpose::text = any('{SURVEY}')), updated_at = now()
from company c
where c.id = o.company_id and c.code = '12996446000105' and o.channel = 'WHATSAPP' and o.address = '+5555996981032';
```

- Depois de mudar um opt-out, esperar o cache de 5 min do contato-service (`OPTOUT_CACHE_TTL_SECONDS`) antes de disparar.

## Templates de dev úteis

Todos `APPROVED`, `ativo`, sem variáveis, sem header de mídia e sem flow (2026-11-23): `teste_csat` (EXPERTS, UTILITY), `teste_experts_csat_3` (EXPERTS, MARKETING), `nps_exp_2025_03a` (SURVEY, UTILITY), `experts_irlembrete_normalcomdebitos` (EXPERTS, UTILITY) e `teste_nf_ia_01` (EXPERTS, MARKETING).

## Onde conferir

- Banco `dev_crm_atendimento_zendesk` (proxy `sql_crm_dev`, 5434): `mensagem_ativa` pelo `id_message_broker` e o último `mensagem_ativa_status` (`id_mensagem`, `status`, `id_erro`, `erro`). Bloqueio: `BLOQUEADA_OPTOUT`, `id_erro = OPTOUT_DO_TITULAR`, `erro` com `comunicacao <FINALIDADE>`.
- Logs: `gcloud logging read` no `contabilizei-dev-01`, `resource.labels.container_name="atz-worker-whatsapp-ativo-dev"`, texto em `jsonPayload.message` (`envio barrado por opt-out`, `opt-out de pesquisa pelo nome do template`). Não precisa de VPN.

## Armadilhas da execução (2026-11-23, E2E do PRD-178306)

- **Pod antigo durante o rollout:** depois do `helm-deploy-gke-dev`, o pod antigo do `atz-worker-whatsapp-ativo-dev` continua consumindo a subscription `atendimento-zendesk.envio-whatsapp-ativo-sub` até ser encerrado (no teste, ~4 min depois do pod novo subir). Um envio nessa janela roda o código antigo. Antes de disparar, conferir que só o pod novo está de pé (evento `Killing` do antigo em `resource.type="k8s_pod"`) ou checar no log qual `pod_name` processou o ativo (`processando whatsapp ativo ID <id>`); a imagem do pod sai do evento `Pulled` (tag `<versão>-<sha curto>-dev`).
- **Busca de log com hífen:** no `gcloud logging read`, o texto livre `"opt-out de pesquisa pelo nome"` não acha nada; filtrar pelo campo, `jsonPayload.message:"opt-out de pesquisa pelo nome do template"`.
- O `UPDATE` que restaura os opt-outs não volta o `updated_at` original; fica registrado o horário da restauração.

Resultado do E2E e evidências: comentário no PRD-178306 e `~/.local/share/bahcode/features/f1795098054786.doc/tests/w4k/evidencias/`.
