---
name: dependencias-mcp-notas-fiscais
description: "Dependências do mcp-notas-fiscais: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - mcp-notas-fiscais
repositorio: mcp-notas-fiscais
---

# Dependências do mcp-notas-fiscais

O que o `mcp-notas-fiscais` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `978d78c` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `experts-nfs` (7×): `app/tools/emitir_nota.py:47`, `app/tools/emitir_nota_exterior_retroativa.py:14`, `app/tools/emitir_nota_nacional_retroativa.py:14`
- `experts-service` (6×): `app/clients/experts_service_client.py:24`, `app/clients/__tests__/test_experts_service_client.py:45`
- `contabilizei-agents` (3×): `Makefile:29`
- `emissor-whatsapp` (2×): `app/clients/experts_nfs_client.py:125`, `app/clients/__tests__/test_experts_nfs_client.py:90`

### Repositórios que citam este

- `contabilizei-agents` (14×): `app/agents/before_tool.py:31`, `app/agents/mcp.py:9`, `app/agents/__tests__/before_tool_test.py:248`
- `zendesk-agents` (4×): `src/infra/clients/index.ts:3`, `src/infra/clients/mcp-notas-fiscais.client.ts:11`, `src/infra/clients/mcp-notas-fiscais.client.spec.ts:2`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `cnpj-alfanumerico`, `k8s-configmap`, `kong-config`

### No grafo manual ([[grafo-chamadas-canais]])

- Consome: `experts-nfs`, `experts-service`
- Consumido por: `contabilizei-agents`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Fila Cloud Tasks**: `emissor-whatsapp`
- **Cloud Run / function**: `contabilizei-agents`, `emissor-whatsapp`, `experts-nfs`

### Bancos e dados

- Redis: `redis`

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
