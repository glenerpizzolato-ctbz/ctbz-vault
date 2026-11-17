---
name: testes-roteamento-bp-n1-n2
description: "Plano de testes da PRD-176795 (BP WhatsApp: SOCI ou migração não finalizados → AIDA 24/7 Ativação BP; os dois finalizados → AIDA Geral 24/7 BP): matriz de cenários, regressões, massa, pré-requisitos e pontos em aberto (origem do sinal de migração, IDs dos grupos diferentes dos atuais)"
metadata:
  type: project
tags:
  - ultimate
  - testes
  - ativacao
  - bp
jira: https://contabilizeicontabilidade.atlassian.net/browse/PRD-176795
---

# Testes do roteamento BP N1/N2 (PRD-176795)

Plano montado em 2026-11-17. Épico PRD-176794 "[BP] Segmentação de Fluxos de Atendimento Wpp ZD". Receita de execução: [[testar-bot-whatsapp]]; testes anteriores parecidos (Entrega 03, Experts): [[testes-roteamento-n1-ativacao]].

## Regra do card

Todo novo atendimento Zendesk **BP** via **WhatsApp**:

- SOCI **não** finalizado **OU** migração **não** finalizada → `AIDA 24/7 [Ativação] [WhatsApp] [BP]` (`29248799750812`).
- SOCI finalizado **E** migração finalizada → `AIDA Geral 24/7 [WhatsApp] [BP]` (`23609834550556`).

A mudança fica no dialogue builder da Ultimate (bot `[prod] ctbz wpp main`), não em repositório (nenhum repo citado guarda esses IDs até agora).

## Pontos em aberto (resolver antes de testar)

1. **IDs diferentes dos grupos atuais.** Hoje o BP em abertura cai em `AIDA [Ativação] [WhatsApp] [BP]` (`29248769628572`, [[rollout-ia-ativacao]]) e o grupo geral conhecido é `AIDA Geral [WhatsApp] [BP]` (`22427993443100`, [[roteamento-n1-ativacao-soci]]). O card cita `29248799750812` e `23609834550556`, com "24/7" no nome. Confirmar com `buscar-grupo-zendesk` se são grupos novos, se estão ativos e com agente (IA) atribuído.
2. **De onde vem "migração finalizada".** A consulta CNPJ do `plataforma-crm-web` (`BuscarDadosGeralWhatsAppBotFacade`) devolve `abertura` (`Empresa.isAbertura`), `jiraFinalizado` e `jiraStatus`, mas nenhum campo de migração. Definir com Produto/CRM qual é o sinal (campo da empresa, status de outro Jira, tag/org do Zendesk como `abertura_ou_migrao`) e se precisa de mudança no `plataforma-crm-web` ou no `atendimento-zendesk` para expô-lo ao bot.
3. **Cliente de abertura (sem migração) e cliente de migração (sem SOCI).** A regra usa OU/E dos dois sinais. Definir o valor de cada sinal quando ele não se aplica: abertura sem migração conta como "migração finalizada"? Migração sem SOCI conta como "SOCI finalizado"? Sem isso, cliente de abertura finalizado pode ficar preso na Ativação para sempre.
4. **Escopo do "todo novo atendimento".** A regra vale também para quem cai em `Pointer | Status Tickets` (tickets abertos), para os itens do menu (NF, Conta PJ, Plano de saúde) e para BP fora da abertura (`aberturaEmpresa = false`)? Hoje só o ramo de abertura vai para a AIDA Ativação BP.

## Decisão e estado em prd (2026-11-17)

- **Decisão do Glener:** a "migração" se resume ao processo de abertura: BP com processo de abertura em qualquer status diferente de Finalizado → AIDA 24/7 Ativação BP; Finalizado → AIDA Geral 24/7 BP. Os pontos 2 e 3 acima ficam resolvidos assim.
- Grupos conferidos no Zendesk de prd: `29248799750812` = AIDA 24/7 [Ativação] [WhatsApp] [BP] e `29248769628572` = AIDA [Ativação] [WhatsApp] [BP] (os dois criados em 2026-07-29); `23609834550556` = AIDA Geral 24/7 [WhatsApp] [BP] e `22427993443100` = AIDA Geral [WhatsApp] [BP].
- Lido pela API do dashboard ([[dashboard-read-api]]) às ~15h30: o reply ativo é `Wpp Shared | Ativacao Inbound v09` (`6af322ab6f3e8ec9090f221b`, editado em 2026-11-10). Nele, plano sem `EXPERT` → `flagRolloutAtivacaoInboundBP` (sempre true) → template `Escalate | IA BP - Wpp Ativ Migr` (`6aac615c8788beddef16efcc`, editado em 2026-09-17) → **`29248769628572`** (sem 24/7). Só quando a flag é false o BP passa por `serviceStatus` → `Escalate | Inbound Humano - Wpp Ativ Migr` (`6aac586ddc4538309e0f7fbc`, editado em 2026-11-17 18:01 UTC), cujo ramo "plano sem EXPERT" já vai para **`29248799750812`**.
- **Conclusão:** em prd, BP em abertura ainda cai na AIDA [Ativação] BP sem 24/7. Para valer a regra do card, falta trocar o `escalateTo` do template `Escalate | IA BP - Wpp Ativ Migr` (ou desviar o ramo da flag) para `29248799750812`.
- O ramo Finalizado BP (empresa ativa) passa pelo fluxo BP principal: `Wpp BP | Id atend IA 24x7` já cita `23609834550556`, e o `Wpp BP | Menu BPM` cita `22427993443100`.
- Processos de teste SOCI-255767 e SOCI-255830 voltaram para o plano `AVANCADO` em 2026-11-17 (rota pública `carrega-dados-categoria-planos`). O telefone do Glener ainda não foi apontado de novo (contagem 0).

## Matriz de cenários (BP, WhatsApp)

| # | Cliente | SOCI | Migração | Esperado |
| --- | --- | --- | --- | --- |
| 1 | Abertura em andamento | não finalizado | n/a | AIDA 24/7 Ativação BP (`29248799750812`) |
| 2 | Abertura concluída | finalizado | n/a (ver ponto 3) | AIDA Geral 24/7 BP (`23609834550556`) |
| 3 | Migração em andamento | n/a | não finalizada | AIDA 24/7 Ativação BP |
| 4 | Migração concluída | n/a | finalizada | AIDA Geral 24/7 BP |
| 5 | Abertura + migração | finalizado | não finalizada | AIDA 24/7 Ativação BP |
| 6 | Abertura + migração | não finalizado | finalizada | AIDA 24/7 Ativação BP |
| 7 | Abertura + migração | finalizado | finalizada | AIDA Geral 24/7 BP |
| 8 | BP ativo antigo, sem abertura nem migração | n/a | n/a | AIDA Geral 24/7 BP (confirmar) |

Variações a cobrir em pelo menos um cenário de cada destino:

- **Planos BP:** `BASICO`, `AVANCADO` (padrão), `PREMIUM`/multibenefícios: todos entram em `basicoPadraoMultibeneficios`.
- **Fora do horário comercial** (noite/fim de semana): os grupos são 24/7, o ticket não pode ir para Business Hours nem fila noturna.
- **Telefone com 2+ empresas/processos** (BP em finalizado + BP em abertura): conferir qual o bot usa (hoje, o primeiro da contagem).
- **Cliente com ticket aberto** (`ticketsAbertosQuantidade > 0`): conforme a decisão do ponto 4.

## Regressão (não pode mudar)

| # | Cenário | Esperado (como hoje) |
| --- | --- | --- |
| R1 | Experts em abertura, segundo ≤ 24 | AIDA [Ativação] [WhatsApp] [Experts] (`31714889423900`) |
| R2 | Experts em abertura, segundo :30, um status por bloco | drops N1 da Entrega 03 ([[roteamento-n1-ativacao-soci]]) |
| R3 | Experts com Jira finalizado | menu completo → Experts Grupo Padrão (`15320473247900`) ([[menu-inic-experts-ramificacoes]]) |
| R4 | BP pelo chat web / e-mail | sem mudança (regra é só WhatsApp) |
| R5 | Consulta CNPJ sem resposta / `jiraFinalizado` vazio | "Sistema temporariamente indisponível" (ou fallback combinado), sem ticket órfão |
| R6 | Telefone sem empresa nem processo | fluxo de não cliente, sem cair nos grupos BP |

## Massa e preparação (prd)

- **Abertura BP:** processos de teste SOCI-255767 (`4891157268267008`) e SOCI-255830 (`4550028081496064`) ([[ativacao-processos-abertura-teste]]). Em 2026-11-17 o telefone do Glener foi tirado dos dois e o 255767 estava com `EXPERT_ESSENCIAL`: voltar o plano para `AVANCADO` (rota pública `carrega-dados-categoria-planos`) e apontar o telefone de novo.
- **SOCI finalizado:** o processo `FINALIZADO` some da contagem; esse caminho passa pela consulta CNPJ (`jiraFinalizado`) da empresa na plataforma. Precisa de uma **empresa de teste BP com o telefone do Glener**, e a transição para Finalizado do SOCI de teste cria cards reais (FIN/PLA/CIT): combinar com a Abertura antes.
- **Migração:** não há massa de migração de teste. Depende do ponto 2 (pedir à Ativação/CRM uma empresa de teste em migração).
- **Organização do Zendesk:** o usuário de teste `21878313229212` está na org `5405377070236`, que injeta `jira_finalizado` **e** `jira_não_finalizado`, `expert_essencial` etc. em todo ticket. Se algum gatilho do roteamento olhar essas tags, tirar o usuário da org antes.
- **Cache de 3 h** do `plataforma-crm-web` por `idProcesso` no `jiraStatus`: depois de mudar o status, esperar ou usar outro processo.

## Execução e evidência

- Ciclo por cenário igual ao da [[testar-bot-whatsapp]]: preparar dado → `processos_bot.py` → baseline `zd_tickets.py` → "Oi" no WhatsApp Web → grupo pelo `zd_tickets.py --since-id` → `zd_fechar_sem_csat.py` → GIF recortado.
- Conferir no ticket: grupo, tags (`processo:`, `escalated_to_ai`) e se o agente IA atendeu. Para entender um desvio: logs de conversa da Ultimate ([[logs-conversa-ultimate]]).
- Evidência por cenário em comentário na sub-task de testes (E2E) do PRD-176795: ticket, grupo esperado x obtido, GIF.
- Antes de publicar no prd: backup JSON do bloco alterado no dialogue builder (como [[backup-roteamento-n1-ativacao-v1]]) para rollback.
- Pós-virada (sem escrita): amostra de tickets BP WhatsApp de 24–48 h (BigQuery, [[zendesk-tickets-bigquery]]) cruzando grupo x `jiraFinalizado`/migração, para pegar o que a massa de teste não cobre.

## Rascunho em edição e transferência sem texto (2026-11-17, ~16h)

- O Glener está editando o template `Escalate | IA BP - Wpp Ativ Migr` (rascunho `6afc9a4c5c19c334eb3daa2a`, que a rota `getReply` não lê: 404). No rascunho há uma condição de parâmetro "Está em +555596981032" (só o telefone de teste) que leva a uma **Transferência nova** para `29248799750812`. O fallback continua na transferência antiga (`6aa14933c80bcc6bd14b1802`, para `29248769628572`). Dá para testar só com o telefone de teste antes de abrir para todos.
- **A Ultimate não exige texto em toda transferência, pelo menos não no que já está publicado:** o bot tem 20 transferências publicadas com texto vazio (1.790 com texto), entre elas a própria `6aa14933…` deste template (publicada em 2026-09-17) e a de `Escalate | IA Exp - Wpp Ativ Migr` (publicada em 2026-11-10). A trava apareceu ao publicar com um nó **novo**, então pode ser uma validação recente que só vale para nós criados ou editados. Não foi confirmado.
- A Transferência nova do rascunho não tem a ação `add tags > escalated_to_ai`, que a antiga tem: copiar, senão o ticket perde a tag.

## Execução em prd (2026-11-17, 15h30–15h50) — sub-task PRD-177894

Canário publicado pelo Glener: `Pointer | Ativacao Inbound - Wpp Shared` (`673d356b4a876ce1756ac515`) com `telefone in +555596981032` → `Wpp Shared | Ativacao Inbound v10 | 176795` (`6afc9cace8f9c0c6f5cb5021`), que só difere da v09 no destino do BP: `Escalate | IA BP V2 - Wpp Ativ Migr` (`6afc9c23be5f83fd66fd47ca`) → `29248799750812`. Os outros telefones continuam na v09.

| # | Cenário | Ticket | Grupo obtido | Resultado |
| --- | --- | --- | --- | --- |
| 1 | BP, SOCI Aguardando Protocolo, inbound | 30356205 | AIDA 24/7 [Ativação] [WhatsApp] [BP] | OK |
| 2 | BP, SOCI EM_ANALISE, inbound | 30356343 | AIDA 24/7 [Ativação] [WhatsApp] [BP] | OK |
| R1 | Experts, EM_ANALISE, segundo :30 | 30356369 | Cadastro [Ativação] [Whatsapp] | OK (sem regressão) |
| 0 | BP respondendo ativo especial (3 tickets) | 30356058, 30356125, 30356160 | AIDA [Ativação] [WhatsApp] [BP] (antigo) | **Falhou**: o ramo de retorno de ativo não foi ajustado |

- **Retorno de ativo é outro caminho:** com ativo especial habilitado para o telefone (`mensagem_ativa` do `atendimento-zendesk`, banco `prd_crm_atendimento_zendesk`, `habilitado` e dentro de `validade_em_minutos`), o bot faz `[atnd-zd] GET | ativos especiais` → `URA_FLOW = ATIVACAO_MIGRACAO` e entra no `Outbound Especiais Ativ Migr v01/v02`, que usa o template antigo `Escalate | IA BP - Wpp Ativ Migr` (`29248769628572`), sem passar pelo Pointer de inbound. Cada conversa consome um ativo (PATCH). Os processos de teste recebem ativos reais da operação (cobrança de assinatura, pendência de certificado, protocolo), então **antes de testar inbound, contar os ativos habilitados do telefone** e consumi-los.
- A IA do grupo 24/7 respondeu cerca de 1 min depois da transferência; no grupo antigo, foi ~1 s. Ela respondeu com os dados da org de testes do Zendesk (CNPJ 37.657.502/0001-08), não com os do processo.
- Depois de fechar um ticket do grupo 24/7, a IA ainda mandou uma resposta atrasada no WhatsApp ("Olá! Boa tarde. Como posso te ajudar?").
- **Não testados:** BP Finalizado → AIDA Geral 24/7 (sem massa: processo finalizado some da contagem e o caminho é o da empresa ativa) e BP com o rollout desligado.
- **Estado deixado:** processo `4891157268267008` (SOCI-255767) em **EM_ANALISE**, plano `AVANCADO`, **com o telefone do Glener** (`5596981032`) nos sócios, `socioLogin` e `atributos.soci__telefone`. O processo `4550028081496064` (SOCI-255830) ficou intocado, com plano `AVANCADO` e o telefone fictício `12985858585`.

## Caminho do retorno de ativo de Ativação (lido em 2026-11-17)

1. **Disparo:** lotes MASSIVA de WhatsApp ativo pelo `atendimento-zendesk`, feitos pelo time de Ativação, com `integracao = categoria = ATIVACAO_MIGRACAO`. É a única integração de Ativação: em 14 dias foram ~88 mil mensagens e 236 templates, BP e Experts juntos. Cada linha de `mensagem_ativa` guarda `doc_tipo = processo_abertura_id`, `doc_valor = <idProcesso>`, `validade_em_minutos = 1440` e `habilitado = true` até ser respondida.
2. **Resposta do cliente** (log da Ultimate): `[atnd-zd] POST | inicio atend wpp` → `[atnd-zd] GET | ativos especiais | Exp` (acha o ativo habilitado do telefone) → `sessaoAutenticada = true`, `entrouRetornoAtivo = true`, tags `support_ativ_migr`, `src_outbound`, `sys_template_ativo:<template>`, `id_mensagem_ativa:<id>` → `[atnd-zd] PATCH | ativos especiais ATIVACAO_MIGRACAO` (marca como recebido, `habilitado = false`, e publica o texto do ativo como comentário privado no ticket, no tópico `atendimento-zendesk-whatsapp-ativo-comentario-privado`) → `URA_FLOW = ATIVACAO_MIGRACAO` → `[bots-api] GET | business hours status`.
3. **Roteamento:** `Wpp Exp | Business Hours Outbound v13` (condição `ativosEspeciaisCategoria in ATIVACAO_MIGRACAO`) → `Pointer | Outbound Especiais Ativ Migr - Wpp Shared` (`6aac6b6b71597c4922df02ef`) → `Wpp Shared | Outbound Especiais Ativ Migr v02` (`6af319e8d02ed8f099104157`): `ativoEspecialAtivacaoMigracaoIntegracao` inclui `ATIVACAO_MIGRACAO` → `flagRolloutAtivacaoInboundBP` (sempre true) → `Escalate | IA BP - Wpp Ativ Migr` (`29248769628572`). Senão → `flagRolloutIAAtivExp` → IA Experts ou `serviceStatus` (horário).
4. **Experiência:** o cliente não vê menu nem mensagem do bot. A conversa vai direto para a AIDA, que recebe o texto do ativo como contexto e responde em ~1 s sobre o assunto do ativo (ex: cobrança de assinatura).
- Na prática a separação BP x Experts funciona: numa amostra de 100 tickets recentes do grupo `29248769628572` com `src_outbound` + `support_ativ_migr`, 95 eram BP; nos 61 do `31714889423900`, 56 eram Experts. A variável `ativoEspecialAtivacaoMigracaoIntegracao` não é só o `integracao` do banco (que é sempre `ATIVACAO_MIGRACAO`); a origem dela não foi conferida.
- **Volume:** ~4,3 mil tickets de retorno de ativo no grupo antigo desde 2026-11-10 (contagem da busca do Zendesk, aproximada). É o maior caminho de entrada do BP em abertura.
- **Para a PRD-176795:** apontar o `Outbound Especiais Ativ Migr v02` (ou o template `Escalate | IA BP - Wpp Ativ Migr`) para o `IA BP V2` / `29248799750812`.

## Empresa ativa BP com SOCI não finalizado (alinhado com o relator em 2026-11-17)

Regra nova: cliente **com empresa BP ativa** cujo processo de abertura (SOCI) ainda não foi finalizado também vai para a AIDA 24/7 [Ativação] [WhatsApp] [BP], e não para a AIDA Geral.

Implementação do Glener (publicada às 16h19, canário pelo telefone de teste):
- `Pointer | Journey router - Wpp Shared [d]` (`…a64b4d`): `telefone in +555596981032` → `Journey router v09 | 176795` (`6afca6ba6280b3968fd650a7`); os demais telefones → `v08` (`…3c1682`).
- No `v09`, ramo `possuiAcessoBasicoPadraoMultibeneficios = true`: `[atnd-zd] GET | count + list processos by phone` → `totalProcessosAberturaListTotal > 0` (adiciona as tags `processo:{{primeiroIdProcessoListTotal}}`, `support_ativ_migr`, `src_inbound`) → `[atnd-zd] GET | fetch 1st processo` → `plano` contém EXPERT → Geral; `statusJira in Finalizado` → Geral; senão → `Escalate | IA BP V2 - Wpp Ativ Migr` (`29248799750812`). Sem processo, ou com falha em qualquer integração → template `Escalate | IA BP 24/7 - Wpp Shared` (`6afca7ca0cbdd7a205533c2c`).
- No `v08`, esse ramo ia direto para um nó com escalate para `22427993443100`.

Pontos da validação:
- **O template "IA BP 24/7" aponta para `22427993443100` (AIDA Geral [WhatsApp] [BP], sem 24/7)**, e não para `23609834550556` (AIDA Geral 24/7), que é o grupo do card. O comportamento de quem não tem processo é o mesmo do `v08`; confirmar qual dos dois grupos é o certo.
- A decisão é pelo **telefone**, não pela empresa: um sócio de empresa BP ativa que esteja abrindo **outra** empresa também vai para a Ativação. Só o **primeiro** processo da lista é considerado; se ele for Experts, a conversa vai para a Geral, mesmo com um processo BP em andamento no mesmo telefone.
- `statusJira in Finalizado` quase nunca bate: a contagem já descarta os processos `FINALIZADO`. É inofensivo.
- As tags `support_ativ_migr`/`src_inbound`/`processo:` entram também nos tickets que vão para a Geral (processo Experts ou finalizado), porque são gravadas antes da decisão.
- Nas falhas de integração, o fallback é a Geral: seguro.
- **Massa:** o telefone de teste não tem empresa na plataforma (`buscar-por-telefone` vazio, e o telefone fictício `12985858585` dos processos de teste também não). Para testar esse ramo, é preciso ligar o telefone a uma empresa BP ativa de teste.

### Revisão: trocar a contagem por telefone por `aberturaEmpresa` + `jiraFinalizado` (2026-11-17)

- O Glener manteve o template com escalate para `22427993443100` e tirou o "24/7" do nome. O ponteiro só para o telefone de teste é proposital: é o teste em prd antes da virada.
- `jiraFinalizado`, `aberturaEmpresa`, `possuiAcessoBasicoPadraoMultibeneficios` e `possuiAcessoExperts` saem da **mesma** integração (`[pltf-crm] GET | consulta CNPJ - Shared` / `POST | autentica CNPJ - Shared`, `data.data.empresaLogada.*`). Então já estão preenchidas quando o Journey router decide o ramo BP. Vêm de `Empresa.isAbertura` e `Empresa.getJiraFinalizado()` no `plataforma-crm-web`, e o DTO do bot tem `jiraFinalizado = false` como padrão.
- O Menu Inic Experts (`Wpp Exp | Menu Inic v56`, nó `6a465cb6e0826b8881fbaf7b`) só olha `jiraFinalizado` **depois** de `aberturaEmpresa = true` (e de não ter ticket aberto): true → menu completo; false → menu sem Jira (Ativação); vazio → "Sistema temporariamente indisponível".
- **Empresas ATIVO no BigQuery** (`contabilizei-dataflow.dw_contabilizeiapp.Empresa`, 2026-11-17):

| abertura | jiraFinalizado | empresas | ativadas em 90 dias |
| --- | --- | --- | --- |
| true | true | 148.073 | 12.520 |
| false | false | 25.447 | 1.999 |
| true | false | 1.829 | 1.600 |
| false | false (com jiraIssueId) | 511 | 6 |
| demais | | ~300 | ~1 |

- **Conclusão:** `jiraFinalizado` sozinho não serve. As ~26 mil empresas que não vieram de abertura (migração) têm `jiraFinalizado = false` para sempre e iriam todas para a Ativação. A regra certa é a do Menu Inic: `aberturaEmpresa = true` **e** `jiraFinalizado = false` → AIDA 24/7 Ativação BP; qualquer outra combinação (e vazio) → Geral. Isso dá ~1,8 mil empresas, quase todas ativadas nos últimos 90 dias.
- Vantagens sobre a contagem por telefone: decide pela empresa autenticada, não pelo telefone (o sócio que abre outra empresa não é desviado, e não depende do primeiro processo da lista) e tira duas integrações do caminho.

### Ajuste publicado (2026-11-17 16h44) e plano de testes do ramo empresa ativa

- `Journey router v09` (`6afca6ba6280b3968fd650a7`, 13 nós, sem as integrações de contagem por telefone): `possuiAcessoBasicoPadraoMultibeneficios = true` → `aberturaEmpresa` (`true` → `jiraFinalizado`; `*` → `Escalate | IA BP Aida Geral - Wpp Shared` → `22427993443100`) → `jiraFinalizado` (`true` → Geral; `*` → `Escalate | IA BP V2 - Wpp Ativ Migr` → `29248799750812`).
- O `*` do `jiraFinalizado` cobre `false` **e vazio**. Na prática, o DTO do CRM usa `false` como padrão e, se a consulta de CNPJ falhar, o ramo BP nem é alcançado. O risco é baixo, mas `is:false` → V2 e `*` → Geral deixaria o fallback explícito.

| # | Cenário (empresa autenticada) | Esperado |
| --- | --- | --- |
| B1 | BP ativa, `abertura = true`, `jiraFinalizado = false` | AIDA 24/7 [Ativação] [WhatsApp] [BP] (`29248799750812`) |
| B2 | BP ativa, `abertura = true`, `jiraFinalizado = true` | AIDA Geral [WhatsApp] [BP] (`22427993443100`) |
| B3 | BP ativa, `abertura = false` (migração) | AIDA Geral [WhatsApp] [BP] |
| B4 | Telefone com 2 empresas BP (uma B1 e uma B2), escolher cada uma | segue a empresa escolhida |
| R2 | Empresa Experts ativa | sem mudança (ramo `possuiAcessoExperts`) |
| R3 | Telefone fora do canário | `v08` (só por estrutura e amostra pós-virada) |

- **Massa:** empresa BP de teste na plataforma ligada ao telefone de teste, com `abertura`/`jiraFinalizado` alternáveis (entidade `Empresa` da plataforma; escrita em prd só pelo usuário ou pelo time dono).

### Execução do ramo empresa ativa (2026-11-17, 17h00–17h10) — comentário 29777959 no PRD-177894

| # | Cenário | Massa | Ticket | Grupo | Resultado |
| --- | --- | --- | --- | --- | --- |
| B2 | BP ativa, abertura true, jiraFinalizado true | [[empresa-teste-bp-ativa]] (51596322000186) | 30358491 | AIDA Geral [WhatsApp] [BP] | OK |
| B1 | BP ativa, abertura true, jiraFinalizado false | impersonate de empresa AVANCADO real | 30358564 | AIDA 24/7 [Ativação] [WhatsApp] [BP] | OK |
| B3 | BP ativa vinda de migração (abertura false) | impersonate de empresa AVANCADO real | 30358579 | AIDA Geral [WhatsApp] [BP] | OK |
| R2 | Experts ativa | impersonate de empresa EXPERT_ESSENCIAL real | 30358650 | menu de boas-vindas Experts | OK (sem mudança) |

- **Impersonate na prática:** chamada da coleção Bruno do `bots-api` (header `x-ctbz-api-gateway-token`, token `DECK_BRUNO_EXPERTS_TO_BOTS_API_prod` do `docs/bruno/.env`, que está **entre aspas** no arquivo; tire as aspas ao usar com curl). Log da conversa: `[bots-api] GET | impersonate` → `[SET] CNPJ IMPERSONATE` → `[pltf-crm] GET | consulta CNPJ` → Journey router. Lembrar do `DELETE` no fim.
- Para escolher empresas reais por estado: `contabilizei-dataflow.dw_contabilizeiapp.Empresa` (`status = ATIVO`, `abertura`, `jiraFinalizado`) cruzada com `saude_empresa.empresa` (`plano`). O snapshot pode estar alguns dias atrasado; confirme o caminho pelo log da conversa.
- A rota `POST /plataforma/rest/ativacao/jira/body` (`plataforma-web`) não funcionou: pelo `plataforma-web-dot-contabilizeiapp.appspot.com` deu 401; pelo `app.contabilizei.com.br` deu 200 em 6 ms, sem log de aplicação, e o campo não mudou. Usar o impersonate.
- Ticket que fica parado no menu do bot (sem grupo, status `new`) não fecha pela API: o bot segura a conversa até o timeout.
- **Estado restaurado no fim:** impersonate desligado; SOCI-255767 de volta a Aguardando Protocolo (via Ajuste de Fluxo → Aguardar protocolo), plano `AVANCADO` e telefone fictício `12985858585`; SOCI-255830 em Iniciado, `AVANCADO`, `12985858585`; a empresa de teste manteve `jiraFinalizado = true` (nada foi alterado nela) e o telefone do Glener, que ele mesmo adicionou.
- **Segurança:** as rotas de impersonate do `bots-api` só passam pelo token do gateway, sem autenticação de usuário, e o par fica no Redis sem TTL. No código, a rota `POST /ativacao/jira/body` do `plataforma-web` e a `GET /rest/empresa/{id}/finalizar-jira` do monolito não têm `@AcessoRestrito`, e o filtro de SSO não bloqueia requisição sem token.
