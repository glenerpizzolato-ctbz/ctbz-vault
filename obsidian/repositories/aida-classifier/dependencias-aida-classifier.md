---
name: dependencias-aida-classifier
description: "Dependências do aida-classifier: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - aida-classifier
repositorio: aida-classifier
---

# Dependências do aida-classifier

O que o `aida-classifier` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `2253d6f` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `aida-back` (13×): `.env.example:23`, `app/routers/aida_back.py:2`, `app/schemas/aida_back.py:54`

### Repositórios que citam este

- `sentinela-atendimento` (7×): `sentinela_atendimento/zendesk/api/dto/pubsub_dto.py:143`, `sentinela_atendimento/zendesk/service/tema_origem.py:6`, `sentinela_atendimento/zendesk/service/ticket_classification_service.py:16`
- `aida-back` (1×): `contabilizeiai/config/config.py:86`
- `zendesk-agents` (1×): `src/infra/google-cloud/pubsub/topics.ts:9`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `pipeline`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `aida-classifier-classification-event`
- **Fila Cloud Tasks**: `aida-classifier`

### Bancos e dados

- Cloud Tasks: `google-cloud-tasks`
- Firestore: `google-cloud-firestore`
- Pub/Sub: `google-cloud-pubsub`
- Redis: `redis`

### Terceiros

- OpenAI: `openai`
- Zendesk: `example.zendesk.com` em `tests/unit/services/test_zendesk_service.py:20`

<!-- deps:auto:fim -->
