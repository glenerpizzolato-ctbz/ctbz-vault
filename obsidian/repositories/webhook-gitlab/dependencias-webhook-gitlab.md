---
name: dependencias-webhook-gitlab
description: "Dependências do webhook-gitlab: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - webhook-gitlab
repositorio: webhook-gitlab
---

# Dependências do webhook-gitlab

O que o `webhook-gitlab` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `18afb91` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

_Nenhum._

### Repositórios que citam este

_Nenhum._
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `ide-bahcode`, `pipeline`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Scheduler**: `webhook-gitlab-canais-past-mr-reminder`, `webhook-gitlab-canais-today-mr-needs-attention`, `webhook-gitlab-canais-today-mr-reminder`
- **Cloud Run / function**: `webhook-gitlab`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- GitLab API: `gitlab.com/api` em `README.md:39`
- Google Chat: `chat.googleapis.com` em `README.md:49`

<!-- deps:auto:fim -->
