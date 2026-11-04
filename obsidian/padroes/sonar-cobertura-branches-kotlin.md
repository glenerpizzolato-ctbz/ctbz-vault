---
name: sonar-cobertura-branches-kotlin
description: Gate de 90% de cobertura de branches no código novo em Kotlin - safe calls, let/takeIf e lambdas inline geram ramos que os testes não alcançam; como achar e eliminar
metadata:
  type: reference
---

# Sonar: cobertura de branches em Kotlin

Nos repositórios Kotlin da CTBZ (ex: `microsservico-agrupamento-guias`), o quality gate do MR exige **90% de cobertura de branches no código novo** (`new_branch_coverage`), além de 80% de cobertura geral e de linhas. Dá para cair nele com todos os casos lógicos testados, porque o Kotlin gera ramos extras no bytecode.

## Como diagnosticar

- Pelo MCP do Sonar: `get_project_quality_gate_status` com `pullRequest` (o id aparece no log do job `sonar-merge-request`, na URL `...&pullRequest=<id>`) mostra qual condição falhou.
- Localmente: `./mvnw test jacoco:report` e cruzar `target/site/jacoco/jacoco.xml` (atributos `mb`/`cb` de cada `line`) com as linhas do `git diff -U0 origin/master -- src/main`. Somar `cb/(cb+mb)` dessas linhas aproxima o número do Sonar.

## O que gera ramo não coberto

- Cadeia de safe calls com lambdas inline (`x?.filter { }?.uppercase()?.takeIf { }`): cada `?.` e cada lambda inline vira ramo, e alguns são inalcançáveis.
- `?.let { }` sobre um valor que já foi validado antes (o ramo nulo nunca acontece).
- `isNullOrEmpty`/`isNullOrBlank` depois de `?.`: ramo duplicado do nulo.

## Como eliminar sem mudar comportamento

- Trocar `x?.op1()?.op2()` + `takeIf` por `x.orEmpty().op1().op2()` e um `if (isEmpty()) throw`.
- Quando o nulo já foi barrado antes, usar `!!` (o JaCoCo ≥ 0.8.x filtra o ramo do `!!`) com um comentário explicando, em vez de `?.let`.
- Exemplo real: MR !95 do `microsservico-agrupamento-guias` (PRD-174790), de 81,3% para 100% de branches no código novo só com essas trocas.
