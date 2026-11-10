---
name: experts-service-deploy-e-variaveis-de-ambiente
description: "experts-service: onde ficam as variáveis de deploy (CI/CD do GitLab) x as do app, onde roda no GKE e a concorrência do consumer de guias"
metadata:
  type: reference
tags:
  - experts-service
  - deploy
  - pubsub
atualizado_em: 2026-11-10
---

# Deploy e variáveis de ambiente

- O deploy é pelo componente `ctbz/devops/recursos/pipeline/ci-cd` (helm, job `helm-deploy-gke-<env>` com o `gke-deployer`, no cluster privado, namespace `experts-<env>`). As variáveis de deploy **e as do app** ficam no repositório `~/repositories/pipeline` (`gitlab.com/ctbz/devops/recursos/pipeline`), em `custom/ctbz/experts/backend/experts-service.yml` (comum), `experts-service.dev.yml` e `experts-service.prd.yml`, no bloco `variables:`. É o mesmo lugar onde o `atendimento-zendesk` define as suas (ex: `METRICS_EVENTS_MAX_MESSAGES`). A listagem das variáveis de CI do projeto pela API do GitLab mostra o resultado dessas customizações.
- Escala em prd: `SCALEDOBJECT_*` (KEDA) de 2 a 5 réplicas, por CPU 50% e por um trigger externo do Prometheus que só olha a subscription `experts-service.sub.desconexao.evalutate-message-ia`. A `experts-service.sub.guia-imposto` não está no trigger.
- Os tokens do app (`TOKEN_ZENDESK`, `TOKEN_PLATAFORMA`...) não aparecem nesses arquivos: devem vir de variáveis protegidas/mascaradas do projeto ou de um secret; não confirmado.

## Concorrência do consumer de guias

- `GuiaImpostoNotifierConsumer` (`experts-service.sub.guia-imposto`): `maxMessages` = `CONSUMER_GUIA_IMPOSTO_NOTIFIER_MAX_MESSAGES`, padrão 10 desde 2026-11-10 (antes 3), `maxStreams: 1`, `allowExcessMessages: false`. Work-item #18.
- Motivo: rajada do fintech em 2026-11-09 (~63 mil guias, ~26 msg/s) deixou a mensagem mais antiga 34 min sem ack; com 3 por pod e o HPA em 5 pods a vazão parou em ~23 msg/s, com a CPU em ~10%.
- Limite para subir mais: o pool do Postgres é `max: 4`, compartilhado pela API e por todos os consumers (instância do Cloud SQL perto do `max_connections`), e cada mensagem consulta a API de empresa/plano da plataforma.
- **Armadilha do `PubsubConsumer`** (`src/infra/google-cloud/pubsub-consumer.ts`): quando a subscription ainda não existe, o `getSubscription` devolve o objeto do `sub.create(...)`, e o `flowControl` passado em `subOpts` não é aplicado (num teste com o emulador, 200 mensagens rodaram em paralelo com `maxMessages` 3). Só vale até o próximo restart; em prd as subscriptions já existem.
- **Como medir a concorrência localmente:** subir `messagebird/gcloud-pubsub-emulator`, criar tópico e subscription antes, instanciar o consumer real com as dependências simuladas com latência e contar as mensagens em processamento. Script usado no PRD-176493 (fora do repo).
