---
name: file-transcriber-build-e-imagem
description: "file-transcriber: serviço Python (uv); o Node que o Wiz acusava vinha do basedpyright; lock deve ser gerado num container limpo do uv"
metadata:
  type: reference
---

# Build e imagem

- Serviço Python (FastAPI) com `uv`. O Dockerfile instala com `uv sync --locked --no-dev`, então o que estiver no grupo `dev` do `pyproject.toml` não entra na imagem.
- O Node.js que o Wiz acusava (22.15.1, CVE-2026-111497) vinha do pacote `nodejs-wheel-binaries`, dependência do `basedpyright`, que estava nas dependências de produção. Em 2026-10-26 eles foram para o grupo `dev` (file-transcriber!25). O CI usa `uv sync --locked`, que inclui o grupo dev, então o `make lint_check` continua funcionando.
- **Armadilha ao rodar `uv lock` localmente:** a máquina exporta `UV_EXTRA_INDEX_URL` (mirror PyPI no GitLab) e o lock passa a apontar todas as fontes para ele. Gerar o lock num container limpo: `docker run --rm -v "$PWD":/w -w /w --user $(id -u):$(id -g) -e UV_CACHE_DIR=/tmp/uvc ghcr.io/astral-sh/uv:python3.13-alpine uv lock`.
- Testes e lint: no mesmo container, com `apk add ffmpeg build-base python3-dev crc32c-dev cmake`, rodar `uv sync --locked`, `uv run python -m pytest` (53 testes) e `uv run basedpyright app --level error`.
- Ver [[cve-2026-111497-node2shell]].

## Terraform de staging é legado

A pasta `terraform/staging` (`service_name = "file-transcriber"`, projeto `aida-stg`) criava um Cloud Run avulso que a CI não aplica. Ele ficou parado numa imagem `localbuild` de 2025-07 e foi apagado em 2026-10-30, por causa da CVE-2026-111497. Os serviços reais são `file-transcriber-stg` (aida-stg) e `file-transcriber-prd` (aida-prd), com deploy pela pipeline. Não rodar `terraform apply` nessa pasta: ele recriaria o serviço avulso.
