---
name: team-knowledge-base-deploy-e-imagem
description: "team-knowledge-base: é o código dos Cloud Run team-kb e team-kb-ui (o repo team-kb está vazio); uma imagem só, deploy manual via deploy.sh"
metadata:
  type: reference
---

# Deploy e imagem

- O código dos serviços Cloud Run `team-kb` e `team-kb-ui` (projeto `atendimento-canais-dev`, região `southamerica-east1`) fica aqui, em `ctbz/experts/ferramentas/team-knowledge-base`. O repositório `ctbz/experts/geral/team-kb` (que aparece no `go.mod` como module path) está vazio.
- É uma imagem só para os dois serviços: `kb serve` (servidor MCP HTTP, público) e `kb ui` (UI de auditoria, atrás de IAP), escolhidos com `--command` no Cloud Run.
- O deploy é manual, pelo `deploy.sh`, que gera a tag `gcr.io/contabilizei-tools-production/team-kb:<sha>-localbuild`. A tag bate com o commit do repositório, o que ajuda a saber qual versão está no ar.
- A imagem final é `alpine` com `git` (obrigatório para a trilha de auditoria), que traz `libcurl` e `brotli-libs`. Por isso, CVEs de SO como a da `libbrotli` aparecem aqui. Ver [[cve-2026-111497-node2shell]].
- Testes: `go test ./...` (dá para rodar num container `golang:1.25-alpine` com `git` e `ripgrep` instalados).
