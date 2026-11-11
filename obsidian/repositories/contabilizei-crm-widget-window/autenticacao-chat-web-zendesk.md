---
name: autenticacao-chat-web-zendesk
description: "Como o chat web do widget autentica o cliente no Zendesk Messaging: sessão da plataforma no BFF, JWT assinado pelo atendimento-zendesk (loginUser) e o que não é autenticado (tags do localStorage, WhatsApp, e-mail); e a corrida entre loginUser e abertura do messenger que gera o erro de autenticação no bot"
metadata:
  type: reference
tags:
  - contabilizei-crm-widget-window
  - atendimento-zendesk
  - plataforma-web
  - autenticacao
repositorio: contabilizei-crm-widget-window
---

# Autenticação do chat web no Zendesk Messaging

Cadeia, do app até a Ultimate:

1. **Widget → plataforma-web (BFF)**: todas as rotas `atendimento/...` vão pelo axios `contabilizeiPlataformaWebBFF` com `withCredentials: true` (cookie da sessão do app). Em `localhost` o interceptor manda o header `strinfs-token` (do localStorage). No BFF, cada rota resolve a empresa por `AuthContabilizeiFacade.obterEmpresaLogada()`, então o CNPJ vem da sessão, não do cliente.
2. **BFF → atendimento-zendesk**: `POST atendimento/faleconosco/criar-token-autenticacao` (`FaleConoscoJersey.kt`) chama `FaleConoscoFacade.criarJwtFaleConosco`, que busca o responsável (nome/e-mail, com fallback para a razão social) e chama `atendimento/auth/criar-jwt` pelo `AtendimentoZendeskClient`, que passa no API gateway com os headers `client_id` e `access_token` (este no Secret Manager, `crm.atendimento_zendesk.access-token`).
3. **atendimento-zendesk assina o JWT do Zendesk** (`src/domain/auth/auth.controller.ts` + `infra/auth/jwt/auth.service.ts`): HS256, `kid` e segredo em `app.services.zendesk.authJwt.*`, validade 24h, payload `external_id = sha256(email)`, `email`, `name`, `scope: user`, `email_verified: true`. É o log `AuthController - assinando token`. O controller não tem guard próprio: a proteção é o gateway.
4. **Widget → Zendesk**: `bootZendesk3` carrega o snippet e chama `zE('messenger', 'loginUser', cb => cb(tokenJwt))`. A conversa no Sunshine/Ultimate fica com o usuário autenticado (identificado pelo e-mail do responsável).

O que **não** é autenticado:

- As `conversationTags` (`zE('messenger:set', 'conversationTags', ...)`) vêm de `helpdesk:routing-tags` no localStorage, inclusive o `cnpj:<cnpj>`: o cliente pode alterá-las, e o JWT não leva o CNPJ. Quem tem várias empresas com o mesmo e-mail é o mesmo usuário no Zendesk; a empresa só aparece pela tag.
- O `logoutUser` está comentado no `closeChat`, então o login fica no messenger até o token expirar.
- WhatsApp (`wa.me/554141010021`) e e-mail (`requests/new` da central de ajuda) saem do widget sem levar token nem tags; a identificação ali é a do próprio canal.
- O mobile (`ChatZendeskMobile`) usa a mesma rota de token.

## Corrida entre o loginUser e a abertura do messenger

As views `ChatZendesk` e `ChatZendeskMobile` chamam `bootZendesk3(key)` e logo depois `waitZendeskChatScriptLoad().then(openChat)`. O `bootZendesk3` injeta o snippet e dispara o `authUser()` em paralelo, mas o `openChat` não espera o `loginUser`: ele abre assim que `window.zE` existe (ou depois de 5 s, mesmo sem o snippet carregado). Se o token chega antes do `zE` existir, o `setUser` quebra (`window.zE` indefinido), cai no `catch` ("Error on boot zendesk", só no console) e o login nunca acontece. Se chega depois da abertura, o messenger já abriu anônimo. Nos dois casos o cliente conversa como `Web User <id>`, numa conversa do Sunshine diferente da dele, e o bot de chat da Ultimate responde com o erro de autenticação ("Olá! Não conseguimos confirmar sua autenticação neste momento..." / padrão "Olá! Não foi possível autenticar você em nosso chat.").

Como reconhecer pelos logs (`contabilizei-prod-01`): `AuthController - assinando token` no `atendimento-zendesk-prd` e, segundos depois, linhas `NotificarAgenteNovaMensagemService - Mensagem sem ticket vinculado` do `atz-worker-webhooks-prd` com `nomeSolicitante: "Web User <id>"` e o texto de erro de autenticação. Quando o cliente reabre e o login pega, a conversa autenticada (a de sempre do usuário) cria o ticket, e o Zendesk junta o usuário anônimo ao autenticado: o ticket mostra as mensagens anônimas antes ("Conversation with Web User <id>" na descrição), mas o log da Ultimate da conversa autenticada só começa depois, porque as mensagens anônimas estão no log de outra conversa.

Caso de referência: ticket 30176681 (2026-11-04). 12:46:34Z menu da ouvidoria, 12:46:42Z token assinado, 12:46:46Z saudação do bot já na conversa anônima `6aeb29354bc0b97e96063eb5` (usuário `6aeb29344bc0b97e96063e82`), duas mensagens do cliente respondidas com o erro de autenticação (12:47:01Z e 12:47:14Z). Na reabertura, 12:47:34Z novo token, 12:47:42Z mensagem na conversa autenticada `6aba9f04bf70d09246af6c2f`, 12:47:47Z "Olá! Um de nossos especialistas logo irá te atender..." e o ticket criado em `Ouvidoria [Chat] [BP]` com `sys_grupo_ouvidoria`/`sys_tema_ouvidoria` (o cliente clicou em Reclamação/Elogio). O `ultimateai-webhook` não tem nada desse caso porque o webhook do `chat main` estava desativado até 18:31Z desse dia.
