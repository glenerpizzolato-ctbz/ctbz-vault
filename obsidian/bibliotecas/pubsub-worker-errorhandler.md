---
name: pubsub-worker-errorhandler
description: "Como o PubsubWorker do @contabilizei-private/event-workers (4.x) trata o errorHandler: exceção é capturada e logada, e mensagem não resolvida é nacada pela própria biblioteca"
metadata:
  type: reference
tags:
  - pubsub
  - event-workers
atualizado_em: 2026-11-09
---

# errorHandler do PubsubWorker (event-workers 4.x)

No `PubsubWorker` de `@contabilizei-private/event-workers` (visto na 4.0.1, em `dist/index.mjs`, `handleProcessingError`):

- Se o `handler` lança, a biblioteca chama o `errorHandler(data, error, ctx)` dentro de um `runCatching`. Se o próprio `errorHandler` lançar, a exceção **não sobe**: vira o log `errorHandler failed handling a message`.
- Depois disso, se a mensagem não foi resolvida (nem `ctx.ack()` nem `ctx.nack()`), a biblioteca chama `message.nack()`. Ou seja: um `errorHandler` que lança antes do `ctx.nack()` não deixa a mensagem presa no lease; ela é nacada na hora e segue o backoff e a DLQ normalmente.
- Sem `errorHandler`, a mensagem com erro é sempre nacada.
- Só conta como sucesso nas métricas quando o `errorHandler` termina sem erro e deu `ack`.

Consequência para revisão de código: `try { ... } finally { ctx.nack() }` em volta de um passo que pode falhar no `errorHandler` não muda o destino da mensagem. Ele só serve para padronizar o código ou para trocar o log genérico por um específico (ex: "origem não foi avisada"), como no `send-email-enqueue.worker.ts` do email-service. Visto na revisão do MR !74 do email-service (PRD-175906).
