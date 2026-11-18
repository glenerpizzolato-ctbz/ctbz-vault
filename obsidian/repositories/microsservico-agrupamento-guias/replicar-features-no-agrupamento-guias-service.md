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
atualizado_em: 2026-11-18
---

# Replicar features no agrupamento-guias-service

O [[_agrupamento-guias-service-indice|agrupamento-guias-service]] é o desacoplamento da parte de notificação deste repositório (cópia feita em 2026-10-15, ver [[arquitetura-e-migracao]]) e ainda não foi migrado: até a virada, as duas implementações coexistem e o Kotlin continua recebendo features.

> [!IMPORTANT]
> Toda feature ou correção mergeada no `microsservico-agrupamento-guias` que mexa na notificação (e-mail, WhatsApp, metadados, templates, regras de quem recebe, conteúdo do evento) e que ainda não exista no `agrupamento-guias-service` deve virar um **work-item** (issue) no GitLab do agrupamento-guias-service: https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/work_items

## Como fazer

1. Listar os MRs mergeados depois do último controle abaixo: `glab mr list --merged` (ou `git log origin/master --since=<data>`) no `~/repositories/microsservico-agrupamento-guias`. MR aberto ainda não entra: abrir o work-item quando for mergeado.
2. Para cada um, conferir no `origin/master` do agrupamento-guias-service se já existe (`git grep` em `src/`; o desenho lá é por segmento, ver [[arquitetura-e-migracao]]). Ignorar o que só faz sentido no Kotlin: lote, crons/schedulers, buscas de elegíveis no banco, `controle_notificacao` (lá é por evento, sem lote). A regra de negócio por trás de uma busca (ex: plano que não recebe) entra, porque precisa existir em algum lugar do fluxo novo.
3. Criar o work-item: `glab work-items create --type issue --title "..." --description-file <arquivo>` dentro do repo do service (o comando não aceita `--label`: depois, `glab issue update <iid> --label feature`). Descrição com **Origem** (link do MR e card do Jira), **O que o microsservico faz** e **O que falta aqui** (checklist apontando o arquivo/service do Node).
4. Registrar a linha no controle abaixo.

## Controle

Último levantamento: 2026-11-18 (MRs mergeados até o !104; nenhum MR aberto no microsservico). Nada mergeado antes da cópia ficou de fora: o !91 entrou às 12:52 UTC de 15/10 e o scaffold do service é das 16:51 UTC; os commits de 14/10 da branch do !90 só entraram com ele (30/10).

| MR do microsservico | Card | Situação no service |
| --- | --- | --- |
| !89 squad/autor no WhatsApp e filtro do callback | — | já replicado |
| !91 DADOS_INCOMPLETO com contato incompleto | — | já replicado (`INCOMPLETE_DATA`) |
| !90 Experts SN x LP, template de Experts LP, só planos Expert | PRD-174792 | work-item [#3](https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/work_items/3), MR [!3](https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/merge_requests/3) (`feat/exp-lp-template-planos-expert`, 2026-11-18): template `exp-empacotamento-lp2` e filtro dos planos Expert no `NotificaAgrupamentoUsecase` (Experts sem plano/fora do Expert é ignorado, sem gravar) |
| !92 WhatsApp BP LP sem o plano BASICO | — | work-item [#4](https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/work_items/4), MR [!4](https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/merge_requests/4) (`fix/bp-lp-wpp-sem-basico`, mergeado em 2026-11-18): o `BpLpWppService` devolve `null` para o `BASICO` (`PLANOS_SEM_WHATSAPP_BP`), sem enviar nem gravar; regra no service para não conflitar com o filtro do !3 no usecase |
| !95 opt-out nos e-mails de impostos | PRD-174790 | já replicado (MR !1 do service) |
| !97 + !99 + fix `nrPrestacao` do !100: parcelas no evento e `nomeGuia` com todas as guias e parcelas | PRD-167515, PRD-176358 | work-item [#5](https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/work_items/5), mergeado no MR [!5](https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/merge_requests/5) (2026-11-18): `parcelas` no evento (guias/parcelas opcionais, ao menos um documento), `nomeGuia` no `EnvioEmailService` e `TIPO_PARCELAMENTO_DESCRICAO`; metadados do WhatsApp só não quebram sem guia (chaves de parcela ficam no #6). Falta alinhar o contrato com quem publica o evento |
| !100 + !101 parcelas nos metadados do WhatsApp | PRD-176440, PRD-176511 | work-item [#6](https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/work_items/6), implementado na branch `feat/parcelas-metadados-whatsapp` (MR [!6](https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/merge_requests/6) draft, encadeado sobre o !5, 2026-11-18): chaves de parcela no `buildMetadadosGuia`, menor vencimento entre guias e parcelas, soma com HALF_UP. Deploy só depois do atendimento-zendesk com PRD-176454 em prd |
| !98 ISS no agrupamento (mergeado 2026-11-13) | PRD-175884 | não se aplica: decide quais guias entram no PDF (fica no Kotlin); as descrições de imposto do `nomeGuia` já batem (`imposto.constants.ts`) |
| !102 `validadeEmMinutos = 4320` (3 dias) no WhatsApp de Experts e BP LP, para o ativo disparado no fim de semana não expirar antes da segunda | PRD-176856 | work-item [#10](https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/work_items/10) (2026-11-18); MR [!9](https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/merge_requests/9) em draft (branch `feat/whatsapp-validade-3-dias`, em chaining do !8 do Node 26); a branch antiga `fix/whatsapp-validade-fim-de-semana` (`d9e596a`) ficou obsoleta |
| !104 `agrupamento.parcelas.enabled: true` em prd (2026-11-13) | — | não se aplica como código, mas já pode haver agrupamento só de parcelas, que o master do service rejeita (`guias.min(1)`): aumenta a urgência do #5/#6 |
| commit `40ccb0c3` (2026-11-12) troca dos templates de e-mail de prd pelas versões novas: Experts SN `exp-email-agrupamento-guias-default-v5`, diag. faturamento `...-diag-fatur-v2`, Experts LP `exp-empacotamento-lp2`, BP LP `bpm-empacotamento-lp3` | — | só o Experts LP replicado (no #3); os outros três no work-item [#11](https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/work_items/11) (2026-11-18). MR [!10](https://gitlab.com/ctbz/experts/atendimento-canais/agrupamento-guias-service/-/merge_requests/10) aberto em draft em 2026-11-18 (branch `feat/templates-email-agrupamento`, em corrente sobre !9 do #10 e !8 do Node 26); variáveis conferidas no `email_service` de prd e dev: idênticas às versões anteriores, services sem mudança. UUIDs prd/dev: `default-v5` `25d1382f-2afc-42de-8b55-088ee67841a9`/`4947c568-531d-4a14-a410-e6294b57abee`, `diag-fatur-v2` `9ab02f34-ee50-4d36-80c6-43c565c1e44d`/`e1ddf12d-6afa-4cc7-91d0-dfbecd04de55`, `bpm-empacotamento-lp3` `fb55a332-701c-44cc-91ca-d83127bc98f4`/`0efa5f10-e0e2-4448-9483-a294be549877`. O BP LP de prd do service está duas versões atrás (`8cd92995`, `-bp-lp-v2`). Os templates novos têm `{{nomeGuia}}` sozinho num `<p>`, o que o `<br>` do #5 exige: mergear junto ou antes do #5 |

## Divergências conhecidas (não vêm de MR recente)

- Contato sem e-mail no WhatsApp: o Kotlin exige e-mail também no WhatsApp (`ContatoDTO.fromJson` → `fromJsonEmail`) e vira DADOS_INCOMPLETO; o service exige só nome e telefone (o do service parece o certo).
- WhatsApp de Experts LP: no Kotlin passa pelo `WhatsAppRequestServiceImpl`, que consulta o diagnóstico e pode trocar o template; o `ExpLpWppService` ignora diagnóstico.
- Regime nulo vira Experts SN no Kotlin; o service exige `regimeTributario` (400). Junto de: excluir avulsas, mandar só diagnóstico da competência atual e só agrupamentos `SUCESSO_AGRUPAMENTO`, isso é contrato com quem publica o evento.
- E-mail sem CNPJ: o Kotlin falha (`ERRO_ENVIO_EMAIL`); o service enviaria sem opt-out, mas o schema já exige `cnpj`.
