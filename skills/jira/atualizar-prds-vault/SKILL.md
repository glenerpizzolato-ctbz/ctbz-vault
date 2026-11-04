---
name: atualizar-prds-vault
description: Sincroniza as demandas (PRDs) do vault Obsidian (ctbz/PRDs/) com o Jira — busca os últimos N cards criados pelo usuário ou atribuídos a ele (mais os que estão em backlog no vault), atualiza situação (backlog/pronto), título e datas, aponta cards novos, cancelados e divergências de épico, e regenera as visões, as notas de épico e os números. Use quando o usuário pedir para atualizar/sincronizar/conferir as PRDs ou demandas do vault com o Jira, ou perguntar se o status das demandas no vault está certo.
argument-hint: "[quantidade]"
---

# Atualizar as PRDs do vault a partir do Jira

O vault (`~/dotfiles/docs/ai/obsidian/ctbz/PRDs/`, uso e vocabulário em `_prds-indice.md`) é a fonte da verdade das demandas, mas a situação e as datas mudam no Jira. Esta skill traz o Jira para o vault. O script `scripts/prds.py` faz a parte mecânica (editar front-matter, recalcular período, regenerar visões); a busca no Jira é feita pelo MCP do Atlassian.

## O que é sincronizado

| Vault | Jira |
| --- | --- |
| `situacao` | status: concluído → `pronto`; qualquer outro → `backlog` |
| `titulo` (e o `# título` da nota) | `summary` |
| `data_inicio` | "Data de início" (`customfield_18225`) |
| `data_fim` | "Data Ready for Review" (`customfield_19224`) |
| `data_pronto` | "Data Ready for Release" (`customfield_19226`) |
| `data_referencia`, `periodo`, `mes` | recalculados: data de pronto, ou fim, início, teste; sem nenhuma, a criação do card |

Não são tocados: `tipo`, `atuacao`, `dominio`, `epico`, `data_teste` e as anotações da nota. As situações manuais (`arquivado`, `resolvido-outro-dev`, `esquecido`) são mantidas; o script só avisa quando o card ainda está aberto no Jira. Datas só são preenchidas ou corrigidas com o que o Jira tem, nunca apagadas.

## Passo a passo

1. **Definir N.** Usar o N que o usuário pedir; se não disser, usar 50.
2. **Listar o backlog do vault**, que sempre entra na busca, mesmo fora dos últimos N:

    ```bash
    python3 ~/.claude/skills/atualizar-prds-vault/scripts/prds.py backlog
    ```

3. **Buscar no Jira** com `searchJiraIssuesUsingJql` (cloudId da `contabilizeicontabilidade.atlassian.net`), paginando até N, com `fields: ["summary", "status", "parent", "created", "customfield_18225", "customfield_19224", "customfield_19226"]`:

    ```
    project = PRD AND issuetype not in subTaskIssueTypes() AND (reporter = currentUser() OR assignee = currentUser() OR key in (<chaves do backlog>)) ORDER BY updated DESC
    ```

    Se a lista do backlog vier vazia, tirar o `OR key in (...)`.

    O `assignee` traz também os cards criados por outra pessoa e atribuídos ao usuário (ex: o PO cria e atribui); sem ele, esses cards só seriam encontrados enquanto estivessem em backlog no vault.
4. **Gravar o resultado** num JSON no scratchpad, uma entrada por card (campos vazios podem ser omitidos):

    ```json
    [{"key": "PRD-170830", "summary": "…", "status": "Concluído", "parent": "PRD-165450", "created": "2026-10-08", "dates": {"data_inicio": "2026-10-08", "data_fim": "2026-10-09", "data_pronto": "2026-10-09"}}]
    ```

    `status` é o nome do status no Jira (o script trata "Concluído"/"Done"/"Resolvido"/"Fechado" como concluído e "Cancelado"/"Won't Do"/"Descartado" como cancelado). Se a resposta trouxer `statusCategory`, pode mandar `"statusCategory": "done"`.
5. **Aplicar:**

    ```bash
    python3 ~/.claude/skills/atualizar-prds-vault/scripts/prds.py apply <arquivo.json>
    ```

    O relatório tem as seções:
    - **atualizados**: o que mudou em cada nota.
    - **novos**: cards do Jira sem nota no vault. Não criar automaticamente: perguntar ao usuário quais entram (alguns são de outro dev ou não são demandas dele). Para os que entrarem, criar a nota seguindo o fluxo de PRDs do `CLAUDE.md` (front-matter das notas existentes; `tipo`, `atuacao` e `dominio` inferidos do card e do épico, confirmando com o usuário quando houver dúvida; nota do épico se não existir).
    - **cancelados**: cards cancelados no Jira; sugerir `arquivado` e só aplicar com o ok do usuário.
    - **manuais**: situação manual no vault com card ainda aberto no Jira; só informar.
    - **epico**: épico diferente entre vault e Jira; perguntar antes de mudar (mudar o `epico` da nota e, se preciso, criar a nota do épico).
6. **Regenerar as visões** (sempre, depois do `apply` e de criar ou editar notas à mão):

    ```bash
    python3 ~/.claude/skills/atualizar-prds-vault/scripts/prds.py rebuild
    ```

    Atualiza `_por-epico.md`, `_por-periodo.md`, `_por-dominio.md`, a seção "Demandas" e o front-matter (`dominio`, `periodos`, `qtd_demandas`) das notas de épico e os números do `_prds-indice.md`. Dentro de cada seção, a ordem é data de referência decrescente, com desempate pela chave. Épicos sem nenhuma demanda ficam como estão.
7. **Conferir e reportar:** `git -C ~/dotfiles diff --stat docs/ai/obsidian/ctbz/PRDs` e um resumo para o usuário: quantos cards foram conferidos, o que mudou de situação e as pendências (novos, cancelados, épicos divergentes).
8. **Commit** só com autorização do usuário, ex: `docs(obsidian): sync PRDs with Jira`.

## Quando mexer no script

- **Campo de data novo ou trocado no Jira:** ajustar a tabela acima, a lista de `fields` do passo 3 e o mapeamento no `apply` (`dates`).
- **Status novo no Jira** que signifique concluído ou cancelado: incluir em `DONE_STATUSES` ou `CANCEL_STATUSES`.
- **Mudança no formato das visões:** ajustar o `rebuild` e rodar uma vez para validar o diff antes de commitar.

O script vive em `~/dotfiles/docs/ai/skills/ctbz/jira/atualizar-prds-vault/` (versionado no dotfiles) e chega em `~/.claude/skills/` por symlink (`./installers/setup.sh --symlinks`). Editar sempre a versão do repositório.
