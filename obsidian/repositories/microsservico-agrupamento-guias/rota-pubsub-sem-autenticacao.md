---
name: rota-pubsub-sem-autenticacao
description: "Achado do Farol (P0): PubSubApi (/pubsub/{topico}) publica em qualquer tópico com a SA do pod; quem alcança de fato (Kong com key-auth/ACL x rede do cluster) e a correção"
metadata:
  type: project
tags:
  - microsservico-agrupamento-guias
  - seguranca
  - kong
analisado_em: 2026-11-27
---

# Rota /pubsub sem autenticação (achado do Farol)

`PubSubApi.kt` expõe `POST /pubsub/{pub-sub}` e `POST /pubsub/{pub-sub}/delete`, que chamam `pubSubTemplate.publish(topico, body, atributos)` sem nenhuma validação. Não tem `@Profile` (o `PubSubInitConfig` tem `@Profile("local")`) e o projeto não tem Spring Security: **nenhuma rota da aplicação autentica**, todas dependem do Kong e da rede.

## O que de fato está exposto (conferido em 2026-11-27)

- **Internet sem credencial: não.** No `kong-config/prd/heimdall_legado/atendimento-canais/microsservico-agrupamento-guias/microsservico-agrupamento-guias.yaml`, o serviço tem `key-auth` (`access_token` ou `x-ctbz-api-gateway-token`) + `acl` (grupo `microsservico-agrupamento-guias`). Hosts `api-gateway.contabilizei.com`, `api.contabilizei.com.br` e `api-gateway.ctbz.prd`, path `/agrupamento-guias` sem filtro de sub-path.
- **Qualquer consumer do Kong do grupo: sim.** Cinco consumers têm a ACL: `bruno-experts-to-…`, `bots-api-to-…`, `cronjob-to-…` (a chave das crons do Cloud Scheduler) e dois `deck_heimdall_legacy_to_many_*`. Quem tiver qualquer dessas chaves publica em qualquer tópico via `/agrupamento-guias/pubsub/<topico>`.
- **De dentro do cluster: sim, sem credencial nenhuma**, direto em `microsservico-agrupamento-guias.atendimento-canais-prd.svc.cluster.local:8080/pubsub/...` (salvo NetworkPolicy, não conferida).
- O tópico pode ser nome curto (projeto do pod) ou nome completo `projects/<p>/topics/<t>`; o limite real é o IAM da SA.
- Ninguém chama `/pubsub` em `~/repositories` nem na coleção Bruno; só o `api-docs.yaml` do catálogo documenta.

## Correção

Remover `PubSubApi.kt`, `PubSubApiTest.kt` e as duas rotas do `src/main/catalog-model/apis/api-docs.yaml` (ou `@Profile("local")` se quiserem manter para teste local). Mudança simples e sem consumidor. Defesa em profundidade, em cards à parte: restringir `pubsub.topics.publish` da SA aos tópicos usados e avaliar autenticação na aplicação.

## Andamento

- Card [[PRD-179714]] (épico CTS Eng Canais), sub-tasks PRD-179715 (dev) e PRD-179716 (e2e). MR draft !105, branch `feat/PRD-179714`, remove `PubSubApi`, o teste e as rotas do `api-docs.yaml`.
- Em aberto: IAM da SA e autenticação na aplicação.
