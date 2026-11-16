---
name: processo-abertura-teste
description: "Como criar e manipular um processo de abertura de teste (dev e prd): Admin IS/pré-cadastro cria o processo e o SOCI; admin da Abertura atualiza status; o que não funciona (SOCI criado à mão)"
metadata:
  type: reference
tags:
  - contabilizei-abertura
  - testes
---

# Processo de abertura de teste

Levantado em 2026-11-16 para testar o roteamento N1 Ativação por status do SOCI ([[roteamento-n1-ativacao-soci]]). Não há passo a passo completo e validado; o que existe:

- **Criação:** o processo nasce no pré-cadastro (`contabilizei-precadastro`) e na Abertura, que cria a issue SOCI (`JiraService.createIssue`) e grava o `idJira` no `ProcessoAbertura`. A doc do pré-cadastro (base de conhecimento, `contabilizei-precadastro/documentacoes/DASHBOARD.md`) manda **fazer um cadastro pelo Admin IS (`contabilizei-leads-front-admin`) em dev ou prod** e depois acessar o dashboard ([dev](https://contabilizei-precadastro-teste.appspot.com/cadastro/#/dashboard), [prod](https://cadastro.contabilizei.com.br/cadastro/#/dashboard)) com o CPF cadastrado. O BFF é o `contabilizei-leads-back` (time de Aquisição); a abertura entra por `rest/auth/processoabertura/`.
- **SOCI criado à mão no Jira não serve:** não há `ProcessoAbertura` nem empresa/sócio na Abertura, então as rotas por telefone não o encontram e o `JiraSyncService` não sincroniza.
- **Vínculo com o telefone:** as rotas `integracao/twilio/processo/telefone/{telefone}` buscam empresas da Abertura cujo **sócio** tem o telefone (`empresaDAO.getByManyTelefonesSocio`). O telefone de teste precisa estar no sócio do processo.
- **Atualizar status sem mexer no Jira:** a Abertura tem `PUT /rest/admin/processoabertura` (web) com o JSON completo do processo (`status`, `idJira`, passos…) e, no worker, `POST /worker/rest/admin/processoabertura/sincronizar/abertura-jira/{idProcesso}` (processo → Jira) e `POST .../sincronizar/jira-abertura` (Jira → processo). Exemplos de dev na coleção Bruno `~/repositories/experts-bruno/contabilizei-abertura/Atualiza campos abertura-Jira Soci/` (host `contabilizei-abertura-teste`). Em prod são escritas em dado real: só com o processo de teste e aval do time da Abertura.
- **Consultar:** `~/repositories/experts-bruno/contabilizei-abertura/integracao/tw/processo/{telefone}.bru` e `processo-id.bru` (Abertura direto) e `ultimate-ai-bots/bots/wpp-main/id_abertura/` (rotas do `atendimento-zendesk` pelo gateway, como o bot chama).
- As evidências da Entrega 02 (PRD-157558) não registram como o teste foi feito.

## Admin da Abertura

- Tela de processos: https://admin.contabilizei.com/abertura/sistema-admin/#/processosabertura (`contabilizei-abertura-front-admin`, login SSO de operador). Use para editar processo de teste (telefone do sócio, plano, status) sem chamar `/rest/admin/*` à mão. Processos de teste prontos: [[ativacao-processos-abertura-teste]].

## Criar processo por REST (verificado em 2026-11-16)

- **A Abertura não tem rota de criação.** As rotas `auth/processos-abertura` (`/{cpf}`, `/todos/{cpf}`) só consultam; as de `admin/processoabertura` só atualizam, sincronizam, transicionam (`/{id}/{nomeTransicao}`), arquivam ou reindexam processos que já existem.
- A criação é do **pré-cadastro** (`contabilizei-precadastro`, `rest/auth/processoabertura/`), chamado pelo `contabilizei-leads-back` (BFF do Admin IS e do Checkout), ambos do time de Aquisição. Nenhum dos dois estava clonado em `~/repositories`, não há coleção Bruno deles, e as rotas exigem usuário SSO com perfil de vendas/pré-cadastro.
- Para mudar o status de um processo existente: `PUT /rest/admin/processoabertura` com o token SSO da coleção `experts-bruno/contabilizei-abertura` (em prd, só montar e o usuário executa).
- Caminhos quando o Admin IS não funciona: descobrir o erro na plataforma; clonar `contabilizei-leads-back`/`contabilizei-precadastro` para mapear a rota e o payload; ou pedir o processo de teste ao time de Aquisição/Abertura. Contato de tecnologia da Abertura: [[abertura|informed captain da Abertura]] (Alessandro Voigt Cigoline).
