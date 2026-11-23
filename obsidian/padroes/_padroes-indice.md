---
name: padroes-indice
description: "Índice dos padrões técnicos do time (convenções e defaults que valem para qualquer serviço: nomenclatura, frameworks, logs, credenciais, dependências)"
metadata:
  type: reference
tags:
  - padroes-indice
---

# Padrões do time

Convenções que valem para qualquer serviço, uma nota por padrão.

> [!NOTE] O que entra aqui
> Só **convenções e defaults**: o que, se alguém fizer diferente, está errado. Processo de trabalho (Jira, MR, deploy) fica em [[_fluxo-de-trabalho-indice|fluxo-de-trabalho]], armadilhas de pipeline/Sonar em [[_ci-indice|ci]], comportamento inesperado de bibliotecas em [[_bibliotecas-indice|bibliotecas]] e o que é específico de um sistema na pasta dele.

- [[pubsub-nomenclatura|Nomenclatura de Pub/Sub]] — tópico `<serviço>.p2p.<nome>`, subscription `<serviço>.sub.<nome>` e sufixo `-local` na execução local
- [[alertas-pubsub-idade-da-mensagem|Alerta de Pub/Sub por idade da mensagem]] — alertar pela mensagem mais antiga sem ack (sustentada), não por quantidade; como calibrar o limite e a armadilha do valor parado no ackDeadline
- [[dependencias-entre-repositorios|Dependências entre repositórios]] — cada repositório tem a nota `dependencias-<repo>.md` com o que consome (repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, confirmado no código e espelhado no provedor, mais o levantamento automático da skill `mapear-dependencias`; é o que a revisão de MRs lê para achar quebra de fluxo dependente
- [[frameworks-nodejs|Frameworks Node.js]] — back-end em Fastify (padrão), NestJS em atendimento-zendesk/experts-twilio/relacionamento-service, Express só legado; front em React ou Vue
- [[node-26-typescript-nativo|Node 26 com TS nativo]] — modelo do survey-service (Node 26, sem build, tsconfig nodenext) e o que um repo precisa mudar para adotar
- [[pino-objeto-antes-da-mensagem|Pino: objeto antes da mensagem]] — `logger.x('msg', {campos})` descarta os campos em silêncio; usar `logger.x({campos}, 'msg')` e `err` para erro
