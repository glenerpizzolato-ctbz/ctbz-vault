---
name: prc-wpp-notificacoes-com-dados-de-outra-empresa
description: PRC — cliente recebe notificações/chat no WhatsApp com nome e empresa de outro cliente; validar usuários do telefone na Zendesk, mesclar duplicados e, se a Zendesk estiver ok, abrir chamado no CRM para validar a base de envios
metadata:
  type: reference
tags:
  - prc
canal:
  - wpp
dominio:
  - atendimento
  - notificacoes
sistemas:
  - zendesk
  - crm
acr:
  - PRD-103649
ocorrencias:
  - PRC-150957
qtd_ocorrencias: 1
ultima_ocorrencia: 2026-09-24
---

# Cliente recebe notificações WPP com dados de outra empresa

## Sintoma

Cliente diz que seus dados e CNPJ estão corretos na plataforma, mas no WhatsApp recebe de forma recorrente notificações em nome de outra pessoa/empresa. No chat também aparecem os dados do outro cliente.

## Causa provável

- Vínculo antigo na Zendesk: havia um processo automático (já descontinuado) que deletava um usuário e fazia merge automático com outros usuários. Com isso, o telefone do cliente pode ter ficado atrelado a um ticket/usuário da outra empresa.
- Se a Zendesk estiver limpa, o conflito pode estar na base de envios do CRM (lista de disparo associando o telefone ao cliente errado).

## Como resolver

1. Buscar na Zendesk todos os usuários com o telefone do cliente (ver [[PRD-151519 - Cliente com mais de um contato cadastrado com mesmo telefone na zendesk]] — busca por `*<8 dígitos>`).
2. Para cada usuário, conferir a organização atual e os tickets em `https://contabilizei.zendesk.com/agent/users/<id>/requested_tickets`. Verificar se algum está na organização da outra empresa.
3. Se algum estiver na organização errada, remover/ajustar o vínculo.
4. Mesclar os usuários duplicados sem organização no usuário que concentra os atendimentos (ex.: o do canal On).
5. Conferir na organização da outra empresa se existe ticket antigo com o cliente (sinal do merge automático antigo). Se for só histórico, não há ação.
6. Se a Zendesk estiver ok e a PRC não disser quais comunicações chegam com o nome errado, abrir chamado no projeto CRM (`ctbz-atendimento.atlassian.net`) para validar se há conflito do telefone/usuário na base de envios.
   - Exemplo: [CRM-1882](https://ctbz-atendimento.atlassian.net/browse/CRM-1882)

## Devolutiva sugerida na PRC

```
Encontrei N usuários na Zendesk para o telefone do cliente. Nenhum deles está em outra organização atualmente, tudo certo na Zendesk.

Fiz o merge do usuário <id sem organização> para o <id principal>, que concentra os atendimentos.

Na organização da outra empresa existiu um ticket com o cliente. É um caso antigo, de quando um usuário era deletado e o merge com outros usuários era feito automaticamente.

A PRC não especifica quais comunicações chegam com o nome errado. Abri o chamado <CRM-XXXX> para o CRM validar se existe conflito com o usuário do cliente na base de envios.
```

Peça ao atendimento o telefone afetado e prints das notificações. Sem isso, não dá para saber qual fluxo (Zendesk ou CRM) está enviando.

## ACR para vincular

[PRD-103649](https://contabilizeicontabilidade.atlassian.net/browse/PRD-103649): ZENDESK: [Merge de usuários], para casos em que usuários são vinculados indevidamente

- PRC de exemplo: [PRC-150957](https://contabilizeicontabilidade.atlassian.net/browse/PRC-150957)
