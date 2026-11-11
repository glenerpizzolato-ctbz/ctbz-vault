---
name: infra-indice
description: "Índice de notas de infraestrutura GCP: onde cada serviço roda (GKE, Cloud Run, functions), Pub/Sub, Scheduler e Cloud Tasks por projeto, com repositórios que citam cada recurso"
metadata:
  type: reference
tags:
  - infra-indice
---

# Infra

Catálogo de onde cada serviço e recurso roda na GCP, para localizar rapidamente um serviço que está fora, um tópico sem consumidor ou um agendamento que não disparou. O mapa de projetos por domínio fica no `CLAUDE.md` global; aqui ficam as listas.

As notas são geradas pelo script da skill `atualizar-catalogo-gcp` (`~/.claude/skills/atualizar-catalogo-gcp/`); não editar à mão, rodar a skill de novo. Última geração: 2026-10-09.

Campos: **repos** = repositórios em `~/repositories` cujo código cita o nome exato do recurso (produtor, consumidor ou quem cria); **config** = repos de configuração que citam quase tudo; **consumidor provável** = prefixo do nome da subscription (convenção `<consumidor>.sub.<evento>`); push → serviço que recebe o push.

## Serviços

- [[gke-workloads|Workloads no GKE]] — deployments, statefulsets e cronjobs por cluster (dev/prod, privado/público) e namespace
- [[cloud-run-servicos|Cloud Run e functions]] — serviços Cloud Run, Cloud Run functions e jobs por projeto

## Mensageria e agendamentos

- [[schedulers|Cloud Scheduler]] — agendamentos por projeto: cron, alvo e repositórios
- [[cloud-tasks|Cloud Tasks]] — filas por projeto: taxa, tentativas e repositórios
- [[pubsub-atendimento-canais-dev|Pub/Sub atendimento-canais-dev]] — Atendimento / canais, dev: 20 tópicos, 43 subscriptions
- [[pubsub-atendimento-canais-prd|Pub/Sub atendimento-canais-prd]] — Atendimento / canais, prod: 19 tópicos, 47 subscriptions
- [[pubsub-contabilizei-experts-dev|Pub/Sub contabilizei-experts-dev]] — Experts, dev: 50 tópicos, 74 subscriptions
- [[pubsub-contabilizei-experts-prd|Pub/Sub contabilizei-experts-prd]] — Experts, prod: 41 tópicos, 61 subscriptions
- [[pubsub-aida-stg|Pub/Sub aida-stg]] — AIDA, dev/stg: 23 tópicos, 23 subscriptions
- [[pubsub-aida-prd|Pub/Sub aida-prd]] — AIDA, prod: 32 tópicos, 38 subscriptions
- [[pubsub-contabilizei-crm-dev|Pub/Sub contabilizei-crm-dev]] — CRM, dev: 180 tópicos, 284 subscriptions
- [[pubsub-contabilizei-crm|Pub/Sub contabilizei-crm]] — CRM, prod: 125 tópicos, 173 subscriptions
- [[pubsub-contabilizeiapp-dev-02|Pub/Sub contabilizeiapp-dev-02]] — App Contabilizei, dev: 13 tópicos, 9 subscriptions
- [[pubsub-contabilizei-impostos-teste|Pub/Sub contabilizei-impostos-teste]] — Impostos, dev: 203 tópicos, 210 subscriptions
- [[pubsub-contabilizei-impostos|Pub/Sub contabilizei-impostos]] — Impostos, prod: 198 tópicos, 225 subscriptions
- [[pubsub-contabilizei-issue|Pub/Sub contabilizei-issue]] — Issue, dev/prod: 7 tópicos, 7 subscriptions
- [[pubsub-fintech-228118|Pub/Sub fintech-228118]] — Fintech, prod: 131 tópicos, 128 subscriptions
- [[pubsub-contabilizei-dev-01|Pub/Sub contabilizei-dev-01]] — K8s dev, dev: 5 tópicos, 1 subscriptions

## Guias

- [[deploy-saude-pos-deploy|Deploys e saúde pós-deploy]] — achar os deploys pela API do GitLab, ler no log do job onde foram parar (Cloud Run, Terraform, GKE) e verificar a saúde pelo Cloud Monitoring sem VPN
- [[cloud-run-gen2-container-threat-detection|Cloud Run: Container Threat Detection exige gen2]] — deploy falha com INVALID_ARGUMENT em serviço gen1; trocar EXECUTION_ENVIRONMENT para gen2 (mín. 1 CPU / 512Mi)

## Arquitetura (manual)

- [[grafo-chamadas-canais|Grafo de chamadas Canais/Experts/AIDA]] — quem consome quem entre os repos do atendimento, papel e stack de cada um, fluxo do knowledge book e onde ficam envs, rotas do Kong, CI e libs

## Visões

- [[por-repositorio|Recursos GCP por repositório]] — para cada repo, os tópicos, subscriptions, schedulers, filas e serviços que ele cita
