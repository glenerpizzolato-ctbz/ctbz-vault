---
name: dependencias-contabilizei-abertura
description: "Dependências do contabilizei-abertura: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - contabilizei-abertura
repositorio: contabilizei-abertura
---

# Dependências do contabilizei-abertura

O que o `contabilizei-abertura` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `develop` @ `eb66180048` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-guias` (5×): `contabilizei-abertura-core/src/main/resources/filtered/parametro.desenv.properties:257`, `contabilizei-abertura-core/src/main/resources/filtered/parametro.homolog.properties:262`, `contabilizei-abertura-core/src/main/resources/filtered/parametro.prod.properties:270`
- `contabilizei-impostos` (3×): `contabilizei-abertura-core/src/main/resources/filtered/parametro.desenv.properties:252`, `contabilizei-abertura-core/src/main/resources/filtered/parametro.homolog.properties:257`, `contabilizei-abertura-core/src/main/resources/filtered/parametro.teste.properties:263`
- `plataforma-crm-web` (1×): `contabilizei-abertura-core/src/main/java/br/com/contabilizei/abertura/core/service/ProcessoAberturaService.java:2365`

### Repositórios que citam este

- `contabilizei-abertura-BB` (269×): `Makefile:5`, `bitbucket-pipelines.yml:84`, `contabilizei-abertura-bff/pom.xml:8`
- `atendimento-zendesk` (73×): `.config.json:190`, `environments/_deprecated/config-dev.json:261`, `environments/_deprecated/config-local.json:261`
- `contabilizei-back-core` (28×): `src/main/resources/filtered/parametro.desenv.properties:811`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:610`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:639`
- `plataforma-central-rotinas` (26×): `src/main/resources/filtered/parametro.desenv.properties:842`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:616`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:640`
- `plataforma-web` (26×): `src/main/resources/filtered/parametro.desenv.properties:844`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:621`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:644`
- `firestore-to-bigquery` (25×): `configs/robots-ccm.json:2`, `configs/robots-chat-blip-atvalgomais.json:2`, `configs/robots-chat-blip-atvbalcaounico.json:2`
- `ctbz-acessos` (20×): `.config/projetos-e-roles.json:14`, `reports/lista_devsecops_roles_owner_all_projects.csv:19`
- `plataforma-monolito` (19×): `src/main/resources/filtered/parametro.desenv.properties:811`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:603`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:632`
- `plataforma-crm-web` (18×): `src/test/java/br/com/contabilizei/crm/infra/http/client/autoatendimento/certificado/CertificadoClientTest.kt:65`, `src/main/resources/filtered/parametro.desenv.properties:181`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:139`
- `plataforma-back-worker` (15×): `src/main/resources/filtered/parametro.desenv.properties:800`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:595`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:620`
- `plataforma-fopag-worker` (15×): `src/main/resources/filtered/parametro.desenv.properties:326`, `src/main/resources/filtered/parametro.desenvolvimento-1.properties:212`, `src/main/resources/filtered/parametro.desenvolvimento-2.properties:232`
- `experts-bpmn` (6×): `PRD-88296/processos.bpmn:12`
- `contabilizei-pagamentos` (5×): `contabilizei-pagamentos-core/src/main/resources/parametro.desenv.properties:3`, `contabilizei-pagamentos-core/src/main/resources/parametro.desenv3.properties:3`, `contabilizei-pagamentos-core/src/main/resources/parametro.homolog-reg.properties:3`
- `plataforma-faturamento-worker` (4×): `src/main/resources/filtered/parametro.desenv.properties:664`, `src/main/resources/filtered/parametro.prod.properties:709`
- `aida-back` (3×): `contabilizeiai/clients/abertura_client.py:7`, `contabilizeiai/services/certificado/documentos_certificado_service.py:295`, `contabilizeiai/services/certificado/entrevista_certisign_service.py:227`
- `contabilizei-front-admin` (2×): `src/sistema-admin/assets/js/endpoint_hom.js:24`, `src/sistema-admin/assets/js/endpoint_stg.js:26`
- `oi-contabilizei-functions` (1×): `functions/tests/settings/mockFirebaseConfigs.json:176`
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `atalhos`, `experts-bruno`, `experts-drawio`, `k8s-configmap`, `kong-config`, `pipeline`, `vault-roleset`

### Libs internas

- `br.com.contabilizei.jira:contabilizei-jira` (`contabilizei-abertura-core/pom.xml`)
- `br.com.contabilizei:contabilizei-abertura` (`contabilizei-abertura-bff/pom.xml`)
- `br.com.contabilizei:contabilizei-abertura-bff` (`contabilizei-abertura-report/pom.xml`)
- `br.com.contabilizei:contabilizei-abertura-core` (`contabilizei-abertura-bff/pom.xml`)
- `br.com.contabilizei:contabilizei-abertura-test` (`contabilizei-abertura-bff/pom.xml`)
- `br.com.contabilizei:contabilizei-abertura-web` (`contabilizei-abertura-report/pom.xml`)
- `br.com.contabilizei:contabilizei-abertura-worker` (`contabilizei-abertura-report/pom.xml`)
- `br.com.contabilizei:contabilizei-backup` (`contabilizei-abertura-core/pom.xml`)
- `br.com.contabilizei:contabilizei-configcat` (`contabilizei-abertura-core/pom.xml`)
- `br.com.contabilizei:contabilizei-data-streaming` (`contabilizei-abertura-core/pom.xml`)
- `br.com.contabilizei:contabilizei-datastore` (`contabilizei-abertura-test/pom.xml`)
- `br.com.contabilizei:contabilizei-datastore-console` (`contabilizei-abertura-web/pom.xml`)
- `br.com.contabilizei:contabilizei-issue-client` (`contabilizei-abertura-core/pom.xml`)
- `br.com.contabilizei:contabilizei-metadata` (`contabilizei-abertura-worker/pom.xml`)
- `br.com.contabilizei:contabilizei-queue` (`contabilizei-abertura-core/pom.xml`)
- `br.com.contabilizei:contabilizei-sso-client` (`contabilizei-abertura-core/pom.xml`)
- `br.com.contabilizei:contabilizei-storage` (`contabilizei-abertura-core/pom.xml`)
- `br.com.contabilizei:contabilizei-utils` (`pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Tópico**: `ingestor-streaming`, `topic-name`
- **Fila Cloud Tasks**: `carregarDados-queue`, `certificado-digital`, `zendesk-queue`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Google Chat: `chat.googleapis.com` em `.old-tests/contabilizei-abertura-core/test/resources/application.properties:76`
- Jira / Confluence: `2fcontabilizeicontabilidade.atlassian.net` em `.old-tests/contabilizei-abertura-core/test/resources/static/json/jira/jira_changelog_history.json:21`, `contabilizeicontabilidade.atlassian.net` em `.old-tests/contabilizei-abertura-core/test/java/br/com/contabilizei/abertura/integracao/escritoriovirtual/service/PayloadJiraMock.java:9`
- Zendesk: `contabilizei.zendesk.com` em `contabilizei-abertura-core/src/main/resources/filtered/parametro.prod.properties:132`, `contabilizei1595352016.zendesk.com` em `.old-tests/contabilizei-abertura-core/test/resources/application.properties:119`, `contabilizei1637606740.zendesk.com` em `contabilizei-abertura-core/src/main/resources/filtered/parametro.desenv.properties:127`

<!-- deps:auto:fim -->
