---
name: dependencias-cnpj-alfanumerico
description: "Dependências do cnpj-alfanumerico: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - cnpj-alfanumerico
repositorio: cnpj-alfanumerico
---

# Dependências do cnpj-alfanumerico

O que o `cnpj-alfanumerico` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `6722cff` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `emissor-whatsapp` (6×): `clone.sh:2`, `experts-nfs-analysis.md:45`
- `experts-admin` (3×): `clone.sh:11`, `experts-admin-analysis.md:1`
- `contabilizei-agents` (3×): `clone.sh:18`, `contabilizei-agents-analysis.md:1`
- `experts-nfs` (2×): `clone.sh:5`, `experts-nfs-analysis.md:1`
- `experts-service` (2×): `clone.sh:6`, `experts-service-analysis.md:1`
- `experts-tarefas-assessor` (2×): `clone.sh:7`, `experts-tarefas-assessor-analysis.md:1`
- `ms-relatorio-faturamento` (2×): `clone.sh:9`, `ms-relatorio-faturamento-analysis.md:1`
- `ticketing-service` (2×): `clone.sh:10`, `ticketing-service-analysis.md:1`
- `tarefas-assessor-admin` (2×): `clone.sh:14`, `tarefas-assessor-admin-analysis.md:1`
- `mcp-notas-fiscais` (2×): `clone.sh:17`, `mcp-notas-fiscais-analysis.md:1`
- `zendesk-agents` (2×): `clone.sh:21`, `zendesk-agents-analysis.md:1`
- `emissor-whatsapp-reports` (1×): `clone.sh:2`
- `experts-alertas` (1×): `clone.sh:3`
- `experts-ms-nps` (1×): `clone.sh:4`
- `html-to-pdf` (1×): `clone.sh:8`
- `relacionamento-admin` (1×): `clone.sh:12`
- `relatorio-faturamento-admin` (1×): `clone.sh:13`
- `file-transcriber` (1×): `clone.sh:16`
- `experts-dominios-functions` (1×): `clone.sh:19`
- `relacionamento-service` (1×): `clone.sh:20`
- `bots-api` (1×): `clone.sh:22`

### Repositórios que citam este

_Nenhum._

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Fila Cloud Tasks**: `emissor-whatsapp`
- **Cloud Run / function**: `contabilizei-agents`, `emissor-whatsapp`, `experts-nfs`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
