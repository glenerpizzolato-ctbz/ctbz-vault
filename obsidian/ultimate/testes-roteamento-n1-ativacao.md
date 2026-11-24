---
name: testes-roteamento-n1-ativacao
description: "Como testar o roteamento N1 Ativação por status do SOCI (Entrega 03, PRD-177631): plano por grupo, o que impede testar em prd com o WhatsApp do usuário, caminhos avaliados e regras de segurança (banco prd, Zendesk prd, SOCI de cliente real)"
metadata:
  type: project
tags:
  - ultimate
  - testes
  - abertura
jira: https://contabilizeicontabilidade.atlassian.net/browse/PRD-177631
---

# Testes do roteamento N1 Ativação (Entrega 03)

Sessão de 2026-11-16. O ajuste da Entrega 03 ([[PRD-176172]]) foi publicado em prd pelo Glener no dialogue builder da Ultimate (bot `[prd] ctbz zendesk 41 41010021 main`). A sub-task de testes é o PRD-177631. Mapa, diff e origem do `statusJira`: [[roteamento-n1-ativacao-soci]].

> [!TIP]
> Desde 2026-11-24 o teste é a skill `testar-roteamento-n1-ativacao` (`~/ctbz-vault/skills/ativacao/`), com a tabela dos 9 cenários, a preparação, o ciclo e os scripts.

## Escopo combinado

- **Um cenário por grupo**: Cadastro, Pós Vendas, Pré CNPJ, Pré CNPJ - Módulo tributário, Pré CNPJ - Assinatura JC, Retenção Abertura, Finalizado BP (AIDA Geral [BP]), Finalizado Expert (Onboarding [Experts]) e ELSE (Atendimento). São 9 cenários.
- Fluxo planejado: pôr o processo de teste no status → conversar com o bot (hoje: o Glener envia e o Claude aguarda; o Claude não acessa mais o WhatsApp Web, ver [[testar-bot-whatsapp]]) → conferir o grupo do ticket → print e referência → comentar a evidência no PRD-177631.
- Execução em prd: o Claude **monta** as escritas (SQL, chamadas admin) e o **usuário executa** (`! psql ...`), conforme a regra de prd somente leitura do CLAUDE.md.

## O que descobrimos (e que mudou o plano)

- **Mock no `prd_issue_ticketing` não serve**: o bot não lê o `ticketing-service`. O `statusJira` vem do `ProcessoAbertura.status` (Datastore da Abertura), e o processo é achado pelo **telefone do sócio** ([[roteamento-n1-ativacao-soci]]).
- **O telefone do usuário não está ligado a nenhum processo de abertura**, então o bot nunca chega no roteamento por SOCI com ele.
- **SOCI de cliente real não pode ser usado**: o SOCI-562684 (cliente real, Finalizado) só tem 1 transição que muda de status; as outras disparam cards FIN/PLA/CIT e outras ações reais. A mudança ainda vai para a Abertura pelo `JiraSyncService`.
- **SOCI criado à mão no Jira não serve**: sem `ProcessoAbertura` e sem sócio na Abertura, o endpoint de contagem não o encontra.
- **Finalizado não passa pela rota de processos**: a contagem descarta processos `FINALIZADO`. Os cenários AIDA [BP] e Onboarding [Experts] dependem de outro ramo do fluxo (dados gerais da empresa no `plataforma-crm-web`, com cache de 3 h por `idProcesso` e `null` quando a empresa não é tratada como abertura). Falta confirmar no dialogue builder qual ramo leva ao drop de Finalizado.
- **Não há rota REST de criação de processo na Abertura**; quem cria é o pré-cadastro, pelo Admin IS ([[processo-abertura-teste]]). O usuário não conseguiu criar pela plataforma.

## Caminhos avaliados

| Caminho | Situação |
| --- | --- |
| A) DEV: Abertura dev + bot dev + Zendesk sandbox | recomendado para os 9 cenários; sem risco |
| B) prd com processo de teste (`[TESTE TI, NAO MEXER]`), status mudado via `PUT /rest/admin/processoabertura` | escolhido pelo usuário; travado na criação do processo |
| C) prd sem escrita: conferir tickets reais do N1 Ativação (BigQuery/logs) contra o status do processo | complemento pós-virada |

Próximo passo em aberto (2026-11-16): conseguir o processo de teste em prd com o CPF e o telefone do Glener, via [[abertura|informed captain da Abertura]] (Alessandro Voigt Cigoline) ou time de Aquisição.

## Regras e armadilhas da sessão

- Prd somente leitura para o Claude, mesmo a pedido; escrita em prd sempre executada pelo usuário.
- Zendesk de prd: a nota [[zendesk-sunco-prod-politica]] pede que IA não acesse API nem navegador do Zendesk de prd. Nesta sessão a skill `buscar-grupo-zendesk` chamou a API de prd duas vezes, a pedido do usuário. Confirmar a regra antes de validar tickets pelo navegador.
- Os tickets de teste caem em filas reais da operação: avisar antes e fechar depois.
- Os screenshots do claude-in-chrome não ficam salvos em disco; a evidência no Jira vai em texto (ticket, grupo esperado e obtido) e o usuário anexa os prints.

## Piloto 1 (2026-11-16, 16:09) — EM_ANALISE, processo de plano AVANCADO

- Preparação: SOCI-255767 transicionado para EM_ANALISE pelo MCP do Jira (chegou à Abertura em ~30 s); telefone do sócio do processo `4891157268267008` gravado pelo time da Abertura direto no banco. Contagem do telefone: 1 processo em `basicoPadraoMultibeneficios` (plano AVANCADO).
- Conversa: "Oi" no WhatsApp Web para `[prd] ctbz zendesk 41 41010021 main`. O menu do bot não apareceu; abriu o ticket **30339109** já no grupo **AIDA [Ativação] [WhatsApp] [BP]** (`29248769628572`), atribuído a "Contador Inteligente ~ admin" (agente de IA), que respondeu no WhatsApp.
- **Conclusão:** processo de abertura de plano BP (AVANCADO) vai para a AIDA Ativação BP e não passa pelos drops do fluxo Experts. Para testar o roteamento da PRD-176172, o processo de teste precisa estar com **plano Experts** (trocar no admin da Abertura).
- O usuário de teste no Zendesk está na organização `5405377070236`, e o ticket ganhou tags de outra empresa (`cnpj:37657502000108`, `expert_essencial`, `jira_finalizado`, `debora.cardoso`). A plataforma não tem empresa nesse telefone (buscar-por-telefone vazio), então são dados antigos da org/usuário do Zendesk. Conferir antes dos próximos testes.
- Evidência: GIF `~/Downloads/piloto-roteamento-n1-em-analise-30339109.gif`; ticket 30339109 fechado pela skill `fechar-tickets-teste-zendesk`.
- Ferramentas usadas: `scratchpad/processos_bot.py` (contagem/dados), `scratchpad/zd_tickets.py` (últimos tickets do requester com grupo; usa a auth da skill de fechar tickets), audits do ticket por `GET /api/v2/tickets/{id}/audits.json`.

## Piloto 2 (2026-11-16, 16:18) — EM_ANALISE, processo com plano EXPERT_ESSENCIAL

- Contagem: 1 processo em `experts`. "Oi" → ticket **30339331** já em **AIDA [Ativação] [WhatsApp] [Experts]** (`31714889423900`), atribuído ao "Contador Inteligente" (IA), com `escalated_to_ai`. Pedido de atendente → a IA perguntou o assunto e, na última mensagem, disse que ia transferir ao assessor. O teste foi interrompido aí pelo Glener (não parecia o ramo esperado) e o ticket foi fechado. GIF: `~/Downloads/piloto2-roteamento-n1-em-analise-30339331.gif`.
- **Telefone sem empresa na plataforma:** `buscar-por-telefone` (`+555596981032` e `+5555996981032`) volta 0 em ativas/rascunho, inativas e qualquer status. A rota `autenticacao/basico-padrao` sem CNPJ dá 500.
- **Mas o usuário do Zendesk (`21878313229212`) está na organização `5405377070236` "Contabilizei - Squad Engenharia Canais - Testes"** (única, default), com campos de empresa de teste: `cnpj 37657502000108`, `plano_de_pagamento expert_essencial`, `abertura_ou_migrao Abertura`, `regime Lucro presumido`, `possui_assessor_ongoing`. As tags da org (`jira_finalizado` **e** `jira_não_finalizado`, `expert_essencial`, `debora.cardoso`, `lucas.knabben_expert`, `possui_assessor_ongoing`…) entram em todo ticket do usuário. Gatilhos que olham essas tags podem desviar o roteamento; tirar o usuário da org (ou limpar as tags) antes de concluir algo.

## Piloto 3 (2026-11-16, 16:40) — EM_ANALISE, plano EXPERT_ESSENCIAL, fora do rollout da IA — **OK**

- "Oi" enviado por script exatamente no segundo :30 UTC (`while(new Date().getUTCSeconds()!==30)…` e clique no botão de enviar do WhatsApp Web), para a config rodar fora de `flagRolloutIAAtivExp` (segundo ≤ 24, ver [[rollout-ia-ativacao]]). O bot respondeu "Vamos chamar um especialista…" e abriu o ticket **30339953** em **Cadastro [Ativação] [Whatsapp]** (`28283501432220`), com `escalated_to_human` e `processo:4891157268267008`. **Resultado = esperado.**
- O ticket foi atribuído a um agente humano (`29523126981532`): fechar logo após conferir.
- Evidência: comentário 29713786 no PRD-177631, com o GIF embutido (`~/Downloads/piloto3-em-analise-cadastro-30339953.gif`).
- **Armadilhas do ciclo:**
  - Depois de fechar um ticket, o WhatsApp manda o CSAT. A próxima mensagem vira resposta da pesquisa (abre um ticket em "Experts CSAT - Respostas"). Encerrar o CSAT antes do próximo cenário.
  - Logo depois do CSAT, o bot responde "Seu atendimento anterior já foi finalizado…" e pede uma nova mensagem: mandar de novo no segundo :30.
- **Ciclo por cenário:** transicionar o SOCI pelo MCP do Jira → conferir `statusJira` na rota de dados (~30 s) → encerrar o CSAT pendente → enviar no segundo :30 → `zd_tickets.py --since-id` → fechar com `fechar_tickets.py close` → comentário com o GIF no PRD-177631 (`uploadAttachmentToJiraIssue` fase 1 + `curl` + `addOrEditJiraIssueComment` com `inlineFileId`).

## Cenários 2 a 4 e armadilhas do CSAT (2026-11-16, 16:50–17:03)

| # | Status SOCI (transição Jira) | Grupo obtido | Ticket | Resultado |
| --- | --- | --- | --- | --- |
| 2 | Aguardando Cliente | Pré CNPJ [Ativação] [Whatsapp] (28283155272220) | 30340273 | OK |
| 3 | Processo Adm MT | Pré CNPJ - Módulo tributário [Ativação] [WhatsApp] (30023019944860) | 30340474 | OK |
| 4 | Ajuste de Fluxo (fora do mapa → ELSE) | Atendimento [Ativação] [Whatsapp] (5318551320604) | 30340554 | OK no grupo; **sem a tag `sys_grupo_ativacao_exp`** |

- Evidências: comentários no PRD-177631 com GIF recortado (só o chat do bot).
- **Transições do SOCI:** Solicita Reembolso exige campos de cancelamento (Etapa do Cancelamento, Motivo, ticket de contato, canais) → não usar em teste. Em Stand-by exige o grupo "SOCI - Pontos Focais" + data de retorno e motivo. **Ajuste de Fluxo é um hub**: dele dá para ir a EM_ANALISE, PENDENCIA, Aguardando Protocolo, Preenchimento MT, Ag Análise MT, Aguardando Formatura, Aguardando pagamento, Gerar DBE automática etc.
- **CSAT:** a tag `sys_nao_oferecer_csat` só é respeitada pelo gatilho de CSAT BP. Os gatilhos "Experts • CSAT trigger survey Human WhatsApp" (`27492316041500`) e "Ativação • trigger csat survey - human" (`29997958429596`) disparam no `closed` **a não ser que** o ticket já tenha `sys_csat_survey_sent` (ou `sys_csat_response_exp`, `crm_807_closed`, `fup_canal_off_block_csat`…). Para fechar ticket de teste sem pesquisa: adicionar `sys_csat_survey_sent` + `sys_csat_response_exp` **antes** de fechar (`PUT /api/v2/tickets/{id}/tags.json`, depois status `closed`). A pesquisa chega no WhatsApp minutos depois (visto ~10 min) e a próxima mensagem vira resposta dela; não responder pelo Claude (polui o CSAT), pedir ao Glener.
- **GIF sem vazar conversas:** recortar a lista de chats do WhatsApp Web antes de subir (`scratchpad/crop_gif.py`: quadros cheios cortados a partir de 33,5% da largura; quadros de zoom ampliados e com margem de 9% cortada). Conferir a folha de contato antes de anexar.
- **Envio no segundo :30:** o `javascript_tool` tem timeout de 45 s; usar espera de no máximo 40 s e repetir se voltar `retry`.

## Cenário 5 e situação final (2026-11-16, 17:08)

| # | Status SOCI | Grupo obtido | Ticket | Resultado |
| --- | --- | --- | --- | --- |
| 5 | Aguardando Protocolo (via Ajuste de Fluxo) | Pré CNPJ - Assinatura JC [Ativação] [WhatsApp] (30023034651676) | 30340715 | OK |

- Fechado com `sys_csat_survey_sent` + `sys_csat_response_exp` antes do `closed`: nenhuma pesquisa enviada.
- **Não testados:** Pós Vendas (nenhuma transição do SOCI-255767 leva a Iniciado/NAO_INICIADO/Pós Vendas); Retenção (Solicita Reembolso exige campos do fluxo real de cancelamento); Finalizado BP/Experts (não passa pela rota de processos, ver [[menu-inic-experts-ramificacoes]]).
- Estado deixado: SOCI-255767 em **Aguardando Protocolo**, processo `4891157268267008` com plano `EXPERT_ESSENCIAL` e o telefone do Glener como sócio.

## Cenário 6 (2026-11-16, 17:27) — Iniciado → Pós Vendas — **OK**

- Processo `4550028081496064` (SOCI-255830): telefone do sócio trocado pelo admin com a sessão SSO (`GET` + `PUT https://appabertura.contabilizei.com/rest/admin/processoabertura`, campos `empresa.socios[0].telefone`, `socioLogin.telefone`, `atributos.soci__telefone`); plano → `EXPERT_ESSENCIAL` pela rota pública; transição em loop **"Atualizar Sistema"** (Iniciado → Iniciado, sem campos obrigatórios) fez a Abertura gravar `Iniciado` em ~1 min 15 s ("Registro de Follow" pede etapa e canal).
- Ticket **30341220** em **Pós Vendas [Ativação] [Whatsapp]** (`28283527238556`), `processo:4550028081496064`. Com 2 processos no telefone, o bot usa o primeiro da lista da contagem.
- Fechado com o bloqueio de CSAT: nenhuma pesquisa enviada.

**Placar:** 6 de 9 cenários OK (Cadastro, Pré CNPJ, Módulo tributário, ELSE, Assinatura JC, Pós Vendas). Faltam Retenção (Solicita Reembolso exige campos do cancelamento real) e Finalizado BP/Experts (fora do caminho de processos).
- Estado deixado: SOCI-255767 em Aguardando Protocolo e SOCI-255830 em Iniciado, ambos com plano `EXPERT_ESSENCIAL` e o telefone do Glener como sócio.

- **Encerrado em 2026-11-16:** o Glener deu os testes por concluídos com 6/9. A justificativa dos cenários 7, 8 e 9 está no comentário 29720370 do PRD-177631.
