---
name: commit-push-automatico
description: Em branch de trabalho ou com MR aberto, terminar o pedido já commitando, dando push e atualizando o MR, sem perguntar
metadata:
  type: feedback
---

# Commit e push automáticos

Quando a sessão está numa branch de feature/fix (não na padrão) ou a branch já tem MR/PR aberto, terminar uma alteração pedida pelo usuário (inclusive ajuste de review) já com testes rodados, commit, push e descrição do MR atualizada (se ela ficou desatualizada), sem perguntar "quer que eu commite/dê push?".

**Por quê:** em 2026-11-03, no MR !95 do `microsservico-agrupamento-guias` (PRD-174790), o usuário teve de pedir commit, push e atualização do MR em mensagens separadas e se irritou: "Quando fizer o que eu pedi pode commitar e dar push já se estiver branch e/ou MR aberto."

**Como aplicar:**
- Stage explícito dos arquivos, nunca `git add -A`; nunca commitar config local com credenciais (`application-local.yml`, `.env`).
- Na branch padrão, ou com testes falhando, não commitar: avisar.
- A regra está também nas instruções comuns (`~/dotfiles/.config/AI_COMMON_INSTRUCTIONS.md`, seção Commits).
