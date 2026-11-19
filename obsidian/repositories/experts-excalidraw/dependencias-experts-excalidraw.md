---
name: dependencias-experts-excalidraw
description: "Dependências do experts-excalidraw: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - experts-excalidraw
repositorio: experts-excalidraw
---

# Dependências do experts-excalidraw

O que o `experts-excalidraw` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `1a90c07` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `html-to-pdf` (2×): `PRD-80587.excalidraw:533`
- `plataforma-crm-web` (2×): `arch.excalidraw:948`
- `plataforma-fopag-worker` (2×): `arch.excalidraw:1022`
- `atendimento-zendesk` (2×): `arch.excalidraw:2012`

### Repositórios que citam este

_Nenhum._

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Cloud Run / function**: `function-email-holerites`, `html-to-pdf`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
