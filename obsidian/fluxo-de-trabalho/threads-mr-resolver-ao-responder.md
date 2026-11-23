---
name: threads-mr-resolver-ao-responder
description: "Ao responder threads de revisão em MR do GitLab a pedido do usuário, resolver a thread logo depois da resposta, sem deixá-la aberta"
metadata:
  type: feedback
tags:
  - gitlab
  - code-review
atualizado_em: 2026-11-09
---

# Resolver as threads ao responder

Quando o usuário pedir para validar e responder threads de revisão de um MR (de pessoas ou de bots como GitLab Duo e "Revisão automática"), responder e já **resolver** cada thread: `glab api -X PUT "projects/<proj>/merge_requests/<iid>/discussions/<id>?resolved=true"`.

**Why:** no MR !74 do email-service (09/11/2026), o usuário pediu explicitamente para fechar as threads e não deixá-las abertas, depois que deixei algumas abertas "para o revisor resolver".

**How to apply:** vale tanto para quando a thread gera ajuste no código quanto para quando a resposta só explica (falso positivo, thread repetida). Revisores automáticos costumam repetir a mesma thread em revisões novas, e falsos positivos (ex: dizer que `z.guid()` não existe no Zod 4) precisam ser conferidos na versão instalada antes de responder.
