---
name: 2026-11-27-rotas-pubsub-abertas-agrupamento
description: "Correção do achado P0 do Farol: rotas /pubsub do microsservico-agrupamento-guias publicavam em qualquer tópico sem autenticação"
metadata:
  type: project
tags:
  - performance
titulo: "Rotas /pubsub abertas no microsservico-agrupamento-guias (Farol P0)"
data: 2026-11-27
periodo: 2026QD3
categorias: [seguranca]
impacto: alto
fontes: ["[[PRD-179714]]", "[[rota-pubsub-sem-autenticacao]]"]
---

# Rotas /pubsub abertas no microsservico-agrupamento-guias (Farol P0)

## Contexto

O Farol apontou como P0 que o `PubSubApi` do `microsservico-agrupamento-guias` expunha `POST /pubsub/{topico}`, que publica qualquer body em qualquer tópico do Pub/Sub com a Service Account do pod. Isso permitiria injetar mensagens nos tópicos de envio de e-mail e WhatsApp e mandar guias e boletos falsos aos clientes pelos canais oficiais.

## O que fiz

- Validei o achado contra o código e a config do Kong: pela internet sem credencial não alcança (key-auth + ACL), mas alcança por qualquer um dos 5 consumers do grupo (o Kong libera todo o prefixo) e por qualquer pod do cluster, sem credencial. Também identifiquei que o tópico aceita nome completo de outro projeto, limitado só pelo IAM da SA, e corrigi premissas do relatório (host, build Maven).
- Confirmei que as rotas não tinham consumidor (outros repositórios e Bruno), abri o card com sub-tasks e o MR que remove o controller, o teste e as rotas do catálogo.
- Deixei mapeados os próximos passos de defesa em profundidade (IAM da SA restrito aos tópicos usados, autenticação na aplicação).

## Resultado

Superfície de publicação arbitrária no Pub/Sub de prod removida, sem impacto em consumidores (1166 testes passando).

## Evidências

- [[PRD-179714]] · MR !105 https://gitlab.com/ctbz/experts/atendimento-canais/microsservico-agrupamento-guias/-/merge_requests/105
- Análise: [[rota-pubsub-sem-autenticacao]]
