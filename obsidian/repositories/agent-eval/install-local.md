---
name: agent-eval-install-local
description: "agent-eval: pnpm install falha no postinstall do onnxruntime-node (download CUDA 404); pular com ONNXRUNTIME_NODE_INSTALL_CUDA=skip"
metadata:
  type: reference
---

# Install local do agent-eval

- O `pnpm install`/`pnpm add` falha no postinstall do `onnxruntime-node@1.21.0`: sem `nvcc`, ele assume CUDA 12 e tenta baixar `onnxruntime-linux-x64-gpu-1.21.0.tgz` do GitHub, que responde 404. Rodar com `ONNXRUNTIME_NODE_INSTALL_CUDA=skip npm_config_onnxruntime_node_install_cuda=skip pnpm install`: o runtime de CPU continua funcionando, só o CUDA EP fica fora. Visto em 2026-11-19, no upgrade do Vitest 5 (MR !2).
- **O mesmo 404 quebra o `docker build`** (estágios `builder` e `production`, no `pnpm install`), com qualquer imagem base: conferido em 2026-11-19 com `node:24.22.1-slim` (o do master) e `node:24-slim`. Numa cópia do Dockerfile com `ENV ONNXRUNTIME_NODE_INSTALL_CUDA=skip` no estágio `base`, a imagem builda inteira (inclusive o `prefetch:model`). O Dockerfile já apaga os providers CUDA/TensorRT, então pular o download não tira nada que o Cloud Run usa. Achado no work-item agent-eval#4 (volta para `node:24-slim`).
- Testes: `pnpm test` (sem cobertura) e `pnpm test:coverage`; typecheck com `pnpm typecheck`.
