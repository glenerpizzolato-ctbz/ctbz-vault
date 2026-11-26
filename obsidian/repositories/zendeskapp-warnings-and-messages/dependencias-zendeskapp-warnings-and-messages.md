---
name: dependencias-zendeskapp-warnings-and-messages
description: "Dependências do zendeskapp-warnings-and-messages: o que ele consome (atendimento-zendesk, sentinela-foundations, ZAF) e quem o consome"
metadata:
  type: reference
tags:
  - dependencias
  - zendeskapp-warnings-and-messages
repositorio: zendeskapp-warnings-and-messages
---

# Dependências do zendeskapp-warnings-and-messages

Padrão em [[dependencias-entre-repositorios]].

## Consome

### Repositórios internos

- `atendimento-zendesk`: API de avisos e mensagens (domínio novo, PRD-179389), via `client.request` do ZAF com JWT HS256 assinado pelo proxy (`iss` 2a7ed7a5-…) — por `src/lib/http/api-client.ts`. Rotas ainda em desenvolvimento.

### Libs internas

- `@contabilizei-private/sentinela-foundations` (tokens CSS do design system Sentinela) — `src/main.tsx`

### Infra GCP

_Nada confirmado ainda._

### Bancos e dados

_Nada._

### Terceiros

- Zendesk Apps Framework 2.0 (SDK em `static.zdassets.com`, `src/iframe.html`) e zcli.
- Google Fonts (Inter).

## Consumido por

_Ninguém (app de tela, usado pela operação no Zendesk)._
