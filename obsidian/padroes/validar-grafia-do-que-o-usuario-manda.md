---
name: validar-grafia-do-que-o-usuario-manda
description: "Padrão para os agentes: conferir a grafia do que o usuário manda, principalmente entre aspas duplas e crases (nomes de repo, branch, pasta, variável, título), e avisar antes de usar; caso do repo criado como zendeskapp-warnings-and-menssages"
metadata:
  type: feedback
tags:
  - padroes
  - escrita
criado_em: 2026-11-26
---

# Validar a grafia do que o usuário manda

A regra está nas instruções comuns dos agentes (`~/dotfiles/.config/AI_COMMON_INSTRUCTIONS.md`, seção Escrita > "Erros de grafia no que o usuário manda"): conferir a grafia do texto recebido, principalmente o que vem entre aspas duplas (`"..."`) ou crases (`` `...` ``), e avisar antes de usar um provável erro. Ação difícil de desfazer (criar repo, branch, recurso, card, enviar mensagem) pede confirmação da grafia; correção trivial pode seguir corrigida, avisando. Nome que já existe com a grafia "errada" usa o nome real.

**Why:** em 2026-11-26 o repositório do app de avisos foi criado como `zendeskapp-warnings-and-menssages` (o certo é `messages`) e o nome se espalhou: caminho no GitLab, arquivos de CI no repo `pipeline`, chave do Sonar, `package.json`, títulos de sub-tasks, pastas locais, worktrees e notas do vault. A correção exigiu dois MRs novos (pipeline!3586 e zendeskapp-warnings-and-messages!2), rename do projeto, um projeto novo no Sonar e a troca das pastas.

**How to apply:** ao receber um nome entre aspas ou crases que vai virar recurso, ler a palavra com atenção (inglês e português) antes do primeiro uso, e apontar a dúvida na hora, não depois de criar.
