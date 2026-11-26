---
name: 2026-11-25-alertas-e-duplicatas-holerite
description: "Fim do holerite enviado em dobro e primeiros alertas do envio de holerite (subscription própria com DLQ, alertas de Pub/Sub testados em prd, trava de destroy do deploy)"
metadata:
  type: project
tags:
  - performance
titulo: "Fim do holerite em dobro e alertas do envio de holerite por e-mail"
data: 2026-11-25
periodo: 2026QD3
categorias: [qualidade, entrega]
impacto: alto
fontes: ["[[PRD-178821]]", "[[observabilidade-holerite]]", "[[e2e-holerite-dev]]", "[[experts-functions-deploy-prd-trava-destroy]]"]
---

# Fim do holerite em dobro e alertas do envio de holerite por e-mail

## Contexto

A `function-email-holerites` recebia as folhas por uma subscription do Eventarc com ack de 10 s e sem DLQ. Em prd, 8% das requisições passavam de 10 s e eram reentregues ainda em processamento, então o cliente recebia o holerite em dobro. Uma folha que falhava sempre sumia depois de 24 h, e nenhuma falha do fluxo gerava alerta.

## O que fiz

- **Subscription própria (experts-functions !11 e !14):** ack de 600 s e DLQ depois de 10 tentativas. Para a DLQ funcionar sem `pubsub.admin`, dei ao service agent do Pub/Sub roles mínimas pelo vault-roleset (!728 e !729).
- **Testes E2E em dev, com script no vault:** caminho feliz 17/17; DLQ nas 3 rodadas, com 10 tentativas cada; requisições de até 47 s sem nenhuma reentrega simultânea.
- **Alertas de Pub/Sub (!12):** holerite na DLQ e folha parada na fila. Testei em prd sem impacto em cliente, publicando direto no tópico da DLQ: o incidente abriu e fechou sozinho, e as evidências estão na PRD-178827.
- **Alertas de log ERROR com CNPJ e período e de taxa de 5xx (!13):** a regra de 5xx foi validada contra 30 dias de prd e teria pego as quedas de 26 a 29/10 e de 04/11.
- **Duplicação durante a virada:** quando o deploy deixou as duas subscriptions ativas ao mesmo tempo, apaguei o trigger antigo na hora. Também corrigi a pipeline central (pipeline!3568): tirei os imports one-off, que iam quebrar todo deploy, e deixei a trava de destroy liberável por `TF_ALLOW_DESTROY`.

## Resultado

- O holerite em dobro acabou em prd em 25/11/2026. Só existem a `function-email-holerites-sub` e a DLQ no tópico.
- Uma folha que falha não se perde mais: fica 7 dias na DLQ e avisa o canal `[chat] Alertas - GCP Experts`.
- O fluxo passou a ter 4 alertas. Antes, nenhuma falha dele gerava alerta.

## Evidências

- Jira: PRD-178821, com as sub-tasks PRD-178822, PRD-178824, PRD-178825, PRD-178846, PRD-178912 e PRD-179355; os testes estão na PRD-178827, nos comentários 29991764 e 30045804.
- MRs: experts-functions !11, !12, !13 e !14; vault-roleset !728 e !729; pipeline !3568.
- Notas: [[observabilidade-holerite]], [[e2e-holerite-dev]], [[experts-functions-deploy-prd-trava-destroy]].
