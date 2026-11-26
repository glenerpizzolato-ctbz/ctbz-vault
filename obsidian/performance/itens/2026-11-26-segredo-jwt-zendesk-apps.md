---
name: 2026-11-26-segredo-jwt-zendesk-apps
description: "Mapeamento da injeção do segredo do JWT dos apps Zendesk e descoberta de riscos: segredo igual em dev e prd em todos os apps, impresso em claro no log do deploy de prd, variáveis sem mask/protect"
metadata:
  type: project
tags:
  - performance
titulo: "Riscos no segredo do JWT dos apps Zendesk (dev = prd, vazamento no log do deploy)"
data: 2026-11-26
periodo: 2026QD3
categorias: [seguranca]
impacto: alto
fontes: ["[[zendesk-apps-segredo-jwt]]", "[[PRD-179389]]"]
---

# Riscos no segredo do JWT dos apps Zendesk

## Contexto

Ao montar o app novo Avisos e Mensagens (PRD-179389), levantei como os segredos dos apps Zendesk chegam à instalação e ao gateway.

## O que fiz

- Mapeei o fluxo dos 16 zendeskapps do grupo: variável do GitLab -> `envsub` -> `zcli apps:update` (que reescreve as configurações da instalação a cada deploy) -> parâmetro seguro no Zendesk; validação no Kong com o segredo do Secret Manager; o `ZendeskAppsGuard` do atendimento-zendesk não confere assinatura.
- Conferi por hash (sem expor valores) que o `JWT_SECRET_KEY` é o mesmo em dev e prd em todos os apps checados, e que o deploy de prd do whatsapp-ativo imprime o segredo em claro no log (`cat dist/zcli.apps.config.json`, variável sem mask, jobs visíveis a todos os membros).
- Propus a correção (mask/protect, tirar o `cat`, segredo por ambiente com rotação coordenada gateway + apps) e já deixei o app novo sem o `cat` no deploy.

## Resultado

Riscos documentados com a correção sugerida; afeta todos os apps Zendesk do atendimento e o gateway de prd.

## Evidências

- [[zendesk-apps-segredo-jwt]]
- MR do pipeline do app novo: https://gitlab.com/ctbz/devops/recursos/pipeline/-/merge_requests/3582
