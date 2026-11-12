---
name: widget-tags-roteamento-ouvidoria
description: Como o widget do chat web manda tags de roteamento (conversationTags) para o Zendesk, de onde vêm as tags sys_grupo_ouvidoria/sys_tema_ouvidoria e por que elas podem ficar velhas no localStorage
metadata:
  type: reference
tags:
  - contabilizei-crm-widget-window
  - zendesk
  - ouvidoria
---

# Tags de roteamento do widget (ouvidoria)

Análise feita sobre a cópia local de 2026-04-29 (`develop`). O remoto fica no Bitbucket (`contabilizei-ninjas`), e o `git fetch` falhou por falta de acesso.

- `ChatZendesk/services/index.ts` → `openChat()` chama `addConversationTags()`, que lê o `localStorage['helpdesk:routing-tags']` e faz `zE('messenger:set', 'conversationTags', tags)`. O ticket nasce com essas tags (no handoff, elas aparecem como `zen:ticket:tags`). As views `ChatZendesk` e `ChatZendeskMobile` chamam `openChat()` ao montar.
- O botão "Reclamação/Elogio" (`ZendeskMigration/components/OmbudsmanFlowOptions`) grava `[...roteamento.tags, 'sys_grupo_ouvidoria', 'sys_tema_ouvidoria', 'cnpj:<cnpj>']` no redux e no `localStorage`, e abre o chat direto.
- Quem vê o menu "Atendimento" / "Reclamação/Elogio" é decidido pelo `OmbudsmanValidationGuard`: só no fluxo `BASICO_PADRAO`, e só quando o BFF `atendimento/faleconosco/elegivel-auditoria/verificar` responde `true`. O backend dessa rota não está em `~/repositories`.
- O `localStorage` só é sobrescrito no `ServiceChannels.handleClick` (`setRoutingTagsToLocalStorage(roteamento.tags)`) e limpo no `resetHelpdeskLocalStorage` (header, TrackedLink, faqs saga). O `RedirectToAIGuard` (direto para a IA) troca só o redux. Por isso, um caminho que abre o chat sem passar por esses pontos reenvia as tags da sessão anterior, inclusive as de ouvidoria.
- No `atendimento-zendesk`, o `BuscarTagsChatPorConversationService` lê o mesmo `zen:ticket:tags` do metadata da conversa no Sunshine para descobrir o fluxo (`sys_tema_ouvidoria` → `BotsTipoFluxo.OUVIDORIA`).

- Origem: o fluxo de ouvidoria veio do PRD-118831 (URA unificada no widget). Os commits são `fbd5cbb`, `895320c` e `0f603ce` (20/10/2025) e `dfb1f6f` (30/10/2025, tags no botão). Foi para produção na release 0.96.0, em 10/11/2025. A elegibilidade é estar na lista da ouvidoria ou ter tido ticket nas últimas 24h.

## Fluxo de menus (ordem dos guards no `Helpdesk/Footer`)

`ChatInProgressGuard` (se há chat em andamento, abre o chat direto) → `WarmupApiDataGuard` → `DisconnectedClientZMGuard` (cliente em desconexão: "Continuar o mesmo atendimento" abre o chat direto, ou "Iniciar um novo atendimento") → `SelectServiceFlowGuard` (menu inicial: Contabilidade `BASICO_PADRAO`, Contabilizei Bank `BANK`, Saúde e Benefícios `CORRETORA`; na Contabilidade entra o `OmbudsmanValidationGuard`) → `BrokerValidationGuard` (Saúde: sem plano, mostra mensagem e para) → `OpenTicketsGuard` (com ticket aberto: "Consultar um atendimento em andamento" ou "Falar sobre um novo assunto"; Experts pulam) → `SelectSubjectsZM` com o `RedirectToAIGuard` (flag ConfigCat `ATENDIMENTO_BOT_ULTIMATE_PARA_IA_CHAT`: Contabilidade vai direto para a IA com `sys_canal_chat`, `sys_grupo_aida_geral`, `cnpj:`) ou tema/subtema → `RoutingIteration` (API `atendimento/widget/v2/roteamento/{id}`: FAQ, autoatendimento ou atendimento humano com `roteamento.tags`) → menu de canais (Chat, WhatsApp, E-mail) → `chat/open` → view `ChatZendesk` → `openChat()`.

Os caminhos que abrem o chat sem passar pelo menu de canais (chat em andamento, "Continuar" da desconexão e reconexão no mesmo tema) não regravam o `helpdesk:routing-tags` e reenviam o que já estava gravado.

## Por que o menu de canais não mostra o Chat

O botão Chat do `ServiceChannels` só aparece quando `elegivelChat` (da rota `atendimento/widget/dados-empresa` da `plataforma-web`, `DadosEmpresaDTO.getElegivelChat`) é `true`, ou quando o plano tem "expert" e o fluxo é `CORRETORA` (`conditionalElegibiltyChatExperts`). O `elegivelChat` é falso para todo plano cuja descrição contém "EXPERT". WhatsApp vem de `elegivelWhatsApp` (Avançado, Premium, Multibenefícios, Experts, ou Básico com autopilot ou comércio) e E-mail é sempre `true`.

Consequência: um cliente Experts que escolhe Contabilidade com a flag `ATENDIMENTO_BOT_ULTIMATE_PARA_IA_CHAT` ligada pula tema/subtema (o `RedirectToAIGuard` chama `setChannelInteration`) e cai direto no menu de canais só com WhatsApp e E-mail, sem chance de chegar à IA pelo chat. Sem a flag, passa por tema/subtema e cai no mesmo menu sem Chat. Para testar o caminho da IA, usar uma empresa de plano não Experts. (Código local: widget `develop` de 29/04/2026, `plataforma-web` `develop` de 30/06/2025.)

## O que cada canal faz (`ServiceChannels.handleClick`)

Antes de qualquer canal, grava `roteamento.tags` em `helpdesk:routing-tags` (ou apaga, se vazio) e registra no Segment `selecionou canal <canal>`.

- **Chat**: `verifyAndOpenChat` (se havia reconexão, espera o ticket antigo fechar, até 3 tentativas de 3 s) → `chat/open` → `ChatZendesk` → `openChat()` manda as `conversationTags` → Ultimate. O widget continua aberto no chat.
- **WhatsApp**: se há `idTema` no localStorage, faz POST em `atendimento/widget/v2/temas/cadastrar-selecao-atendimento-whatsapp` (`idTema`, `idSubtema`); abre `wa.me/554141010021` com o texto "Olá, eu quero falar sobre o tema X e assunto Y" (sem tema: "Olá, eu quero falar sobre Contabilidade"). As routing tags não vão para o WhatsApp. Fecha o widget.
- **E-mail**: busca em `atendimento/faleconosco/formulario-tickets/buscar?idTema&idSubTema` o formulário e o campo do subtema e abre `contabilizeics.zendesk.com/hc/pt-br/requests/new?ticket_form_id=…&tf_<campo>=<tagSubtema>` (sandbox em dev). As routing tags não vão para o ticket. Fecha o widget.

No caminho direto para a IA não há tema no localStorage: o WhatsApp vai sem registro de tema e com o texto genérico, e o E-mail abre o formulário padrão.

Os temas do widget vêm do BFF (`atendimento/widget/v2/temas`, `bank/temas`, `corretora/temas`). O cadastro equivalente com tags fica no seed `atendimento-zendesk/prisma/seeds/v3/temas-subtemas-prod.ts`: Contabilidade tem 13 temas (incluindo "Ouvidoria", com autoatendimento `sys_validar_acesso_ouvidoria`) e Bank tem 4, sem subtemas.

## De onde vem a `sys_canal_chat` (e se ela garante chat web)

Ela tem três origens:

- **Widget, atalho da IA** (`RedirectToAIGuard`): vai junto das `conversationTags`, então já está na criação do ticket.
- **Widget, ticket de formalização** (`createFormalizationTicketZM`): o ticket "Formalização de atendimento via Fale Conosco", criado pela API (`via: Web service`) quando o cliente encerra no FAQ ou no autoatendimento. Não é conversa de chat: é o registro de um atendimento resolvido ou abandonado dentro do widget, sem abrir canal. A rota é `atendimento/tickets/criar-ticket-formalizacao` (BFF), com `origem: Fale Conosco` e as `routing-tags` + `sys_canal_chat`. Quem dispara: o cliente responde "sim, resolveu" no FAQ (`Helpdesk/Faqs`), não interage depois dos artigos (expiração), ou passa pelo autoatendimento (impostos em aberto `DueTaxesGuard`, carta de responsabilidade, mensalidade por boleto/Pix, informe de rendimentos) e confirma ou não interage. Se o cliente diz "não resolveu", segue para o menu de canais e não cria esse ticket. Os tickets nascem `new`, sem comentário além do da API.
- **Gatilho do Zendesk `14919819857948`**: adiciona a tag nos tickets de Native Messaging que nasceram sem ela (ex: tema/subtema → Chat, botão Reclamação/Elogio). Visto no ticket 30176681.

Medição no BigQuery (`raw_tb_ticket_events`, tickets criados de 01/10 a 10/11/2026): os 31.692 tickets `Native Messaging` tinham a tag (nenhum sem), e nenhum ticket `WhatsApp` a tinha (o WhatsApp usa `sys_canal_whatsapp`). Mas 1.750 tickets com a tag (5,2%) não são conversa de chat web: 1.678 de formalização (`Web service`), 71 `Closed Ticket` (follow-up que herda as tags) e 1 `Side Conversation`. Ou seja, a tag indica "veio do Fale Conosco do app"; para ter só o chat web, filtrar também por `via = Native Messaging` (ou excluir `Web service`/`Closed Ticket`).

Diagrama estilo BPMN publicado em https://claude.ai/artifact/K9Gd5f9VbosysyYTG8kfgR.

Caso real: [[PRD-176094 - Ticket de chat web cai na Ouvidoria sem o cliente pedir]].
