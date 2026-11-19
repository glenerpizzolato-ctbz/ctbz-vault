---
name: dependencias-atalhos
description: "Dependências do atalhos: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - atalhos
repositorio: atalhos
---

# Dependências do atalhos

O que o `atalhos` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `fix/PRD-174640` @ `f47ad37` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `zendesk-agents` (26×): `public/data.js:105`
- `contabilizei-agents` (25×): `public/data.js:42`
- `bots-api` (22×): `public/app.js:462`, `public/data.js:33`, `README.md:33`
- `canais-adk` (18×): `.env.example:12`, `public/data.js:233`
- `experts-nfs` (17×): `public/data.js:388`, `README.md:30`
- `agent-eval` (13×): `public/data.js:215`
- `email-service` (12×): `public/data.js:69`
- `atendimento-canais-admin` (11×): `.env.example:12`, `public/data.js:224`
- `contato-service` (10×): `public/data.js:571`
- `contabilizei-abertura` (9×): `public/app.js:59`, `public/data.js:1000`
- `atendimento-zendesk` (8×): `public/data.js:24`
- `experts-service` (6×): `public/data.js:78`
- `emissor-whatsapp` (6×): `public/data.js:334`
- `experts-zendesk` (6×): `public/data.js:406`
- `experts-api-gateway` (5×): `public/data.js:361`
- `webhook-gitlab` (4×): `public/data.js:242`
- `emissor-whatsapp-reports` (4×): `public/data.js:343`
- `experts-alertas` (4×): `public/data.js:352`
- `experts-async-publisher` (4×): `public/data.js:370`
- `experts-contabil` (2×): `public/data.js:379`
- `experts-twilio` (2×): `public/data.js:397`
- Configuração, CI e documentação citadas: `k8s-configmap`, `kong-config`, `team-knowledge-base`, `vault-roleset`

### Repositórios que citam este

_O nome `atalhos` é comum demais para busca por token; procurar pelo host, rota ou tópico._

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
