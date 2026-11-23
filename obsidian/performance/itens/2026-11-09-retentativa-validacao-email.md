---
name: 2026-11-09-retentativa-validacao-email
description: "Investigação da perda de e-mails no restart do Cloud SQL e correção da retentativa na validação do email-service"
metadata:
  type: project
tags:
  - performance
titulo: "E-mails perdidos no restart do Cloud SQL: causa raiz e retentativa na validação do email-service"
data: 2026-11-09
periodo: 2026QD3
categorias:
  - incidente
  - qualidade
impacto: alto
fontes:
  - "[[alertas-de-envio]]"
  - "[[cloud-sql-alteracoes-com-restart]]"
---

# E-mails perdidos no restart do Cloud SQL: causa raiz e retentativa na validação do email-service

## Contexto

O alerta "Falha ao validar o e-mail" do email-service disparou em 09/11/2026 às 07:10 para um template do experts-service. Parecia um erro de payload, mas a causa foi uma alteração manual da instância Cloud SQL `atendimento-canais` (HA regional), que reiniciou o Postgres.

## O que fiz

- Cruzei o alerta com os logs dos pods e o audit log do Cloud SQL e mostrei que o erro era de infraestrutura (`57P01` e timeout de conexão), não de validação.
- Achei a causa no código: o `errorHandler` do `ValidationWorker` dava ack em qualquer exceção, sem retentar. O mesmo defeito já tinha causado perda no disparo massivo de 15/10 (#49).
- Abri o work-item #52 e implementei a correção: nack em erro passageiro, ack direto só em falha permanente ou payload ilegível, e, na última das 5 tentativas, callback para a origem e envio à DLQ com o payload inteiro para poder republicar. Também extraí o helper de última tentativa compartilhado com o enqueue worker. Cobertura de 100% nos arquivos alterados.

## Resultado

- 2 e-mails perdidos recuperados no mesmo dia, sem código e sem escrita em banco de prd. O payload foi achado na `task_scheduler` do experts-service, cruzando os 54 avisos do lote com `email_replications` (52 SENT, 2 sem registro). Os 2 foram republicados no tópico e saíram SENT em cerca de 5 s (PRD-175908).
- Uma queda de banco dentro da janela de retentativa deixa de descartar envios, e o que esgota as tentativas fica recuperável pela DLQ.
- Validado em dev com o banco derrubado: um envio passou na 3ª tentativa depois que o banco voltou; outro esgotou as 5 tentativas, avisou a origem e foi para a DLQ com o payload inteiro (evidências com prints na pasta da feature no BahCode, `evidencias/`).

## Continuação: replicação órfã em rajada (#49, caso 2, 19/11/2026)

- O mesmo esgotamento do pool reapareceu em 17/11 e 19/11 com outro sintoma: o dispatch rodava antes de a linha existir (`REPLICATION_NOT_FOUND`, falha permanente) e o e-mail ficava `PENDING` para sempre (8 envios de guias do experts-service). Confirmei a sequência pelos logs e documentei no #49.
- Corrigi pela causa, não pelo sintoma: a linha é gravada antes do publish no `send-email-validated` (validação e rota `POST /send`), com nack se o insert falhar. O consumer `replicate-record`, que concorria com o dispatch e dividia o pool, foi removido.
- Planejei o deploy em duas etapas (código e alerta primeiro; a subscription só depois do deploy em prd), porque o terraform roda antes do helm e removê-la junto abriria uma janela com `REPLICATION_NOT_FOUND` em todos os envios.

- Validação em prd no mesmo dia do deploy (23/11): teste simples pelo tópico e pela rota e rajada de 20 envios, todos `SENT` e com a linha gravada antes do enfileiramento. Os 8 e-mails presos foram reenviados e entregues, a partir do payload original do experts-service, depois de conferir que nenhuma guia tinha sido notificada de novo. O caso de 15/10 foi descartado porque as guias já estavam vencidas (PRD-178304, PRD-178307).
- Nos testes, achei que 15 logs perdiam todos os campos em prd por causa da ordem dos argumentos do pino. Corrigi e atualizei o AGENTS.md para o agente de código não repetir o erro (MR !81, PRD-178406).

## Evidências

- Work-item: https://gitlab.com/ctbz/experts/atendimento-canais/email-service/-/work_items/52
- Branch `fix/validation-transient-retry` (email-service)
- Work-item #49 (caso 2): https://gitlab.com/ctbz/experts/atendimento-canais/email-service/-/work_items/49 — branches `fix/record-before-dispatch` e `chore/remove-replicate-record-sub`
- [[alertas-de-envio]]
