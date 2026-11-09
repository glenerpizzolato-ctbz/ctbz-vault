---
name: proposta-ajuste-alerta-ultimate-ip
description: "Proposta (09/11/2026) de qual alerta da Ultimate deve abrir IP automático e com qual limiar, baseada em 40 dias de dados: o Technical error quase não tem ruído, o ruído do chat vem de Falha de integração e Webhook respondendo erro; regra agregada ≥20 em 5 min por 5 min só pegaria o IP-4361"
metadata:
  type: project
tags:
  - incidentes
  - grafana
  - ultimate
  - jsm-ops
---

# Proposta: qual alerta da Ultimate abre IP automático

Contexto: o contact point `ATENDIMENTO CANAIS - V2` já existe (ver [[abertura-automatica-ip-grafana]]). Antes de apontar a regra para ele com P1/P2, o receio é abrir vários IPs por instabilidades pequenas, como os alertas que chegam no chat "Engenharia Canais | Grafana". Proposta para levar ao time antes de mudar qualquer regra. Andamento no [IP-4383](https://contabilizeicontabilidade.atlassian.net/browse/IP-4383).

## De onde vêm os dados

- Métrica `logging.googleapis.com/user/ultimateai_events` (projeto `atendimento-canais-prd`), por `bot` e `event`, minuto a minuto, de 30/09 a 09/11/2026 (40 dias, a métrica começa em 30/09). Puxada pela API do Cloud Monitoring (`timeSeries`, `ALIGN_DELTA` de 60s, `REDUCE_SUM` por `metric.label.bot` e `metric.label.event`) e simulada com janela de 5 min, como o `increase(...[5m])` das regras.
- Histórico real de disparos no Grafana (`/api/v1/rules/history`), que só guarda desde 11/10/2026.

## O que os dados mostram

- **O Technical error não é o alerta ruidoso.** No `[prod] ctbz wpp main`, o pico diário fica em 1 ou 2 erros em 5 min. Passou de 10 só duas vezes em 40 dias: 01/10 das 15:17 às 15:21 (pico 16, 5 min) e o IP-4361 em 03/11 (pico 413 em 5 min, das 08:17 às 11:10). Somando todos os bots, o maior valor fora do incidente foi 17 em 5 min.
- **O ruído do chat vem de outras regras:**
  - `Falha de integração backend por integração (≥10 em 5 min)`: 12 disparos desde 11/10, todos entre 10 e 16 erros, cada um numa integração específica (ex: o de 06/11 às 10:29, integração `69f23ff119a977e1d0a170cd` do wpp main). É instabilidade de uma API chamada pelo bot, não queda da Ultimate.
  - `Webhook respondendo erro (≥20 em 10 min)` (4xx/5xx do Cloud Run `ultimateai-webhook`): 15 disparos desde 11/10, quase todo dia entre 20:35 e 21:30, muitas vezes com o mesmo valor (82). Padrão diário, a investigar (rotina agendada ou chamada recorrente).
  - `Action Failed acima do normal (≥50 em 5 min)` (só chat): pico diário de 1 a 3; passou de 50 só no IP-4361 (1.329 em 5 min). `Falha de escalonamento`: nenhum disparo.
- No IP-4361 os erros técnicos começaram às 08:16 (BRT) e subiram rápido: 10/min às 08:17, 20/min às 08:19, ~30/min a partir de 08:24.

## Simulação de limiares para o Technical error (40 dias)

| Regra | Episódios em 40 dias | 1º disparo em 03/11 |
|---|---|---|
| Atual: ≥10 em 5 min por bot | 2 (01/10 e 03/11) | 08:17 |
| ≥10 em 5 min por bot, sustentado 10 min | 1 (03/11) | 08:26 |
| ≥20 em 5 min por bot, sustentado 5 min | 1 (03/11) | 08:22 |
| ≥30 em 5 min por bot | 1 (03/11) | 08:19 |
| ≥50 em 5 min por bot | 1 (03/11) | 08:20 |
| **Soma dos bots ≥20 em 5 min, sustentado 5 min** | **1 (03/11)** | **08:22** |
| Soma dos bots ≥10 em 5 min, sustentado 5 min | 2 (01/10 por 1 min e 03/11) | 08:21 |

O IP-4361 foi aberto à mão às 08:59, então qualquer opção abriria o IP 35 a 40 minutos antes.

## Proposta

1. **Só uma regra abre IP: Technical error agregado.** `sum(increase(...{event=~"(?i)technical.?error"}[5m]))` **sem `by (bot)`**, condição ≥20, `for: 5m`, label `severity: critical` (P2), apontada para o `ATENDIMENTO CANAIS - V2`. Por que agregada: uma queda da Ultimate atinge vários bots ao mesmo tempo, e a regra por bot abriria um IP por bot (no IP-4361 seriam 2, e o `fina + avisos` oscilou várias vezes entre 10 e 15, o que poderia gerar alertas repetidos). Com uma instância só, um incidente gera um IP. O limiar 20 fica acima do maior valor normal (17) e o `for: 5m` descarta picos curtos como o de 01/10.
2. **As regras atuais continuam no chat, sem abrir IP.** O Technical error ≥10 por bot segue como aviso precoce. Falha de integração, Webhook respondendo erro, Action Failed e escalonamento não abrem IP.
3. **Reduzir o ruído do chat à parte:** Falha de integração com `for: 5m` ou limiar maior; investigar o padrão diário das 20h40 do Webhook respondendo erro antes de mexer na regra.
4. **Implantação em duas fases para não abrir IP por engano:**
   - Fase 1 (cerca de 2 semanas): a regra nova vai para o V2 **sem prioridade P1/P2**, então chega ao JSM Ops como P3 e não abre IP. Conferir com o Gabriel quantos alertas chegaram e se algum seria falso positivo.
   - Fase 2: subir para P2 (`severity: critical` ou `og_priority`, conforme a integração nova ler a prioridade) e fazer um teste controlado de abertura de IP com o Gabriel.
5. **Evitar IP duplicado com o alerta oscilando:** manter `autoClose` desligado no V2 (o alerta continua aberto no JSM Ops enquanto o IP é tratado) ou, se a versão do Grafana suportar, usar "keep firing for" de uns 15 min na regra.

## Riscos e perguntas para o time

- Amostra pequena: só um incidente real em 40 dias. A proposta precisa ser revista quando houver mais histórico.
- Queda isolada de um bot pequeno (survey, ouvidoria, trial) dificilmente soma 20 em 5 min e continuaria só no chat. Aceitamos isso, ou criamos uma regra por bot com limiar próprio?
- Limiar 20 ou 30? P1 ou P2? Quem recebe o IP aberto automaticamente?
- Como a integração nova do JSM Ops lê a prioridade: label `severity` (como as regras de notas) ou `og_priority` com `overridePriority` no contact point (que hoje está desligado no V2)?

## Decisão do time (09/11/2026): abrir IP quando 3 ou mais bots tiverem o problema

- Como só houve um incidente real, a decisão foi seguir com um critério de abrangência: abrir IP quando **3 ou mais bots** tiverem Technical error ao mesmo tempo.
- O limiar por bot tem que ser baixo, porque os bots pequenos têm pouco volume: no IP-4361 o `wpp main` chegou a 413 em 5 min, o `fina + avisos` a 37, mas o `survey` e a `ouvidoria` só a 5 ou 6. Com ≥5 por bot, a regra quase não dispararia no incidente; com ≥2 por bot ela funciona.
- Query validada no próprio Grafana (`/api/ds/query`, datasource Cloud Monitoring, `promQL`): `count(sum by (bot)(increase(logging_googleapis_com:user_ultimateai_events{monitored_resource="cloud_run_revision",service_name="ultimateai-webhook",event=~"(?i)technical.?error"}[5m])) > 1.5)` com condição ≥3 (threshold > 2.5). Nos últimos 35 dias, fora do incidente, nunca passou de 1 bot. Em 03/11 chegou a 4 bots, ficou ≥3 das 08:38 às 10:36 e, com `for: 3m`, dispararia às ~08:41 (18 min antes da abertura manual, mas 24 min depois do alerta atual).
- Limitação: uma queda concentrada no `wpp main` (que tem a maior parte do volume) não dispara essa regra. Se for preciso cobrir esse caso, uma segunda regra de volume (ex: soma dos bots ≥100 em 5 min por 5 min) também pode ir para o V2.
- Armadilha ao testar query no `/api/ds/query` com o datasource Stackdriver: sem o bloco `timeSeriesList` (`projectName`, `crossSeriesReducer: REDUCE_NONE`, `filters: []`) a resposta volta sem frames, mesmo com a query certa.
- Permissão: a conta do Glener é `Viewer` na org, mas tem `alert.rules:write`/`create` na pasta **Experts** (onde estão as regras da Ultimate), então consegue criar e editar regras ali. Contact points continuam só com o DevOps.

## Implantado em 09/11/2026 (fase 1, sem prioridade)

- Grupo novo **"UltimateAI IP automático (every 1m)"** na pasta Experts, criado pelo ruler API (`POST /api/ruler/grafana/api/v1/rules/<folderUID>`) para não reenviar o grupo "UltimateAI Jornada", que continua com as 10 regras de antes. As duas regras apontam para o `ATENDIMENTO CANAIS - V2`, com os mesmos labels das regras OPSGENIE (sem `severity`), `noData: OK`, `execErr: KeepLast`, `repeat_interval: 4h`:
  - [UltimateAI - Technical error em 3+ bots (≥2 em 5 min cada) • IP](https://grafana.ctbz.com.br/alerting/grafana/ag3t0pjywj3eof/view) (uid `ag3t0pjywj3eof`): `count(sum by (bot)(increase(...[5m])) > 1.5)` > 2.5, `for: 3m`.
  - [UltimateAI - Technical error em volume (soma dos bots ≥100 em 5 min) • IP](https://grafana.ctbz.com.br/alerting/grafana/dg3t0pjz1iw3kd/view) (uid `dg3t0pjz1iw3kd`): `sum(increase(...[5m]))` > 99.5, `for: 5m`.
- Primeira avaliação às 15:42 de 09/11: as duas com `health=ok`, estado normal.
- Sem prioridade P1/P2, chegam ao JSM Ops como P3 e não abrem IP. Próximos passos: confirmar com o Gabriel que os alertas chegam na integração nova e como ela lê a prioridade; validação até 23/11/2026 e, sem falso positivo, adicionar a prioridade (label `severity: critical` ou `og_priority`) e testar a abertura do IP.
- A regra antiga `Technical error ... • OPSGENIE` (`dfzuj16itedc0d`) continua apontando para o `ATENDIMENTO CANAIS` (integração de Experts, não abre IP). Pode ser pausada ou removida quando as regras novas estiverem abrindo IP.
- Documentado em 09/11/2026: seção "Alertas de abertura automática" do [post-mortem](https://outline.ctbz.com.br/doc/ip-4361-r3NlcCxCiH) (com o porquê das duas regras e a validação de 2 semanas), linha do tempo de 09/11, plano de ação IP-4381, IP-4383 e comentário no IP-4361.
- 09/11/2026: o DevOps ligou `overridePriority: true` no `ATENDIMENTO CANAIS - V2`. A fase 2 fica definida: adicionar o label `og_priority: P2` (ou `P1`) nas duas regras; não depende mais de configurar a integração no JSM Ops. Como as regras ainda não têm o label, continuam chegando como P3 e a validação segue igual até 23/11.
