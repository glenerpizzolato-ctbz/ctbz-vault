---
name: monitor-mensagens-sistema-indisponivel
description: "O MonitoramentoMensagensSistemaIndisponivelService do atz-worker-webhooks: loga quando o cliente recebe uma mensagem de erro do bot, mas só reconhece textos fixos (case-sensitive); e as linhas NotificarAgente* como fonte das mensagens do bot"
metadata:
  type: reference
tags:
  - atendimento-zendesk
  - ultimate
  - sunshine
---

# Monitor de mensagens de sistema indisponível

O `MonitoramentoMensagensSistemaIndisponivelService` (`src/domain/fila-atendimento/services/monitoramento-mensagens-sistema-indisponivel/`) roda no consumer de conversas do `atz-worker-webhooks-prd`, que recebe os webhooks do Sunshine. Para cada mensagem de texto, ele procura com `includes` um destes textos fixos e, se achar, faz `logger.error` com `Cliente recebeu a mensagem de erro: <TIPO> - conversationId '<sunshine>' - <texto>`:

| Tipo | Texto procurado |
|---|---|
| `ERRO_TRANSBORDO_HUMANDO` | "Não consegui te conectar a nossa equipe, o sistema temporariamente indisponível..." |
| `ERRO_NAO_AUTENTICADO_PLATAFORMA` | "Olá! Não foi possível autenticar você em nosso chat." |
| `ERRO_REQUISICAO_API_BOT` | "Sistema temporariamente indisponível. Por favor, tente novamente em alguns minutos." |
| `FALLBACK_REQUISICAO_API_BOT` | "O sistema temporariamente indisponível..." |
| `FALLBACK_SELECAO_BOT` | "Estamos enfrentando instabilidades no momento..." |

> [!WARNING]
> O `includes` diferencia maiúsculas e exige o texto exato. No incidente de 2026-11-03, só o `ERRO_REQUISICAO_API_BOT` disparou (4.008 vezes). As variantes "Olá, sistema temporariamente indisponível…", "O sistema está temporariamente fora de serviço…" e "Estamos enfrentando uma instabilidade nos nossos canais…" não batem com nenhum texto e não aparecem no monitor. Ao trocar o texto do fallback na Ultimate, atualizar essa lista.

Fonte mais completa no mesmo worker: as linhas `NotificarAgenteNovaMensagemService` e `NotificarAgenteAtualizacaoTicketService` logam um JSON com `sunshineConversationId`, `textoUltimaMensagemAgenteOuBot` e, quando há ticket, `ticketId`, `nomeGrupo` e o nome, telefone e e-mail do solicitante. Elas pegam qualquer texto do bot, inclusive o do chat web. A skill `mapear-erros-ultimate` usa as duas fontes (ver [[eventos-de-erro-ultimate]]).
