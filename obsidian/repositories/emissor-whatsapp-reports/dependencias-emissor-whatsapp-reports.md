---
name: dependencias-emissor-whatsapp-reports
description: "Dependências do emissor-whatsapp-reports: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - emissor-whatsapp-reports
repositorio: emissor-whatsapp-reports
---

# Dependências do emissor-whatsapp-reports

O que o `emissor-whatsapp-reports` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `fix/cve-node2shell` @ `28134d4` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `emissor-whatsapp` (13×): `bitbucket-pipelines.yml:140`, `package.json:2`, `src/emissor-massivo.router.ts:6`
- `experts-nfs` (3×): `src/emissor-massivo/nota-link.ts:6`, `src/utils/config-manager/config.dev.ts:7`, `src/utils/config-manager/config.ts:7`

### Repositórios que citam este

- `experts-api-gateway` (3×): `config/kong-template.yml:15`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `cnpj-alfanumerico`, `experts-drawio`, `pipeline`

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Fila Cloud Tasks**: `emissor-whatsapp`
- **Cloud Run / function**: `emissor-whatsapp`, `emissor-whatsapp-reports`

### Bancos e dados

- Cloud Storage: `@google-cloud/storage`
- Firestore: `@google-cloud/firestore`
- Pub/Sub: `@google-cloud/pubsub`
- Secret Manager: `@google-cloud/secret-manager`

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
