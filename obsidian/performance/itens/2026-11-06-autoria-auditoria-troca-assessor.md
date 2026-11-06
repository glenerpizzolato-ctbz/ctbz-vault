---
name: 2026-11-06-autoria-auditoria-troca-assessor
description: "Gap de integridade da auditoria de troca de assessor no experts-service (autor forjável)"
metadata:
  type: project
tags:
  - performance
titulo: "Gap de integridade na auditoria de troca de assessor (experts-service)"
data: 2026-11-06
periodo: 2026QD3
categorias:
  - seguranca
impacto: alto
fontes:
  - "[[PRD-165484]]"
  - "[[PRD-175691]]"
  - "[[auditoria-troca-assessor]]"
---

# Gap de integridade na auditoria de troca de assessor (experts-service)

- **Período:** 2026QD3 · **Categorias:** seguranca · **Impacto:** alto

## Contexto

Ao validar a correção do [[PRD-165484]] (passar a gravar o autor da troca de assessor, para investigar trocas indevidas), investiguei quem valida o token antes do `experts-service`. A correção deixou o `author` sempre preenchido, mas não o tornou confiável.

## O que fiz

Mapeei a cadeia de autenticação (front `experts-admin` → Zelador/Guardião → Kong → `experts-service`) cruzando código, `kong-config` (dev e prd) e testes em dev feitos pelo dev. Achei dois caminhos em que o autor da auditoria é forjável:

- Rotas `/v1/...` de escrita: sem hook de autenticação; o autor vem de `request.body.author`. Protegidas só pela chave de consumer do Kong, que 12+ serviços têm. Em dev, `GET /v1/events` responde 200 com a chave do Kong e sem Bearer — comportamento esperado da API interna, mas mostra que `/v1` não tem identidade de usuário.
- Rotas `/view/...`: sem `key-auth` nem plugin JWT no Kong (confirmado na config dev e prd); o serviço só faz `keycloak.jwt.decode`, sem verificar a assinatura (`src/infra/auth/keycloak.ts`). O serviço aceitar Bearer de assinatura inválida foi confirmado em teste local; se a rota `/view` é alcançável por fora do Zelador ainda não foi confirmado em dev/prd.

## Resultado

A coluna "Autor" da auditoria de troca de assessor não é um registro confiável contra ator deliberado: quem tem chave de consumer pode escrever uma troca pela `/v1` com qualquer `author`, bypassando a tela do admin. Para o uso legítimo pela tela (via `/view`), o autor é o e-mail real do Keycloak, então erros honestos ficam atribuídos certo. Correções propostas: verificar a assinatura do token (`verifyOffline`/JWKS) no serviço e/ou plugin JWT no Kong na rota `/view`, e nas rotas `/v1` parar de confiar em `body.author` (exigir identidade autenticada ou restringir qual consumer pode definir autor). Exposição interna (exige chave de consumer ou alcançar a rota `/view`); não é brecha anônima externa.

**Correção (2026-11-06):** aberto o card [[PRD-175691]] (Defeito, épico CTS Eng Canais) + sub-task [[PRD-175692]] `[experts-service]`, ambos em Building. Implementado o `verifyOffline` (JWKS + `kid`, fail-closed) no `experts-service`, com teste automatizado e coleção Bruno das rotas `/view`; branch `fix/PRD-165484` com push. Follow-up registrado no card: autoria autodeclarada nas rotas `/v1`.

## Evidências

- [[PRD-165484]]
- [[auditoria-troca-assessor]] (nota do repositório `experts-service`)
- `kong-config`: `dev/experts/experts-service/experts-service.yaml` e `prd/heimdall_legado/experts/experts-service/experts-service.yaml` (rota `.view.route` sem plugins)
- `experts-service`: `src/infra/auth/keycloak.ts` (`decode` sem verificar assinatura), `src/api/index.ts` (rotas `/v1` sem hook)
