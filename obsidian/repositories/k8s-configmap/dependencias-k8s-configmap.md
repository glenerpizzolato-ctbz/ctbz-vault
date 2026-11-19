---
name: dependencias-k8s-configmap
description: "Dependências do k8s-configmap: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - k8s-configmap
repositorio: k8s-configmap
---

# Dependências do k8s-configmap

O que o `k8s-configmap` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

## Consome

### Repositórios internos

_Nada confirmado ainda._

### Libs internas

_Nada confirmado ainda._

### Infra GCP

_Nada confirmado ainda._

### Bancos e dados

_Nada confirmado ainda._

### Terceiros

_Nada confirmado ainda._

## Consumido por

Quem consome os contratos deste repositório; a revisão de MRs confere se o diff quebra algum deles.

_Nada confirmado ainda._

<!-- deps:auto:inicio (gerado por mapear-dependencias; não editar à mão) -->

## Levantamento automático

Gerado em 2026-11-19 sobre `fix/agrupamento-guias-redis-sentinel` @ `23e991d2` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-abertura` (86×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atendimento-zendesk-dev.yaml:83`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atz-worker-adicionar-mensagem-privada-dev.yaml:83`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atz-worker-classificacao-atendimento-dev.yaml:83`
- `experts-service` (68×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/atendimento-canais-dev/bots-api.yaml:13`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atendimento-zendesk-dev.yaml:103`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atz-worker-adicionar-mensagem-privada-dev.yaml:103`
- `ticketing-service` (37×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atendimento-zendesk-dev.yaml:99`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atz-worker-adicionar-mensagem-privada-dev.yaml:99`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atz-worker-classificacao-atendimento-dev.yaml:99`
- `contato-service` (36×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/atendimento-canais-dev/bots-api.yaml:28`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/atendimento-canais-dev/contato-service.yml:4`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/atendimento-canais-dev/email-service.yml:26`
- `contabilizei-pagamentos` (36×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/billing-dev/contabilizei-adyen.yaml:7`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/billing-dev/contabilizei-iugu.yaml:7`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/billing-dev/contabilizei-pagamentos-cupom.yaml:4`
- `bots-api` (34×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/atendimento-canais-dev/bots-api.yaml:4`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atendimento-zendesk-dev.yaml:109`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atz-worker-adicionar-mensagem-privada-dev.yaml:109`
- `zendesk-agents` (32×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atendimento-zendesk-dev.yaml:108`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atz-worker-adicionar-mensagem-privada-dev.yaml:108`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atz-worker-classificacao-atendimento-dev.yaml:108`
- `plataforma-central-rotinas` (30×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atendimento-zendesk-dev.yaml:88`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atz-worker-adicionar-mensagem-privada-dev.yaml:88`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atz-worker-classificacao-atendimento-dev.yaml:88`
- `aida-back` (30×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atendimento-zendesk-dev.yaml:105`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atz-worker-adicionar-mensagem-privada-dev.yaml:105`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atz-worker-classificacao-atendimento-dev.yaml:105`
- `atendimento-zendesk` (25×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atendimento-zendesk-cronjob.yaml:4`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atendimento-zendesk-dev.yaml:4`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atendimento-zendesk.yaml:4`
- `contabilizei-impostos` (18×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/impostos-dev/contabilizei-robo-integrador.yaml:8`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/impostos-dev/rpa-regularize-pgfn.yaml:8`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/impostos-dev/rpa-simples-nacional.yaml:8`
- `monitoria-ia` (15×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atendimento-zendesk-dev.yaml:33`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atz-worker-adicionar-mensagem-privada-dev.yaml:33`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atz-worker-classificacao-atendimento-dev.yaml:33`
- `contabilizei-movimentacao-back` (11×): `contabilizei-dev-01/contabilizei-cluster-dev-01/contabil-dev/contabilizei-movimentacao-back-worker.yaml:4`, `contabilizei-dev-01/contabilizei-cluster-dev-01/contabil-dev/contabilizei-movimentacao-back.yaml:4`, `contabilizei-dev-01/contabilizei-cluster-dev-01/contabil-homolog/contabilizei-movimentacao-back-worker.yaml:4`
- `experts-nfs` (6×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/atendimento-canais-dev/bots-api.yaml:14`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/ia-dev/contabilizei-agents.yaml:19`, `contabilizei-dev-01/contabilizei-private-cluster-dev-01/ia-dev/mcp-notas-fiscais.yaml:9`
- `microsservico-agrupamento-guias` (3×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/atendimento-canais-dev/microsservico-agrupamento-guias.yaml:4`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/atendimento-canais-prd/microsservico-agrupamento-guias.yaml:4`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/impostos-prd/microsservico-agrupamento-guias.yaml:4`
- `atendimento-zendesk-cronjob` (3×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atendimento-zendesk-cronjob.yaml:4`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/crm-prd/atendimento-zendesk-cronjob.yaml:4`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/crm/atendimento-zendesk-cronjob.yaml:4`
- `relacionamento-service` (3×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/relacionamento-service.yaml:4`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/crm-prd/relacionamento-service.yaml:4`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/crm/relacionamento-service.yaml:4`
- `experts-ms-nps` (3×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/experts-dev/experts-ms-nps.yaml:4`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/experts-prd/experts-ms-nps.yaml:4`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/experts/experts-ms-nps.yaml:4`
- `ms-relatorio-faturamento` (3×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/experts-dev/ms-relatorio-faturamento.yaml:4`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/experts-prd/ms-relatorio-faturamento.yaml:4`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/experts/ms-relatorio-faturamento.yaml:4`
- `fintech-payments` (3×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/fintech-dev/fintech-payments.yaml:4`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/fintech-prd/fintech-payments.yaml:4`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/fintech/fintech-payments.yaml:4`
- `contabilizei-guias` (3×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/fintech-dev/fintech-payments.yaml:35`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/fintech-prd/fintech-payments.yaml:37`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/fintech/fintech-payments.yaml:37`
- `atendimento-canais-admin` (2×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/atendimento-canais-dev/atendimento-canais-admin.yml:4`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/atendimento-canais-prd/atendimento-canais-admin.yaml:4`
- `email-service` (2×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/atendimento-canais-dev/email-service.yml:4`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/atendimento-canais-prd/email-service.yaml:4`
- `canais-adk` (2×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/zendesk-agents.yaml:13`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/crm-prd/zendesk-agents.yaml:13`
- `contabilizei-agents` (2×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/ia-dev/contabilizei-agents.yaml:4`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/ia-prd/contabilizei-agents.yaml:4`
- `mcp-notas-fiscais` (2×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/ia-dev/mcp-notas-fiscais.yaml:4`, `contabilizei-prod-01/contabilizei-private-cluster-prod-01/ia-prd/mcp-notas-fiscais.yaml:4`
- `plataforma-faturamento-worker` (1×): `contabilizei-dev-01/contabilizei-private-cluster-dev-01/reforma-tributaria-dev/tax-radar.yaml:54`
- Configuração, CI e documentação citadas: `vault-roleset`

### Repositórios que citam este

- `survey-service` (21×): `.claude/skills/add-channel/SKILL.md:20`, `AGENTS.md:83`, `docs/PLAN.md:177`
- `atendimento-zendesk` (11×): `.context/tasks/prd-externalizar-configuracoes-env-vars/gap-analysis-env-dev.md:3`, `README.md:301`, `docs/redis-ioredis-migration.md:119`
- `canais-adk` (1×): `docs/nf-devolutiva-sessao.md:158`
- `meta-webhooks` (1×): `README.md:74`
- `relacionamento-service` (1×): `README.md:50`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `ide-bahcode`, `pipeline`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `classificacao-atendimento`, `fintech-crm.enviar-email`, `fintech-crm.enviar-push-notification`, `fintech-recebiveis.notificacao-015`, `fintech-recebiveis.retorno-liquidacao`, `fintech-recebiveis.retorno-registro-antecipacao-precontratada`, `parcelamento-rpa-callback`, `rpa-regularize-pgfn`, `rpa-simples-nacional`, `verificar-cancelamento-parcelamento-retorno`
- **Subscription**: `dataflow-batch-service`, `fintech-recebiveis.agendar-liquidacao-sub`, `fintech-recebiveis.registrar-antecipacao-precontratada-sub`, `rpa-regularize-pgfn-sub`, `rpa-regularize-pgfn-teste-sub`, `rpa-simples-nacional-sub`, `rpa-simples-nacional-teste-sub`
- **Cloud Run / function**: `bots-api`, `contabilizei-agents`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- GitLab API: `gitlab.com/api` em `contabilizei-prod-01/contabilizei-private-cluster-prod-01/ia-prd/ai-code-reviewer-web.yaml:20`
- Google Chat: `chat.googleapis.com` em `contabilizei-dev-01/contabilizei-private-cluster-dev-01/fintech-dev/fintech-conciliacao.yaml:19`
- Google Gemini / Vertex AI: `aiplatform.googleapis.com` em `contabilizei-dev-01/contabilizei-private-cluster-dev-01/reforma-tributaria-dev/tax-radar.yaml:20`, `generativelanguage.googleapis.com` em `contabilizei-dev-01/contabilizei-private-cluster-dev-01/reforma-tributaria-dev/tax-radar.yaml:24`
- Meta (WhatsApp Cloud API / Graph): `graph.facebook.com` em `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atendimento-zendesk-dev.yaml:111`
- Zendesk: `contabilizei.zendesk.com` em `contabilizei-prod-01/contabilizei-private-cluster-prod-01/crm-prd/atendimento-zendesk-prd.yaml:54`, `contabilizei1637606740.zendesk.com` em `contabilizei-dev-01/contabilizei-private-cluster-dev-01/crm-dev/atendimento-zendesk-dev.yaml:69`

<!-- deps:auto:fim -->
