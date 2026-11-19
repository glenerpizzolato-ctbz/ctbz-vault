---
name: dependencias-ultimate-ai-bpmn
description: "Dependências do ultimate-ai-bpmn: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - ultimate-ai-bpmn
repositorio: ultimate-ai-bpmn
---

# Dependências do ultimate-ai-bpmn

O que o `ultimate-ai-bpmn` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `97399a6` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `bots-api` (15×): `"bots/[prod] ctbz wpp main/use_cases/custom/bank/Wpp Bank | Autentica\303\247\303\243o Bank [A] [B] [E]/reply.bpmn":399`, `bots/[prod] ctbz wpp main/use_cases/custom/bank/Wpp Bank | Hours Router [A] [B] [E]/reply.bpmn:147`, `bots/[prod] ctbz wpp main/use_cases/custom/corretora/Wpp Corretora | Hours Router [A] [B] [E]/reply.bpmn:146`

### Repositórios que citam este

_Nenhum._

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Zendesk: `contabilizei.zendesk.com` em `bots/[prod] ctbz wpp main/use_cases/custom/exp/Wpp Exp | Outbound Especiais Jump [A] [B] [E]/metadata.json:9`

<!-- deps:auto:fim -->
