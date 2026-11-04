---
name: prc-zendesk-contatos-duplicados-mesmo-telefone
description: PRC — cliente com mais de um contato cadastrado com o mesmo telefone na Zendesk; causa (ticket ignorado/perdido) e como descobrir e mesclar via front admin
metadata:
  type: reference
tags:
  - prc
canal:
  - wpp
dominio:
  - atendimento
sistemas:
  - zendesk
  - atendimento-canais-admin
acr:
  - PRD-151519
qtd_ocorrencias: 0
---

# Cliente com mais de um contato cadastrado com mesmo telefone na zendesk

## Sintoma / possíveis causas

- Cliente está sendo **ignorado** no atendimento: **ticket aberto perdido**
  (o ticket fica vinculado a um contato "bifurcado" e não ao contato principal do cliente).

## Como descobrir

1. Acessar o front admin (precisa ser pelo front, pois exige permissão de admin na Zendesk):
   `https://admin.ctbz.com.br/api/atendimento-canais/sustentacao/zendesk/usuarios`
2. Pesquisar pelos últimos 8 dígitos do telefone do cliente, com `*` na frente:
   `*${ULTIMOS_8_DIGITOS_TELEFONE_CLIENTE}`
3. Verificar se aparece mais de um contato para o mesmo telefone.

## Como resolver

- **Mesclar** os contatos pelo próprio front admin.

> [!warning] Cuidado antes de mesclar
> Os contatos que bifurcam (os que serão mesclados no principal) devem ter
> **apenas telefone cadastrado** — **sem organização** e **sem e-mail**.
> Caso contrário, não podem ser mesclados.

## ACR para vincular

PRCs que caem nesse problema devem ser vinculadas à ACR:
[PRD-151519](https://contabilizeicontabilidade.atlassian.net/browse/PRD-151519)
— Desincronização de Dados de Contato: Atualização de E-mail do Responsável
