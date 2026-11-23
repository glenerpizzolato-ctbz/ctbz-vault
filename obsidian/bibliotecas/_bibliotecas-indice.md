---
name: bibliotecas-indice
description: "Índice de comportamentos inesperados de bibliotecas usadas nos serviços (zod, event-workers etc.)"
metadata:
  type: reference
tags:
  - bibliotecas-indice
---

# Bibliotecas

Comportamentos inesperados de bibliotecas usadas nos serviços e como contorná-los. Uma nota por armadilha.

- [[zod-union-mensagens-de-erro]] — zod v4: `z.union` de valor único ou lista devolve "Invalid input" genérico com enum inválido; como recuperar a mensagem específica
- [[pubsub-worker-errorhandler|errorHandler do PubsubWorker]] — event-workers 4.x: exceção no `errorHandler` é capturada e logada pela biblioteca, e mensagem sem ack/nack é nacada na hora (não fica presa no lease)
