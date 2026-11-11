---
name: prc-chat-ticket-cai-na-ouvidoria
description: PRC/ACR — ticket do chat web (app) é encaminhado para Ouvidoria [Chat] [BP] sem o cliente ter pedido; a tag sys_grupo_ouvidoria não vem da Ultimate, vem das conversationTags do widget (botão Reclamação/Elogio, guardadas no localStorage)
metadata:
  type: reference
tags:
  - prc
canal:
  - chat
dominio:
  - atendimento
  - ultimate
sistemas:
  - zendesk
  - ultimate
  - contabilizei-crm-widget-window
acr: "[[PRD-176094]]"
ocorrencias:
  - PRC-154516
qtd_ocorrencias: 1
ultima_ocorrencia: 2026-11-04
---

# Ticket de chat web cai na Ouvidoria sem o cliente pedir

## Sintoma

Um ticket do chat web (`via: native_messaging`, `sys_canal_chat`, bot de chat da Ultimate `66bf4a1be43522b403cd876b`) vai para o grupo `Ouvidoria [Chat] [BP]` (`14918795937052`) com as tags `sys_grupo_ouvidoria` e `sys_tema_ouvidoria`. No conversation log e no dialogue builder da Ultimate não aparece nenhum nó que defina essas tags.

## Causa

- As tags já estão **no audit de criação** do ticket. Elas não vieram de uma ação posterior.
- No audit seguinte, o `ChatStartedEvent` traz em `value.control_context` o metadata do handoff: `zen:ticket:tags = "sys_grupo_ouvidoria,sys_tema_ouvidoria,cnpj:<cnpj>"`. São as **conversationTags do Web Widget**, que o Zendesk aplica sozinho. A Ultimate só escala; o grupo de entrada é o `Default Ultimate Bot - [Chat][WhatsApp] [BP]` (`15262373080476`).
- Na sequência, o gatilho `Direcionamento para grupo Ouvidoria [Chat] [BP]` (id `14919379813404`) troca o grupo para Ouvidoria.
- Quem monta essa string é o `contabilizei-crm-widget-window`, no botão "Reclamação/Elogio" (`OmbudsmanFlowOptions`). Ver [[widget-tags-roteamento-ouvidoria]]. O botão só aparece para quem está no fluxo `BASICO_PADRAO` e é elegível (`atendimento/faleconosco/elegivel-auditoria/verificar`). As tags ficam no `localStorage` (`helpdesk:routing-tags`) e são reenviadas a cada `openChat()`.

## Como confirmar

1. Pegar os audits do ticket (`GET /api/v2/tickets/{id}/audits.json`, coleção Bruno `zendesk-api`), ver se as tags estão no `Create` e ler o `control_context.zen:ticket:tags` do `ChatStartedEvent`.
2. Para confirmar o clique do cliente, buscar no Mixpanel o evento `[atendimento] widget - chat - acoes menuClicado= ouvidoria` (source `widget-zendesk-migration`) pelo CNPJ, pouco antes da criação do ticket. Se o evento existir, foi escolha do cliente. Se não existir, as tags ficaram velhas no `localStorage`.
3. O link da Ultimate tem que ser o da conversa do ticket. O `platformConversationId` é a tag `conversationid:<id>` do ticket, e o UUID da Ultimate está no audit `resolutions_service` (`via.source.from.conversation_id`).

## Reconstruir o que o cliente fez no widget antes da Ultimate

Antes da Ultimate o cliente não digita nada: o "chat" do widget é um menu de botões montado no front (`setChatMessages` só no redux), que não é persistido nem vai para o Sunshine. O que dá para reconstruir:

1. **Logs do backend (Cloud Logging, `contabilizei-prod-01`, namespace `crm-prd`)**, buscando o CNPJ em ~30 min antes da criação do ticket. Cada abertura do widget gera `BuscarClienteEmReconexaoUsecase` + `VerificarClienteElegivelOuvidoriaService` (warm-up). A escolha de "Contabilidade" gera `VerificarClienteElegivelOuvidoriaController` (o `OmbudsmanValidationGuard`, que mostra "Atendimento" / "Reclamação/Elogio"). A abertura do chat gera `AuthController - assinando token` (o `bootZendesk3` da view do chat). As rotas de tema e roteamento (`widget/v2/temas`, `widget/v2/roteamento`) **não logam**.
2. **Tags de criação do ticket** (BigQuery, ver [[zendesk-tickets-bigquery]]): se vieram só `cnpj:` + `sys_grupo_ouvidoria` + `sys_tema_ouvidoria`, o `roteamento.tags` estava vazio, ou seja, o cliente não passou por tema/subtema.
3. **O botão clicado só aparece no Mixpanel** (`[atendimento] widget - chat - acoes menuClicado= contabilidade|ouvidoria|atendimento` e `direcionamento= transbordoia`, source `widget-zendesk-migration`, propriedade `cnpj`). Os logs não distinguem "Reclamação/Elogio" de "Atendimento" com redirecionamento para a IA (flag `ATENDIMENTO_BOT_ULTIMATE_PARA_IA_CHAT`), que também abre o chat em poucos segundos.

Os 6 tickets do PRC-154516 (todos de 2026-11-04, horários UTC), levantados assim em 2026-11-11:

| Ticket | CNPJ | Elegível por | Menu Contabilidade → chat aberto | Ticket criado | Observação |
| --- | --- | --- | --- | --- | --- |
| 30176681 | 69205161000118 | ticket nas últimas 24h | 12:46:34 → 12:46:42 (8s); de novo 12:47:28 → 12:47:34 (6s) | 12:47:47 | a 1ª abertura ficou anônima (erro de autenticação no bot); o ticket nasceu na 2ª, ver "Caso 30176681" abaixo |
| 30176961 | 35266533000102 | tabela habilitados ouvidoria | 12:55:30 → 12:55:33 (3s) | 12:56:04 | plano Experts; já tinha aberto o menu às 12:41:02, 12:46:04 e 12:49:55 sem abrir chat |
| 30177240 | 54774635000175 | ticket nas últimas 24h | 13:04:19 → 13:04:22 (3s) | 13:04:28 | reabriu o chat às 13:08:23 |
| 30177825 | 53418519000150 | ticket nas últimas 24h | 13:17:45 → 13:17:48 (3s) | 13:17:59 | tinha o ticket 30178392 de WhatsApp aberto em paralelo |
| 30179964 | 45008015000134 | ticket nas últimas 24h | 14:11:45 → 14:11:51 (6s) | 14:12:07 | — |
| 30180929 | 58013722000160 | ticket nas últimas 24h | 14:36:57 → 14:37:02 (5s) | 14:37:21 | reabriu o chat às 14:39:13 |

Em todos, de 3 a 8 segundos entre o menu "Atendimento / Reclamação/Elogio" aparecer e o chat abrir, sem nenhum tema no caminho (as tags de criação não têm `roteamento.tags`). Isso bate com um clique direto em "Reclamação/Elogio", mas a confirmação do botão depende do Mixpanel.

### Caso 30176681: erro de autenticação no chat antes do ticket

Levantado em 2026-11-11 pelos logs de `contabilizei-prod-01` (sem API do Zendesk/Sunco). O ticket mostra mensagens de erro de autenticação antes da saudação "Olá! Um de nossos especialistas logo irá te atender...", mas o log da Ultimate da conversa do ticket (`6aba9f04bf70d09246af6c2f`) só começa nessa saudação. São duas conversas:

| Hora (UTC) | Fonte | Evento |
| --- | --- | --- |
| 12:46:34 | `atendimento-zendesk-prd` | `VerificarClienteElegivelOuvidoriaController` (menu Atendimento / Reclamação/Elogio) |
| 12:46:42 | `atendimento-zendesk-prd` | `AuthController - assinando token` para o responsável (JWT gerado sem erro) |
| 12:46:46 | `atz-worker-webhooks-prd` | bot: "Olá! Me conta em poucas palavras como podemos te ajudar" na conversa **anônima** `6aeb29354bc0b97e96063eb5`, usuário `Web User 6aeb29344bc0b97e96063e82`, sem ticket |
| 12:46:58 | idem | cliente: "Atendimento esta bem ruim." |
| 12:47:01 | idem | bot: "Olá! Não conseguimos confirmar sua autenticação neste momento..." |
| 12:47:11 | idem | cliente: "impostos" |
| 12:47:14 | idem | bot: a mesma mensagem de erro de autenticação |
| 12:47:28 → 12:47:34 | `atendimento-zendesk-prd` | widget reaberto: menu da ouvidoria de novo e novo token |
| 12:47:42 | `atz-worker-webhooks-prd` | mensagem do cliente na conversa **autenticada** `6aba9f04bf70d09246af6c2f` (a mesma do ticket 30163979 de 03/11, já fechado) |
| 12:47:47 | idem | bot: "Olá! Um de nossos especialistas logo irá te atender..."; ticket 30176681 criado em `Ouvidoria [Chat] [BP]` com `sys_grupo_ouvidoria`, `sys_tema_ouvidoria`, `sys_canal_chat`, `cnpj:69205161000118` |

- **Causa do erro de autenticação:** corrida no widget (`contabilizei-crm-widget-window`). O `bootZendesk3` pede o JWT em paralelo com o carregamento do snippet e o `openChat` não espera o `loginUser`; o messenger abriu anônimo e o bot de chat da Ultimate respondeu com o erro de autenticação. Detalhes e como reconhecer em [[autenticacao-chat-web-zendesk]].
- **Por que o ticket mostra as mensagens anônimas:** quando o login funcionou, o Zendesk juntou o usuário anônimo ao autenticado (descrição do ticket: "Conversation with Web User 6aeb29344bc0b97e96063e82"). O log da Ultimate da conversa anônima é outro; o `ultimateai-webhook` não registrou nada porque o webhook do `chat main` estava desativado até 18:31Z desse dia.
- **Relação com a ACR:** nenhuma com a causa da Ouvidoria. O erro de autenticação não grava tags; o ticket caiu na Ouvidoria pelo clique em "Reclamação/Elogio" (menu → token em 8 s e de novo em 6 s, e o texto do cliente é uma reclamação). É um segundo problema, do widget, que apareceu no mesmo atendimento.
- **Reproduzir a busca:** `gcloud logging read '("6aeb29354bc0b97e96063eb5" OR "6aeb29344bc0b97e96063e82" OR "6aba9f04bf70d09246af6c2f") AND timestamp>="2026-11-04T12:40:00Z" AND timestamp<"2026-11-04T13:00:00Z"' --project contabilizei-prod-01` e, para o token, `"69205161000118" AND "AuthController"`.

## Menu de canais, atalho da IA e o que cada canal faz

Levantado em 2026-11-11 sobre o código local (`contabilizei-crm-widget-window` `develop` de 29/04/2026 e `plataforma-web` `develop` de 30/06/2025; produção pode estar mais nova, o texto do menu em prd já é outro). Detalhes em [[widget-tags-roteamento-ouvidoria]] e no diagrama https://claude.ai/artifact/K9Gd5f9VbosysyYTG8kfgR.

- **Ordem dos menus:** chat em andamento → desconexão → menu inicial (Contabilidade/Bank/Saúde) → ouvidoria (Atendimento / Reclamação-Elogio, só elegíveis) → ticket em aberto (Experts pulam) → tema e subtema, ou atalho da IA → FAQ/autoatendimento → **menu de canais** → abre o chat. O menu de canais é sempre o último.
- **Atalho da IA:** com a flag ConfigCat `ATENDIMENTO_BOT_ULTIMATE_PARA_IA_CHAT` ligada, Contabilidade (`BASICO_PADRAO`) pula tema, subtema, FAQ e autoatendimento e vai direto ao menu de canais, com `sys_canal_chat`, `sys_grupo_aida_geral` e `cnpj:` só no redux até o cliente escolher o canal.
- **Chat só para quem tem `elegivelChat`:** o botão Chat depende do `elegivelChat` da rota `atendimento/widget/dados-empresa` (`DadosEmpresaDTO.getElegivelChat`), que é falso para todo plano com "EXPERT" na descrição. Experts só têm Chat no fluxo Saúde e Benefícios (`conditionalElegibiltyChatExperts`). Assim, um Experts que escolhe Contabilidade vê só WhatsApp e E-mail, com ou sem a flag da IA.
- **O que cada canal faz:** antes de tudo, `roteamento.tags` é gravado em `helpdesk:routing-tags`.
  - **Chat:** se era reconexão, espera o ticket antigo fechar (até 3 × 3 s), abre o chat e o `openChat()` manda as tags como `conversationTags` → Ultimate. É o único canal que leva as tags.
  - **WhatsApp:** se há tema, registra em `atendimento/widget/v2/temas/cadastrar-selecao-atendimento-whatsapp`; abre `wa.me/554141010021` com "Olá, eu quero falar sobre o tema X e assunto Y" (sem tema: "sobre Contabilidade") e fecha o widget.
  - **E-mail:** busca o formulário do subtema em `atendimento/faleconosco/formulario-tickets/buscar` e abre `contabilizeics.zendesk.com/hc/pt-br/requests/new` com formulário e assunto preenchidos (sem tema, o formulário padrão) e fecha o widget.

**Ligação com a ACR:** para um cliente Experts no fluxo Contabilidade, o menu de canais não oferece Chat, então o botão "Reclamação/Elogio" (que abre o chat direto, sem passar pelo menu de canais) é o único jeito de chegar ao chat web. Isso explica o ticket 30176961 (plano Experts): abriu o menu três vezes sem abrir chat e, na quarta, abriu o chat em 3 s, caindo na Ouvidoria. É hipótese pelo código; a confirmação do botão continua sendo o Mixpanel.

## Ocorrências

- PRC-154516 → ACR PRD-176094. A análise está documentada no comentário do Glener no card: 142 tickets com `sys_grupo_ouvidoria` de 25/10 a 10/11 (133 chat, 9 WhatsApp); de 01/11 a 10/11, 70 dos 89 de chat vieram do `zen:ticket:tags` do widget e os outros 19 são do incidente da Ultimate de 03/11. ACR concluída em 2026-11-10, com origem `Defeito`, causa `Falha de codificação`, item legado e produto `Atendimento Zendesk > Autoatendimento`. O Bolt e o card apontavam a integração "Buscar tags do chat por conversation" como origem, mas ela só lê o metadata gravado pelo widget.

- 2026-11-04, ticket 30179964 (CNPJ 45008015000134, conversa Sunshine `6ae9b7c9b2f8ffdccc0963cf`, conversa Ultimate `094916e2-3fcc-4dc5-9dfd-60817fd55e2f`). O ticket 30177825 (conversa `6980b21f14c5843b4e676211`) teve o mesmo caminho.
- Desde 2026-10-25, cerca de 140 tickets saíram com `sys_grupo_ouvidoria`, quase todos do chat. De 01/11 a 10/11, a maioria trouxe a tag pelo `zen:ticket:tags` do widget.

- Conclusão final de 2026-11-11 (comentário 29498396 na PRD-176094): causa direta é o clique em "Reclamação/Elogio" por clientes elegíveis, com a regra das 24h como causa contribuinte; incidente e API de elegibilidade descartados.
- Incidente da Ultimate de 03/11 descartado como causa (análise de 2026-11-11 na nota [[PRD-176094]]): tickets de chat nascem com ouvidoria todo dia útil (ex: 21 em 20/10, 16 em 04/11, 10 em 10/11). Entre os clientes elegíveis que abriram o chat, 2,8% (28/10), 5,5% (04/11) e 3,8% (10/11) caíram na ouvidoria e o resto foi para a IA; entre os não elegíveis, nenhum.

## Origem

Não é novo. A tag entrou no widget no commit `dfb1f6f5f35cc95174d187d67b9a15f4a196d2bc` (Matheus Leite, 30/10/2025, "feat: ajustado fluxo para abrir chamado com tags certas"), do card PRD-118831 "[URA unificada] Tratamento do Widget (Ultimate)" (épico PRD-117730). Foi para produção na release 0.96.0, em 10/11/2025. A regra do card: quem está na lista da ouvidoria ou teve ticket nas últimas 24h vê "Atendimento" e "Reclamação/Elogio".

Os dados batem com a data: nenhum ticket de chat com a tag entre 23/10 e 09/11/2025, e tickets todos os dias a partir de 10/11/2025. Desde então são de 200 a 400 tickets de chat por mês (60% a 75% dos tickets com a tag). O PDF com o fluxo completo está anexado no comentário do card.
