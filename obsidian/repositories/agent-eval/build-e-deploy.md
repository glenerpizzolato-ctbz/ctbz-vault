---
name: agent-eval-build-e-deploy
description: "agent-eval: imagem Debian slim (onnxruntime exige glibc), deploy manual via deploy.sh, container precisa do baseline montado do GCS"
metadata:
  type: reference
---

# Build e deploy

- Imagem `node:<versão>-slim` (Debian, não Alpine): o `onnxruntime-node` só tem binários glibc.
- Sem CI: o deploy é manual, pelo `deploy.sh` (`--skip-baseline` reaproveita o baseline já no GCS). Defaults: `PROJECT_ID=atendimento-canais-dev`, `SERVICE=agent-eval-${ENVIRONMENT}`.
- O container precisa de `/mnt/agent-eval/baseline/baseline.json` (montado do GCS no Cloud Run). Sem ele, a imagem sobe e para com ENOENT, o que é esperado num teste local.
- Testes: `pnpm typecheck` e `pnpm test` (vitest, 65 testes), sem dependência privada.
- Ver [[cve-2026-111497-node2shell]].
