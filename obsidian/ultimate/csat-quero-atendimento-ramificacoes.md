---
name: csat-quero-atendimento-ramificacoes
description: "Destinos do botão \"Quero atendimento\" no reply Wpp Exp | CSAT v19 (bot wpp main prd): FUP de transbordo → Business Hours; retorno de CSAT → HUMAN_CP/ReRoute, mesmo tema x novo assunto, contagem de empresas, acesso Experts e concierge. Como ler o dialogue builder pela API"
metadata:
  type: reference
tags:
  - ultimate
  - csat
  - roteamento
---

# CSAT: ramificações do "Quero atendimento"

Reply `Wpp Exp | CSAT v19 | 172747 from 168648 | feat: csat contador parceiro` (`6adba7e9a1a30f11f3f0b61d`), bot `[prod] ctbz wpp main` (`66c6220557465548f3ff0d6e`). Versão publicada lida em 2026-11-17 (publicada em 2026-11-13 pelo Rafael Maestro). Diagrama: https://claude.ai/artifact/AVAA9SH74qDjywA3phKz49

## Resumo para apresentar

Dois caminhos vão para IA, sem passar pela validação de horário: `HUMAN_CP` (contador parceiro) → `Escalate | ReRoute Ticket - Wpp Shared`, que também é uma IA; e o Concierge Experts (grupo `29190745372444`): retorno de CSAT, não é `HUMAN_CP`, novo assunto (ou mesmo tema sem empresa localizada), empresa com acesso Experts e flag `allow_concierge_experts`. Todos os outros destinos (Business Hours Outbound, Init session, reautenticação) passam pela validação de horário comercial e caem no Corujão, segundo o usuário em 2026-11-17.

## Onde o botão aparece

O nó raiz chama `[bots-api] GET | Flags via Tags injection`, checa `started_at_root` e ramifica por `csatTemplate`. "Quero atendimento" existe em dois pontos:

- **Retorno de CSAT** (`csat_retorna_atendimento_0`, botões Sim / Não / Quero atendimento).
- **Follow-up de transbordo** (`follow_up_transbordo_atendimento_3` e `fup_csat_sla_16`, botões Está tudo certo / Quero atendimento).

## Destinos

- **FUP**: tag `CSAT FUP Option 3`, `sysFluxoGlobalID = CSAT_FUP_ESCALATE` → `Pointer | Business Hours Outbound - Wpp Exp [d]`.
- **Retorno de CSAT**: tag `sys_metric_csat_return_to_service`, `PATCH | CSAT - Atualiza Pesquisa - Ignorar` (qualquer resultado segue), depois:
  - `csatSource` contém `HUMAN_CP` (contador parceiro) → `Escalate | ReRoute Ticket - Wpp Shared`.
  - Senão pergunta "mesmo tema ou novo assunto":
    - **Mesmo tema**: com CNPJ (`csatAtivoPossuiCnpj`) → `[pltf-crm] GET | consulta CNPJ`; sucesso → Business Hours Outbound; falha → checagem de acesso Experts. Sem CNPJ → reautenticação (abaixo).
    - **Novo assunto**: sem CNPJ → `Pointer | Init session - Wpp Shared [d]`. Com CNPJ → `count CNPJs`: falha ou 0 empresas (depois de checar telefone internacional) → Init session; 2+ → pergunta "Empresa atual / Outra empresa" (outra → Init session); 1 ou empresa atual → consulta CNPJ → checagem de acesso Experts.
    - Resposta inválida 2x em qualquer pergunta → `Escalate | CSAT - Wpp Exp [C]` (`CSAT_LIMITE_ULTRAPASSADO`).
  - **Checagem de acesso Experts** (`possuiAcessoExperts`): sim e `FLAGS_V2` com `allow_concierge_experts` → transbordo direto para o grupo `29190745372444` (Concierge Experts) com tag `sys_atendimento_ia`; sim sem a flag → Business Hours Outbound (`ESCALATE_ASSESSORES_HUBS`); não → `jaAutenticouEmAtivoCsat = 1` e, com CNPJ, `Pointer | Id Empresa Auth - Wpp Shared`, sem CNPJ, `Wpp Shared | Id Ativacao v13`.

## Como ler o fluxo sem clicar no canvas

Com a página do dialogue builder aberta (sessão logada), o JSON completo da versão sai por `fetch` na própria origem:

- `POST /ai-agents/dashboard/api/dialog/latest-version` com `{botId, replyId}` → `nodes[]` (`type` `text`/`condition`/`integration`, `conditionData.conditions[].next.ref`, `integrationData.answerNodes[]`, `answerOptions[]` dos botões).
- `POST /ai-agents/dashboard/api/action/read-list` e `integration/read-list` com `{botId}` → nomes das ações e integrações pelos ids.
- `GET /ai-agents/dashboard/api/replies?botId=...&limit=5000` → nome dos replies apontados por `next.type == "reply"`.

O retorno do `javascript_tool` corta em ~1000 caracteres, então compactar os nós no navegador e ler em fatias.
