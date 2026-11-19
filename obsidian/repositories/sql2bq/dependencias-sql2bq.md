---
name: dependencias-sql2bq
description: "Dependências do sql2bq: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - sql2bq
repositorio: sql2bq
---

# Dependências do sql2bq

O que o `sql2bq` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

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

Gerado em 2026-11-19 sobre `master` @ `fe04993` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `contabilizei-impostos` (7×): `configs/prod/impostos-codigos-tributarios.json:2`, `configs/prod/impostos-comprovantes-pagamento-federal.json:2`, `configs/prod/impostos-consulta-caixa-postal-ecac.json:2`
- `atendimento-zendesk` (5×): `configs/prod/contabilizei-crm-relacionamento.json:3`, `configs/prod/ctbz-crm-atendimento-zendesk-diario.json:3`, `configs/prod/ctbz-crm-atendimento-zendesk-horario.json:3`
- `contabilizei-pagamentos` (5×): `configs/prod/contabilizei-ms-gateway-adyen-diario.json:2`, `configs/prod/contabilizei-ms-gestao-pagamentos-diario.json:2`, `configs/prod/contabilizei-pagamentos-cupom-diario.json:2`
- `fintech-payments` (3×): `cronjobs/params-prd.yaml:87`
- `saude-empresa-pendencias` (2×): `configs/prod/saude-empresa-pendencias.json:5`, `cronjobs/params-prd.yaml:199`
- `ticketing-service` (1×): `cronjobs/params-prd.yaml:215`

### Repositórios que citam este

_O nome `sql2bq` é comum demais para busca por token; procurar pelo host, rota ou tópico._

### Libs internas

_Nenhuma._

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

_Nenhum recurso do catálogo citado._

### Bancos e dados

- Tabelas/datasets do BigQuery citados: `contabilizei-dataflow.iam.gserviceaccount`

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
