---
name: retorno-ativo-plano-sem-whatsapp
description: "O que acontece quando um cliente de plano sem WhatsApp (Básico) responde a um ativo: o envio barra o plano só com cnpj; nos bots main e fina + avisos da Ultimate o ativo é consultado antes da checagem de plano, então o retorno é encaminhado (IA ou humano) sem olhar o plano"
metadata:
  type: reference
tags:
  - mensagem-ativa
  - whatsapp-ativo
  - ultimate
sistemas:
  - atendimento-zendesk
  - ultimate
conferido_em: 2026-11-13
---

# Retorno de ativo de cliente sem WhatsApp no plano (Básico)

Conferido em 2026-11-13 no dashboard de prd da Ultimate (só leitura, com aprovação do Glener), no `atendimento-zendesk` (`origin/master` 95587b09f), nos logs de prd e no banco de prd (só leitura). O mapa nó a nó está no repo `ultimate-as-a-code`, em `docs/flows/prd/mensagem-ativa.md` (veja [[_ultimate-as-a-code-indice]]).

## Resposta curta

- **No envio**, o `atendimento-zendesk` barra o Básico (`PlanoInelegivelException`, exceto autopilot ou comércio) **só quando o ativo vai com `cnpj`** e a categoria não é `ATIVACAO_MIGRACAO`. Todo caminho de envio (individual, enfileirar, massivo, legacy) passa por `ValidarWhatsappAtivoService.validar` no worker. "Forçar" o envio a um Básico, na prática, é mandar sem `cnpj` (só telefone, ou `processoAberturaId`) ou com `ATIVACAO_MIGRACAO`.
- **No retorno**, os dois bots consultam o ativo pendente logo depois do init, **antes** da identificação da empresa e da checagem de plano. Se há ativo válido para o telefone, o cliente é encaminhado sem o bot olhar o plano.
- **Bot main**: com ativo `CORE`, o cliente precisa clicar em **"Responder mensagem"** e cai em `Default Ultimate Bot - [Chat][WhatsApp] [BP]` com as tags do ativo, que levam ao grupo do disparo (humano ou AIDA, conforme o grupo). Se clicar em "Novo assunto", vai para a identificação e recebe "Seu plano atual não possui atendimento via WhatsApp…". Ativos especiais (CSAT, Jump, Workflows, CSA, ATIVACAO_MIGRACAO) e Experts também não checam plano. A exceção é o `INBOUND` com grupo diferente de `AIDA Geral [WhatsApp] [BP]`: ele volta para o `Journey router`, onde o Básico é bloqueado.
- **Bot fina + avisos**: com ativo `FINANCEIRO`, vai para a AIDA Cobrança Entrada (se `HOUR_IA_24_7`) ou para a Cobrança Entrada humana, conforme o horário. Com ativo `AVISOS`, vai para a `AIDA Geral [WhatsApp] [BP]`. Esse bot **não tem bloqueio de plano em nenhum caminho**: até sem ativo, depois da identificação, ele escala para a AIDA Geral.

## O ativo só vale se

O bot chama `GET bots/whatsapp/mensagem/ativa?telefoneCliente=…&fluxo=…` (main: `ESPECIAIS`, `EXPERTS`, `CORE`; fina + avisos: `FINANCEIRO`, `AVISOS`; contagem pelos logs do GKE em 12 e 13/11/2026). O `BuscarUltimaMensagemAtivaUseCase` só devolve o ativo que:

- foi para algum dos telefones mapeados do cliente, com `habilitado = true` e dentro da validade (`criado_em + validade_em_minutos`; individual comum vale 1 dia por padrão);
- tem `nome_grupo` cadastrado (`zendesk_grupos` para `CORE`/`BANK`/`BASICO_PADRAO`/`OUVIDORIA`/`CORRETORA`, `mensagem_ativa_grupo` para os demais). **Ativo sem grupo, ou com grupo fora do cadastro, some da resposta**, e o cliente segue o fluxo normal (no main, o Básico é bloqueado).

Não há filtro por plano nem por CNPJ na consulta. Ao usar o ativo, o bot faz o `PATCH` que marca `habilitado = false` e status `RESPONDIDA`. Por isso, numa segunda conversa o cliente já cai no fluxo normal.

## Números e bots

| Integração do ativo | Número (config antiga de prd) | Bot da Ultimate |
| --- | --- | --- |
| `CORE`, `BANK`, `EXPERTS`, `INBOUND`, `JUMP`, `CSA`, `FLOW`, `ATIVOS_WORKFLOW`, `ATIVACAO_MIGRACAO` | Main | `[prod] ctbz wpp main` |
| `FINANCEIRO` | Financeiro | `[prod] ctbz wpp fina + avisos` |
| `AVISOS`, `RESERVA` | Avisos | `[prod] ctbz wpp fina + avisos` |

O dashboard mostra o fina + avisos como `building`, mas ele recebe conversas em prd (eventos no `ultimateai-webhook` em 2026-11-13). Antes, o id `693ffec1181a1a7f14d05c18` se chamava "wpp ativacao" (ainda aparece assim na coleção Bruno `ultimate-ai-api`).

## Grupos de escalonamento

| Id | Grupo |
| --- | --- |
| `15262373080476` | Default Ultimate Bot - [Chat][WhatsApp] [BP] |
| `22427993443100` | AIDA Geral [WhatsApp] [BP] |
| `29189206029596` | AIDA Cobrança Entrada - [WHATSAPP] |
| `29189117065244` | Cobrança Entrada - [WHATSAPP] |
| `29190745372444` | Concierge Experts [EXPERTS] |
| `15409966479388` | Hour Holiday [WhatsApp] |
| `15409943127580` | Hour Closed [WhatsApp] |

Nomes vindos de `zendesk_grupos` (banco `prd_crm_atendimento_zendesk`).

## Não conferido

- Quais tags as actions dos nós de escalonamento aplicam e se os gatilhos do Zendesk movem o ticket do grupo do bot para o grupo do disparo.
- Se o `getReply` devolve rascunho ou versão publicada (relevante para o fina + avisos, que está `building`). Para fechar, testar no simulador ou com um ativo de teste em dev.
