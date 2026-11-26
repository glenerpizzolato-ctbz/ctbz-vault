---
name: 2026-11-26-e2e-critico-canais-fale-conosco
description: "Correção do E2E crítico do Canais (finalizar atendimento via chat do Fale Conosco), fora da regressão desde 2024, levando o squad de 75% para 100% dos críticos ALTA rodando em stg"
metadata:
  type: project
tags:
  - performance
titulo: "E2E crítico do Canais de volta à regressão (75% → 100% dos críticos ALTA em stg)"
data: 2026-11-26
periodo: 2026QD3
categorias: [qualidade]
impacto: medio
fontes: ["[[e2e-criticos-canais]]", "[[rodar-testes-e2e-plataforma-crm]]", "[[metrica-e2e-critico]]"]
---

# E2E crítico do Canais de volta à regressão

## Contexto

A meta de Qualidade pede 85% dos testes críticos mapeados com E2E rodando em stg. O Canais estava em 75% (3 de 4 de criticidade ALTA) e o pedido não dizia qual teste faltava.

## O que fiz

- Extraí a lista do dashboard do Metabase (card 35859) e achei o `test_crm_platform_data_e2e:3`, "Deve finalizar um atendimento via chat do Fale Conosco", fora da pipeline desde 31/10/2024 (tag `@regression` removida quando passou a falhar).
- Validei pelo mapa do widget que o cenário continua válido e rodei em stg com VPN: a causa era a inativação dos subtemas de Impostos (conferida no banco de dev e de prod, só leitura) e o Zendesk Messaging em inglês no Chrome headless.
- Ajustei o comando, as fixtures e os seletores, devolvi a tag e validei duas execuções verdes em stg, uma com o filtro da pipeline. Branch `fix/PRD-179610` no `teste-e2e-plataforma-crm`.
- Documentei no vault como rodar, as armadilhas (403 intermitente, retries, idioma do Zendesk) e o mapa dos críticos do squad.

## Resultado

- Com o merge, o Canais passa de 75% para 100% dos críticos ALTA executando em stg (meta 85%).

## Evidências

- [[e2e-criticos-canais]], [[rodar-testes-e2e-plataforma-crm]], PRD-179610.
