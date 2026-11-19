---
name: dependencias-contabilizei-movimentacao-back
description: "Dependências do contabilizei-movimentacao-back: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - contabilizei-movimentacao-back
repositorio: contabilizei-movimentacao-back
---

# Dependências do contabilizei-movimentacao-back

O que o `contabilizei-movimentacao-back` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `develop` @ `cc73a325` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-pagamentos` (7×): `src/main/kotlin/br/com/contabilizei/movimentacao/domain/sustentacao/SustentacaoService.kt:74`, `src/main/kotlin/br/com/contabilizei/movimentacao/infra/resteasy/RestEasyClientConfig.kt:74`, `src/main/resources/application.properties:84`
- `experts-contabil` (4×): `src/main/resources/application.properties:97`

### Repositórios que citam este

_Nenhum._
- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): `experts-drawio`, `k8s-configmap`, `kong-config`, `pipeline`

### Libs internas

- `br.com.contabilizei:contabil-eventos` (`pom.xml`)
- `br.com.contabilizei:contabilizei-movimentacao-back` (`pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Fila Cloud Tasks**: `correcao-movimentacao`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

- Google Chat: `chat.googleapis.com` em `src/test/kotlin/br/com/contabilizei/movimentacao/domain/extrato/jobs/VerificaInconsistenciasIntegracaoBancariaJobTest.kt:36`
- Google Gemini / Vertex AI: `aiplatform.googleapis.com` em `src/main/resources/application.properties:36`
- Jira / Confluence: `contabilizeicontabilidade.atlassian.net` em `src/test/kotlin/br/com/contabilizei/movimentacao/domain/lancamentousuario/correcoes/processadores/CorrecaoLancamentoImpostoTest.kt:36`

<!-- deps:auto:fim -->
