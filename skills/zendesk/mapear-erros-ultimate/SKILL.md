---
name: mapear-erros-ultimate
description: Mapeia as conversas de WhatsApp que caíram em erro nos bots da Ultimate (Zendesk AI agents) num período e gera um CSV por bot, com o cenário de cada conversa (sem resposta, bot voltou, atendido por humano), o tipo de erro (Technical Error / Action Failed), qual versão da mensagem de erro o cliente recebeu e como identificar o cliente (telefone, CNPJ, ticket, sunshineUserId, BSUID, link da conversa na Ultimate). Cruza os eventos do ultimateai-webhook e os logs do atz-worker-webhooks (que pegam também o chat web e o que o webhook perde) com o Sunshine Conversations. Use quando o usuário pedir para levantar/mapear/listar os clientes ou conversas afetados por um incidente, instabilidade ou fallback da Ultimate, ou atualizar esse levantamento.
argument-hint: "<desde (UTC)> [ate (UTC)] [bots: main|fina + avisos|survey|trial|ouvidoria] [saida]"
---

# Mapear as conversas afetadas por erros da Ultimate

O script `scripts/mapear_erros.py` faz tudo em uma execução:

1. Lê os eventos de erro do Cloud Run `ultimateai-webhook` (projeto `atendimento-canais-prd`) no período: `Technical Error`, `Action Failed` e `API Integration ...`. Cada evento traz o bot, o `conversationId` da Ultimate e o `platformConversationId`, que é a conversa no Sunshine. Os eventos de teste são ignorados.
2. Lê também os logs do `atz-worker-webhooks-prd` (projeto `contabilizei-prod-01`), que recebe os webhooks do Sunshine e não depende da Ultimate. Entram as linhas `NotificarAgente…`, com a última mensagem do bot e os dados do ticket, e as do monitor `MonitoramentoMensagensSistemaIndisponivelService`, desde que o texto do bot tenha cara de erro. Essa fonte pega o chat web (`chat main`, sem webhook) e as conversas de WhatsApp que o webhook perde: em 2026-11-03, foram ~1,8 mil a mais. `--so-webhook` desliga essa fonte.
3. Busca cada conversa no Sunshine (`api.smooch.io`) com as credenciais da cloud function `zendeskbot-config`, pela função `gcloud_function` do `bots_api.py` da skill `buscar-empresas-por-telefone`. As credenciais ficam só em memória e nunca são exibidas. O resultado vai para o cache em `~/.cache/mapear-erros-ultimate/`, e uma conversa só é buscada de novo quando teve evento depois da última busca.
4. Detecta as **versões da mensagem de erro** a partir dos próprios dados. O texto que o bot manda até 40 s depois de cada evento é agrupado, e vira variante (`V1..Vn`, na ordem em que apareceu) o texto que saiu pelo menos 3 vezes, em 60% ou mais dos casos depois de um erro, e que tem cara de erro ("indisponível", "instabilidade", "fora de serviço", "tente novamente" etc., na regex `ERROR_HINT`) ou saiu pelo menos 50 vezes depois de erro. Sem essa trava, a saudação de bots com pouco volume, como `ouvidoria` e `fina + avisos`, vira falsa variante. Assim, mudanças no texto do fallback ao longo do incidente aparecem sozinhas. As variantes servem só para contar os erros e classificar o cenário: o script as imprime, mas não separa a planilha por versão (decisão do Glener em 2026-11-03).
5. Grava `<saida>.csv`, a planilha com uma linha por conversa **agrupada por bot**: o bot com mais conversas vem primeiro e, dentro de cada bot, as conversas com mais erros. A partir daí, aplicar filtros no Sheets ou no Excel.
6. Grava `<saida>-resumo-por-bot.csv`, com uma linha por bot e uma linha `TOTAL`:
    - Conversas afetadas e clientes únicos.
    - Mensagens de erro recebidas, conversas com 1 erro, com **mais de 1 erro** (e o percentual), com 3 ou mais, e o máximo numa conversa. O "erro" é a mensagem de erro que o cliente viu: um mesmo erro gera vários eventos na Ultimate, então os eventos não servem para contar.
    - Divisão por tipo: só `Technical Error`, só `Action Failed`, os dois, ou sem evento na Ultimate. Também o total de eventos de cada tipo.
    - Canal, fonte e cenários.

## Como rodar

```bash
python3 -I ~/.claude/skills/mapear-erros-ultimate/scripts/mapear_erros.py --since 2026-11-03T09:00:00Z [--until 2026-11-03T18:00:00Z] [--bots main,ouvidoria] [--out ~/Downloads/arquivo.csv] [--refresh]
```

- `--since` e `--until` são em **UTC**: BRT + 3h. Sem `--until`, vai até agora.
- `--bots` aceita o nome curto (`main`, `fina + avisos`, `survey`, `trial`, `ouvidoria`), o nome completo ou o id. Sem ele, entram todos os bots com eventos.
- A saída padrão é `~/Downloads/ultimate-erros-<data>.csv`.
- Volume: o Sunshine limita a taxa, e com 8 threads o ritmo fica entre ~100 e ~300 conversas por minuto. Para milhares de conversas, rodar em background. Uma segunda execução aproveita o cache.

## Bots

| Bot (nome no log) | id (dashboard) |
|---|---|
| `[prod] ctbz wpp main` | `66c6220557465548f3ff0d6e` |
| `[prod] ctbz wpp fina + avisos` | `693ffec1181a1a7f14d05c18` |
| `[prod] ctbz wpp survey` | `673c0518f9cf7058160ec9ae` |
| `[prod] ctbz wpp trial` | `693ffe9b7e0f42bd5e15a973` |
| `[prod] ctbz wpp ouvidoria` | `68289a56392101722adee8da` |
| `[prod] ctbz chat main` | `66bf4a1be43522b403cd876b` |

`[prod] ctbz fallback` e `[prod] ctbz wpp avisos` também existem no dashboard, mas não são usados e ficam fora.

Bot de cada conversa:
- Quando o webhook registrou a conversa, vale o bot que ele informa.
- Quando a conversa só aparece nos nossos logs: se o canal é web, o bot é o `chat main`, que não tem webhook de alertas configurado. Se é WhatsApp, o bot é o mesmo das outras conversas da mesma integração (`origin_source_integration`). Sem como deduzir, fica `desconhecido (<canal>)`.

Bot novo: adicionar o nome e o id no dicionário `BOTS` do script.

## Colunas do CSV

- **Bot e origem:** `bot`, `canal` (`whatsapp`/`web`) e `fonte` (`webhook_ultimate`, `log_atendimento` ou `ambos`).
- **Cenário (`cenario`):**
  - `sem_resposta_apos_erro`: a última resposta do bot foi a mensagem de erro e nenhum humano respondeu. É a lista de recontato.
  - `erro_sem_mensagem_de_fallback`: houve erro, mas nenhuma das variantes foi enviada.
  - `bot_voltou_a_responder`: o bot voltou ao fluxo normal depois do erro.
  - `atendido_por_humano_apos_erro`.
- **Erro:** `tipo_erro_ultimate` (`sem_evento_na_ultimate` quando a conversa só aparece nos nossos logs), `qtd_technical_error`, `qtd_action_failed`, `primeiro_erro_utc` e `ultimo_erro_utc`. `Technical Error` é erro da plataforma. `Action Failed` é uma action do bot que falhou, que pode ser a nossa API ou a própria Ultimate (ver a nota `eventos-de-erro-ultimate` no vault).
- **Erros e mensagens:** `qtd_erros_recebidos` (mensagens de erro que o cliente recebeu), `mais_de_1_erro` (`sim`/`nao`), `qtd_msgs_cliente_no_periodo_do_erro` (tentativas do cliente), `ultima_msg_cliente_utc` e `ultima_msg_cliente`.
- **Identificação do cliente:**
  - `telefone`: o número real, vindo do campo de telefone do Zendesk no metadata e, na falta dele, do client do WhatsApp.
  - `whatsapp_bsuid`: o `BR.xxx` que a Meta manda no lugar do telefone, que às vezes aparece também na tag `telefone:`.
  - `cnpj`, `carteira`, `zendesk_ticket_id`, `grupo_zendesk`, `nome_solicitante`, `email_solicitante` e `nome_whatsapp`. No chat web não há telefone do WhatsApp: a identificação fica por `sunshine_user_id`, o telefone e o e-mail do solicitante do ticket e o CNPJ.
  - `sunshine_conversation_id`, `sunshine_user_id` e `sunshine_whatsapp_client_id`.
- **Estado e links:** `controle_atual` (quem controla a conversa no switchboard agora), `ultimate_conversation_ids` e `link_ultimate`.

## Depois de rodar

- Mostrar ao usuário o resumo que o script imprime (conversas por bot, com mais de 1 erro, por cenário e por tipo de erro) e o caminho dos dois CSVs (a planilha e o resumo por bot).
- O CSV tem telefone e CNPJ de clientes: fica na máquina do usuário. Só publicar ou enviar para outro lugar se ele pedir.
- Para importar no Google Sheets, desmarcar "Converter texto em números, datas e fórmulas", senão telefone e CNPJ viram número.
- Limitações: os logs do `atz-worker-webhooks` só registram as conversas que o worker processa, então o resultado é bem mais completo que o do webhook, mas não há garantia de que pegue tudo. Para as conversas que só aparecem nesses logs, não há `link_ultimate`, porque o log não traz o id da conversa na Ultimate. O Sunshine devolve as últimas 100 mensagens de cada conversa. Numa conversa muito longa depois do incidente, as mensagens de erro podem ficar de fora.
