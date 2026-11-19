---
name: agent-eval-indice
description: "Índice de notas do repositório agent-eval: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - agent-eval
repositorio: agent-eval
caminho: ~/repositories/agent-eval
---

# agent-eval

Repositório em `~/repositories/agent-eval`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[build-e-deploy|Build e deploy]] — agent-eval: imagem Debian slim (onnxruntime exige glibc), deploy manual via deploy.sh, container precisa do baseline montado do GCS
- [[agent-eval/install-local|Install local]] — pnpm install e docker build falham no download CUDA do onnxruntime-node (404); pular com ONNXRUNTIME_NODE_INSTALL_CUDA=skip
- [[historico-mrs-agent-eval|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
- [[dependencias-agent-eval|Dependências]] — o que consome (repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome
