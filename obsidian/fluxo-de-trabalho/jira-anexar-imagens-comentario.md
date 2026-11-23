---
name: jira-anexar-imagens-comentario
description: "Como documentar evidências de teste no Jira: um comentário por cenário (mais um de resumo), cada imagem inline logo abaixo do texto que a cita (nunca tudo como anexo no fim), pelo MCP da Atlassian (uploadAttachmentToJiraIssue fase 1 + curl + nó media-single no HTML)"
metadata:
  type: reference
tags:
  - jira
  - evidencias
atualizado_em: 2026-11-12
---

# Anexar imagens em um comentário do Jira

## Regra (pedido do Glener, 2026-11-12)

Ao documentar um relatório de teste (E2E, regressão) numa sub-task do Jira:

- **Um comentário por cenário** (C0, C1…), mais um comentário de **resumo** antes deles (contexto, regra testada, massa, tabela cenário × resultado, pendências e limpeza). Publicar na ordem, para os comentários ficarem em sequência.
- Cada comentário de cenário traz **Passos**, **Esperado** e **Resultado**, e a imagem da evidência vai **inline, logo depois da frase que a cita** (nó `<figure data-type="media-single">` no ponto exato, ver abaixo), com `figcaption` dizendo o que ela mostra.
- **Nunca** jogar o texto e todos os arquivos só como anexos no fim do comentário (nada de `inlineFileId`, que anexa no final, nem fase 2 do upload).
- Evidência em texto (log, `psql`, JSON) vira imagem legível: uma imagem por cenário com uma tabela-resumo (tipo, dados de entrada, decisão, resultado ✔/✘) e, abaixo, o log e a consulta de cada envio (receita no fim desta nota). Tokens sempre mascarados.
- Cenário não executado também ganha comentário, explicando por que e onde ele está coberto.

Feito assim na PRD-176998 (testes E2E da PRD-176996, 2026-11-12): 1 resumo + 11 cenários, 11 imagens.

## Como subir

Não há token da API do Jira no `.env`; o caminho é o MCP da Atlassian (`cloudId: contabilizeicontabilidade.atlassian.net`).

1. `discover` → `uploadAttachmentToJiraIssue`, rodado via `executeWrite` com `issueIdOrKey` e `filePath` (fase 1). Ele devolve um `uploadCommand` (curl para `api.media.atlassian.com`) e a `collection` (`upload-user-collection--<n>`).
2. O token do `uploadCommand` vale para a collection inteira (escopo `urn:filestore:upload:*`) por ~20 min: dá para reaproveitá-lo num loop, trocando só `name=` e `--data-binary @arquivo`, em vez de chamar a fase 1 por arquivo. Cada curl devolve o `data.id` (fileId).
3. Para embutir no comentário, **não** rodar a fase 2 (duplicaria o anexo): chamar `addOrEditJiraIssueComment` com `contentFormat: html`, `inlineFileId` (lista de ids, na ordem desejada), `inlineFileCollection` (um valor vale para todos) e `inlineFileName`. As imagens são anexadas ao final do corpo.
3b. Para deixá-los como anexos soltos da issue (lista de arquivos, sem embutir), rodar a fase 2 para cada fileId: `uploadAttachmentToJiraIssue` com `issueIdOrKey` e `fileId` (usado na PRD-175909 em 2026-11-09).
4. Para editar um comentário existente (ex: um que só tem o título "Testes em PRD"), ler antes com `listJiraIssueComments` em `responseContentFormat: html` e passar o corpo atual inteiro em `commentBody`, senão ele é substituído.

Usado em 2026-10-30 para as evidências de teste em produção da PRD-174797.

## Posicionar as imagens no meio do texto e gerar imagem a partir de evidência em texto

- Para colocar cada imagem num ponto exato do comentário (e não só no final), não usar `inlineFileId`: escrever no `commentBody` HTML o nó `<figure data-type="media-single" data-layout="center" data-width="90" data-width-type="percentage"><div data-type="media" data-media-type="file" data-id="<fileId>" data-collection="<collection>" data-alt="x.png"></div><figcaption>…</figcaption></figure>`. Arquivo não-imagem (ex: zip com as evidências brutas) entra como `<div data-type="media-group"><div data-type="media" …></div></div>`. Os dois viram anexos da issue automaticamente (sem fase 2). Sem `data-width-type="percentage"` a imagem fica minúscula.
- Quando as evidências são só texto (saídas de `psql`, logs, JSON), dá para gerar PNG legível montando um HTML com tabela/`<pre>` e tirando screenshot com `google-chrome --headless=new --no-sandbox --hide-scrollbars --user-data-dir=<tmp> --window-size=1400,4000 --screenshot=out.png file://…html`, depois cortar a sobra branca com PIL (`ImageChops.difference(...).getbbox()`). Usado em 2026-11-11 no card de teste E2E PRD-176514.
