---
name: emissor-whatsapp-reports-build-e-teste
description: "emissor-whatsapp-reports: clone local aponta para o Bitbucket (o atual é GitLab); build exige token npm e bundle prévio; imagem node:22-bookworm (Debian, por causa do Chrome)"
metadata:
  type: reference
---

# Build e teste

- O clone em `~/repositories/emissor-whatsapp-reports` tem `origin` no Bitbucket (antigo). O repositório atual é `ctbz/experts/backend/emissor-whatsapp-reports` no GitLab, adicionado como remote `gitlab`.
- O Dockerfile copia `build/index.js` pronto: gerar antes com `pnpm build` (esbuild). O `pnpm install` da imagem precisa de token do registry `@contabilizei-private` (ver [[atendimento-canais-admin/build-e-deploy|build-e-deploy do atendimento-canais-admin]] para o truque do token temporário).
- Imagem `node:22-bookworm` completa (Debian, não alpine), por causa do Google Chrome instalado via apt. A CVE-2026-111497 (libbrotli1) foi tratada no !3 com a imagem fixada em `22.23.4-bookworm` e upgrade manual da `libbrotli1`; desde o !4 (2026-11-19) voltou para a tag de linha `node:22-bookworm`, que já traz a `libbrotli1 1.0.9-2+deb12u1`.
- O servidor (Fastify) sobe na 8080 e imprime `listening`; `/` responde 404. Testes: `pnpm test` (22 testes).
- Ver [[cve-2026-111497-node2shell]].
