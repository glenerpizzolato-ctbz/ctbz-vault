---
name: mr
description: Abre (ou atualiza) o Merge Request no GitLab da branch atual pelo glab - confere se os commits da branch condizem com a feature/card (o não commitado é ignorado), dá push e cria o MR com a descrição da feature, o card do Jira, o work-item (Closes) e o branch chaining, e move a sub-task do Jira para Pull Request; quando os commits formam mais de uma parte, divide sem perguntar em MRs pequenos em corrente (branch chaining). Use quando o usuário pedir para abrir/criar/subir o MR, ou quando o BahCode mandar `/mr` (botão MR do conjunto ou aba MR da feature), com instruções extras nos argumentos (ex: "Abra em draft", override do pré-voo).
argument-hint: "[instruções]"
---

# Abrir o MR

O BahCode manda `/mr` a partir da worktree do conjunto. O contexto da feature chega pelo hook da worktree ou pelo prompt do Claude do conjunto: card do Jira, descrição da feature (`<inventário>/<id>.doc/description.md`), sub-task do conjunto, work-item do GitLab e a frente de que esta depende (branch chaining). Os argumentos (`$ARGUMENTS`) trazem instruções extras e mandam mais que os padrões abaixo.

## 1. Conferir o escopo

1. Descobrir a base: a branch alvo da frente, se o contexto citar branch chaining; senão a branch padrão do remoto (`git symbolic-ref refs/remotes/origin/HEAD`).
2. Ler o que vai no MR, **só o que está commitado**: `git fetch origin`, `git log --oneline origin/<base>..HEAD` e `git diff origin/<base>...HEAD --stat`. O não commitado da worktree (arquivos alterados, novos ou apagados no `git status`) não vai para o MR: não ler, não validar, não commitar e não bloquear por causa dele; deixar como está.
3. Comparar os commits com a feature (descrição, card, work-item e o que os argumentos citam). Se algum commit trouxer alteração que não faz parte dela (arquivo de outra demanda, debug, config local, `.env`, lixo de build), **não abrir o MR**: listar o que destoa, com arquivo e motivo, e parar. Na dúvida, perguntar.

## 2. Dividir em MRs pequenos (corrente)

Mais MRs pequenos são preferíveis a poucos grandes, mas só quando o MR é grande o bastante para a divisão ajudar a revisão. **Se a mudança toca poucos arquivos (até uns 5 arquivos, ou uns 200 linhas de diff), abrir um MR só, mesmo que os commits formem partes separáveis**: não forçar a corrente, que nesse tamanho só gera MRs vazios de contexto, mais pipelines e mais merges em ordem. O código, os testes dele e a doc da mesma mudança vão sempre juntos. Nesse caso, ignorar o pedido de dividir dos argumentos (e não rodar os `extra-mr`/`mr-base` do BahCode), e dizer na resposta que ficou um MR só pelo tamanho.

Acima desse tamanho, ver se os commits formam mais de uma parte que se sustenta sozinha (ex: refactor preparatório, migração ou contrato, a regra de negócio, a doc de outra frente). Se formarem, **dividir sem perguntar**, em branch chaining, um MR atrás do outro na ordem da dependência:

- A divisão segue a ordem dos commits: cada corte é um commit da branch. MR 1 = `origin/<base>..<corte 1>`, alvo a base; MR 2 = `<corte 1>..<corte 2>`, alvo a branch do MR 1; e assim por diante. A branch atual fica como o **último** MR da corrente (alvo a branch do penúltimo).
- Criar as branches intermediárias nos cortes sem trocar a branch da worktree nem reescrever commits: `git branch <tipo>/<key>-<n>-<parte> <sha do corte>` e `git push -u origin <branch>`.
- Se os commits misturam assuntos de um jeito que só daria para separar reescrevendo-os, não reescrever: separar só o que já está separado por commits (ou seguir com um MR só).
- Cada MR leva o título com a key e a parte (ex: `PRD-123 (1/3) migração da tabela`), e na descrição a seção **Dependência** cita o MR anterior e o próximo da corrente.
- Abrir na ordem, do primeiro ao último (o alvo de cada um precisa existir no remoto), todos com as mesmas flags (`--draft` etc.).
- Não dividir quando a mudança é pequena (acima), quando a branch já tem MR aberto (só atualizar, como no passo 4) ou quando os argumentos pedirem um MR só.
- **No BahCode**, cada MR da corrente é uma **task** do sub-terminal (sub-task + MR, no mesmo workspace). O MR da branch atual é a task 1, que o BahCode já acha sozinho; cada um dos outros vira uma task a mais. O pedido traz os comandos:
  - `'<binário>' extra-mr <feature> <pasta> <link do MR> --base <link do MR anterior da corrente> --subtask <KEY>`: rodar uma vez para cada MR que não é o da branch atual, na ordem da corrente. Omitir o `--base` no primeiro (ele sai da base da feature) e o `--subtask` quando não houver uma sub-task só daquela parte (a sub-task da task 1 não se repete).
  - `'<binário>' mr-base <feature> <link do penúltimo MR>`: depois, para gravar de qual MR sai o da branch atual (o último da corrente).
  - Ex. com 2 MRs: `extra-mr … <MR 1>` (sem `--base`), e `mr-base … <MR 1>`. Com 3: `extra-mr … <MR 1>`, `extra-mr … <MR 2> --base <MR 1>`, e `mr-base … <MR 2>`.

## 3. Branch e commits

- Se estiver na branch padrão ou em HEAD solto, criar a branch: `feat/<key do card>` (ou `fix/…`, conforme a natureza), ou `<tipo>/<breve-descricao>` sem card.
- Não commitar nada: o MR leva só os commits que já existem na branch. Se não houver nenhum commit à frente da base, não abrir o MR e avisar.
- `git push -u origin <branch>`.

## 4. Criar o MR

Na corrente (passo 2), repetir para cada MR. Se a branch já tem MR aberto (`glab mr list --source-branch <branch>`), não criar outro: atualizar a descrição se preciso e devolver o link.

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

## 5. Depois de abrir

- Mover no Jira (`transitionJiraIssue` pelo MCP do Atlassian) a sub-task do conjunto (a da task 1) e a de Desenvolvimento `[repo]` para *Pull Request*, só pelos status do fluxo (ignorar outros, como *Code Review*). Na corrente do BahCode, cada task a mais com `--subtask` tem a sua sub-task movida pelo próprio BahCode quando o MR dela abre (e concluída no merge); não mover a sub-task de uma task pelo MR de outra.
- Responder com o link de cada MR (na ordem da corrente), a branch alvo de cada um e o que foi movido no Jira.
