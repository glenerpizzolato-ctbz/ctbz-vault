---
name: validar-drop-ativacao
description: Explica por que um ticket de WhatsApp do bot (Ultimate) caiu num grupo do Zendesk (drop para atendimento humano ou IA) no contexto da Ativação - a partir do id ou link do ticket, cruza o ticket (banco do atendimento-zendesk), a trilha de chamadas do bot (logs do load balancer), o estado do cliente pelas rotas do bot (empresa ativa, onboarding x ongoing, processo de abertura, contagem) e o changelog do SOCI, compara o grupo obtido com o esperado (drops por status do SOCI, rollout da IA, retorno de ativo, menu de empresa ativa) e dá o veredito com os links do processo, do SOCI e do log da conversa na Ultimate. Aceita uma pergunta opcional para guiar a resposta (ex: "por que não caiu em Pré CNPJ?"). Use quando o usuário pedir para validar/explicar o drop, o grupo ou o roteamento de um ticket de Ativação, ou perguntar por que um atendimento caiu (ou não) em um grupo.
argument-hint: "<ticket id ou link do Zendesk> [pergunta opcional, ex: \"por que não caiu em Pré CNPJ?\"]"
---

# Validar o drop de um ticket de Ativação

Responde "por que este atendimento caiu no grupo X (e não no Y)?" sem chamar a API de prd do Zendesk nem do Sunshine (ver `apis/zendesk-sunco-prod-politica.md` no vault). Contexto do roteamento no vault CTBZ (`~/ctbz-vault/obsidian/ultimate/`): `roteamento-n1-ativacao-soci.md` (drops e origem do `statusJira`), `menu-inic-experts-ramificacoes.md` (empresa ativa: onboarding x ongoing), `rollout-ia-ativacao.md`, `endpoints-autenticacao-bot.md`, `testes-roteamento-bp-n1-n2.md` (BP) e `logs-conversa-ultimate.md`.

## Árvore que o bot segue (o que validar)

1. **Retorno de ativo**: no início de toda sessão o bot checa mensagem ativa pendente (`GET mensagem/ativa?...&fluxo=ESPECIAIS|EXPERTS|CORE`). O ativo só vale se estiver `habilitado`, dentro da validade e com `nome_grupo` cadastrado; ao usá-lo, o bot o marca `RESPONDIDA` (desabilitado), então a sessão seguinte já não o enxerga. O ticket traz `sys_template_ativo:`, `id_mensagem_ativa:` e `src_outbound` ou `src_inbound`. O script lê o registro em `prd_crm_atendimento_zendesk.mensagem_ativa` (integração, categoria, template, autor, `nome_grupo`, `metadados.csat_source`, documento) e o histórico em `mensagem_ativa_status`. Subfluxos (detalhes em `ultimate/csat-quero-atendimento-ramificacoes.md` e `mensagem-ativa/retorno-ativo-plano-sem-whatsapp.md`):
    - **Retorno de CSAT** (`csat_retorna_atendimento_*`, autor `survey-service`, categoria `WORKER_CSAT`): Sim / Não / **Quero atendimento**. `csat_source` com `HUMAN_CP` → ReRoute Ticket (IA). Senão o bot pergunta "mesmo tema ou novo assunto" (vale a primeira resposta). **Ativo com CNPJ**: mesmo tema → consulta CNPJ → Business Hours Outbound; novo assunto → contagem de empresas → acesso Experts (Concierge ou Business Hours). **Ativo sem CNPJ** (ex: `doc_tipo = processo_abertura_id`, cliente em abertura): Init session / reautenticação → **nova identificação** → contagem de processos → Ativação Inbound, onde valem o rollout da IA e os drops por status.
    - **Follow-up de transbordo** (`follow_up_transbordo_atendimento_*`, `fup_csat_sla_*`): Quero atendimento → Business Hours Outbound.
    - **Demais ativos** (`CORE`, `EXPERTS`, `INBOUND`, `ATIVACAO_MIGRACAO`…): "Responder mensagem" → grupo do ativo (`nome_grupo`); "Novo assunto" → identificação normal.
    - Regra prática: tag de ativo **sem** contagem/dados de processo na sessão = o destino é do fluxo do ativo; **com** contagem/dados depois = a conversa voltou para a identificação normal e o veredito segue os drops.
    - A transcrição (`comments_formatted`) mostra o caminho: perguntas do bot, "Quero atendimento", as respostas de tema e as transferências feitas depois ("Transferência de ticket via app {grupo: A} para {grupo: B}"). O script toma como **drop do bot** o grupo de antes da primeira transferência.
2. **Empresa ativa no telefone** (`buscar-por-telefone`, depois consulta CNPJ): avaliada antes dos processos.
    - `abertura=false` ou `jiraFinalizado=true` → menu completo (cliente **ongoing**/onboarding): Falar com Assessor → valida `emailAssessorOngoing` → Experts Grupo Padrão (`15320473247900`) ou Triagem IA. Não passa pelos drops de Ativação.
    - `abertura=true` e `jiraFinalizado=false` → menu sem Jira → Ativação Inbound (drops). Ticket aberto do CNPJ desvia antes para `Pointer | Status Tickets`.
3. **Sem empresa ativa** → contagem de processos pelo **telefone do sócio** (descarta `FINALIZADO`) → dados do **primeiro** processo (`statusJira`, `plano`).
4. **Ativação Inbound**:
    - Experts: segundo do relógio ≤ 24 no início → AIDA [Ativação] [Experts] (`31714889423900`); senão, drop por status.
    - BP: sempre AIDA [Ativação] [BP] (`29248769628572`) primeiro.
    - Quando a IA transfere para humano (`escalated_to_ai` + grupo humano), o destino deveria seguir o drop do status, mas há casos em que a IA usa outro critério (ex: etapa do SOCI). Confirmar no log da Ultimate.
5. **Drops por status** (Entrega 03, em `scripts/roteamento.json`): Cadastro, Pós Vendas, Pré CNPJ, Pré CNPJ - Módulo tributário, Pré CNPJ - Assinatura JC, Retenção; fora do mapa → ELSE Atendimento [Ativação] (`5318551320604`, Experts com tag `sys_grupo_ativacao_exp`).

## Como rodar

1. Rodar o script (sobe e derruba sozinho o proxy `sql_crm_prd` se ele estiver fora; leva ~1 min pelos logs):

    ```bash
    python3 -I ~/.claude/skills/validar-drop-ativacao/scripts/validar_drop.py <id ou link> [--status "<status na hora>"] [--processo <id>] [--janela-min 180] [--sem-logs] [--json]
    ```

    Ele imprime e salva `~/Downloads/validar-drop-<ticket>.md` com: veredito automático, ramo provável, grupo atual x esperado x drop pelo status, notas, links, estado atual pelas rotas do bot, trilha de chamadas (load balancer), outros tickets do telefone e a transcrição.
2. **Status na hora da conversa**: o script usa o `statusJira` de **hoje**. Ler o changelog do SOCI (`getJiraIssue` com `expand: "changelog"` e `fields: ["status"]`, `cloudId: contabilizeicontabilidade.atlassian.net`; se o histórico for longo, `listJiraIssueChangelogs` pelo `discover`) e achar o último `status` antes do horário do ticket. Se for diferente, rodar de novo com `--status "<status>"`. No mesmo changelog, conferir `[SOCI] Telefone` na data (telefone do sócio diferente do da conversa = processo fora da contagem) e a `[SOCI] Etapa do Processo`.
3. **Grupo ao longo do tempo** (quando há `escalated_to_ai` ou suspeita de transferência por agente): `contabilizei-dataflow.sbox_bi_atendimento_zendesk.raw_tb_ticket_events` (D-1, ver `db/zendesk-tickets-bigquery.md`), olhando os `Change` de `group_id` e o `EscalationEvent`. Para tickets de hoje, só o log da Ultimate.
4. **Log da Ultimate**: o link sai pronto (bot pelo `businessphone:`, período e `platformConversationId`). Abrir no navegador é acesso ao Zendesk de prd: só com aprovação do usuário na conversa, e só leitura. Sem aprovação, entregar o link para ele validar.

## Veredito

Responder em português, curto, nesta ordem:

1. **Onde caiu e por quê** (ou, com pergunta, a resposta direta a ela: ex: "não caiu em Pré CNPJ porque o SOCI estava em Em Stand-by às 13:51, que está fora do mapa → ELSE"). Indicar a confiança: confirmado (status do changelog + trilha) ou provável.
2. **Checklist**: canal/ativo, empresa ativa (ongoing x onboarding x em abertura), processo listado na contagem (e por que não, se não), status na hora, plano, rollout da IA, transferência da IA, grupo esperado x obtido.
3. **Links**: ticket, log da Ultimate, SOCI, processo no admin da Abertura, trilha no Cloud Logging, e o caminho do relatório.
4. Se o drop estiver errado por configuração (status faltando no mapa, IA usando outro critério), dizer o que mudar e onde (dialogue builder / `roteamento.json` / nota do vault).

Códigos do veredito automático: `OK` (bateu com o drop), `OK_VIA_IA` (IA atendeu e transferiu para o grupo do drop), `OK_IA` (ainda na AIDA, como esperado pelo rollout/BP), `IA_INESPERADA` (na AIDA sem estar no rollout), `RETORNO_ATIVO`, `FORA_DA_ATIVACAO` (empresa ativa → menu completo), `DIVERGENTE`, `SEM_DADOS`. O código é ponto de partida, não o veredito: a palavra final vem do status no changelog e do log da conversa.

## Por que não teve IA

Quando a pergunta for sobre a ausência da IA, o script traz a nota "Sem IA" com o motivo:
- O fluxo do ativo escalou direto, sem passar pela Ativação Inbound.
- A empresa está ativa e o cliente caiu no menu completo.
- O cliente Experts ficou fora do sorteio do rollout (a sessão começou depois do segundo 24).
- O plano é BP sem IA, o que é inesperado.

No retorno de CSAT sem CNPJ, a nova identificação passa por um Init session, que recarrega a config e refaz o sorteio. Por isso vale o segundo da **última** checagem de ativo antes do ticket, não o do envio da pesquisa.

## Armadilhas

- **Transferência que não ficou**: mais de uma transferência saindo do mesmo grupo e o ticket de volta nele indica que algo devolveu o grupo, provavelmente um gatilho do Zendesk pelas tags `sys_grupo_*` que o bot gravou. Confirmar no histórico de eventos (BigQuery, D-1) antes de afirmar.
- **Duas respostas de tema** (ex: "Novo assunto" e logo depois "Mesmo tema"): o bot segue a primeira; a segunda cai na sessão nova.

- **Estado atual x estado na hora**: empresa, processo, plano e status vêm das rotas de hoje. Tickets antigos exigem o changelog do SOCI; a trilha do load balancer fica 30 dias.
- **POSTs não aparecem na trilha** (buscar-por-telefone, consulta CNPJ): o telefone vai no corpo. A trilha mostra os GETs (ativo, contagem, dados, flags, opt-out, serviços por CNPJ). A ausência de contagem/dados com chamadas por CNPJ indica ramo de empresa ativa.
- **Início da conversa estimado** pela primeira checagem de ativo da sessão; a config que sorteia o rollout roda logo antes, então o segundo pode errar por 1 s perto do limite (24/25).
- **Telefone com BSUID** (`BR.xxx`) ou ticket sem `requester_phone`: passar o telefone à mão não é suportado; usar a tag `telefone:` do ticket ou pedir ao usuário.
- **Mais de um processo**: o bot usa o primeiro da contagem; a tag `processo_id:` do ticket mostra qual ele usou.
- **Mapa mudou**: ao alterar os drops no dialogue builder, atualizar `scripts/roteamento.json` e `ultimate/roteamento-n1-ativacao-soci.md`.
- Os relatórios têm telefone, CNPJ e conversa do cliente: ficam em `~/Downloads`. Só compartilhar se o usuário pedir.
