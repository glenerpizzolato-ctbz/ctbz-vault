---
name: gitlab-duo-requested-changes
description: "Como tirar o MR do estado requested_changes deixado pelo GitLab Duo depois de corrigir o que ele pediu: pedir revisão de novo ao Duo"
metadata:
  type: reference
tags:
  - gitlab
  - code-review
atualizado_em: 2026-11-13
---

# GitLab Duo em "requested changes"

Quando o GitLab Duo revisa um MR e marca **requested changes**, o MR fica com `detailed_merge_status: requested_changes`. Isso não muda ao corrigir o código, ao resolver as threads, nem com a aprovação de outra pessoa. Também não adianta tirar o Duo dos revisores: o estado continua.

Para atualizar, é preciso pedir uma nova revisão ao Duo. Se ele não achar mais nada, aprova o MR e o status vira `mergeable`. Há duas formas:

- Na interface: "Request review" (ou o ícone de re-request) ao lado do `GitLabDuo` na lista de revisores.
- Pela API, mantendo os revisores atuais na lista, porque `reviewer_ids` substitui os que estão lá: `glab api -X PUT "projects/:id/merge_requests/<iid>" -F 'reviewer_ids=[<id-revisor-atual>,<id-GitLabDuo>]'`. Os ids saem de `glab api "users?username=GitLabDuo"`. Passar o campo como `-f "reviewer_ids[]=..."` falha com o erro "field name containing a bracket".

O Duo comenta "started review session …" e termina em cerca de 1 a 2 minutos.

Exemplo: email-service !76 (13/11/2026). O Duo pediu mudanças, a correção foi commitada e a thread resolvida, mas o MR continuou em `requested_changes`. Depois que pedi uma nova revisão ao Duo, ele aprovou em uns 80 segundos.
