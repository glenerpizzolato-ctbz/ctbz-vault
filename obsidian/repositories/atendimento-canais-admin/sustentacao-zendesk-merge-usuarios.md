---
name: sustentacao-zendesk-merge-usuarios
description: Sustentação Zendesk do admin — como achar a auditoria de um merge de usuários recusado, por que o motivo não aparece (corpo do 422 descartado) e o que já foi testado que NÃO bloqueia o merge na Zendesk
metadata:
  type: reference
tags:
  - atendimento-canais-admin
  - zendesk
---

# Merge de usuários da Zendesk pela Sustentação

A tela `sustentacao/zendesk/usuarios` mescla o duplicado no principal com `PUT /api/v2/users/{duplicado}/merge` (`src/server/clients/zendesk-support/zendesk-support.api.ts`, `mergeUser`), depois de uma simulação (token) em `zendesk-usuarios.service.ts` (`aplicarMerge`).

## Achar a auditoria (inclusive dos recusados)

Toda tentativa grava um log com `jsonPayload.log="zendesk-sustentacao-audit"` (e a coleção `auditoria` no Firestore). No Cloud Logging:

```bash
gcloud logging read 'jsonPayload.acao="usuario.merge"' --project atendimento-canais-prd --freshness=2d --format=json
```

O registro traz `alvo` (`duplicado->principal`), `chamado`, `operador`, `resultado` e `status`. A requisição do front aparece como 502 em `/api/sustentacao/zendesk/usuarios`.

## Armadilha: o motivo da recusa se perde

Quando a Zendesk responde fora de 2xx, o `aplicarMerge` guarda só o `status` (ex: 422) e descarta o corpo da resposta, então nem o log nem a auditoria dizem por quê. Melhoria possível: guardar o corpo do erro na auditoria.

## `{"resultado":"sem_simulacao"}` (409, auditoria `bloqueado`)

O token da simulação (`zendesk-sustentacao.simulation.ts`) é de uso único, vale 5 min e fica num `Map` da instância. Ele é consumido **antes** da chamada à Zendesk, então um merge que a Zendesk recusou também gasta o token: clicar em aplicar de novo sem simular devolve `sem_simulacao`. Também acontece se passar de 5 min ou se a instância reiniciar (Cloud Run com min 0, max 1). Solução: simular de novo e aplicar.

## Causa conhecida do 422: `external_id` no duplicado (prod)

Em prod a Zendesk recusa o merge quando o duplicado tem `external_id` (hash do login SSO/JWT), com a mensagem `"Não é possível fundir <nome> enquanto ele tiver uma ID externa."`. No sandbox o mesmo cenário mescla (configuração de SSO diferente), então **não dá para reproduzir lá**. Como resolver pela API (coleção `experts-bruno/zendesk-api`, prod): guardar o valor, `PUT /users/<duplicado>.json` com `{"user":{"external_id":null}}` e depois `PUT /users/<duplicado>/merge.json` com `{"user":{"id":<principal>}}`. O e-mail do duplicado vira identidade secundária do principal e os tickets migram. Caso: PRC-154451 (2026-11-24). Melhoria possível no admin: a simulação apontar `external_id` no duplicado e oferecer limpá-lo.

## O que já foi testado no sandbox e NÃO bloqueia o merge (2026-11-24)

- Duplicado com `external_id` (hash de SSO/JWT) e e-mail verificado → mescla (200) **no sandbox**; em prod bloqueia (ver acima).
- Duplicado com `phone` igual ao de uma identidade `phone_number` do principal (`shared_phone_number: true`) → mescla (200).
- O que deu 422 (com corpo vazio): um segundo merge para o mesmo principal logo depois de outro, ou seja, falha transitória enquanto a Zendesk processa o anterior. Tentar de novo depois de alguns segundos passou. No PRC-154451 o 422 se repetiu 4 minutos depois (21:05 e 21:09), então lá **não** é transitório.

Caso: PRC-154451 (usuários 1275653644 → 362718497699), ver [[PRD-151519 - Cliente com mais de um contato cadastrado com mesmo telefone na zendesk]].
