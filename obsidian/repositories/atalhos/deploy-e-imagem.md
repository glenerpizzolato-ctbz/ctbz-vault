---
name: atalhos-deploy-e-imagem
description: "Deploy do atalhos (Cloud Run atalhos-engenharia), imagem base e como validar o container localmente"
metadata:
  type: reference
tags:
  - atalhos
---

# Deploy e imagem do atalhos

- O serviço é o Cloud Run `atalhos-engenharia`, no projeto `atendimento-canais-dev` (us-central1, atrás do IAP); só existe em dev. Repositório: https://gitlab.com/ctbz/experts/ferramentas/atalhos (branch `master`).
- O `.gitlab-ci.yml` só inclui o componente da pipeline central (`ctbz/devops/recursos/pipeline/ci-cd`); a config do deploy fica em `custom/ctbz/experts/ferramentas/atalhos.yml` (`SERVICE: atalhos-engenharia`) no repositório da pipeline.
- O `Dockerfile` não tem dependências de runtime: copia `package.json`, `server.js` e `public/` e roda `node server.js` na porta 8080.
- A imagem base fica fixada em `node:22.23.4-alpine` desde a correção da CVE-2026-111497 (node2shell, sub-task PRD-174640, ver [[cve-2026-111497-node2shell]]). Não voltar para tag flutuante (`node:22-alpine`).
- Validar localmente: `pnpm test`, depois `docker build -t atalhos . && docker run --rm -p 18080:8080 atalhos` e `curl localhost:18080/` (deve voltar 200).
