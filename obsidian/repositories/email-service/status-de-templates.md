---
name: email-service-status-de-templates
description: "Soft delete de templates no email-service: coluna status (active/inactive), rotas activate/inactivate, bloqueio no envio (TEMPLATE_INACTIVE) e listagem só com ativos por padrão"
metadata:
  type: reference
tags:
  - email-service
  - templates
---

# Status (soft delete) de templates

Entregue em 4 MRs encadeados (!75 → !76 → !77 → !78), em 2026-11.

- **Coluna**: `email_templates.status` (`active` | `inactive`), `NOT NULL DEFAULT 'active'` com check constraint (migration `0007_quick_roulette`). Os templates antigos ficam `active` pelo default.
- **Rotas**: `PATCH /api/v1/email-templates/inactivate` e `/activate`, pelo `id` ou pelo `name` na querystring (mesma validação do GET). Idempotentes (não fazem UPDATE se o status já é o pedido) e 404 quando o template não existe.
- **Cache**: trocar o status invalida `email_template:<id>`, o cache de 1h do disparo (`findByIdWithCache`). Sem isso o disparo usaria o template inativo por até 1h.
- **Envio**: a validação recusa com `Email template "<id>" is inactive` no `template_id` (callback `INVALID_PAYLOAD`). O disparo cobre o e-mail já na fila: `TemplateInactiveError` → `failure_reason` `TEMPLATE_INACTIVE`, falha permanente, sem retentativa e sem alerta.
- **Listagem**: `GET /api/v1/email-templates/list?status=active|inactive`, padrão `active` (itens e `total`). O GET por `id`/`name` mostra também os inativos, com o `status`, para dar para reativar.
- Um template inativo continua ocupando o nome: criar outro com o mesmo nome dá 409.

## Testes E2E

Roteiro por MR em PRD-177224 (sub-task de testes, um comentário por MR). Para testar o caminho do **disparo** (e não o da validação), que tem janela de segundos, forçar uma retentativa: rodar local com o pod de dev pausado no KEDA (ver [[teste-banco-fora]]) e `HUBSPOT_STMP_HOST` inválido, para o SMTP falhar com erro passageiro e o job entrar no backoff do BullMQ (~10s, ~20s…); mudar o estado nesse intervalo e a próxima tentativa já lê o novo estado. Serve para qualquer regra checada no dispatch antes do SMTP.

## Revisão do GitLab Duo (falsos positivos)

- No !77, o Duo apontou que o cache de 1h do `findByIdWithCache` deixaria um template inativado passar. Não procede: `EmailTemplateDAO.updateStatus` chama `invalidateCache(id)` (MR !76).
- No !78, o Duo disse que o `and(...)` do Drizzle põe parênteses mesmo com uma condição só. Não procede na versão instalada: com uma condição, o `and` devolve a própria condição e o SQL fica `"email_templates"."status" = $1` (teste passando).

## Deploy em dev (2026-11-13)

- Com merges seguidos no master, a pipeline do último merge pode quebrar no `tag-from-package-json` (`fatal: tag '0.1.74' already exists`): o merge entrou antes do commit `[skip ci]` que sobe a versão. Correção: rodar uma pipeline nova no master (`glab ci run -b master`), que já pega a versão incrementada.
- O deploy de dev não é automático: o job `service-account-dev` é manual e destrava `terraform-resources-dev`, migrations e `helm-deploy-gke-dev` (prd fica atrás do `service-account-prd`, também manual). O `terraform-resources-dev` pode falhar com `invalid_grant: Invalid JWT Signature` e passar sozinho no retry automático.
