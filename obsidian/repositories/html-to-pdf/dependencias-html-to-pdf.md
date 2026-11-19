---
name: dependencias-html-to-pdf
description: "Dependências do html-to-pdf: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - html-to-pdf
repositorio: html-to-pdf
---

# Dependências do html-to-pdf

O que o `html-to-pdf` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `c05cc53` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

_Nenhum._

### Repositórios que citam este

- `experts-functions` (31×): `Dockerfile:14`, `catalog-info.yaml:11`, `catalog-model/apis/html-to-pdf-api.yaml:4`
- `experts-dominios-functions` (28×): `bitbucket-pipelines.yml:301`, `functions/email-holerites/src/services/holerite-sender.service.ts:6`, `functions/email-holerites/terraform/development/variables.tf:25`
- `ms-relatorio-faturamento` (5×): `src/domain/relatorio-financeiro/facade/index.ts:4`, `src/domain/relatorio-financeiro/facade/sign-relatorio/index.ts:6`, `src/infra/http-clients/index.ts:4`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `cnpj-alfanumerico`, `experts-excalidraw`, `pipeline`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Cloud Run / function**: `html-to-pdf`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
