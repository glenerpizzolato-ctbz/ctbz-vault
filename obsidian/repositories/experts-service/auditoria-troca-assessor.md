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

**Armadilha de segurança:** o hook `validateKeycloakJWT` (`src/infra/auth/keycloak.ts`, aplicado só nas rotas `/view`) usa `keycloak.jwt.decode`, que não verifica a assinatura (a própria lib `keycloak-backend` avisa); confere apenas `exp` e `aud` contendo `experts-service`. Um JWT com assinatura inválida é aceito e o `email` dele vira o autor. As rotas `/v1` não têm hook nenhum (o autor vem do body). Confirmado em teste local em 2026-11-06 ([[PRD-165484]]); falta conferir se a borda valida o token.

**Teste ponta a ponta local:** dá para montar o app real com `getServer()` de `src/app.ts` + `getTestDatabase()`/`getTestPubsub()` (testcontainers) e um `EventConsumer` para ver a linha na tabela `event`. A migração de carteira chama o Zendesk antes (`getOrganizationField`), então precisa de `vi.mock('@infra/http-clients/zendesk')` como no `assessor.api.spec.ts`. Não subir o serviço com o `.env` local padrão: o `PUBSUB_ENDPOINT` vem comentado e o `GCLOUD_PROJECT` aponta para `contabilizei-experts-dev`, então o serviço consumiria as subscriptions reais de dev.

**Rotas `/view` no Bruno:** documentadas em `docs/bruno/view/` (assessor, empresa, events, batch, nfs), cada uma com `auth: bearer {{admin_bearer}}` (o `x-ctbz-api-gateway-token` é herdado da coleção). Preencher `admin_bearer_dev`/`admin_bearer_prd`/`admin_bearer_local` em `docs/bruno/.env`. A requisição `view/events/list-events` tem o passo a passo para validar a assinatura (token válido → 200, sem token → 401, token adulterado → hoje 200).

**Fix da verificação de assinatura (2026-11-06):** [[PRD-175691]] / sub-task PRD-175692. Branch `fix/PRD-165484` no `experts-service` troca `keycloak.jwt.decode` por `verifyOffline` em `src/infra/auth/keycloak.ts` (JWKS do realm `ctbz` em `/protocol/openid-connect/certs`, cache + `kid`, fail-closed: 401 inválido/expirado/sem token, 403 sem `aud`). Teste em `src/infra/auth/keycloak.spec.ts`. O hook `createValidateKeycloakJWT` aceita um resolvedor de chave injetável, usado no teste com par RSA gerado na hora.

**Como testar a validação em dev (2026-11-06):** o browser não manda `Authorization`; o `experts-admin` fala com o Zelador por cookie de sessão, e o Zelador injeta o Bearer do Keycloak na chamada ao serviço. Então o caso "token válido → 200" se testa pela própria tela (aba HISTÓRICO), e os casos "sem token / assinatura adulterada → 401" chamando `api-dev…/experts-service/view/...` direto pelo Bruno. As secrets `api_key_dev` (API key) e `access_token_exp_dev` (token do Heimdall/atendimento-zendesk) do `docs/bruno/.env` não são JWT e não servem como Bearer; nenhuma secret local gera um token aceito (RS256 com a chave privada do realm).

**Armadilha do `hasRole`:** `src/infra/auth/helpers.ts` lê `user.resource_access['experts-service'].roles` sem checar nulo. Usuário com `experts-service` no `aud`, mas sem papel nesse client do Keycloak, recebe **500** (`Cannot read properties of undefined (reading 'roles')`) em vez de 403 nas rotas com `hasRole` (ex: troca de assessor `PUT /view/v1/empresa/:cnpj/assessor`). Já existia antes do fix de assinatura (o `helpers.ts` não mudou). Para testar a troca em dev, o usuário precisa do papel `gerente*.editor` ou `assessor*.editor` no client `experts-service` do realm `ctbz`.
