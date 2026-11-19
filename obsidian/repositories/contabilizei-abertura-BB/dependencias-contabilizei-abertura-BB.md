---
name: dependencias-contabilizei-abertura-BB
description: "Dependências do contabilizei-abertura-BB: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - contabilizei-abertura-BB
repositorio: contabilizei-abertura-BB
---

# Dependências do contabilizei-abertura-BB

O que o `contabilizei-abertura-BB` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `feature/PRD-147979` @ `ab82a5813` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-abertura` (269×): `Makefile:5`, `bitbucket-pipelines.yml:84`, `contabilizei-abertura-bff/pom.xml:8`
- `contabilizei-guias` (5×): `contabilizei-abertura-core/src/main/resources/filtered/parametro.desenv.properties:255`, `contabilizei-abertura-core/src/main/resources/filtered/parametro.homolog.properties:261`, `contabilizei-abertura-core/src/main/resources/filtered/parametro.prod.properties:269`
- `contabilizei-impostos` (3×): `contabilizei-abertura-core/src/main/resources/filtered/parametro.desenv.properties:250`, `contabilizei-abertura-core/src/main/resources/filtered/parametro.homolog.properties:256`, `contabilizei-abertura-core/src/main/resources/filtered/parametro.teste.properties:262`
- `plataforma-crm-web` (1×): `contabilizei-abertura-core/src/main/java/br/com/contabilizei/abertura/core/service/ProcessoAberturaService.java:2346`

### Repositórios que citam este

_Nenhum._

### Libs internas

- `br.com.contabilizei.jira:contabilizei-jira` (`contabilizei-abertura-core/pom.xml`)
- `br.com.contabilizei:contabilizei-abertura` (`contabilizei-abertura-bff/pom.xml`)
- `br.com.contabilizei:contabilizei-abertura-core` (`contabilizei-abertura-bff/pom.xml`)
- `br.com.contabilizei:contabilizei-abertura-test` (`contabilizei-abertura-bff/pom.xml`)
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
