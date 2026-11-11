---
name: microsservico-agrupamento-guias-replicar-features-no-agrupamento-guias-service
description: "Regra: toda feature/correção de notificação mergeada no microsservico-agrupamento-guias que não exista no agrupamento-guias-service vira um work-item no GitLab do agrupamento-guias-service; como conferir a lacuna e controle do que já foi aberto"
metadata:
  type: project
tags:
  - microsservico-agrupamento-guias
  - agrupamento-guias-service
  - notificacao
  - migracao
atualizado_em: 2026-11-11
---

# Replicar features no agrupamento-guias-service

O [[_agrupamento-guias-service-indice|agrupamento-guias-service]] é o desacoplamento da parte de notificação deste repositório (cópia feita em 2026-10-15, ver [[arquitetura-e-migracao]]) e ainda não foi migrado: até a virada, as duas implementações coexistem e o Kotlin continua recebendo features.

> [!IMPORTANT]
> Toda feature ou correção mergeada no `microsservico-agrupamento-guias` que mexa na notificação (e-mail, WhatsApp, metadados, templates, regras de quem recebe, conteúdo do evento) e que ainda não exista no `agrupamento-guias-service` deve virar um **work-item** (issue) no GitLab do agrupamento-guias-service: https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/work_items

## Como fazer

1. Listar os MRs mergeados depois do último controle abaixo: `glab mr list --merged` (ou `git log origin/master --since=<data>`) no `~/repositories/microsservico-agrupamento-guias`. MR aberto ainda não entra (ex: !98 ISS, aberto em 2026-11-11): abrir o work-item quando for mergeado.
2. Para cada um, conferir no `origin/master` do agrupamento-guias-service se já existe (`git grep` em `src/`; o desenho lá é por segmento, ver [[arquitetura-e-migracao]]). Ignorar o que só faz sentido no Kotlin: lote, crons/schedulers, buscas de elegíveis no banco, `controle_notificacao` (lá é por evento, sem lote). A regra de negócio por trás de uma busca (ex: plano que não recebe) entra, porque precisa existir em algum lugar do fluxo novo.
3. Criar o work-item: `glab work-items create --type issue --title "..." --description-file <arquivo>` dentro do repo do service (o comando não aceita `--label`: depois, `glab issue update <iid> --label feature`). Descrição com **Origem** (link do MR e card do Jira), **O que o microsservico faz** e **O que falta aqui** (checklist apontando o arquivo/service do Node).
4. Registrar a linha no controle abaixo.

## Controle

Último levantamento: 2026-11-11 (MRs mergeados até o !101).

| MR do microsservico | Card | Situação no service |
| --- | --- | --- |
| !89 squad/autor no WhatsApp e filtro do callback | — | já replicado |
| !91 DADOS_INCOMPLETO com contato incompleto | — | já replicado (`INCOMPLETE_DATA`) |
| !90 Experts SN x LP, template de Experts LP, só planos Expert | PRD-174792 | work-item [#3](https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/work_items/3) |
| !92 WhatsApp BP LP sem o plano BASICO | — | work-item [#4](https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/work_items/4) |
| !95 opt-out nos e-mails de impostos | PRD-174790 | já replicado (MR !1 do service) |
| !97 + !99 + fix `nrPrestacao` do !100: parcelas no evento e `nomeGuia` com todas as guias e parcelas | PRD-167515, PRD-176358 | work-item [#5](https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/work_items/5) |
| !100 + !101 parcelas nos metadados do WhatsApp | PRD-176440, PRD-176511 | work-item [#6](https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/work_items/6) |
| !98 ISS no agrupamento | PRD-175884 | MR aberto: abrir work-item quando mergear |
