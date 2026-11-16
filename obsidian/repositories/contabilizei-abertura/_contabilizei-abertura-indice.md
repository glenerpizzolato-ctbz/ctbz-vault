---
name: contabilizei-abertura-indice
description: "Índice de notas do repositório contabilizei-abertura: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - contabilizei-abertura
repositorio: contabilizei-abertura
caminho: ~/repositories/contabilizei-abertura
---

# contabilizei-abertura

Repositório em `~/repositories/contabilizei-abertura`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[contagem-processos-abertura-por-telefone]] (em `repositories/atendimento-zendesk/`) — `GET /rest/integracao/twilio/processo/telefone/{telefone}`: busca por `socios.telefone` com variantes com/sem 9 e devolve inclusive processos Finalizados
- [[roteamento-n1-ativacao-soci]] — origem do `statusJira` no fluxo de processos do bot WhatsApp (telefone do sócio → empresa da Abertura → `ProcessoAbertura.status` no Datastore, sincronizado do Jira pelo `JiraSyncService`); o `ticketing-service` não entra no roteamento
- [[processo-abertura-teste]] — como criar (Admin IS/pré-cadastro) e manipular (admin `processoabertura`) um processo de abertura de teste em dev e prd; SOCI criado à mão não serve Admin: https://admin.contabilizei.com/abertura/sistema-admin/#/processosabertura
