---
name: testar-roteamento-n1-ativacao
description: Roda (e ensina) o teste do roteamento N1 Ativação do bot de WhatsApp (Ultimate) em prd - para cada cenário, põe o processo de abertura de teste no status do SOCI, confere o statusJira que o bot lê, pede ao Glener a mensagem no segundo :30 (fora do rollout da IA), confere o grupo do ticket no Zendesk contra o esperado, fecha o ticket sem CSAT e registra a evidência no Jira. Use quando o usuário pedir para testar/validar/fazer regressão do roteamento N1 Ativação por status do SOCI, conferir para qual grupo do Zendesk o bot manda um status, ou entender como testar esse fluxo.
argument-hint: "[cenários, ex: cadastro pre-cnpj mt | todos] [card de teste, ex: PRD-177631]"
---

# Testar o roteamento N1 Ativação (status do SOCI → grupo do ticket)

O bot de WhatsApp Expert/BP encaminha o cliente em ativação para um grupo do Zendesk conforme o status do processo de abertura (`statusJira`, lido do `ProcessoAbertura.status` da Abertura, achado pelo **telefone do sócio**). Esta skill valida esse mapa cenário a cenário em prd. Contexto e histórico: `~/ctbz-vault/obsidian/ultimate/testes-roteamento-n1-ativacao.md`, mapa completo em `ultimate/roteamento-n1-ativacao-soci.md`, receita genérica em `ultimate/testar-bot-whatsapp.md` e processos de teste em `ultimate/ativacao-processos-abertura-teste.md`.

## Regras fixas

- **O Claude não acessa o WhatsApp Web do Glener** (nem lê, nem envia por script, nem captura tela). Todo envio, resposta de CSAT e GIF é **pedido ao Glener**, e o Claude **aguarda a confirmação** no chat antes de seguir. O resultado é conferido pelo Zendesk.
- **Prd somente leitura para o Claude no banco**; escrita em banco de prd é montada e executada pelo usuário. As transições do SOCI (MCP do Jira), a Abertura (admin com SSO) e o Zendesk (requester de teste) são as escritas permitidas aqui, sempre nos processos de teste.
- **Nunca usar SOCI de cliente real** nem transições que disparam cards (FIN, PLA, CIT, Controle/Auditoria Pós CNPJ), `Solicita Reembolso` (fluxo real de cancelamento) ou `Em Stand-by` sem necessidade.
- Os tickets caem em **filas reais**: avisar o Glener e fechar cada ticket logo após conferir.
- Credenciais: gateway pela skill `buscar-empresas-por-telefone` (`bots_api.py`) e Zendesk pelo `.env` de `~/repositories/experts-bruno/zendesk-api` (via skill `fechar-tickets-teste-zendesk`). Nunca exibir valores.

## Dados fixos

- Telefone de teste: `+555596981032`. End-user do Zendesk: `21878313229212`, na org de testes `5405377070236`, cujas tags (`jira_finalizado`, `jira_não_finalizado`, `expert_essencial`…) entram em todo ticket; considerar isso ao ler o resultado.
- Bot: `+55 41 4101-0021` (`[prd] ctbz zendesk 41 41010021 main`).
- Processos de teste (Curitiba, "teste teste"): `SOCI-255767` → processo `4891157268267008`; `SOCI-255830` → processo `4550028081496064`. Com 2 processos no telefone, o bot usa o **primeiro** da contagem: deixar o telefone em um só por vez.

## Cenários

| # | Grupo esperado (id) | Status do SOCI a usar | Como chegar |
| --- | --- | --- | --- |
| 1 | Cadastro [Ativação] [Whatsapp] (`28283501432220`) | EM_ANALISE | de Iniciado |
| 2 | Pré CNPJ [Ativação] [Whatsapp] (`28283155272220`) | Aguardando Cliente | de Iniciado ou Ajuste de Fluxo |
| 3 | Pré CNPJ - Módulo tributário [Ativação] [WhatsApp] (`30023019944860`) | Processo Adm MT (ou Preenchimento MT, Ag Análise MT) | via Ajuste de Fluxo |
| 4 | Pré CNPJ - Assinatura JC [Ativação] [WhatsApp] (`30023034651676`) | Aguardando Protocolo | via Ajuste de Fluxo |
| 5 | Pós Vendas [Ativação] [Whatsapp] (`28283527238556`) | Iniciado | transição em loop "Atualizar Sistema" num processo em Iniciado (~75 s) |
| 6 | Atendimento [Ativação] [Whatsapp] (`5318551320604`) + tag `sys_grupo_ativacao_exp` (Experts) | Ajuste de Fluxo (fora do mapa → ELSE) | de Iniciado |
| 7 | Retenção Abertura [Ativação] [WhatsApp] (`29996619254940`) | Solicita Reembolso | **não testável em prd** sem aval da Abertura (exige campos do cancelamento real) |
| 8 | AIDA Geral [WhatsApp] [BP] (`22427993443100`) | Finalizado (BP) | **fora do caminho de processos**: `FINALIZADO` some da contagem; outro ramo (dados gerais da empresa) |
| 9 | Onboarding [Experts] (`5318567086108`) | Finalizado (Experts) | idem ao 8 |

Ajuste de Fluxo é um hub: dele se vai a EM_ANALISE, PENDENCIA, Aguardando Protocolo, Preenchimento MT, Ag Análise MT, Aguardando Formatura, Aguardando pagamento etc. Antes de transicionar, listar as transições do status atual (`listJiraIssueTransitions`, pelo `discover` do MCP do Atlassian) e escolher só as da tabela. Os cenários 7 a 9 são reportados como "não testado" com o motivo, salvo pedido explícito com outro caminho (ex: DEV).

## Preparação (uma vez por sessão)

1. **Telefone no processo**: conferir com `python3 scripts/processos_bot.py +555596981032`. Se a contagem vier `total: 0`, pedir ao Glener para logar no admin da Abertura (https://admin.contabilizei.com/abertura/sistema-admin/) no Chrome e, numa aba de `admin.contabilizei.com`, fazer `fetch` same-origin com `credentials: 'include'`: `POST https://appabertura.contabilizei.com/rest/admin/processoabertura/atualizar-telefone-socio-login` com `{"idProcessoAbertura": <id>, "telefone": "5596981032"}`; depois `GET /rest/admin/processoabertura/{id}`, trocar `atributos.soci__telefone` e `PUT /rest/admin/processoabertura`.
2. **Plano Experts**: `GET https://contabilizei-abertura.appspot.com/rest/public/processoabertura/carrega-dados-categoria-planos/{idProcesso}/EXPERT_ESSENCIAL` (sem auth). Plano BP (`AVANCADO`) vai direto para a AIDA Ativação BP e não passa pelos drops. A contagem deve listar o processo em `experts`.
3. **Ativo especial pendente**: se houver `mensagem_ativa` habilitada e válida para o telefone (`prd_crm_atendimento_zendesk`, `destino = '+555596981032'`), a conversa entra pelo retorno de ativo; consumir antes (cada uma abre um ticket a fechar).
4. Avisar o Glener que os tickets vão cair em filas reais.

## Ciclo por cenário

1. **Status**: transicionar o SOCI pelo MCP do Jira (`transitionJiraIssue`).
2. **Sincronização**: repetir `python3 scripts/processos_bot.py +555596981032 <idProcesso>` até o `statusJira` refletir (~30 a 75 s).
3. **Baseline**: `python3 scripts/zd_tickets.py 1` e anotar o último id.
4. **Pedir ao Glener**: perguntar se há CSAT pendente na conversa (ele encerra; o Claude nunca responde CSAT) e pedir que envie `Oi` ao bot com o relógio no **segundo :30**, para cair fora do rollout da IA de Ativação Experts (`ultimate/rollout-ia-ativacao.md`). Aguardar o "enviei". Se o bot disser "Seu atendimento anterior já foi finalizado…", pedir novo envio no próximo :30.
5. **Conferir**: `python3 scripts/zd_tickets.py 3 --since-id <baseline>` e comparar grupo e tags com a tabela. Atribuído à IA ("Contador Inteligente", `escalated_to_ai`) = caiu no rollout: repetir no :30.
6. **Fechar sem CSAT**: `python3 scripts/zd_fechar_sem_csat.py <ticketId>` (confere o requester e grava `sys_csat_survey_sent` + `sys_csat_response_exp` antes do `closed`).
7. **Evidência**: pedir o GIF ao Glener; se a lista de conversas aparecer, `python3 scripts/crop_gif.py <raw.gif> ~/Downloads/<final>.gif` e **conferir a folha `.sheet.png`** antes de subir. Comentar no card de teste: `uploadAttachmentToJiraIssue` (fase 1) → `curl` → `addOrEditJiraIssueComment` com `contentFormat: html` e `inlineFileId`, com status, grupo esperado, grupo obtido, ticket e OK/FALHOU.

## Fechamento

- Relatório em `~/Downloads/roteamento-n1-ativacao-<AAAA-MM-DD>.md`: tabela cenário → status → grupo esperado → grupo obtido → ticket → OK/FALHOU/não testado (com motivo).
- Rodar `fechar-tickets-teste-zendesk` (`list`) para garantir que não sobrou ticket aberto.
- Perguntar ao Glener se tira o telefone dele dos processos (voltar ao fictício `12985858585` nos quatro lugares: `empresa.socios[*].telefone`, `socioLogin.telefone`, `atributos.soci__telefone` e `[SOCI] Telefone` `customfield_19133`) e se volta o plano para `AVANCADO`.
- Registrar o resultado e qualquer armadilha nova em `ultimate/testes-roteamento-n1-ativacao.md`.

## Armadilhas

- Mudar `[SOCI] Telefone` ou o tipo de plano no Jira **não** reflete na Abertura: a sincronização copia só status e macro etapa.
- Jira e Abertura podem divergir; o bot lê a Abertura.
- A pesquisa CSAT chega minutos depois do `closed` se o ticket fechar sem as tags; a próxima mensagem vira resposta dela (ticket em "Experts CSAT - Respostas").
- Ticket de messaging com a conversa ainda ativa no bot não muda de status pela API: tentar de novo depois.
- Não deixar URL com query string na aba do claude-in-chrome ao usar o `javascript_tool` no admin da Abertura (a saída é bloqueada).
