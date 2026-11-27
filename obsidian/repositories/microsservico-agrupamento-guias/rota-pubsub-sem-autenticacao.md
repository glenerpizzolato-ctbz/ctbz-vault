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

## Origem do PubSubApi (git)

- Criado em 2022-10-18 por Kathelin D'Agostin (`573338bc`), poucos dias após o commit inicial do repo (2022-10-06), como utilitário para simular os eventos de guia: atributos fixos de dev (`sistema-origem=s~contabilizeiapp-dev-02`, `bucket-name=impostos-teste`, CNPJ fixo). Ajustes até 2022-12-01 (Kathelin, Renan Monticelli). O tópico sempre foi livre pelo path e o controller sempre subiu em prod.
- 2026-11-09, Bruno Menescal (`356ca28d`, "[PRD-167515] Ajuste rota local"): os atributos passaram a vir livres da query, o que ampliou o risco. Isso perdeu o `deleted`, que voltou em 2026-11-10 (`aa58fc48`), junto com o `PubSubApiTest`. A intenção era uso local, mas faltou o `@Profile("local")`.
- 2026-11-27: MR !105 mergeado (`b0b9f314`) e publicado em dev (helm revision 46). E2E em dev pelo Kong (`api-dev.contabilizei.com.br/agrupamento-guias`, token `DECK_BRUNO_EXPERTS_TO_MICROSSERVICO_AGRUPAMENTO_GUIAS_DEV` do `docs/bruno/.env`): `/pubsub/*` com token → 404 do Spring; sem token → 401 do Kong; rota legítima → 200; os 9 consumers subiram. Evidências na PRD-179716 (concluída). Prod ainda pendente.

## Como testar o deploy em dev sem VPN

O pod roda no `contabilizei-private-cluster-dev-01` (namespace `atendimento-canais-dev`), que exige VPN para o `kubectl`. Para acompanhar o rollout sem ela, usar o Cloud Logging do `contabilizei-dev-01`: filtro `resource.type="k8s_container" AND resource.labels.namespace_name="atendimento-canais-dev" AND resource.labels.container_name="microsservico-agrupamento-guias"`. A mensagem da aplicação fica em `jsonPayload.message` (`Started MicrosservicoAgrupamentoGuiasApplicationKt`, `started bean '...ChannelAdapter'`), e a contagem por `resource.labels.pod_name` mostra quando os pods antigos saíram (exit 143). Para testar uma rota inexistente sem efeito colateral, usar um nome de tópico inexistente.
