---
name: sonar-duplicacao-codigo-novo
description: "Quality gate do SonarQube falhando por duplicação em código novo (limite 6%): como diagnosticar pelo MCP e por que mexer em arquivo antigo pode piorar"
metadata:
  type: reference
tags:
  - padroes
  - sonar
---

# Sonar: duplicação em código novo

O quality gate dos MRs (`sonar-merge-request`) exige `new_duplicated_lines_density` abaixo de 6%, além de cobertura nova ≥ 80% (branches ≥ 90%) e 0 issues novas. Um job novo copiado de um irmão (ex: um job ou service por público, como Experts SN/LP e BP LP) costuma estourar esse limite.

## Diagnóstico

1. No log do job, a linha `QUALITY GATE STATUS: FAILED - View details on ...pullRequest=<id>` traz o id do PR no Sonar.
2. `get_project_quality_gate_status(projectKey, pullRequest=<id>)` mostra qual condição falhou.
3. `search_duplicated_files(pullRequest=<id>)` lista os arquivos e as linhas duplicadas.

## Armadilhas

- **Mexer num arquivo antigo transforma as linhas dele em código novo.** Se o arquivo continuar parecido com o novo, a duplicação conta dos dois lados e pode até piorar (no !90 do `microsservico-agrupamento-guias`, mexer só no fluxo do service de BP LP fez a duplicação ir de 6,46% para 6,12%, ainda acima do limite).
- O Sonar ignora diferenças em literais (strings de log e constantes). Só identificadores diferentes quebram o bloco duplicado, então trocar textos não resolve.

## O que resolveu

Extrair para um service comum o que é idêntico entre os públicos e deixar em cada classe específica só o que muda (ex: o público e a busca de elegíveis no job, o remetente e o template no e-mail), com poucos parâmetros e sem flag escolhendo o caminho. No !90, a duplicação caiu para 0,0%.

## Código declarativo (ex: models do Drizzle)

Quando a duplicação vem de declarações que se repetem por natureza, como as colunas de tabelas parecidas no Drizzle (estado e histórico do opt-out no `contato-service`), não há lógica para extrair. Basta mexer num comentário dentro do trecho para ele virar código novo e estourar o limite (no !55 do `contato-service`, foi para 6,12%). Nesse caso, excluir esses arquivos da detecção de duplicação no `sonar-project.properties`, com um comentário explicando o motivo: `sonar.cpd.exclusions=src/model/**/*.ts`. Os models desse repo já ficavam fora da cobertura. No !55, o quality gate passou depois disso.
