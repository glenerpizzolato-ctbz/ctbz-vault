---
name: 2026-10-08-opt-out-notificacoes-impostos
description: "Opt-out de notificações de impostos por contato (WhatsApp e e-mail)"
metadata:
  type: project
tags:
  - performance
titulo: "Opt-out de notificações de impostos por contato (WhatsApp e e-mail)"
data: 2026-10-08
periodo: 2026QD3
categorias:
  - entrega
  - outros-times
impacto: alto
fontes:
  - "[[PRD-169773]]"
  - "[[PRD-170025]]"
  - "[[PRD-169775]]"
  - "[[PRD-169776]]"
  - "[[PRD-170306]]"
  - "[[PRD-170057]]"
  - "[[PRD-170664]]"
  - "[[PRD-174790]]"
  - "[[contrato-optout]]"
  - "[[vault-roleset/secrets-e-permissoes]]"
---

# Opt-out de notificações de impostos por contato (WhatsApp e e-mail)

- **Período:** 2026QD3 · **Categorias:** entrega, outros-times · **Impacto:** alto

## Contexto

Clientes que não queriam receber notificações de impostos não tinham como recusá-las por canal e finalidade.

## O que fiz

Criei o opt-out de WhatsApp no `contato-service` com gestão no `atendimento-canais-admin`, a finalidade do opt-out e o registro do bloqueio; troquei o opt-out por empresa pelo por contato. Depois levei `optout_purpose: TAX` e o CNPJ normalizado (preservando o alfanumérico) aos e-mails de impostos em três repositórios (microsservico-agrupamento-guias!95, experts-service!147, agrupamento-guias-service!1), tratei o callback `BLOCKED_OPTOUT` e documentei o contrato de opt-out do email-service para outros consumidores. No primeiro envio real, rastreei o 401 do Kong até a credencial do consumer (suspeita: expansão de variável do CI cortando a key no `$`) e propus a correção.

## Resultado

Notificações de imposto por WhatsApp e e-mail respeitando o opt-out, com contrato documentado para outros times.

- 2026-11-04: na subida do opt-out nos e-mails do agrupamento em prd (PRD-174790), investigação do 401 do `email-service` no `contato-service` pelos logs do Kong, do Secret Manager e das pipelines, sem expor credenciais; causa raiz no `$` do token gravado pelo `create-secret-value`, corrigida e documentada como padrão para o time.

## Evidências

- [[create-secret-value-cifrao]] e [[contrato-optout]] (incidente de 2026-11-04)

- [[PRD-169773]]
- [[PRD-170025]]
- [[PRD-169775]]
- [[PRD-169776]]
- [[PRD-170306]]
- [[PRD-170057]]
- [[PRD-170664]]
- [[PRD-174790]]
- [[contrato-optout]]
- [[vault-roleset/secrets-e-permissoes]]
