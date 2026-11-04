---
name: mr
description: Abre (ou atualiza) o Merge Request no GitLab da branch atual pelo glab - confere se os commits da branch condizem com a feature/card (o não commitado é ignorado), dá push e cria o MR com a descrição da feature, o card do Jira, o work-item (Closes) e o branch chaining, e move a sub-task do Jira para Pull Request. Use quando o usuário pedir para abrir/criar/subir o MR, ou quando o BahCode mandar `/mr` (botão MR do conjunto ou aba MR da feature), com instruções extras nos argumentos (ex: "Abra em draft", override do pré-voo).
argument-hint: "[instruções]"
---

# Abrir o MR

O BahCode manda `/mr` a partir da worktree do conjunto. O contexto da feature chega pelo hook da worktree ou pelo prompt do Claude do conjunto: card do Jira, descrição da feature (`<inventário>/<id>.doc/description.md`), sub-task do conjunto, work-item do GitLab e a frente de que esta depende (branch chaining). Os argumentos (`$ARGUMENTS`) trazem instruções extras e mandam mais que os padrões abaixo.

## 1. Conferir o escopo

1. Descobrir a base: a branch alvo da frente, se o contexto citar branch chaining; senão a branch padrão do remoto (`git symbolic-ref refs/remotes/origin/HEAD`).
2. Ler o que vai no MR, **só o que está commitado**: `git fetch origin`, `git log --oneline origin/<base>..HEAD` e `git diff origin/<base>...HEAD --stat`. O não commitado da worktree (arquivos alterados, novos ou apagados no `git status`) não vai para o MR: não ler, não validar, não commitar e não bloquear por causa dele; deixar como está.
3. Comparar os commits com a feature (descrição, card, work-item e o que os argumentos citam). Se algum commit trouxer alteração que não faz parte dela (arquivo de outra demanda, debug, config local, `.env`, lixo de build), **não abrir o MR**: listar o que destoa, com arquivo e motivo, e parar. Na dúvida, perguntar.

## 2. Branch e commits

- Se estiver na branch padrão ou em HEAD solto, criar a branch: `feat/<key do card>` (ou `fix/…`, conforme a natureza), ou `<tipo>/<breve-descricao>` sem card.
- Não commitar nada: o MR leva só os commits que já existem na branch. Se não houver nenhum commit à frente da base, não abrir o MR e avisar.
- `git push -u origin <branch>`.

## 3. Criar o MR

Se a branch já tem MR aberto (`glab mr list --source-branch <branch>`), não criar outro: atualizar a descrição se preciso e devolver o link.

Senão, `glab mr create` com:

- `--draft` quando os argumentos pedirem draft;
- `--target-branch <base>` (a da frente, no branch chaining);
- `--title`: `<KEY> <descrição curta>` com card, ou a descrição curta da mudança;
- `--remove-source-branch`, `--yes` e `--description` em Markdown, em português, seguindo o template do repo se houver (`.gitlab/merge_request_templates/`), senão:
  - **Contexto**: o objetivo, a partir da descrição da feature e do card (link `https://contabilizeicontabilidade.atlassian.net/browse/<KEY>`);
  - **O que mudou**: os pontos principais do diff;
  - **Como testar**;
  - **Dependência**: a frente/MR de que este depende, no branch chaining;
  - `Closes <link do work-item>`, quando o conjunto resolve um;
  - o override do pré-voo, quando os argumentos pedirem para registrá-lo.

## 4. Depois de abrir

- Mover no Jira (`transitionJiraIssue` pelo MCP do Atlassian) a sub-task do conjunto e a de Desenvolvimento `[repo]` para *Pull Request*, só pelos status do fluxo (ignorar outros, como *Code Review*).
- Responder com o link do MR, a branch alvo e o que foi movido no Jira.
