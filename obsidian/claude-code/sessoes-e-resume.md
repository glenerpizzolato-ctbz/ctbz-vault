---
name: sessoes-e-resume
description: Onde o Claude Code guarda as sessões, como o título delas é gravado e como retomar uma sessão de qualquer pasta com o `cr`
metadata:
  type: reference
---

# Sessões do Claude Code e resume em qualquer pasta

- As sessões ficam em `~/.claude/projects/<caminho-da-pasta-com-hífens>/<session-id>.jsonl`, uma pasta por diretório onde o `claude` foi aberto. Por isso o `/resume` nativo lista só as sessões da pasta atual.
- Cada linha do `.jsonl` tem o `cwd` da sessão. O título fica em linhas próprias: `{"type":"ai-title","aiTitle":"..."}` (gerado automaticamente) e `customTitle` (quando a sessão é renomeada com `/rename` ou aberta com `claude -n`). Vale a última ocorrência no arquivo.
- As subpastas dentro de cada projeto guardam as sessões de subagentes, que não entram no resume.
- A retenção das sessões é controlada por `cleanupPeriodDays` no `~/.claude/settings.json` (padrão: cerca de 30 dias). Está em `365` desde 2026-10-15. Esse arquivo não é versionado no dotfiles.

## `cr`: resume global

A função `cr [busca]` de `~/dotfiles/.config/claude/terminal` (carregada pelo `ctbz/terminal`, só no ambiente CTBZ) lista as sessões de todas as pastas (as mais recentes primeiro), usando `src/utils/claude-sessions.util.sh`. A escolha é feita no `fzf`, e depois ela entra na pasta da sessão e roda `claude --resume <id>`. Depende do `fzf`, instalado pelo `setup.sh --core`.
