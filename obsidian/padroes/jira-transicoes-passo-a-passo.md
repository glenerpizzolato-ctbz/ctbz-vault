---
name: jira-transicoes-passo-a-passo
description: "No Jira, o status de qualquer card muda uma transição por vez pelo workflow; inclui a regra de sub-task de código ser do tipo Desenvolvimento e como converter Subtarefa → Desenvolvimento"
metadata:
  type: reference
tags:
  - jira
  - workflow
atualizado_em: 2026-11-03
---

# Transições do Jira: uma por vez

Em **todos** os cards do Jira (PRD, rotina, PRC, sub-task etc.), a mudança de status tem que seguir o workflow, **uma transição por vez**: cada status só oferece as transições para os próximos passos, e não dá para pular direto para o status final (ex: de `To-do` para `Concluído`).

Como fazer pelo MCP do Atlassian:

1. Tentar a transição desejada com `transitionJiraIssue`; se ela não existir no status atual, o erro lista as disponíveis (`Available: ...` com nome e id).
2. Aplicar a próxima transição do caminho, ler as disponíveis no novo status e repetir até chegar no status final.
3. Usar o `transitionId` quando já se sabe o caminho, porque o nome é o da transição, não o do status de destino.
4. Já estar no status de destino conta como sucesso: listar as transições de um card que outro clique ou agente acabou de mover devolve só as do status novo, e a do destino some da lista.

## Caminhos conhecidos (projeto PRD)

- `Backlog` → `To-do`: depende do tipo do card. Em `Melhoria do produto` é `Priorizar` (id `501`); em outros tipos (ex: rotina) é `Detailed` (id `51`). De `Backlog`, a `Melhoria do produto` também oferece `Priorizar backlog` (741 → `Backlog Priorizado`) e `Enviar para o Backlog` (551).
- `Backlog` → `Building`: não há transição direta; passar por `To-do` e depois `Started` (61).
- `To-do` → `Building`: `Started` (id `61`). Ela exige **Story Points** (`customfield_10004`) preenchido: o campo aparece na tela da transição como não obrigatório, mas sem valor a transição é recusada. Passar em `fields` do `transitionJiraIssue` (`{"customfield_10004": 2}`) ou gravar antes com `editJiraIssue`; sem estimativa, 2 no card (1 na sub-task).
- `Aguardando Priorização` → `To-do`: `To-do` (id `341`); sub-tasks recém-criadas costumam nascer nesse status e não têm `Started` disponível antes disso.
- `Building` → `Pull Request`: `Gerar Pull Request` (id `331`). No mesmo ponto existe `Iniciar Revisão` (361 → `Code Review`), que não deve ser usada.
- `Building` → `Concluído`: `Finished` (id `121`). Outras saídas de `Building`: `Waiting` (171), `Para Validação` (201), `Aguardar Processamento` (211).
- `Ready for Release` → `Concluído`: `Released`.
- De qualquer status: `Archived` (151) e `Backlog` (191).

## Caminhos conhecidos (sub-task `Subtarefa` do projeto PRD)

- Ao criar, a sub-task oferece: `Backlog` (2), `Archived` (41), `To Do` (71) e `Executar` (21).
- Colocar em desenvolvimento: `Executar` (id `21`) leva direto para `Sendo feito`.
- A criação de `Subtarefa` também exige o campo **Assigned Squad** (`customfield_18419`, ex: `{"id": "68720"}` = Engenharia Canais); sem ele volta 400.

## Sub-task de código = `Desenvolvimento`

- Sub-task que envolve código é do tipo **`Desenvolvimento`** (id `21253`), não `Subtarefa` (id `5`); `Subtarefa` só para o que não é código nem teste. Preencher também `Quarter` (`customfield_21194`) e `Assigned Squad` na sub-task.
- Fluxo do `Desenvolvimento`: `To-do`, `Building`, `Pull Request`, `Code Review`, `Waiting Test`, `Ready to Test`, `Teste`, `Ready for Release`, `Concluído`, `Archived` etc. De `Concluído` volta para `To-do` com a transição `To-do` (id `341`).
- Converter `Subtarefa` → `Desenvolvimento`: `editJiraIssue` com `issuetype: {"id": "21253"}`. Só funciona se o status atual existir nos dois fluxos (`Concluído`, `Archived`); senão volta 400 "O tipo de item selecionado é inválido". Para uma sub-task em `Tarefas pendentes`: `Executar` (21) → `Finalizar` (31, vai para `Concluído`) → trocar o tipo → `To-do` (341) → `editJiraIssue` com `resolution: null` (a resolução fica "Itens concluídos" depois da volta).

Ex: concluir uma rotina em `To-do` = `Started` (61) e depois `Finished` (121). Ver também [[rotina-deploy-separada]]; nos PRCs, `Started` reatribui o card para quem a executou (ver `_prcs-indice`).
