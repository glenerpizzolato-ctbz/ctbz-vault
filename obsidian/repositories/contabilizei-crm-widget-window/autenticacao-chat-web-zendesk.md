---
name: autenticacao-chat-web-zendesk
description: "Como o chat web do widget autentica o cliente no Zendesk Messaging: sessão da plataforma no BFF, JWT assinado pelo atendimento-zendesk (loginUser) e o que não é autenticado (tags do localStorage, WhatsApp, e-mail)"
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
