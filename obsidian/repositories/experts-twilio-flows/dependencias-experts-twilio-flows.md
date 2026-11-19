---
name: dependencias-experts-twilio-flows
description: "Dependências do experts-twilio-flows: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - experts-twilio-flows
repositorio: experts-twilio-flows
---

# Dependências do experts-twilio-flows

O que o `experts-twilio-flows` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `6d18589` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `emissor-whatsapp` (16×): `whatsapp/main/hom/parent_flow.json:2016`, `whatsapp/main/hom/subflows/CadTomador.json:153`, `whatsapp/main/hom/subflows/NFIndiv.json:1438`

### Repositórios que citam este

_Nenhum._

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `twilio-metrics-flow`
- **Subscription**: `twilio-metrics-flow`
- **Fila Cloud Tasks**: `emissor-whatsapp`, `feedback-hub`
- **Cloud Run / function**: `emissor-whatsapp`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `docs/git_workflow.md:153`

<!-- deps:auto:fim -->
