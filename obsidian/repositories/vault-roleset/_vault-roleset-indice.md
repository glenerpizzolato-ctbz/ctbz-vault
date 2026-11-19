---
name: vault-roleset-indice
description: "Índice de notas do repositório vault-roleset: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - vault-roleset
repositorio: vault-roleset
caminho: ~/repositories/vault-roleset
---

# vault-roleset

Repositório em `~/repositories/vault-roleset`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[secrets-e-permissoes]] — bindings de SA aos secrets do contabilizei-sm-prod/dev e nome completo do secret
- [[create-secret-value-cifrao]] — no job `create-secret-value`, duplicar cada `$` do valor (`$$`), senão o secret é gravado diferente do original (ex: 401 no Kong)
- [[permissoes-projeto-sa]] — permissões de uma SA em outros projetos (ex: BigQuery no contabilizei-data) ficam no JSON da SA; como conferir se já estão aplicadas
