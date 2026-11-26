---
name: zendeskapp-warnings-and-messages-plano-testes-e2e
description: "Plano de testes E2E da base do app Avisos e Mensagens (PRD-179547): pipelines e deploy em dev/prd, permissões por grupo e chamada autenticada ao atendimento-zendesk pelo Kong; pré-requisitos que faltam"
metadata:
  type: project
tags:
  - zendeskapp-warnings-and-messages
  - tests
criado_em: 2026-11-26
---

# Plano de testes E2E (base do app)

Sub-task de teste: [PRD-179547](https://contabilizeicontabilidade.atlassian.net/browse/PRD-179547) (o roteiro completo, com os cenários A1-A5, B1-B5 e C1-C6, está na descrição dela).

## Pré-requisitos levantados em 2026-11-26

- `JWT_SECRET_KEY` **não estava** nas variáveis do GitLab do projeto (as outras estavam: `ZENDESK_APP_ID`, `ZENDESK_OAUTH_TOKEN`, `PERMISSION_GP_*`, por `dev`/`prd`). Sem ela, o `tooling/zcli-config.ts` do deploy para com "Variáveis de ambiente sem valor".
- O app ainda não tem rota no Kong: as rotas existentes têm `kong-path-allow` por app. Proposta: `/atendimento/zendesk/apps/warnings-and-messages` → `atendimento-zendesk`, liberando `/api/v1/zendeskapps/warnings-and-messages` (ver [[autenticacao-kong-jwt]]).
- O `GET /healthz` do atendimento-zendesk não passa pelo Kong nem pelo `ZendeskAppsGuard`; para provar os segredos, o teste usa um `GET /api/v1/zendeskapps/warnings-and-messages/ping` com o guard, chamado por um botão "Testar conexão" na tela.
- Os deploys são manuais: a pipeline da `master` (merge) fica `manual` com `deploy-dev` e `deploy-prd`.
- As variáveis `CUSTOM_JOB_*` aparecem também como variáveis do projeto no GitLab (espelho da config do repo `pipeline`); o deploy atual já apaga o `dist/zcli.apps.config.json` no fim (`rm -f`).

## Execução (2026-11-26)

Resultado no comentário da PRD-179547, com prints (cópia local em `~/Downloads/e2e-PRD-179547/`). Card concluído.

- **A (pipelines)**: MR verde; merge na master com release; `deploy-dev` e `deploy-prd` manuais atualizaram só o app do próprio ambiente (app_id 1321165 e 1321150), sem segredo no log; instalações conferidas pela API (`env`, `baseUrl` do Kong novo, grupos, restrição).
- **B (permissões)**, em dev e prd: dois grupos → Publicador; só Editor → Publicador; só Leitor → Leitor; nenhum → ícone some (mesmo para admin).
- **C (chamada autenticada)**: botão "Testar conexão" OK em ~350-500 ms, com o `sub` do agente logado; negativos pelo Kong ok (401/403).
- Faltaram C4 (DevTools: segredo não chega ao navegador) e C6 (print do erro com a rota fora).

## Como trocar os grupos do usuário para testar

O token de serviço da coleção `experts-bruno/zendesk-api` é de outro usuário ("Engenharia Experts", agente) e leva 403 em `group_memberships`. Com a sessão de admin no navegador, a própria API do Zendesk aceita a escrita com o CSRF da página: `authenticity_token` de `GET /api/v2/users/me.json` no header `X-CSRF-Token`, e `POST /api/v2/group_memberships.json` / `DELETE /api/v2/group_memberships/<id>.json` (os ids vêm de `GET /api/v2/users/<id>/group_memberships.json`). O app só relê os grupos depois de recarregar o Zendesk. Ids do usuário Glener: prd `14670538379292`, dev `15426900694556`.
