---
name: jira-anexar-imagens-comentario
description: "Como anexar imagens locais (ex: evidências de teste) dentro de um comentário do Jira pelo MCP da Atlassian, sem token de API próprio: uploadAttachmentToJiraIssue (fase 1) + curl + addOrEditJiraIssueComment com inlineFileId"
metadata:
  type: reference
tags:
  - jira
  - evidencias
atualizado_em: 2026-11-09
---

# Anexar imagens em um comentário do Jira

Não há token da API do Jira no `.env`; o caminho é o MCP da Atlassian (`cloudId: contabilizeicontabilidade.atlassian.net`).

1. `discover` → `uploadAttachmentToJiraIssue`, rodado via `executeWrite` com `issueIdOrKey` e `filePath` (fase 1). Ele devolve um `uploadCommand` (curl para `api.media.atlassian.com`) e a `collection` (`upload-user-collection--<n>`).
2. O token do `uploadCommand` vale para a collection inteira (escopo `urn:filestore:upload:*`) por ~20 min: dá para reaproveitá-lo num loop, trocando só `name=` e `--data-binary @arquivo`, em vez de chamar a fase 1 por arquivo. Cada curl devolve o `data.id` (fileId).
3. Para embutir no comentário, **não** rodar a fase 2 (duplicaria o anexo): chamar `addOrEditJiraIssueComment` com `contentFormat: html`, `inlineFileId` (lista de ids, na ordem desejada), `inlineFileCollection` (um valor vale para todos) e `inlineFileName`. As imagens são anexadas ao final do corpo.
3b. Para deixá-los como anexos soltos da issue (lista de arquivos, sem embutir), rodar a fase 2 para cada fileId: `uploadAttachmentToJiraIssue` com `issueIdOrKey` e `fileId` (usado na PRD-175909 em 2026-11-09).
4. Para editar um comentário existente (ex: um que só tem o título "Testes em PRD"), ler antes com `listJiraIssueComments` em `responseContentFormat: html` e passar o corpo atual inteiro em `commentBody`, senão ele é substituído.

Usado em 2026-10-30 para as evidências de teste em produção da PRD-174797.
