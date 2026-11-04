---
name: next-tasks-indice
description: "Índice das próximas tarefas (ainda não viraram PRD) por tema"
metadata:
  type: reference
tags:
  - next-task-indice
---

# Próximas tarefas

Tarefas e ideias futuras que ainda não viraram card no Jira (substitui a aba "tarefas" da planilha "organization - ctbz", descontinuada em 2026-10). Uma nota por tarefa (`task-<slug>.md`); só ficam aqui as tarefas em aberto.

## Como usar

- **Anotar uma próxima tarefa** ("anote uma próxima tarefa sobre X"): criar `task-<slug>.md` com o mesmo front-matter das demais (`origem: conversa`, `anotado_em: AAAA-MM-DD`) e adicionar a linha na seção do tema abaixo (criar a seção se o tema for novo).
- **Quando for resolvida** (virou PRD ou foi descartada): apagar a nota `task-<slug>.md` e a linha dela neste índice. Se a seção `## Notas` tiver contexto útil, levá-lo antes para a nota do PRD criado. Daí em diante a demanda é acompanhada em [[_prds-indice|PRDs]]; o histórico da tarefa fica no git.

## Vocabulário

- **tipo:** `tarefa` (algo definido para fazer), `ideia` (ainda uma pergunta/possibilidade)
- **tema:** agrupador livre em kebab-case (ex: `agrupamento-guias`, `opt-out`, `csat-transbordo`, `atendimento-canais-admin`, `novos-repositorios`)
- **dominio:** mesmo vocabulário dos PRDs (ver [[_prds-indice|PRDs]])

## Agrupamento de guias

- [[task-criar-emails-agrupamento-guias]] — Criar e-mails do agrupamento de guias

## Opt-out

- [[task-optout-validar-empresa-ao-salvar]] — Opt-out: não salvar opt-out de contato sem empresa preenchida
- [[task-optout-vincular-contato-a-empresa]] — Opt-out: adicionar contato existente a uma empresa

## CSAT Transbordo

- [[task-csat-transbordo-observabilidade]] — CSAT Transbordo: visibilidade além do dashboard (ideia)
- [[task-csat-transbordo-dashboard]] — CSAT Transbordo: tela de dashboard

## Admin do atendimento-canais

- [[task-front-gerenciar-cache-canais]] — Tela para gerenciar cache de canais

## Novos repositórios

- [[task-repo-ultimate-as-a-code]] — Criar repositório ultimate-as-a-code
- [[task-repo-agrupamento-guias-service]] — Criar repositório agrupamento-guias-service (notificações)

## Terminal

- [[task-alias-fechar-processo-vpn]] — Alias para fechar processo aberto da VPN

## Mapeamento

- [[task-mapeamento-fronts-e-skill]] — Mapear os fronts e o que fazem + skill para atualizar
- [[task-mapeamento-zendesk]] — Mapear Zendesk (zd) (ideia)

## IA do time

- [[task-vault-compartilhado-time]] — Criar vault compartilhado do time / marketplace de skills (ideia)
