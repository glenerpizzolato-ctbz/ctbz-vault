---
name: frameworks-nodejs
description: "Framework HTTP padrão nos repositórios Node.js do time (Fastify) e as exceções (NestJS, Express); front em React/Vue"
metadata:
  type: reference
tags:
  - padroes
  - nodejs
---

# Frameworks nos repositórios Node.js

Levantamento pelos `package.json` de `~/repositories` (2026-11-17).

- **Back-end: Fastify é o padrão.** Usam: agent-eval, agrupamento-guias-service, bots-api, canais-adk, canais-certificado-digital, contato-service, downdetector, email-service, emissor-whatsapp-reports, experts-dominios-functions, experts-functions, experts-ms-nps, experts-nfs, experts-service, experts-tarefas-assessor, experts-zendesk, monitoria-ia, ms-relatorio-faturamento, survey-service, ticketing-service, zendesk-agents, ctbz_experts_atendimento-canais_zendesk-agents, zendesk-proxy.
- **NestJS (exceção):** atendimento-zendesk, experts-twilio e relacionamento-service (este com o adapter Fastify).
- **Express (legado/pontual):** experts-alertas e proxy-feature-flags-gitlab.
- **Front-end:** React (atendimento-canais-admin, aida-front, front-admin, zendeskapps) e Vue (experts-admin, relacionamento-admin, tarefas-assessor-admin, relatorio-faturamento-admin, webviews-frontend, contabilizei-front-vue).

Para refazer o levantamento: `for d in ~/repositories/*/; do grep -oE '"(@nestjs/core|express|fastify|koa|react|vue)"' "$d/package.json" 2>/dev/null | tr -d '"' | tr '\n' ' ' | sed "s|^|${d}: |"; echo; done`
