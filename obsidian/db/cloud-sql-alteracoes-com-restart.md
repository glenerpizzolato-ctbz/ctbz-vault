---
name: cloud-sql-alteracoes-com-restart
description: "Alterações de instância do Cloud SQL que reiniciam o Postgres (ex: habilitar alta disponibilidade/REGIONAL) e como identificar no audit log que um alerta veio delas"
metadata:
  type: reference
tags:
  - db
  - cloud-sql
---

# Alterações do Cloud SQL que derrubam conexões

Algumas alterações de instância do Cloud SQL reiniciam o Postgres e derrubam as conexões abertas, mesmo fora da janela de manutenção. A mais comum é habilitar alta disponibilidade (`settings.availabilityType: REGIONAL`, intents `UPDATE_ZONE` + `ENABLE_HIGH_AVAILABILITY`).

## Caso real (09/11/2026)

Na instância `atendimento-canais-prd:us-central1:atendimento-canais` (bancos do email-service, contato-service e bots-api), o HA foi habilitado manualmente às 06:59 BRT e a operação durou ~17 min (até 07:17). Nesse intervalo:

- 07:07 as conexões caíram com `57P01` (`terminating connection due to administrator command`, routine `ProcessInterrupts`).
- O `microsservico-agrupamento-guias` (GKE prod, pool `atendimento-canais-database-pool`) entrou em crash loop: o Flyway não conseguia conexão no boot (`SQL State 08001`, `Connection reset` no `enableSSL`) e o pod só subiu às 07:19, depois do fim da operação.
- O Grafana disparou às 07:19 o alerta `HTTP Error % • CANAIS • CHAT` (email-service 36% e agrupamento 100% de 5xx). A resolução chegou às 09:19 como um card com o mesmo título, `Instâncias: 0` e taxa 0,00%: card com `Instâncias: 0` é o aviso de resolvido, não um novo disparo.
- Até ~07:17 os health checks de banco dos pods estouravam timeout (`health check 'database' timed out after 2000ms`) e as queries falhavam com `Connection terminated due to connection timeout`.

## Como identificar

```bash
# operações recentes da instância (UPDATE manual coincide com a janela do alerta?)
gcloud sql operations list --instance <instancia> --project <projeto> --limit 8
# o que foi alterado e por quem
gcloud logging read 'protoPayload.serviceName="cloudsql.googleapis.com" AND protoPayload.methodName:"instances.update"' --project <projeto> --limit 5 --format=json
```

O `request.body` traz o patch (ex: `{"settings": {"availabilityType": "REGIONAL"}}`) e o `metadata.intents` do evento de conclusão mostra o efeito (`ENABLE_HIGH_AVAILABILITY`).

Serviços que tratam erro transitório de banco como falha definitiva (ack sem retry) perdem mensagens nessa janela: ver [[alertas-de-envio]] no email-service.
