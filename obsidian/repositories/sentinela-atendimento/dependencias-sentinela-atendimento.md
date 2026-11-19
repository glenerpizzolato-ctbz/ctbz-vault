---
name: dependencias-sentinela-atendimento
description: "Dependências do sentinela-atendimento: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - sentinela-atendimento
repositorio: sentinela-atendimento
---

# Dependências do sentinela-atendimento

O que o `sentinela-atendimento` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `6c09351` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `aida-back` (55×): `sentinela_atendimento/infra/config/config.py:109`, `sentinela_atendimento/super_ouvidoria/api/dto/super_ouvidoria_dto.py:1`, `sentinela_atendimento/super_ouvidoria/repository/classificador_temas_repository.py:1`
- `aida-classifier` (7×): `sentinela_atendimento/zendesk/api/dto/pubsub_dto.py:143`, `sentinela_atendimento/zendesk/service/tema_origem.py:6`, `sentinela_atendimento/zendesk/service/ticket_classification_service.py:16`
- `aida-front` (4×): `sentinela_atendimento/super_ouvidoria/repository/super_ouvidoria_repository.py:3`, `.context/_meta/key-decisions.md:342`, `.context/workflows/super-ouvidoria-flow.md:15`
- `atendimento-zendesk` (2×): `sentinela_atendimento/infra/config/config.py:76`

### Repositórios que citam este

- `aida-front` (4×): `.env.development:26`, `.env.production:27`, `.env.staging:22`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `pipeline`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

- BigQuery: `google-cloud-bigquery`
- Cloud Tasks: `google-cloud-tasks`
- Firestore: `google-cloud-firestore`
- Pub/Sub: `google-cloud-pubsub`
- Redis: `redis`

### Terceiros

- Google Gemini / Vertex AI: `google-cloud-aiplatform`
- LiteLLM (gateway de LLMs): `litellm`
- Zendesk: `contabilizei.zendesk.com` em `tests/api/test_zendesk_worker_api.py:153`, `media.zendesk.com` em `tests/api/test_zendesk_worker_api.py:871`, `test.zendesk.com` em `tests/zendesk/service/test_zendesk_api_client.py:58`

<!-- deps:auto:fim -->
