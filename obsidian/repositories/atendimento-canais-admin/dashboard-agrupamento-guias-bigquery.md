---
name: atendimento-canais-admin-dashboard-agrupamento-guias-bigquery
description: "Dashboard Agrupamento de Guias: tabelas do BigQuery dw_ms_agrupamento_guias que o admin lê, armadilhas de item_grupo_guia e de controle_guias, e particularidades de rodar check/testes numa worktree"
metadata:
  type: reference
---

# Dashboard Agrupamento de Guias e BigQuery

O dashboard `/notificacoes/dashboards/agrupamento-guias` lê tudo de `contabilizei-dataflow.dw_ms_agrupamento_guias` (queries em `src/server/domains/controle-notificacao/controle-notificacao.source.ts`).

Tabelas replicadas no dataset (conferido em 2026-10-29): `controle_guias`, `controle_notificacao`, `diagnostico_aumento_imposto`, `grupo_guia`, `historico_processamento_grupo_guia` e `item_grupo_guia`.

## item_grupo_guia (grupo → guias)

- Colunas: `id`, `grupo_guia_id`, `controle_guia_id`, `created_at`, `updated_at`.
- **A réplica repete pares**: cerca de 1,23 mi de linhas para 1,22 mi de pares distintos `grupo × guia`. É preciso usar `DISTINCT` antes do join, senão a guia aparece duas vezes e o valor é somado duas vezes.
- **Há itens órfãos**: cerca de 50 mil apontam para um `controle_guia_id` que não existe em `controle_guias`. O join com `controle_guias` deve ser LEFT, e a guia órfã é listada só pelo id (ex: grupo 372962).
- Usada pela rota `GET /api/notificacoes/controle-notificacao/grupos/:grupoId/guias` (PRD-174490), que alimenta a seção "Guias do agrupamento" do modal do olhinho.

## controle_guias

- `periodo_apuracao` é FLOAT (`CAST(... AS INT64)`); `id` não se repete.
- `data_para_pagamento` está sempre às 23:59:59 UTC, então formatar em `America/Sao_Paulo` mantém o mesmo dia.
- Valor pago = `valor_principal + valor_multa + valor_juros + valor_acrescimos`. Tokens de `imposto`: SIMPLES, DARF_UNIFICADO, INSS_SIMPLES, TFE, ISS, CSLL, IRPJ_32, FGTS, COFINS etc. Tokens de `status`: REGISTRADO, CANCELADA, VENCIDA, PENDENTE, PARCELADA, AGUARDANDO_EMISSAO, PAGAMENTO_AGENDADO, REGISTRADO_PARCELADO.

## Worktree: armadilhas

- Uma worktree nova não tem `node_modules`: rodar `pnpm install --frozen-lockfile` (rápido, usa o store). Sem isso, `npx vitest` baixa um vitest global e falha ao carregar o config.
- Na worktree, `biome check --write <arquivos>` ignora os caminhos passados ("provided but ignored"). Rodar `./node_modules/.bin/biome check --write` sem caminhos e conferir no `git status` que só os seus arquivos mudaram.
- O `vitest run` com caminhos falha no threshold global de cobertura (90%) por rodar só uma parte da suíte; para ver os testes, usar `--coverage.enabled=false`, e para medir a cobertura dos arquivos alterados, usar `--coverage.reporter=json-summary`.
- O app é servido em produção sob `VITE_BASE_URL=/api/atendimento-canais` (Dockerfile).

## Sem coleção Bruno

O `atendimento-canais-admin` é front (as rotas `/api/...` servem só às próprias telas), e o usuário definiu que **front não precisa de coleção Bruno**: não criar `docs/bruno` aqui, mesmo ao criar ou alterar rota de API. Uma coleção criada por engano no PRD-174490 foi removida no MR !168.
