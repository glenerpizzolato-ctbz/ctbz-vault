---
name: prcs-indice
description: "Índice dos playbooks de PRC (soluções de chamados recorrentes) por canal"
metadata:
  type: reference
tags:
  - prc-indice
---

# PRCs

Playbooks de chamados (PRC) já investigados: **uma nota por problema** (não por chamado), com sintoma, causa, como confirmar/resolver e a ACR para vincular. Os chamados PRC-xxxxx em que a solução foi aplicada ficam em `ocorrencias`.

## Estrutura

- `itens/<ACR> - <sintoma>.md` — uma nota por problema; o nome do arquivo é a chave da ACR seguida do sintoma (a melhor chave de busca). A classificação fica no front-matter.
- [[PRCs.base|Tabela filtrável (Obsidian Bases)]] — ordenada pelos problemas mais recorrentes.

## Como usar

- **Ao resolver um PRC:** procurar aqui um playbook do mesmo problema. Se existir, adicionar o chamado em `ocorrencias`, atualizar `qtd_ocorrencias`/`ultima_ocorrencia` (data de criação do chamado) e enriquecer a nota se houver algo novo. Se não existir, criar `itens/<ACR> - <sintoma>.md` com o mesmo front-matter e adicionar a linha abaixo.
- **Comunicar sobre PRCs:** mensagens sobre PRCs (andamento, repasses, pedidos ao time) vão para o [chat dedicado de PRCs](https://mail.google.com/mail/u/0/#chat/space/AAQAfFlovh4) (ver [[_comunicacao-indice|Comunicação]]).
- **Transferir um PRC para outro squad:** não usar a transição `Transferido` nem mudar o status: o PRC fica em `TODO` e só se troca o campo **Assigned Squad** (`customfield_18419`) para o squad de destino (ex: `Fiscal`).
- **Concluir uma ACR (tipo `Análise de Causa raiz`):** de `Backlog`, o único status de conclusão direto é `Archived`. Para ir a `Concluído`, seguir `Priorizar` (201) → `To-do` (661) → `Detalhar Hipótese` (481, status `Detalhamento`) → `Finalizar` (651). O `Finalizar` exige `Qual a origem do problema?` (`customfield_25658`), `Causa Raiz do Incidente/Defeito` (`customfield_21524`), `Item novo ou legado?` (`customfield_34238`), `Produto e Subproduto` (`customfield_35839`, cascata) e `Critérios para aceite` (`customfield_18415`, em ADF, não string), além de `A causa raiz é crítica?` e `Assigned Squad`. Ao concluir, uma automação troca o responsável para `SVC-Robo Ativacao e Fluxo Auto`.
- **ACR:** em `acr`, usar link `"[[PRD-xxxxx]]"` quando a ACR tiver nota em [[_prds-indice|PRDs]] (e adicionar o playbook em `prcs` da nota do PRD); senão, só a chave.

## Vocabulário

- **canal:** `wpp`, `email`, `chat` (lista; um problema pode envolver mais de um canal)
- **dominio:** mesmo vocabulário dos PRDs (ver [[_prds-indice|PRDs]])
- **sistemas:** sistemas envolvidos, em kebab-case (ex: `zendesk`, `meta`, `crm`, `contato-service`, `experts-service`, `atendimento-zendesk`)
- **acr / ocorrencias / qtd_ocorrencias / ultima_ocorrencia:** ACR(s) a vincular e chamados em que o problema apareceu

## WhatsApp

- [[PRD-134632 - Meta não entrega mensagem - healthy ecosystem engagement (131049)]] — Meta barra ativo WPP (erro 131049, limite de marketing/reclassificação de template); confirmar em `mensagem_ativa_status`, retentar só após 24h; vincular à ACR PRD-134632 · 2 ocorrências
- [[PRD-168944 - Cliente não quer receber pesquisa (CSAT e-ou NPS)]] — só CSAT → `blocklist` no experts-service; CSAT+NPS → opt-out do contato-service no front admin; vincular à ACR PRD-168944 · 3 ocorrências
- [[PRD-103649 - Cliente recebe notificações WPP com dados de outra empresa]] — telefone do cliente vinculado a outra empresa; checar usuários do telefone na Zendesk, mesclar duplicados; se Zendesk ok, chamado no CRM para validar base de envios; ACR PRD-103649 · 1 ocorrência
- [[PRD-151519 - Cliente com mais de um contato cadastrado com mesmo telefone na zendesk]] — ticket perdido por contato duplicado na Zendesk; buscar `*<8 dígitos>` no front admin e mesclar (só contatos sem org/e-mail)
- [[PRD-172999 - Cadastro de telefone internacional]] — cliente no exterior pede cadastro de telefone com DDI ≠ +55; cadastrar pelo CRUD de telefone internacional do front admin, vincular à ACR (Rotina) PRD-172999 e fechar com `Solved` · 3 ocorrências
- [[PRD-174011 - Cliente não recebe notificação do agrupamento de guias]] — grupo_guia nunca chegou a SUCESSO_AGRUPAMENTO (sem guia ou guias emitidas depois do dia 15/vencimento, `GUIAS_AGUARDANDO_GERACAO` não é retentado); conferir grupo_guia/controle_notificacao no ms_agrupamento_guias; ACR PRD-174011 · 1 ocorrência

## E-mail

- [[PRD-167733 - Cliente não consegue enviar email - cai no spam do atendimento.experts]] — e-mail do cliente para atendimento.experts@ cai no nosso spam (Google), sem bounce; whitelist na regra anti-spam; ACR PRD-167733 · 5 ocorrências
- [[PRD-168944 - Cliente não quer receber pesquisa (CSAT e-ou NPS)]] — só CSAT → `blocklist` no experts-service; CSAT+NPS → opt-out do contato-service no front admin; vincular à ACR PRD-168944 · 3 ocorrências
- [[PRD-168171 - Cliente não consegue enviar email - bloqueio de spam no provedor do cliente]] — provedor do cliente (Microsoft) barra como spam, NDR 5.7.520 AS(4810); orientar contornos; ACR PRD-168171
- [[PRD-174011 - Cliente não recebe notificação do agrupamento de guias]] — grupo_guia nunca chegou a SUCESSO_AGRUPAMENTO (sem guia ou guias emitidas depois do dia 15/vencimento, `GUIAS_AGUARDANDO_GERACAO` não é retentado); conferir grupo_guia/controle_notificacao no ms_agrupamento_guias; ACR PRD-174011 · 1 ocorrência

> [!info] Colunas do board (Engenharia Canais - PRCs, board 13246) → status
> `pronto para triagem` = `Backlog`; `Pronto para ajuste manual` = `To-do`; `ajuste manual em andamento` = `Em Andamento`; `ajuste manual Pausado` = `Paused`; `Com time de dev / acr / fornecedor` = `Aguardando Dev` + `Aguardando fornecedor`; `Com time de Negócio` = `AGUARDANDO NEGÓCIO`; `problema do cliente resolvido` = `Concluído`; `transferido ou arquivado` = `Transferido` + `Archived`. Os PRCs sem dono das colunas de entrada saem de `getJiraBoardIssueData` (boardId 13246) com a JQL `status in (Backlog, "To-do", "Aguardando fornecedor", "Aguardando Dev") AND assignee is EMPTY`; a aba PRCs do BahCode lista esses e os mapeia de hora em hora contra os playbooks daqui.

> [!warning] Armadilha do board (Engenharia Canais - PRCs)
> A transição `Started` (To-do → Em Andamento, coluna "ajuste manual em andamento") reatribui o card para quem a executou. Para deixar o card com outra pessoa, atribuir **depois** de mover.

## Chat

- [[PRD-176094 - Ticket de chat web cai na Ouvidoria sem o cliente pedir]] — `sys_grupo_ouvidoria` vem do `zen:ticket:tags` do widget (botão Reclamação/Elogio, localStorage), não da Ultimate; confirmar no `ChatStartedEvent.control_context` dos audits e no Mixpanel; ACR PRD-176094 · 1 ocorrência
