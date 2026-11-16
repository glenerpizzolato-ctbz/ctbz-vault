---
name: ticketing-service-indice
description: "Índice de notas do repositório ticketing-service: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - ticketing-service
repositorio: ticketing-service
caminho: ~/repositories/ticketing-service
---

# ticketing-service

Repositório em `~/repositories/ticketing-service`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.


- [[roteamento-n1-ativacao-soci]] — origem do `statusJira` no fluxo de processos do bot WhatsApp (telefone do sócio → empresa da Abertura → `ProcessoAbertura.status` no Datastore, sincronizado do Jira pelo `JiraSyncService`); o `ticketing-service` não entra no roteamento
