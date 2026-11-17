---
name: empresa-teste-bp-ativa
description: "Empresa de testes BP ativa em prd (CNPJ 51596322000186, plano AVANCADO) ligada ao telefone de teste do Glener: para testar no bot WhatsApp os fluxos de cliente com empresa ativa (Journey router), com os campos de autenticação que o bot recebe"
metadata:
  type: reference
tags:
  - ultimate
  - testes
  - bp
---

# Empresa de testes BP ativa (prd)

- **CNPJ `51596322000186`**: empresa de testes BP **ativa** em prd, plano `AVANCADO`. Em 2026-11-17 o Glener adicionou a ela o telefone de teste (`+555596981032`). Com isso, o `buscar-por-telefone` do bot passou a listar 1 empresa em `basicoPadraoMultibeneficios`.
- O mesmo CNPJ também existe em **dev** como empresa Experts SN do grupo 3 do agrupamento de guias ([[notificacao-agrupamento-experts-bp-lp]]). Os ambientes são diferentes e os dados também.
- Campos que o bot recebe em prd (`bots_api.py telefone-cnpj +555596981032 51596322000186 --env prd`, 2026-11-17): `status = ATIVO`, `categoriaPlano = AVANCADO`, `abertura = true`, `jiraFinalizado = true`, `jiraStatus = Finalizado`, `idProcesso = null`. No `Journey router v09` ([[testes-roteamento-bp-n1-n2]]), isso leva à AIDA Geral [WhatsApp] [BP] (cenário B2).
- Para os cenários de abertura não finalizada (B1) ou migração (B3), é preciso mudar `abertura`/`jiraFinalizado` da empresa ou usar o impersonate do `bots-api` (ver a nota de testes).
- Teste pelo WhatsApp: receita em [[testar-bot-whatsapp]]. Com o telefone ligado a uma empresa, o bot vai para o fluxo de cliente com empresa (autenticação → Journey router), e não para o de processo de abertura.

## Como mudar `abertura` e `jiraFinalizado` (levantado em 2026-11-17)

Os campos ficam na entidade `Empresa` (`contabilizei-back-core/.../model/Empresa.java`: `abertura` l.180, `jiraFinalizado` l.303, `dataJiraFinalizado` l.305). A entidade tem `@Cache` do Objectify de 24 h. Os dois campos só são gravados por código; não há tela de admin que os edite.

- **`jiraFinalizado = true`:**
  - Webhook do Jira (`POST /rest/precadastro/abertura/public/atualizar-flag-jira-finalizado` no monolito, só para FINALIZADO/FINALIZAR/FINALIZADO_B_A).
  - `PUT /rest/empresa/atualizarStatusJira/{cnpj}` ou o botão "Não finalizado" do admin: só marca `true` se o Jira estiver finalizado de fato.
  - `GET /rest/empresa/{id}/finalizar-jira` (monolito, `EmpresaFacade.finalizarJira`): marca `true` e a data atual sem consultar o Jira.
  - Job de notificação de notas no `plataforma-back-worker`.
- **`jiraFinalizado = false`:** só `POST /ativacao/jira/body` no `plataforma-web` (`AtualizarEmpresaFinalizadaService`, text/plain com os CNPJs separados por vírgula).
- **`abertura`:** gravado na criação da empresa (`true` para abertura, `false` para migração). Depois disso, só o `POST /rest/admin/view/empresa/salvar` aceita `"abertura"`, mas ele refaz o cadastro inteiro (sócios, ramos, plano, notificações): arriscado. Fora isso, só update direto na entidade.
- **Cache:** quem grava pelo DAO limpa o cache do Objectify. Edição direta no Datastore não limpa, e o bot pode ver o valor antigo por até 24 h (`PUT /rest/empresa/resave/{idEmpresa}` força o resave). O `plataforma-crm-web` não tem cache próprio para esses campos.

## Impersonate (`bots-api` + Ultimate)

- `bots-api` (`src/domain/ultimateai/impersonate/impersonate.router.ts`): `PUT /ultimate-ai/v1/impersonate` `{cnpj, telefone}` grava no Redis `ultimate-ai:impersonate:<telefone>` **sem TTL**; `GET` (header `x-bots-api-telefone`) devolve `{cnpj, telefone, impersonating}`; `DELETE` apaga. As rotas não têm autenticação. Há coleção Bruno em `docs/bruno/ultimate-ai/impersonate/`. O `bots-api` não chama o CRM: só guarda o par.
- Na Ultimate: `Wpp Shared | Id Empresa Count` (`6a996986d7cec5465398a561`) chama `[bots-api] GET | impersonate - Shared` (variáveis `CNPJ_IMPERSONATE`, `IMPERSONATING`). Com `IMPERSONATING = true`, roda a ação `[SET] CNPJ IMPERSONATE` (põe o CNPJ da sessão) e vai para `Pointer | Id Empresa Auth - Wpp Shared`, que chama `[pltf-crm] GET | consulta CNPJ - Shared` **só com o CNPJ** (não usa o telefone). Por isso todos os campos de autenticação (`possuiAcesso*`, `aberturaEmpresa`, `jiraFinalizado`, plano, assessor) vêm **reais do CRM para o CNPJ impersonado**. O impersonate pula só o vínculo telefone ↔ empresa; os dados não são inventados nem fixos.
- Não dá para forçar campos: o estado vem da empresa real. Para testar um estado, é preciso impersonar uma empresa que já esteja nele.
