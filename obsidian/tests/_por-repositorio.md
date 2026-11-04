---
name: _por-repositorio-tests
description: "Índice dos roteiros de teste agrupados por repositório envolvido"
metadata:
  type: reference
tags:
  - tests-indice
---

# Testes por repositório

Um roteiro aparece em todos os repositórios que ele envolve.

## microsservico-agrupamento-guias

- [[preparar-grupo-guia-agrupamento]] — `grupo_guia`, `controle_guias`, consumer `agrupar-guias`, reprocessamento de erros

## plataforma-faturamento-worker

- [[preparar-grupo-guia-agrupamento]] — rota `envia-empresa-ms-agrupamento-guia/{idEmpresa}` que publica em `agrupar-guias-empresa`

## dotfiles

- [[fechar-tickets-teste-zendesk]] — skill `docs/ai/skills/ctbz/zendesk/fechar-tickets-teste-zendesk`
- [[preparar-grupo-guia-agrupamento]] — `src/google/publish-topic.google.js topic=agrupar-guias-empresa`

## bots-api

- [[clientes-inativos-cnpjs-teste]] — CNPJs inativos por motivo para testar o fluxo de clientes inativos (flag `sys_rollout_cliente_inativo` removida, horário de atendimento)

## plataforma-crm-web

- [[clientes-inativos-cnpjs-teste]] — CNPJs inativos por motivo para testar o fluxo de clientes inativos (endpoint de autenticação por CNPJ/telefone que retorna o motivo)

## ultimate-ia

- [[clientes-inativos-cnpjs-teste]] — CNPJs inativos por motivo para testar o fluxo de clientes inativos (fluxo na Ultimate)

## experts-bruno

- [[fechar-tickets-teste-zendesk]] — coleção `zendesk-api` (credenciais e rotas de tickets)
- [[destravar-atendimento-ultimate]] — coleção `sunhine-api-full` (Switchboard Actions e Delete Conversation)
