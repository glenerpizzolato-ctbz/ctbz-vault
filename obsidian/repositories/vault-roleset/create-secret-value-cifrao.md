---
name: create-secret-value-cifrao
description: "No job create-secret-value, cada `$` do valor tem de ser duplicado (`$$`), senão o secret é gravado diferente do original"
metadata:
  type: reference
tags:
  - vault-roleset
  - secret-manager
  - gitlab-ci
---

# `create-secret-value`: duplicar o `$` no valor

Ao gravar um secret pelo job `create-secret-value` (branch `create-secret-value`, **Run new pipeline**, inputs `secret_endpoint` e `secret_value`), **cada `$` do valor tem de ser digitado em dobro (`$$`)**. Com um `$` só, o valor gravado no Secret Manager sai diferente do original, mesmo com o `expand: false` do job e com o README dizendo que `$` é aceito sem escape. O `$$` é o escape de `$` do GitLab e é gravado como um `$` só.

## Como aparece

- O serviço sobe normalmente (o `secrets-init` resolve o secret sem erro), mas a chamada autenticada falha (ex: `401` do Kong no `key-auth`).
- O mesmo token, testado à mão (Bruno, curl), funciona. A diferença está só no que foi gravado no Secret Manager.
- Afeta principalmente as keys de consumer do Kong geradas pela pipeline do `kong-config`, cujo charset inclui `$` (`!@#$%^&*()_+=-[]{}|:,.<>?~`).

## Como gravar

1. No valor a colar em `secret_value`, trocar cada `$` por `$$` (ex: `ab$cd` → `ab$$cd`).
2. Rodar a pipeline e conferir no log do job a linha `Created version [N] of the secret [...]` (o log mostra o endpoint, nunca o valor).
3. Reiniciar o deployment que usa o secret: o `secrets-init` só lê o `versions/latest` na subida do pod.
4. Para conferir sem expor o valor, comparar hashes (quem tiver `secretAccessor`, via PAM): `gcloud secrets versions access <N> --secret=<nome> --project contabilizei-sm-prod | sha256sum` contra `printf '%s' '<token>' | sha256sum`.

## Caso real

2026-11-04 (PRD-174790): o secret `emailserviceatendimentocanaisprdpdp_CONTATO_SERVICE_API_KEY` (`projects/1046698394190/...`) foi gravado com o token do consumer `email-service-to-contato-service`, que tem `$`. O `email-service` levou `401` do Kong em todas as consultas de opt-out, e os e-mails de impostos com `optout_purpose` falharam com `OPTOUT_UNAVAILABLE`. Regravado com `$$`, as consultas passaram a voltar 200. Detalhes em [[contrato-optout]].
