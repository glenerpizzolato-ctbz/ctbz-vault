---
name: destravar-atendimento-ultimate
description: "Como destravar uma conversa de WhatsApp presa numa sessão/versão antiga do bot da Ultimate (status 'Sem assistência'): inatividade, pass/release control e delete da conversa no Sunshine"
metadata:
  type: reference
tags:
  - tests
  - ultimate
  - sunshine
dominio:
  - atendimento
  - ultimate
repositorios:
  - experts-bruno
ambiente: prd
atualizado_em: 2026-10-27
---

# Destravar atendimento na Ultimate

Sintoma: testando um bot no WhatsApp, a conversa fica presa numa sessão da Ultimate (no dashboard aparece como `Sem assistência`) e todo "oi" novo cai nessa mesma sessão, rodando a versão antiga/problemática do fluxo em vez da versão publicada com as correções.

O que **não** resolve: fechar o ticket de teste no Zendesk (skill [[fechar-tickets-teste-zendesk]]). Um "oi" depois disso abre outro ticket, mas com a mesma sessão presa na Ultimate.

## Passo a passo

### 1. Esperar o tempo de inatividade (o que funcionou)

Parar de mandar mensagens e esperar a sessão da Ultimate expirar por inatividade. Depois disso, mandar outro "oi": a Ultimate abre uma sessão nova e o fluxo começa do zero, já na versão publicada. Foi assim que destravou em 2026-10-27 (PRD-173035, número de Ouvidoria). O tempo exato da inatividade não foi medido.

### 2. Switchboard: pass control / release control (não resolveu)

O Sunshine Conversations (smooch) tem um switchboard que define qual integração controla a conversa (ex: Ultimate, Zendesk Agent Workspace). As ações ficam na coleção Bruno `~/repositories/experts-bruno/sunhine-api-full/Sunshine Conversations API/Switchboard Actions/` (app de prd `5d659f4dafca510010217b05`, `url` `https://api.smooch.io`, token na secret `sunshine_token` do ambiente `prd`):

- **Pass Control** — `POST /v2/apps/{appId}/conversations/{conversationId}/passControl` com `{"switchboardIntegration": "next"}` (ou o `id`/`name` da integração): torna a integração indicada ativa e deixa as outras em standby.
- **Release Control** — `POST /v2/apps/{appId}/conversations/{conversationId}/releaseControl`: a integração ativa solta o controle e a conversa volta para a integração padrão do switchboard.
- **Offer/Accept Control** — oferece o controle a outra integração (fica `pending`) e ela aceita.

Essas ações só trocam **quem** controla a conversa; não encerram a sessão da Ultimate. Por isso, chamar `releaseControl` e `passControl` não destravou: na próxima mensagem a Ultimate reassume a mesma sessão.

### 3. Apagar a conversa no Sunshine (opção, **não testada**)

> [!WARNING]
> Não foi testado. Validar antes de usar e conferir o que se perde.

A ideia é apagar a conversa no Sunshine para que a próxima mensagem crie uma conversa com outro `conversationId`, e a Ultimate abra uma sessão nova:

- **Delete Conversation** — `DELETE /v2/apps/{appId}/conversations/{conversationId}` (coleção `Sunshine Conversations API/Conversations/Delete Conversation.bru`).
- Apaga a conversa inteira, com mensagens e anexos, em prd. Os tickets do Zendesk continuam existindo, mas o histórico da conversa no Sunshine se perde.
- A conversa padrão (`default`) do usuário não pode ser apagada; nesse caso dá para limpar só as mensagens (`Messages/Delete All Messages.bru`), o que provavelmente não reinicia a sessão da Ultimate.
- O `conversationId` é o do Sunshine (24 caracteres hex), não o ID da conversa no dashboard da Ultimate (UUID).
- Credenciais: secret `sunshine_token` do Bruno, ou o `APP_SERVICES_SUNSHINE_APP_KEY`/`APP_SERVICES_SUNSHINE_SECRET` (auth basic) do `.env` do atendimento-zendesk, conferindo antes se apontam para o app de prd. Nunca exibir os valores.

Antes de apagar, conferir: se o usuário de teste tem outras conversas/canais vinculados que dependem dessa conversa, e se o conversationId é mesmo o da sessão presa (`Get Conversation`).
