---
name: status-template-email
description: "Soft delete de templates de e-mail no admin: listagem por situação, ativar/inativar pelo detalhe e bloqueio de envio com template inativo"
metadata:
  type: project
tags:
  - atendimento-canais-admin
  - email-service
---

# Status (ativo/inativo) de template de e-mail

Contrato do email-service (feature "Soft delete de templates de e-mail", branches `feat/template-status-*`):

- Campo `status` (`active` | `inactive`) em todas as respostas de template, inclusive nos itens de `GET /api/v1/email-templates/list`.
- `PATCH /api/v1/email-templates/activate?id=` e `/inactivate?id=` (ou `?name=`), idempotentes, sem body; invalidam o cache de 1h do template no disparo.
- `GET /list?status=active|inactive`, padrão `active`; valor desconhecido dá 400.
- O template inativo só é recusado no **worker de validação**, depois do `POST /api/v1/send` responder 201. Por isso o admin confere o status antes de enviar.

No admin (branch `feat/email-template-status`):

- Tela `/notificacoes/email/templates`: ativos por padrão, `?situacao=inativos` na URL para os inativos. A rota do app sempre manda `status` para o upstream.
- Detalhe do template: pílula de status e botão Inativar (com `AlertDialog` de confirmação) ou Reativar.
- Listagem (branch `feat/email-template-inativar-listagem`): botão de inativar (ícone `Ban`) ao lado do Ver em cada linha ativa com id, mesma permissão `notificacoes.email.templates.status` e mesma confirmação do detalhe. Reativar continua só no detalhe. A mutation (atualiza o cache do template e invalida as listagens) fica em `-useAlterarStatusTemplate.ts` e o diálogo em `-ConfirmarInativacao.tsx`, usados pelos dois lugares. Rota do app: `PATCH /api/notificacoes/email-templates/status` com `{ id, status }`, log estruturado `email-template-status-alterado` com o autor.
- Envio: o modal desabilita o Enviar e avisa quando o template está inativo; a rota `POST /api/notificacoes/email-envios` busca o template antes e responde 409 `template_inativo`.
- O client lê status ausente como `active` (linhas antigas foram migradas para ativas).

Armadilha: na época, `importacao.arquivo.test.ts` (Windows-1252) já falhava no master, e o `vitest --coverage` não grava o relatório quando algum teste falha; usar `--coverage.reportOnFailure` para medir a cobertura mesmo assim.

## Permissões da área de e-mail (MR !186, encadeado no !185)

Uma chave por operação, concedidas por grupo do Keycloak ou e-mail em `/admin/acessos` (catálogo em `src/lib/auth/access-config.ts` + `access-config.json`, rótulos em `src/routes/admin/acessos/vocabulario.ts`):

- `notificacoes.email`: listar/consultar templates (nome mantido para não tirar o acesso de quem já tinha);
- `notificacoes.email.templates.criar`, `notificacoes.email.templates.status`: operações na tela de Templates (sem item de menu, em `NON_NAV_FEATURE_KEYS`);
- `notificacoes.email.envios`: tela e listagem de Envios;
- `notificacoes.email.envios.enviar`: enviar e subir anexo.

A consulta de um template aceita `notificacoes.email` ou a chave de enviar (`denyUnlessAnyFeatureAccess` em `src/server/middleware/require-feature.ts`), porque o formulário de envio a usa. As chaves novas nascem só com o master: depois do deploy, conceder em `/admin/acessos`.

Para testar componentes que usam `useHasFeature`, simular `#/lib/auth/use-feature` (sem router no teste, o `useRouterState` quebra).

## Auditoria (MR !187, encadeado no !186)

Criar, ativar/inativar e enviar gravam na trilha persistente (`registrarAuditoria`, coleção `auditoria`, tela `/admin/auditoria`), domínio `notificacoes-email`, ações `template.criado`, `template.inativado`, `template.reativado` e `envio.solicitado`. Módulo: `src/server/domains/shared/email-auditoria.ts`. Tentativas recusadas também entram (`bloqueado` = resposta do upstream, `erro` = integração; mesma divisão de `CODIGOS_OPERACIONAIS`). Do envio só as contagens de `descreverEnvio`, nunca destinatários nem variáveis. Antes disso só existia a linha de stdout (30 dias no `_Default`).

Nos testes de rota, simular `auditarEmail` com `importOriginal` (senão o teste tenta escrever no Firestore).

## Testes E2E (feitos em 2026-11-13)

Evidências por MR em PRD-177224 (sub-task de testes), um comentário por MR do admin (A1 !185, A2 !186, A3 !187), depois dos 4 do email-service; sub-task do !187 é a PRD-177327. Como montar o ambiente:

- **O `.env` local do admin aponta para o email-service de produção** (`EMAIL_SERVICE_BASE_URL=https://api.contabilizei.com.br/email-service`). Para testar, subir com as variáveis sobrescritas no ambiente (`EMAIL_SERVICE_BASE_URL=https://api-dev.contabilizei.com.br/email-service` e `EMAIL_SERVICE_API_KEY` com o `kong_token_bruno_dev` de `~/repositories/email-service/docs/bruno/.env`), sem editar o `.env`. O `PORT` da worktree vence o `--port 3000` do script `dev`.
- **Perfis de permissão locais**: `DEV_IMPERSONATE=true` (já no `.env`) liga o RBAC; `DEV_GUARDIAO="Nome:email"` e `DEV_GUARDIAO_GROUPS="/Grupo"` (sem o default Tech, que é master) definem a identidade. Conceder as chaves aos e-mails de teste só no `access-config.json` local, sem commit, um `vite dev --port 307x` por perfil.
- **Concessão gravada no Firestore substitui o baseline da chave** (`mergeFeaturePolicies`): em dev, `notificacoes.email` tem override com duas pessoas, então o e-mail de teste do JSON local leva 403. Para medir só o baseline, subir os perfis com `FIRESTORE_EMULATOR_HOST=127.0.0.1:9`: a leitura falha e o app cai no baseline (log `access-control-store leitura_falhou`). A auditoria desses perfis não grava; usar o perfil master (Firestore real) para testar a trilha.
- **SMTP de dev não entrega**: desde 28/05/2026 todo envio em dev fica FAILED com `421 The from domain should be a connected email sending domain` (HubSpot), qualquer remetente. O envio com template ativo passa pela validação e só cai no SMTP; serve para comparar com o bloqueio do inativo, que nem cria o envio.
- O `PATCH` idempotente (inativar o que já está inativo) também gera `template.inativado` na auditoria.
