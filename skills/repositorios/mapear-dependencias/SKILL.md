---
name: mapear-dependencias
description: Mapeia as dependências de um repositório de ~/repositories na nota `dependencias-<repo>.md` do vault CTBZ - o que ele consome (outros repositórios com o contrato, libs internas, infra GCP, bancos e dados, terceiros) e quem o consome - gerando o levantamento automático de candidatos pelo código (nomes de outros repos, manifestos, catálogo infra/, grafo manual) e confirmando no código os que importam. Use quando o usuário pedir as dependências ou os consumidores de um repositório, perguntar "quem usa/chama X" ou "do que X depende", ao começar a trabalhar num repositório sem nota de dependências, ou antes de mudar um contrato (rota, tópico, tabela, evento) para saber quem quebra.
argument-hint: "<repo...> | --all [--print] [--refresh]"
---

# Mapear dependências de um repositório

Cada repositório com pasta no vault tem a nota `obsidian/repositories/<repo>/dependencias-<repo>.md` (padrão em `obsidian/padroes/dependencias-entre-repositorios.md`), linkada no índice do repo. Ela tem duas partes:

- **Consome** (Repositórios internos, Libs internas, Infra GCP, Bancos e dados, Terceiros) e **Consumido por**: o que foi **confirmado no código**, uma linha por contrato, mantido à mão pelos agentes conforme o trabalho no repositório confirma cada dependência.
- **Levantamento automático**, no fim, entre os marcadores `deps:auto`: os **candidatos** que o script desta skill acha. Ele reescreve só esse bloco e nunca toca no resto da nota.

## Rodar o levantamento

```sh
D() { python3 -I "$HOME/ctbz-vault/skills/repositorios/mapear-dependencias/scripts/deps.py" "$@"; }
D <repo>             # cria/atualiza a nota (e a linha no índice do repo; cria o índice se faltar)
D <repo> --print     # só mostra, sem gravar
D --all              # todos os repos que têm pasta no vault e clone em ~/repositories
D <repo> --refresh   # ignora o cache da varredura
```

Leva poucos segundos: a varredura de cada repo de `~/repositories` fica em cache em `~/.cache/repo-deps/` pela HEAD, e só os repos que mudaram são relidos. O cruzamento usa o código que está clonado, na branch em que está: repositório não clonado não aparece, e um clone velho dá um retrato velho (perguntar antes de dar `git pull` em repos com trabalho local).

O que o script levanta:

- **Repositórios que este cita** e **que citam este**: o nome de cada repo de `~/repositories` buscado como token no código versionado (`git grep -w`), com a contagem e até 3 exemplos `arquivo:linha` (código primeiro, depois teste e documentação). Repos de configuração, CI e documentação (gateway, configmaps, roles, pipeline, diagramas, coleções Bruno, o próprio BahCode) ficam numa linha à parte (`CONFIG_REPOS` no script). Nomes que são palavras comuns (`atalhos`, `pipeline`…) não são buscados como token (`STOP_NAMES`).
- **No grafo manual**: as arestas de `infra/grafo-chamadas-canais.md`.
- **Libs internas**: pacotes `@contabilizei*`/`@ctbz*` e dependências do GitLab da CTBZ nos manifestos (`package.json`, `pyproject.toml`, `requirements*.txt`, `go.mod`, `pom.xml`, `build.gradle`), com o repo que publica cada uma quando ele está clonado.
- **Infra GCP**: a seção do repo em `infra/por-repositorio.md` (catálogo da skill `atualizar-catalogo-gcp`) e os templates de CI incluídos no `.gitlab-ci.yml`.
- **Bancos e dados**: drivers e SDKs (Postgres, Prisma, Drizzle, Redis, BigQuery, Firestore, Pub/Sub…) e as tabelas `contabilizei-data`/`contabilizei-dataflow` citadas.
- **Terceiros**: SDKs (`THIRD_SDKS`) e hosts no código (`THIRD_HOSTS`): Zendesk, Meta, Ultimate, Jira, Slack, Google Chat, OpenAI, Anthropic, Gemini, Twilio, Sentry etc.

## Confirmar e levar para a parte de cima

O levantamento é ponto de partida, não verdade: citar um nome não diz se o repo chama, é chamado, só documenta ou só configura. Para cada candidato relevante ao trabalho em curso (ou todos, se o usuário pedir o mapa completo):

1. Abrir o `arquivo:linha` e achar o **contrato**: método e path da rota (ou o client HTTP e a variável de ambiente da base URL), o tópico/subscription e quem publica, a fila, a tabela, o webhook, a lib e o que dela é usado.
2. Escrever a linha na seção certa de **Consome**, no formato:
   `- \`<provedor>\`: <contrato> — por \`<arquivo do consumidor>\` (<nota do fluxo, se houver>)`
   Ex.: `- \`contato-service\`: \`POST /api/v1/optouts\` — por \`src/routes/api/proxy/contato-service.$.tsx\` ([[optout-tela-contato]])`.
3. **Espelhar no provedor**: na nota `dependencias-<provedor>.md` (rodar `D <provedor>` se ela não existir), em **Consumido por**, a linha `- \`<consumidor>\`: <contrato> — por \`<arquivo do consumidor>\``. As duas pontas sempre juntas: é o **Consumido por** que a revisão de MRs lê para achar quebra de fluxo dependente.
4. Infra e terceiros: dizer o papel (publica/consome o tópico, enfileira/recebe a task, lê/escreve a tabela, chama a API externa com qual credencial) e linkar a nota do catálogo ou do fluxo.
5. Trocar o `_Nada confirmado ainda._` da seção quando ela ganhar a primeira linha. Não copiar o levantamento inteiro para cima.

## Observações

- Não editar o bloco `deps:auto` à mão: ajustes de formato ou de detecção vão para o script (listas no topo: `CONFIG_REPOS`, `STOP_NAMES`, `THIRD_SDKS`, `THIRD_HOSTS`, `DATA_SDKS`).
- Repo novo no vault: o script cria a pasta e o índice no mesmo formato dos outros e a linha no `_repositories-indice.md`.
- O catálogo `infra/` tem data de geração própria (aparece no título da seção); se estiver velho, a skill `atualizar-catalogo-gcp` o atualiza.
