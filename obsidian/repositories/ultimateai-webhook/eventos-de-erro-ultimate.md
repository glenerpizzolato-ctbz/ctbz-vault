---
name: eventos-de-erro-ultimate
description: "Como ler os eventos de erro da Ultimate no log do ultimateai-webhook (Technical Error x Action Failed x API Integration) para separar falha da plataforma Zendesk de falha das nossas APIs"
metadata:
  type: reference
tags:
  - ultimateai-webhook
  - ultimate
  - incidente
---

# Eventos de erro da Ultimate no ultimateai-webhook

O Cloud Run `ultimateai-webhook` (projeto `atendimento-canais-prd`) recebe os eventos da Ultimate e loga cada um com `jsonPayload.message="ultimateai_event"`, `jsonPayload.event`, `jsonPayload.bot` (ex: `[prod] ctbz wpp main`, `fina + avisos`, `survey`, `ouvidoria`) e `conversationId`. Os de erro saem com `severity=ERROR`.

- `Technical Error`: erro interno da plataforma Ultimate/Zendesk. Em dia normal é zero; quando dispara em todos os bots (inclusive o `survey`, que não chama nossas APIs), o problema é da Zendesk.
- `Action Failed`: uma ação do bot falhou, normalmente uma chamada às nossas APIs (atendimento-zendesk → crm-web/fintech etc.). Baseline: 0 a 3 por hora.
- `API Integration`: falha pontual de integração; aparece de forma esporádica.

Consulta para contar por bot e evento:

```bash
gcloud logging read 'resource.labels.service_name="ultimateai-webhook" AND severity>=ERROR AND timestamp>="<início>"' --project atendimento-canais-prd --limit=5000 --format='value(jsonPayload.bot,jsonPayload.event)' | sort | uniq -c | sort -rn
```

Os 500 do nosso lado aparecem em `atendimento-zendesk-prd` e `atz-worker-*` (namespace `crm-prd`, logs em `contabilizei-prod-01`), com `AllExceptionsFilter ... status 500` e `VerificarClienteElegivelOuvidoriaService`.

## Caso de referência: 2026-11-03

Duas frentes ao mesmo tempo: o enum novo `PagtoPlanoSegmento.PRECOS_2027` em 8 planos (só o default 5-0-333 conhecia o valor, os demais serviços quebravam com `IllegalArgumentException`) e um incidente da Zendesk nos AI Agents (status às 07:58 BRT). No webhook, `Technical Error` começou às 11:10Z (08:10 BRT, junto com o incidente da Zendesk) e chegou a ~2.100 em 30 min (~95% dos erros). Já `Action Failed` (~110/h, do baseline de ~1/h) foi o reflexo do nosso lado: 500 em ouvidoria, timeline, `bots/chat/temas` (BANK) e whatsapp-ativo.

## Mapear os clientes afetados

O log do webhook não traz o telefone, só o `conversationId` (Ultimate) e o `platformConversationId` (Sunshine), e o `data` vem vazio. Para listar os clientes afetados: baixar os eventos do bot com `gcloud logging read ... --format=json`, agrupar por `platformConversationId` e consultar o Sunshine de cada conversa (ver [[sunshine-identificar-cliente]]). As mensagens de erro que o bot enviou (o fallback) aparecem nas mensagens da conversa, e servem para separar as versões do texto.

Em 2026-11-03, no `[prod] ctbz wpp main`, o texto de erro mudou ao longo do dia:

| Versão | Texto (início) | Período (UTC) | Evento |
|---|---|---|---|
| V0 | "Sistema temporariamente indisponível..." (sem "Olá") | 10:49 em diante | `Action Failed` (fallback das actions) |
| V1 | "Olá, sistema temporariamente indisponível..." | 11:17–12:33 | `Technical Error` |
| V2 | "Olá! Nosso atendimento pelo WhatsApp está temporariamente indisponível..." (com os e-mails) | 12:34–12:39 | `Technical Error` |
| V3 | "Estamos enfrentando uma instabilidade nos nossos canais..." | 12:40 em diante | `Technical Error` |

No caso conferido (`1a1c6bee...`), o `Action Failed` não gerou nenhuma chamada às nossas APIs nos logs: a action falhou do lado da Ultimate.

## Cobertura do webhook (o que fica de fora)

- O dashboard tem 8 bots: `chat main`, `fallback`, `wpp avisos`, `wpp fina + avisos`, `wpp main`, `wpp ouvidoria`, `wpp survey` e `wpp trial`. `fallback` e `wpp avisos` não são usados (confirmado pelo Glener em 2026-11-03) e podem ser ignorados. Até 2026-11-04, o `chat main` não mandava nenhum evento ao `ultimateai-webhook`. Em 2026-11-04 não havia nenhum `unauthorized_request` nem `bot="unknown"` em 30 dias, ou seja, ele nunca tentou chamar o webhook. A causa era o webhook do bot estar **desativado** na Ultimate. Em 2026-11-04 o Glener ativou, salvou e disparou o "Test webhook", e às 18:31Z chegou `Test Event` do `[prod] ctbz chat main` (200, com o token já aceito, sem mudar secret nem código). Armadilha: o "Test webhook" só chega depois de ativar e **salvar**; um teste antes de salvar não manda nada. Para conferir qualquer bot, procurar `jsonPayload.event="Test Event"` (INFO) ou `unauthorized_request` no log. Como complemento que independe da Ultimate, dá para criar uma métrica de log sobre o `MonitoramentoMensagensSistemaIndisponivelService` do `atz-worker-webhooks-prd` (o `ERRO_NAO_AUTENTICADO_PLATAFORMA` é o erro típico do chat web, ver [[monitor-mensagens-sistema-indisponivel]]).
- Nos bots configurados, o webhook perde pouco. Em 2026-11-03 (09:00Z–15:00Z), a skill `mapear-erros-ultimate` juntou as duas fontes e achou 6.904 conversas com erro. Dessas, 866 eram do chat web (`chat main`, sem webhook) e só 87 de WhatsApp apareceram nos logs do `atz-worker-webhooks-prd` sem evento no webhook (81 do `main` e 6 do `fina + avisos`). Uma contagem anterior, de 1.832 conversas faltando, estava errada: o `cut -d,` usado na comparação quebrou nas vírgulas dentro dos campos do CSV. Para comparar colunas de CSV, usar um parser (`csv` do Python), nunca `cut`.
- Fonte alternativa, que independe da Ultimate: as linhas `NotificarAgente...Service` do `atz-worker-webhooks-prd`, que trazem `sunshineConversationId`, `sunshineUserId`, `ticketId`, `nomeGrupo`, o telefone e o e-mail do solicitante e `textoUltimaMensagemAgenteOuBot`. Buscar pelo texto das mensagens de erro: `resource.labels.container_name="atz-worker-webhooks-prd" AND ("temporariamente indispon" OR "instabilidade" ...)`.

## Textos completos da contingência de 2026-11-03

O V1 ("Olá, sistema temporariamente indisponível. Por favor, tente novamente em alguns minutos.") era o **texto padrão** da mensagem de erro global dos bots de WhatsApp, e não uma mudança. As trocas de contingência (revertidas no PRD-175013) foram:

- Erro global (principal, financeiro e avisos, pesquisa): V2 às 09:34 BRT ("Olá! Nosso atendimento pelo WhatsApp está temporariamente indisponível. Para falar com a gente agora, envie um e-mail contando o que você precisa: Clientes do plano Expert: atendimento.experts@contabilizei.com.br / Demais planos: suporte@contabilizei.com.br. Pedimos desculpas pelo transtorno.") e V3 às 09:40 ("Estamos enfrentando uma instabilidade nos nossos canais de atendimento, causada por uma indisponibilidade global do sistema que utilizamos. Por isso, nosso retorno pode levar mais tempo que o habitual. Pedimos desculpas pelo transtorno e estamos acompanhando a situação para restabelecer o atendimento o quanto antes.").
- Chat web: o padrão "Olá! Não foi possível autenticar você em nosso chat." virou "Olá! Não conseguimos confirmar sua autenticação neste momento. *Para tentar novamente, basta enviar uma nova mensagem aqui no chat*. Se o problema continuar, estamos à disposição pelo e-mail suporte@contabilizei.com.br (...)".
- Ponteiro de inatividade desligado às 09:50 nos três bots de WhatsApp.

Os textos completos que o bot mandou saem do campo `textoUltimaMensagemAgenteOuBot` das linhas `NotificarAgente*` do `atz-worker-webhooks-prd` (`gcloud logging read ... --project contabilizei-prod-01`). Incidente documentado no IP-4361 (ver [[processo-incidentes-ip]]).
