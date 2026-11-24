---
name: ativacao-processos-abertura-teste
description: "Processos de abertura de TESTE em prd (SOCI-255767 e SOCI-255830) para testar fluxos de Ativação da Ultimate (roteamento por status do SOCI), como apontar o telefone do sócio para o seu e consultar pelas rotas do bot"
metadata:
  type: reference
tags:
  - ultimate
  - ativacao
  - abertura
  - testes
---

# Ativação: processos de abertura de teste em prd

Conseguidos pelo Glener em 2026-11-16. Use-os para testar fluxos de Ativação no bot WhatsApp (ex: [[testes-roteamento-n1-ativacao]]). São cadastros de teste ("teste teste", e-mails descartáveis, pagamento CANCELADO), não clientes reais.

| SOCI | ID do processo (Abertura) | Status no Jira | Status na Abertura (`statusJira`) | Plano | CNPJ |
| --- | --- | --- | --- | --- | --- |
| [SOCI-255767](https://contabilizeicontabilidade.atlassian.net/browse/SOCI-255767) | `4891157268267008` | Iniciado | Iniciado | AVANCADO | — |
| [SOCI-255830](https://contabilizeicontabilidade.atlassian.net/browse/SOCI-255830) | `4550028081496064` | Iniciado | Download Certidão (Auto) | AVANCADO | 20881819000112 |

Situação em 2026-11-16, antes de qualquer alteração (em 2026-11-17 o seu telefone foi removido; ver "Tirar o seu telefone dos processos"). Os dois são de Curitiba/PR, com CPF responsável `21383198063`.

- **Link direto do processo no admin:** `https://app.contabilizei.com/abertura/sistema-admin/#/processo/<idProcesso>` (é o "Link Plataforma" que a automação grava no SOCI).

## Armadilhas

- **Plano AVANCADO, não Experts:** a rota de contagem separa por `plano`. Esses processos entram em `basicoPadraoMultibeneficios`, não em `experts`. Para testar o fluxo Experts, o plano do processo provavelmente precisa ser trocado para um Experts.
- **Jira e Abertura podem divergir:** o SOCI-255830 está "Iniciado" no Jira e "Download Certidão (Auto)" na Abertura. O bot lê a **Abertura**. Para testar, mude o status do processo na Abertura (`PUT /rest/admin/processoabertura`), não só no Jira.
- Status `FINALIZADO` some da contagem (ver [[roteamento-n1-ativacao-soci]]).

## Mudar o status pelo Jira (testado em 2026-11-16)

- **Funciona pelo MCP do Jira:** transicionar o SOCI (`transitionJiraIssue`) chega à Abertura em **~30 a 60 s**, pelo webhook `sincronizar/jira-abertura` (`JiraSyncService.atualizarProcessoApartirJira`). Teste: SOCI-255767 Iniciado → EM_ANALISE às 15:48; a rota de dados do bot já mostrava `EM_ANALISE` às 15:49.
- A transição Iniciado → EM_ANALISE marca `enviarEmailCadastro` (e-mail de cadastro para o e-mail do processo, que nesses testes é descartável).
- Só dá para ir aos status que o fluxo do SOCI oferece a partir do status atual (`listJiraIssueTransitions`). A partir de Iniciado: EM_ANALISE, Aguardando Cliente, Em Stand-by, Solicita Reembolso, Refazer, Ajuste de Fluxo. As outras voltam para Iniciado e criam cards (FIN, PLA, Controle/Auditoria Pós CNPJ): evitar.
- **A sincronização copia só o status e a macro etapa.** Editar o campo `[SOCI] Telefone` (`customfield_19133`) no Jira **não** muda o telefone na Abertura. O bot acha o processo pelo telefone do sócio na Abertura, então a contagem continua 0.

## Trocar o plano do processo (testado em 2026-11-16)

- O plano que o bot lê é `ProcessoAbertura.categoriaPlano`. **Mudar o "Tipo de plano de pagamento" no Jira não reflete**, porque a sincronização Jira → Abertura copia só o status. O admin da Abertura também não tem esse campo.
- Rota pública da Abertura, sem autenticação: `GET https://contabilizei-abertura.appspot.com/rest/public/processoabertura/carrega-dados-categoria-planos/{idProcesso}/{plano}` (`ProcessoAberturaService.atualizarDadosPlanos`, só faz `setCategoriaPlano` e salva). Valores: `EXPERT_ESSENCIAL`, `EXPERT_PRO`, `AVANCADO`, `BASICO`… O bot classifica como Experts quando o plano contém `EXPERT`.
- Teste: processo `4891157268267008` AVANCADO → `EXPERT_ESSENCIAL` (HTTP 200); a contagem passou a listá-lo em `experts`. Para voltar: mesma rota com `AVANCADO`.

## Apontar o telefone do sócio para o seu

- **Tela do admin da Abertura (caminho preferido):** https://admin.contabilizei.com/abertura/sistema-admin/#/processosabertura. Lá se busca o processo e se edita sócio, telefone, plano e status, com o login SSO de operador. Em 2026-11-16, o telefone do Glener foi gravado direto no banco pelo time da Abertura.

- Rota da Abertura: `POST https://contabilizei-abertura.appspot.com/rest/admin/processoabertura/atualizar-telefone-socio-login?auth_token=<token>` com `{"idProcessoAbertura": <id>, "telefone": "<DDD+número, 10-11 dígitos, sem 55>"}`. Ela troca o telefone do `socioLogin` do processo e salva pela aplicação, então o cache do Objectify fica coerente.
- **Autenticação (testado em 2026-11-16):** as rotas `/rest/admin/*` exigem a **sessão SSO de operador** (`AuthFilter` + `RequestSSOUserFilter`), a mesma do admin da Abertura (`contabilizei-abertura-front-admin`). O `auth_token` de integração da coleção Bruno dá **401**, e sem sessão o `GET /rest/admin/processoabertura/{id}` em `appabertura.contabilizei.com` também dá 401. Chamar `/rest/public/requestloginadmin` direto dá "erro interno": o login começa pelo front-admin. Caminho: o usuário loga no admin da Abertura no Chrome e o Claude faz `fetch` same-origin em `https://appabertura.contabilizei.com/rest/admin/...` com `credentials: 'include'`.
- Outras rotas úteis do admin: `GET /rest/admin/processoabertura/{id}` (processo completo) e `PUT /rest/admin/processoabertura` (salva o JSON alterado: `status`, `categoriaPlano`…). Ao usar o claude-in-chrome, não deixar URL com query string na aba, porque a saída do `javascript_tool` é bloqueada.

## Tirar o seu telefone dos processos (feito em 2026-11-17)

- Em 2026-11-17 o telefone do Glener (`5596981032`) foi **removido dos dois processos**, voltando ao valor original do cadastro de teste, **`12985858585`** (fictício, conferido no histórico de `[SOCI] Telefone` dos dois SOCIs). Para testar de novo, apontar o telefone outra vez (seção acima).
- O telefone fica em quatro lugares: `empresa.socios[*].telefone` (o que o bot busca), `socioLogin.telefone`, `atributos.soci__telefone` e o campo `[SOCI] Telefone` (`customfield_19133`) do SOCI.
- Passo a passo que funcionou, com o usuário logado no admin da Abertura e `fetch` same-origin numa aba de `admin.contabilizei.com`: `POST https://appabertura.contabilizei.com/rest/admin/processoabertura/atualizar-telefone-socio-login` com `{"idProcessoAbertura": <id>, "telefone": "<novo>"}` troca `socioLogin` **e os sócios da empresa que tinham o mesmo número** (no SOCI-255830 o 2º sócio também ficou `12985858585`, que já era o dele); depois `GET /rest/admin/processoabertura/{id}`, trocar `atributos.soci__telefone` e `PUT /rest/admin/processoabertura` com o JSON (o PUT grava os atributos; o status não muda); por fim editar o `customfield_19133` do SOCI pelo MCP do Jira.
- Conferência: contagem do bot para `+555596981032` e `+5555996981032` voltou `total: 0`.

## Consultar como o bot

Rotas do `atendimento-zendesk` pelo gateway, com as credenciais da skill `buscar-empresas-por-telefone` (`scripts/bots_api.py`, `credentials('prd')` + `gateway_headers`), via **GET**:

- `/atendimento/zendesk/bots/whatsapp/fluxo/interacao/api/v1/bots/whatsapp/identificacao/processos/contagem/{+55telefone}`
- `/atendimento/zendesk/bots/whatsapp/fluxo/interacao/api/v1/bots/whatsapp/identificacao/processos/dados/{idProcesso}/telefone/{+55telefone}`

A rota de dados não confere se o telefone é do processo: só valida o formato, e o `idProcesso` manda.

## Pôr o processo num status que o fluxo do SOCI não alcança (avaliado em 2026-11-16)

- **Pelo Jira não dá para voltar a Iniciado, NAO_INICIADO ou Pós Vendas.** No histórico de SOCIs reais (ex: SOCI-575144), `NAO_INICIADO` é o status de criação e `Iniciado` só vem dele, quando o cliente começa o cadastro. Depois disso o fluxo segue em frente (EM_ANALISE → Aguardando Confirmação → …). O MCP não expõe o desenho do workflow: o caminho se descobre pelas transições do status atual (`listJiraIssueTransitions`) e pelo changelog de SOCIs reais.
- **Solicita Reembolso** exige campos do fluxo real de cancelamento. Preencher dispara o processo de reembolso/retenção: só com aval do time da Abertura.
- **Sem rota pública para o status na Abertura:** a rota pública "atualizar dados do Jira" grava em `atributos` (`setAtributo`), não no campo `status`. O webhook público `sincronizar/jira-abertura` relê o status real da issue no Jira, então não dá para forjar.
- **Testado e NÃO funciona para status (2026-11-16):** o `PUT /rest/admin/processoabertura` com a sessão SSO salva o processo, mas **ignora o campo `status`** (devolveu o status anterior; a tela do admin também não tem campo de status, que vem do Jira). O status do processo só muda pela transição do SOCI no Jira. A API de admin é `https://appabertura.contabilizei.com/rest/admin/...`; chamá-la de uma aba em `admin.contabilizei.com` com `fetch(..., {credentials:'include'})` funciona com o usuário logado.
- ~~Caminho que funciona:~~ `GET` + `PUT /rest/admin/processoabertura` com a **sessão SSO de operador**, pela tela do admin (https://admin.contabilizei.com/abertura/sistema-admin/#/processosabertura) ou por `fetch` same-origin com o usuário logado no Chrome. Isso grava o `status` direto na Abertura, que é o que o bot lê. O Jira fica diferente até o próximo evento da issue, que volta a sincronizar a partir do Jira.

- **Para Pós Vendas / Iniciado:** usar um SOCI que ainda esteja em `Iniciado` no Jira (ex: SOCI-255830, processo `4550028081496064`): uma transição em loop (ex: "Registro de Follow" → Iniciado) dispara o webhook e grava `Iniciado` na Abertura. Falta apontar o telefone do sócio desse processo para o de teste (aba Sócios do admin ou time da Abertura) e trocar o plano para Experts (rota pública `carrega-dados-categoria-planos`).
