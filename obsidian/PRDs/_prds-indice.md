---
name: prds-indice
description: "Hub das demandas (PRDs) que criei na Contabilizei: visões por épico, período e domínio"
metadata:
  type: reference
tags:
  - prd-indice
---

# Demandas (PRDs)

Fonte da verdade das demandas que criei na Contabilizei (substitui a planilha "organization - ctbz", aba "detalhes PRDs", descontinuada em 2026-10).

## Visões

- [[_por-epico|Por épico]]
- [[_por-periodo|Por período (quadrimestre)]]
- [[_por-dominio|Por domínio]]
- [[PRDs.base|Tabela filtrável (Obsidian Bases)]]

## Estrutura

- `itens/PRD-xxxxx.md` — uma nota por demanda; a classificação fica no front-matter (`epico`, `periodo`, `mes`, `dominio`, `tipo`, `situacao`, `atuacao`, datas).
- `epicos/PRD-xxxxx.md` — uma nota por épico, com a lista das suas demandas.
- Nova demanda: criar `itens/<chave>.md` seguindo o mesmo front-matter e adicioná-la às visões.

## Épico na criação do card

Todo PRD novo vai para um épico, nesta ordem: o citado na demanda; senão um épico aberto do mesmo tema (os de `epicos/` e os pais dos PRDs recentes no Jira); senão, como **fallback**, o épico de **CTS do time no quadrimestre atual**, `[AAAA-QDn] CTS - Eng Canais` (2026-QD3: [[PRD-165450]]). O de CTS também é o certo quando a demanda é mesmo um CTS, uma demanda lateral que está rolando fora das iniciativas planejadas. Os de CTS de outros times (`[BAU] - CTS`, `Fiscal Impostos | CTS`, `CTS de Onboarding`) não servem. Sem o épico de CTS do quadrimestre criado, perguntar em vez de usar o de um quadrimestre passado. A regra completa está no `CLAUDE.md` global (seção PRDs).

## Vocabulário

- **situacao:** `backlog` (card criado, ainda não concluído), `pronto`, `arquivado`, `resolvido-outro-dev`, `esquecido`
- **tipo:** `melhoria`, `rotina`, `acr`, `defeito`, `demanda-tecnica`, `demanda-de-produto`, `refinamento`, `configuracao-operacional`, `configuracao-administrativa`, `retrabalho`, `debito-tecnico`
- **atuacao:** `BE`, `FE`, `IA`, `Ultimate`, `Twilio`, `Rotina`
- **dominio:** `atendimento` (Zendesk, tickets, encerramento automático, filas, canais de atendimento, e-mail inbound); `copilot` (Copilot/Concierge Experts, módulo de ações, envio automático de respostas, prompts); `csat` (Pesquisas CSAT, transbordo e contenção); `impostos` (Guias de imposto, agrupamento de guias, diagnóstico/explicação de impostos); `monitoria-ia` (Monitoria com IA, transcrições); `notas-fiscais` (Emissão de NF (plataforma, exterior, bot), experts-nfs); `notificacoes` (WhatsApp ativo, templates, Meta Flows, e-mails, opt-out); `plataforma` (Débitos técnicos, migrações, infra, SSO, CNPJ alfanumérico, admins internos); `ultimate` (Ultimate/URA/bots de WhatsApp, menus, autenticação no chat)
- **periodo:** `AAAAQDn` (quadrimestre); **mes:** `AAAAMM`

## Números

- 398 demandas, 47 épicos
- pronto: 345, backlog: 18, arquivado: 13, resolvido-outro-dev: 13, esquecido: 9

## Campos do Jira na criação

- **Defeito** (e outros tipos do PRD) exige `Critérios para aceite` (`customfield_18415`, texto) e `Resultado Esperado` (`customfield_18416`, texto); sem eles o `createJiraIssue` volta 400.
- **Tipo do card:** correção que deixa o sistema mais resiliente depois de um incidente causado por fator externo (ex: retentativa quando o banco cai, PRD-175906) é **`Melhoria do produto`** (id `19560`), não `Defeito` (id `23416`); o usuário corrigiu isso em 2026-11-09. A troca de tipo entre os dois funciona com `editJiraIssue` (`issuetype: {"id": "19560"}`) mantendo o status `Building`.
- Na sub-task `Qualidade e Testes`, o campo de envolvimento se chama **`Envolvimento:`** (com dois-pontos), `customfield_21691`; pelo MCP, `{"Envolvimento:": "Testes / E2E"}` resolve o cascata (pai `Testes` id 29212, filho `E2E` id 29218).
- **Arquivar** (transição `Archived`, id `111`, resolução `Won't Do`): o motivo opcional `customfield_18509` ("Qual é o motivo para arquivar esta issue?") só aceita documento Atlassian (ADF), não texto simples: `{"type":"doc","version":1,"content":[{"type":"paragraph","content":[{"type":"text","text":"..."}]}]}` no `fields` do `transitionJiraIssue`.
