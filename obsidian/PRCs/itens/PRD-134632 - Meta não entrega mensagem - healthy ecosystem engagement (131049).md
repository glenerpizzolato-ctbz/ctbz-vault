---
name: prc-meta-healthy-ecosystem-engagement-131049
description: PRC — ativo WPP sai do nosso lado mas a Meta barra com erro 131049 "healthy ecosystem engagement"; como confirmar no BD do atendimento-zendesk, causa e devolutiva
metadata:
  type: reference
tags:
  - prc
canal:
  - wpp
dominio:
  - impostos
  - notificacoes
sistemas:
  - meta
  - atendimento-zendesk
  - ms-agrupamento-guias
acr:
  - "[[PRD-134632]]"
ocorrencias:
  - PRC-117437
  - PRC-148268
qtd_ocorrencias: 2
ultima_ocorrencia: 2026-08-24
---

# Meta não entrega mensagem — healthy ecosystem engagement (131049)

## Sintoma

Cliente diz que não recebeu uma notificação pelo WhatsApp (ex.: guias do mês).
Os ativos saem corretamente do nosso lado, mas a **Meta barra a entrega**.

- Erro: `This message was not delivered to maintain healthy ecosystem engagement.`
- Código: `131049` (`400 Bad Request`)

## Causa

- A Meta decide não entregar por N motivos: pode identificar como spam, que o
  cliente não quer receber, pouca interação do cliente com nossos ativos,
  quantidade de mensagens que enviamos, etc.
- É uma política para templates de categoria **Marketing**: o limite é
  **dinâmico** (não fixo) e **compartilhado entre todas as empresas** que
  enviam mensagens ao cliente, não só o nosso volume.
- A Meta pode **reclassificar** um template de `UTILITY` para `MARKETING` por
  conta própria. Nosso BD pode continuar mostrando `UTILITY` enquanto a Meta
  já trata o template como Marketing, então confira a categoria na WABA.
  - Exemplo: `experts_empacotamento_guias_impostosb` estava `UTILITY` no
    `mensagem_ativa_template`, mas `Marketing` na WABA do Zendesk.
- Recomendação da Meta: esperar **pelo menos 24h** antes de reenviar. Reenviar
  antes disso só gera outro erro.

## Fluxo de envio

Serviço de origem (ex.: `microsservico-agrupamento-guias`) → `atendimento-zendesk`
→ Sunshine Conversations API (Zendesk) → Meta.

## Como confirmar (BD do `atendimento-zendesk`)

1. `mensagem_ativa`: filtrar pelo telefone do cliente (testar com e sem o 9):
   ```sql
   select * from mensagem_ativa where destino in ('+55DDD9XXXXXXXX', '+55DDDXXXXXXXX');
   ```
2. `mensagem_ativa_status`: filtrar por `id_mensagem = <id da mensagem_ativa>`.
   O último status traz `erro` = `This message was not delivered to maintain healthy ecosystem engagement.`
   e `id_erro` = `131049`.
3. (Opcional) `mensagem_ativa_template`: buscar pelo `nome` = campo `template`
   da `mensagem_ativa` e comparar a `categoria` com a da WABA na Meta.

## Devolutiva sugerida na PRC

```
Esse caso é a meta barrando o envio ao cliente. Está saindo do nosso lado mas a meta
por N motivos barra o envio com o erro This message was not delivered to maintain
healthy ecosystem engagement.

Identifica que pode ser spam ou que o cliente não quer receber, etc. Algumas causas do
porquê isso acontece é a pouca interação do cliente com nossos ativos, quantidade de
mensagens que enviamos, etc.

Podemos fazer uma devolutiva ao cliente explicando que o terceiro não está entregando as
mensagens e que estamos trabalhando em alternativas junto ao fornecedor para contornar
o problema.
```

## Possíveis soluções de produto (ainda não implementadas)

- Monitorar o erro `131049`, e outros erros específicos da Meta.
- Reter a notificação e reenviar automaticamente depois de 24h.
- Monitorar reclassificações de templates pela Meta.

## ACR para vincular

[PRD-134632](https://contabilizeicontabilidade.atlassian.net/browse/PRD-134632)
— Falha na Entrega do envio de Guias - Healthy Ecosystem Engagement

- PRCs de exemplo: [PRC-117437](https://contabilizeicontabilidade.atlassian.net/browse/PRC-117437),
  [PRC-148268](https://contabilizeicontabilidade.atlassian.net/browse/PRC-148268)
- Docs da Meta: [error codes](https://developers.facebook.com/documentation/business-messaging/whatsapp/support/error-codes),
  [per-user marketing limits](https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/per-user-limits)
