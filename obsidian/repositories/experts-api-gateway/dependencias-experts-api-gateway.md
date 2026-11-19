---
name: dependencias-experts-api-gateway
description: "Dependências do experts-api-gateway: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - experts-api-gateway
repositorio: experts-api-gateway
---

# Dependências do experts-api-gateway

O que o `experts-api-gateway` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `8af1230` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `emissor-whatsapp` (15×): `config/kong-template.yml:15`
- `experts-nfs` (6×): `config/kong-template.yml:40`
- `experts-zendesk` (5×): `config/kong-template.yml:35`
- `experts-twilio` (4×): `Makefile:12`, `config/kong-template.yml:5`
- `emissor-whatsapp-reports` (3×): `config/kong-template.yml:15`
- `experts-async-publisher` (3×): `config/kong-template.yml:20`

### Repositórios que citam este

- `emissor-whatsapp` (2×): `docs/bruno/environments/ctbz-exp-dev.bru:11`, `docs/bruno/environments/ctbz-exp-prd.bru:12`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `experts-drawio`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Fila Cloud Tasks**: `emissor-whatsapp`, `emissor-whatsapp-massivo`, `experts-zendesk`
- **Cloud Run / function**: `emissor-whatsapp`, `emissor-whatsapp-massivo`, `emissor-whatsapp-reports`, `experts-api-gateway`, `experts-async-publisher`, `experts-nfs`, `experts-twilio-metrics`, `experts-zendesk`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
