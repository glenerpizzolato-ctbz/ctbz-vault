---
name: envio-empresas-agrupamento-guias
description: "Quais empresas o plataforma-faturamento-worker envia ao microsservico-agrupamento-guias (tópico agrupar-guias-empresa) por plano e regime, e a mudança de 2026-10-22 que tirou a restrição a EXPERT_ESSENCIAL"
metadata:
  type: reference
tags:
  - plataforma-faturamento-worker
  - microsservico-agrupamento-guias
atualizado_em: 2026-11-27
---

# Envio das empresas ao agrupamento de guias

- **Repositório vigente**: GitLab `ctbz/fiscal-impostos/geral/plataforma-faturamento-worker` (id 81728993). O clone em `~/repositories/plataforma-faturamento-worker` aponta para o Bitbucket antigo (parado em 2026-04-14): ler o código pelo `glab api` ou reclonar.
- `AgrupamentoGuiasFacade.enviaMsAgrupamentoGuia(idEmpresa, periodo)` publica o `EmpacotamentoGuiasDTO` no tópico `agrupar-guias-empresa` (projeto `contabilizei-impostos`); o microsservico monta o `grupo_guia` na madrugada do dia 15.
- **Até 2026-10-22**: só ia empresa com plano `EXPERT_ESSENCIAL` (`isClienteExpert`). Empresa que estava em plano BP (ex: AVANCADO) no dia 15 não ganhava `grupo_guia` nem `historico_processamento_grupo_guia` naquela competência, e portanto nenhuma notificação (caso do PRC-153307, 202603–202605).
- **Desde 2026-10-22** (commit `2d62f7b2`, "segrega agendamento de agrupamento de guias por regime e plano"): quatro lotes, `buscaEmpresasExpertAgrupamentoEmLote` (Experts Simples), `buscaEmpresasExpertLPAgrupamentoEmLote`, `buscaEmpresasLucroPresumidoBPAgrupamentoEmLote` e `buscaEmpresasSimplesBPAgrupamentoEmLote`; `isClienteExpert` passou a aceitar `EXPERT_PRO`. BP Simples ganha grupo, mas não tem notificação no microsservico.
- Diagnóstico por CNPJ: skill `investigar-notificacoes-guias-empresa` (causa `FORA_DO_AGRUPAMENTO_PLANO` / `SEM_GATILHO`).

Relacionado: [[PRD-174011 - Cliente não recebe notificação do agrupamento de guias]], [[notificacao-agrupamento-experts-bp-lp]].
