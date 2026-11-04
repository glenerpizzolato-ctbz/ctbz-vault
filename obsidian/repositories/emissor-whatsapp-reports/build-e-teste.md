---
name: emissor-whatsapp-reports-build-e-teste
description: "emissor-whatsapp-reports: clone local aponta para o Bitbucket (o atual é GitLab); build exige token npm e bundle prévio; libbrotli do Debian vem do security"
metadata:
  type: reference
---

# Build e teste

- O clone em `~/repositories/emissor-whatsapp-reports` tem `origin` no Bitbucket (antigo). O repositório atual é `ctbz/experts/backend/emissor-whatsapp-reports` no GitLab, adicionado como remote `gitlab`.
- O Dockerfile copia `build/index.js` pronto: gerar antes com `pnpm build` (esbuild). O `pnpm install` da imagem precisa de token do registry `@contabilizei-private` (ver [[atendimento-canais-admin/build-e-deploy|build-e-deploy do atendimento-canais-admin]] para o truque do token temporário).
- Imagem `node:22.x-bookworm` completa, por causa do Google Chrome. A `libbrotli1` da base é vulnerável (CVE-2026-111497) e a correção `1.0.9-2+deb12u1` só vem do repositório de segurança. Desde emissor-whatsapp-reports!3, o Dockerfile faz `apt-get install --only-upgrade libbrotli1 libbrotli-dev` e confere a versão.
- O servidor (Fastify) sobe na 8080 e imprime `listening`; `/` responde 404. Testes: `pnpm test` (22 testes).
- Ver [[cve-2026-111497-node2shell]].
