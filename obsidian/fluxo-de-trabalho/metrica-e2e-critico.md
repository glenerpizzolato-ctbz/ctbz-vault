---
name: metrica-e2e-critico
description: Onde fica e como ler a métrica de E2E crítico (meta de 85% dos testes críticos com E2E rodando em stg) no dashboard GE Qualidade – Automação do Metabase, e como tirar a lista de testes de um squad pela API
metadata:
  type: reference
tags:
  - e2e
  - qualidade
  - metabase
atualizado_em: 2026-11-26
---

# Métrica de E2E crítico (GE Qualidade – Automação)

Dashboard: [GE Qualidade – Automação (visão geral)](https://metabase.ctbz.com.br/dashboard/2747-ge-qualidade-automacao-visao-geral?cen%25C3%25A1rio_%28busca%29=&criticality=&deleted=false&desenvolvido=&dev_env=&executa_stg=&feature=&grupo=&id_%28busca%29=&per%25C3%25ADodo=past12months~&plataforma=&squad=canais&test_key_%28busca%29=&tipo_teste=) (Metabase, dashboard 2747, coleção Gestão de Engenharia / Excelência, mantido pelo time de Qualidade). O link acima já vem com `squad=canais` e `deleted=false`; trocar o `squad` para outro time.

## O que a meta mede

A meta do squad é **85% dos testes críticos mapeados com E2E coberto**. No dashboard isso é o gauge **"Indicador – Executa STG (% criticidade ALTA)"**: dos testes ativos (`deleted=false`) de criticidade `ALTO`, quantos têm `stage_status = true` (rodam em stg). Ao lado fica o **"Executa STG (% geral)"**, com todas as criticidades.

- Os testes vêm do cadastro de testes do QAS (tabelas `test_crm_platform_data_e2e`, `test_client_platform_data_e2e`, `test_client_platform_data_ui` etc.), com `test_key` (`<tabela>:<id>`), `scenario` (o mesmo nome do `it(...)` no Cypress), `squad_name`, `criticality_name`, `automation_status` (desenvolvido) e `stage_status` (executa em stg).
- `automation_status = true` e `stage_status = false` costuma ser teste escrito que **não entra na execução da pipeline**: falta a tag `@regression` (os jobs filtram por `@regression+@<feature>`), ou o teste foi tirado por estar falhando.
- Para sair da lista de críticos (teste obsoleto), o caminho é pedir ao QAS com a justificativa; a lista não é editada pelo squad.

## Tirar a lista pela API (sem rolar o dashboard)

Com o Metabase aberto e logado no Chrome, no console da página:

```js
const r = await fetch('/api/card/35859/query', {method:'POST', headers:{'Content-Type':'application/json'}, body:'{}'}).then(r => r.json())
const c = r.data.cols.map(x => x.name)
const rows = r.data.rows.map(v => Object.fromEntries(v.map((x, i) => [c[i], x])))
rows.filter(x => x.squad_name === 'CANAIS' && !x.deleted).map(x => [x.test_key, x.criticality_name, x.automation_status, x.stage_status, x.scenario])
```

O card 35859 é o "Base – Overview unificado (full – latest)" (último retrato de cada teste, ~900 linhas). Passar os filtros do dashboard pela rota `/api/dashboard/2747/dashcard/...` falhou; filtrar no JS é mais simples.

## Por squad

- Canais: [[e2e-criticos-canais]] (repositório [[_teste-e2e-plataforma-crm-indice|teste-e2e-plataforma-crm]]).
