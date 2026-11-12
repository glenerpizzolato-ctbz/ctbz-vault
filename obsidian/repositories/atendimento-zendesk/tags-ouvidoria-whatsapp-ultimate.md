---
name: tags-ouvidoria-whatsapp-ultimate
description: "De onde vêm as tags de ouvidoria num ticket de WhatsApp do bot [prod] ctbz wpp main: sys_grupo_bot_ouvidoria vem do roteamento de tema (Bank 'Reclamação/Elogio'), sys_reclamacao/elogio/sugestao_ouvidoria_exp só do diálogo de Feedback Experts e sys_direcionado_ouvidoria_exp de gatilho do Zendesk"
metadata:
  type: reference
tags:
  - atendimento-zendesk
  - ultimate
  - ouvidoria
  - whatsapp
---

# Tags de ouvidoria no WhatsApp (Ultimate `[prod] ctbz wpp main`)

Levantado em 2026-11-11 a partir da conversa `3710d0fe-4e8b-4077-9b61-5565c1054341` (ticket 30187418, 04/11/2026, cliente Experts Essencial).

## Quem seta cada tag

| Tag | Quem seta | Quando |
| --- | --- | --- |
| `sys_grupo_bot_ouvidoria` | Ultimate, ação `updateConversation > key:tags value:{{dataRoteamentoTags}}` | Vem **dinâmica** da API de roteamento do atendimento-zendesk, conforme o tema escolhido. Também é tag fixa no bot `[prod] ctbz wpp ouvidoria` (ação "add tag grupo ouvidoria"). |
| `sys_reclamacao_ouvidoria_exp`, `sys_elogio_ouvidoria_exp`, `sys_sugestao_ouvidoria_exp`, `sys_trocaasessor_ouvidoria_exp` | Ultimate, ações `[TAG] Feedbacks … Ouvidoria` (`addConversationTags`) | Só no diálogo `Wpp Exp \| Feedback Business Hour v03` (intent `Wpp Exp \| Feedback Business Hour [A] [B] [E]`), o menu de feedback do fluxo **Experts**. Nenhum outro bot usa essas ações. |
| `sys_direcionado_ouvidoria_exp` | Gatilho do Zendesk (`via: Rule`) | Não existe em nenhum bot nem integração da Ultimate. Nos audits de 01/10 a 10/11/2026 aparece em 56 tickets via `Rule`, sempre junto das tags `_ouvidoria_exp` que chegaram via WhatsApp: é consequência delas. |
| `sys_super_ouvidoria_analise_habilitada` | sentinela-atendimento (`via: Web service`) | Ver [[super-ouvidoria-tags-observabilidade]]. |

## Integrações do roteamento por tema (fluxo Bank/Corretora)

- **`Contabilizei - Validar seleção tema`** (`66901ef6c2932ebcec885a00`): `POST {{apigatewayUrl}}/atendimento/zendesk/bots/whatsapp/fluxo/interacao/api/v1/bots/whatsapp/temas/basico-padrao/texto/validar-opcao-selecionada` com `{opcaoSelecionada, cnpj, telefone}` → `idOpcaoSelecionada`, `opcaoValida`.
- **`Contabilizei - Bank/Corretora - Buscar roteamento`** (`66d77ec62d51c15b26520469`): `GET …/temas/basico-padrao/roteamento?cnpj&telefone&id={{idOpcaoSelecionada}}` → `dataRoteamentoTags`, `dataRoteamentoIdExternoGrupo`, FAQ e autoatendimento. As tags e o grupo vêm do cadastro de temas/subtemas do atendimento-zendesk (banco), não da Ultimate.
- No menu do **Bank** ("Conta PJ"), a opção `5 - Reclamação/Elogio` é o tema id `762`; o roteamento devolve `["sys_grupo_bot_ouvidoria","cnpj:…","telefone:…"]` e o grupo `20122706111516` (`Ouvidoria [Whatsapp] [Ouvidoria]`, `tipo_fluxo: OUVIDORIA`, o mesmo de `APP_SERVICES_ZENDESK_OUVIDORIA_WHATSAPP_GROUP_ID`).

## Por que um Experts sai com `sys_grupo_bot_ouvidoria` e sem as `_ouvidoria_exp`

O cliente escolheu "Conta PJ" no menu inicial (`[SET] URA FLOW BANK`), viu os temas do Bank e escolheu "Reclamação/Elogio". Esse caminho é genérico (integrações acima) e transfere direto para a Ouvidoria só com a tag do roteamento. O diálogo de Feedback do Experts, que é o único que seta `sys_reclamacao/elogio/sugestao_ouvidoria_exp` (e por consequência o gatilho põe `sys_direcionado_ouvidoria_exp`), só roda no fluxo Experts/Contabilidade. Ou seja: comportamento esperado da configuração atual, não falha de integração (todas as chamadas retornaram 200/201).

## Como investigar um caso

1. Log da conversa: `POST /ai-agents/dashboard/api/conversation-log/read-by-conversation-id` com `{botId, conversationId}` (rodando no console do dashboard da Ultimate, logado). Os nomes das integrações vêm de `POST /ai-agents/dashboard/api/integration/read-list` (`{botId}`), a definição de uma integração de `integration/read-by-id` (`{integrationId}`), as ações de `action/read-list` e os diálogos de `GET replies/read?limit=5000&botId=…`.
2. Audits do ticket pelo BigQuery (ver [[zendesk-tickets-bigquery]]) para ver o `via` de cada tag (WhatsApp = Ultimate, Rule = gatilho, Web service = API).
3. Cuidado: o `conversationData` do log traz tokens (apigateway, functions, bots) em claro; não copiar para notas nem para respostas.
