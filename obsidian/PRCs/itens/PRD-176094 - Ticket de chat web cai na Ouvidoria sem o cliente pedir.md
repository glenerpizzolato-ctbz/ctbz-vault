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
acr:
  - PRD-176094
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

## Ocorrências

- PRC-154516 → ACR PRD-176094. A análise está documentada no comentário do Glener no card: 142 tickets com `sys_grupo_ouvidoria` de 25/10 a 10/11 (133 chat, 9 WhatsApp); de 01/11 a 10/11, 70 dos 89 de chat vieram do `zen:ticket:tags` do widget e os outros 19 são do incidente da Ultimate de 03/11. ACR concluída em 2026-11-10, com origem `Defeito`, causa `Falha de codificação`, item legado e produto `Atendimento Zendesk > Autoatendimento`. O Bolt e o card apontavam a integração "Buscar tags do chat por conversation" como origem, mas ela só lê o metadata gravado pelo widget.

- 2026-11-04, ticket 30179964 (CNPJ 45008015000134, conversa Sunshine `6ae9b7c9b2f8ffdccc0963cf`, conversa Ultimate `094916e2-3fcc-4dc5-9dfd-60817fd55e2f`). O ticket 30177825 (conversa `6980b21f14c5843b4e676211`) teve o mesmo caminho.
- Desde 2026-10-25, cerca de 140 tickets saíram com `sys_grupo_ouvidoria`, quase todos do chat. De 01/11 a 10/11, a maioria trouxe a tag pelo `zen:ticket:tags` do widget.

## Origem

Não é novo. A tag entrou no widget no commit `dfb1f6f5f35cc95174d187d67b9a15f4a196d2bc` (Matheus Leite, 30/10/2025, "feat: ajustado fluxo para abrir chamado com tags certas"), do card PRD-118831 "[URA unificada] Tratamento do Widget (Ultimate)" (épico PRD-117730). Foi para produção na release 0.96.0, em 10/11/2025. A regra do card: quem está na lista da ouvidoria ou teve ticket nas últimas 24h vê "Atendimento" e "Reclamação/Elogio".

Os dados batem com a data: nenhum ticket de chat com a tag entre 23/10 e 09/11/2025, e tickets todos os dias a partir de 10/11/2025. Desde então são de 200 a 400 tickets de chat por mês (60% a 75% dos tickets com a tag). O PDF com o fluxo completo está anexado no comentário do card.
