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
- A imagem base foi fixada em `node:22.23.4-alpine` para corrigir a CVE-2026-111497 (node2shell, sub-task PRD-174640, ver [[cve-2026-111497-node2shell]]) e voltou para `node:22-alpine` em 2026-11-19 (work-item atalhos#1, MR !3), quando essa tag já resolvia para a 22.23.5. Para conferir se a tag de linha já tem a correção, comparar o digest de `https://hub.docker.com/v2/repositories/library/node/tags/22-alpine` com o das tags `22.23.x-alpine`. No build local, usar `docker build --pull`: sem ele, o Docker usa a `node:22-alpine` que estiver em cache (no teste, uma v22.22.3, ainda vulnerável). O deploy de 2026-11-19 (revisão `00007-d9x`, `atalhos:1.0.2`) já usa a base nova, com Node v22.23.5. Para conferir a base de um deploy, procurar `FROM docker.io/library/node:22-alpine@sha256:` no log do job `build-push-container` e rodar `docker run --rm node@sha256:<digest> node -v`. O job `container-scanning` (Trivy) deixa o SBOM e o relatório nos artefatos.
- Validar localmente: `pnpm test`, depois `docker build -t atalhos . && docker run --rm -p 18080:8080 atalhos` e `curl localhost:18080/` (deve voltar 200).
