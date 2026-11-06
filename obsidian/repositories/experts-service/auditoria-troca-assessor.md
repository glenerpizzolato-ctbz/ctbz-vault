---
name: auditoria-troca-assessor
description: "Onde fica o autor das trocas de assessor no experts-service (event table, resolveAuthor, BigQuery) e como conferir"
metadata:
  type: reference
tags:
  - experts-service
---

# Auditoria das trocas de assessor (autor)

- Toda troca de assessor publica o evento `UPDATED_ASSESSOR_EMPRESA` via `PubsubClient.publishEvent` (`src/infra/google-cloud/pubsub-client.ts`), e o envelope (com `author`, `operation_id`, `batch_id`, `status`) vira linha na tabela `event` do banco `experts_service`.
- O autor vem de `resolveAuthor` (`src/domain/utils/fastify.utils.ts`): e-mail do token Keycloak (`request.user.email`), com fallback para o `author` do body; sem nenhum, a rota responde 400. Usado em `PUT /v1/empresa/:cnpj/assessor`, `POST /v1/massivo/empresa/update-assessor` (campo multipart `author`) e `PUT /v1/assessor/:oldAssessorId/empresas/migrate/:newAssessorId`. Trocas em lote também gravam o autor em `batch_operation.author`.
- **Armadilha:** não colocar `author` (nem campo novo) dentro de `data` do `UPDATED_ASSESSOR_EMPRESA`: o `plataforma-back-worker` (`UpdateAssessorEmpresaDTO`) não ignora propriedades desconhecidas e responde 400 em todo push da `plataforma.update-assessor-empresa-sub` (aconteceu entre 2026-09-28 e 2026-10-01, [[PRD-165484]]).
- A aba HISTÓRICO de `admin.ctbz.com.br/experts/#/assessoria` (`experts-admin`, `AssessoriaHistorico.service.ts`) lê `GET /v1/events?limit&offset`.
- BigQuery: `contabilizei-dataflow.dw_experts_service.event` (carga diária, mesmas colunas, `event_name`, `author`, `created_at`).

Conferir em prd (só leitura):

```sql
select date_trunc('week', created_at)::date semana, count(*) total,
       count(*) filter (where coalesce(author,'') = '') sem_autor
from event where event_name = 'UPDATED_ASSESSOR_EMPRESA' and created_at > now() - interval '60 days'
group by 1 order by 1;
```

`psql -w service=prd_experts_experts_service` (proxy `sql_exp_prd`, porta 5445).
