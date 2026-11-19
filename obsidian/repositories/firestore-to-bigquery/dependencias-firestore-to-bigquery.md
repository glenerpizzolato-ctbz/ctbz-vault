---
name: dependencias-firestore-to-bigquery
description: "Dependências do firestore-to-bigquery: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - firestore-to-bigquery
repositorio: firestore-to-bigquery
---

# Dependências do firestore-to-bigquery

O que o `firestore-to-bigquery` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `f18dcbe` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-abertura` (25×): `configs/robots-ccm.json:2`, `configs/robots-chat-blip-atvalgomais.json:2`, `configs/robots-chat-blip-atvbalcaounico.json:2`
- `emissor-whatsapp` (3×): `configs/experts-notaswpp-massivo-lotes.json:3`, `configs/experts-notaswpp-massivo-notas.json:3`, `configs/experts-notaswpp-singular.json:3`

### Repositórios que citam este

_Nenhum._

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Fila Cloud Tasks**: `emissor-whatsapp`, `notas-recorrentes`
- **Cloud Run / function**: `emissor-whatsapp`

### Bancos e dados

- BigQuery: `google-cloud-bigquery`
- Cloud Storage: `google-cloud-storage`
- Firestore: `google-cloud-firestore`

### Terceiros

- Firebase: `firebase-admin`
- Google Chat: `chat.googleapis.com` em `utils/chat_notification.py:7`

<!-- deps:auto:fim -->
