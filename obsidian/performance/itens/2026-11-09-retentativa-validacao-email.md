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

## Evidências

- Work-item: https://gitlab.com/ctbz/experts/atendimento-canais/email-service/-/work_items/52
- Branch `fix/validation-transient-retry` (email-service)
- [[alertas-de-envio]]
