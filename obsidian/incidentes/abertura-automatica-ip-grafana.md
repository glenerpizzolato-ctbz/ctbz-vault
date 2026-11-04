---
name: abertura-automatica-ip-grafana
description: "Como um alerta do Grafana vira IP no Jira (contact point opsgenie → JSM Ops → IP pelo app Suporte Tecnologia), quais contact points abrem IP e por que o alerta de Technical error da Ultimate não abriu o IP-4361"
metadata:
  type: reference
tags:
  - incidentes
  - grafana
  - jsm-ops
  - ultimate
---

# Abertura automática de IP a partir do Grafana

## Como funciona

- Os IPs automáticos (título `[Grafana]: 🔴 <b>...</b> · ...`) são criados pelo app **Suporte Tecnologia** (reporter), com a descrição no formato do JSM Ops/Opsgenie (`Alias`, `ID`, `Tags`, `Owner`, `Details`, `Action: Create`, `Source:Grafana`, `Squad:`, `Detalhamento:`) e com "Quem identificou a falha?" = Alertas automáticos. Ex: IP-4362, IP-4364, IP-4378, IP-4379, IP-4385 (todos do time de notas).
- O caminho é: regra do Grafana → contact point do tipo `opsgenie` apontando para `api.atlassian.com/jsm/ops/integration/v2/alerts` (JSM Operations) → integração no JSM Ops que abre o IP no Jira.
- O contact point `CTBZ-ALERT-POC-CENTRALIZADOR-NOTAS` (pasta "POC Centralizador") tem duas integrações: Google Chat e opsgenie (template `poc.centralizador`, `sendTagsAs: both`, `autoClose: true`). É dele que saem os IPs automáticos hoje.

## Alertas da Ultimate (time Canais)

- Grafana: https://grafana.ctbz.com.br, regras no grupo "UltimateAI Jornada (every 1m)", métrica de log `logging_googleapis_com:user_ultimateai_events` do Cloud Run `ultimateai-webhook` (projeto `atendimento-canais-prd`).
- Cada alerta existe em duas versões: `• CHAT` (receiver `EXPERTS`, Google Chat) e `• OPSGENIE` (receiver `ATENDIMENTO CANAIS`, labels `Contact: Opsgenie`, `team: canais`, `service: ultimateai-webhook`). Ex: `UltimateAI - Technical error enviado no chat (≥10 em 5 min) • OPSGENIE` (uid `dfzuj16itedc0d`), expr `sum by (bot)(increase(...{event=~"(?i)technical.?error"}[5m]))`.
- São 7 regras sobre `ultimateai_events` (verificado em 04/11/2026): 4 `• CHAT` (falha de integração por `integration_id, bot`, falha de escalonamento, Technical error e Action Failed ≥50 em 5 min) e 3 `• OPSGENIE` (as mesmas, sem o Action Failed). Todas agrupam por `bot` e nenhuma filtra bot, então um bot novo que ligue o webhook (como o `chat main` em 04/11/2026) entra nos alertas sem mexer no Grafana.
- O contact point `ATENDIMENTO CANAIS` é só opsgenie (mesma URL do JSM Ops), mas com template `ctbz.message.2`, `sendTagsAs: tags` e `autoClose: false`, e com outra API key/integração no JSM Ops.
- **No IP-4361 (03/11/2026)** a regra OPSGENIE disparou às 08:18:30 (bot `[prod] ctbz wpp main`) e às 08:27+ (fina + avisos), mas nenhum IP foi aberto: o alerta saiu do Grafana e o que falta está do lado do JSM Ops (a integração de `ATENDIMENTO CANAIS` não abre IP como a do POC Centralizador de notas). O IP foi aberto manualmente às 08:59.

- **Entrega ao JSM Ops (verificado em 04/11/2026):** o status dos receivers (`/api/alertmanager/grafana/config/api/v1/receivers`, que guarda só a última tentativa) mostrava o `ATENDIMENTO CANAIS` com último envio ao JSM Ops em 04/11 às 11:10, em 285 ms e sem erro. Isso indica que a API key é válida e que o JSM Ops aceitou a requisição, mas segundo o Gabriel nenhum alerta da Ultimate apareceu do lado dele. Mesmo assim, nenhum IP foi aberto: entre 03/11 e 04/11, o app Suporte Tecnologia só abriu IPs de notas (Grafana) e do contabilizeiapp (Stackdriver). A entrega do dia 03/11 em si não fica no histórico do Grafana.
- Existe também o contact point `CTBZ-ALERT-POC-CENTRALIZADOR-CANAIS-XP`, só com Google Chat (template `poc.centralizador`) e sem integração com o JSM Ops. Ele parece o começo do caminho 2 (o centralizador de Canais).

## Situação em 04/11/2026: a integração não existia

- O Gabriel Egydio confirmou que **não havia nenhuma integração de Canais no JSM Ops**. A API key do `ATENDIMENTO CANAIS` não ligava o alerta a nenhum lugar que abrisse IP. Era o elo que faltava desde que o time trocou de nome, de "Experts" para "Atendimento Canais".
- O andamento (feito, decisão e pendências) está na sub-task [IP-4383](https://contabilizeicontabilidade.atlassian.net/browse/IP-4383) (Criar monitoramento), do plano de ação IP-4381.
- O Gabriel criou a integração nova, e a API key está com ele e com o Glener.
- Só o time de **DevOps** tem permissão para criar ou editar contact points no Grafana. Para criar o contact point com a nova key foi aberto o chamado [EC-1704](https://contabilizeicontabilidade.atlassian.net/browse/EC-1704) (projeto Engenharia Cross, portal 1213 do service desk). Antes ele tinha sido aberto como SS-10602, no portal 1180, mas foi reaberto no time certo; o EC-1704 é a referência.
- **Decisão (04/11/2026): criar um contact point novo e não alterar o `ATENDIMENTO CANAIS`.** Mudar a API key ou a configuração do existente afetaria de uma vez as 9 regras que apontam para ele (Ultimate, CSAT, CPU do Postgres, HTTP Error %, dependências), com risco de quebrar algo. O contact point novo, com a integração nova do JSM Ops, recebe primeiro as regras que devem abrir IP (a começar pelo Technical error da Ultimate). As demais migram aos poucos, conferindo regra a regra que o alerta chega e abre o IP. O `ATENDIMENTO CANAIS` só é desativado quando nenhuma regra apontar mais para ele.
- Ainda falta, mesmo depois do contact point: a prioridade (as regras de Canais sem `severity` chegariam como P3) e o padrão do centralizador (template `poc.centralizador`, `sendTagsAs: both`, `autoClose: true`).

## O que chegou em cada destino no IP-4361 (03/11/2026)

- **Google Chat (versão `• CHAT`)** chegou no espaço **Engenharia Canais | Grafana** (https://chat.google.com/room/AAAAqIkGXVw), postado pelo app "Quickstart Webhook". "UltimateAI - Technical error enviado no chat • CHAT" apareceu às 08:19, 08:29, 08:34, 08:49, 08:54 e 09:59, com até 281 mensagens de erro técnico em 5 min no bot `[prod] ctbz wpp main` e de 7 a 16 no `fina + avisos`. O time percebeu pelo chat às 08:52, e o IP foi aberto manualmente às 08:59.
- **JSM Ops (versão `• OPSGENIE`, contact point `ATENDIMENTO CANAIS`):** a regra disparou no mesmo horário. Histórico em https://grafana.ctbz.com.br/alerting/grafana/dfzuj16itedc0d/view?tab=history (pasta Experts): bot `[prod] ctbz wpp main` ficou em Alerting de 08:18:30 a 11:14:30; `fina + avisos` oscilou entre 08:27:30 e 11:29:30. As tags enviadas foram os labels no formato `chave:valor` (`alertname`, `bot`, `Contact:Opsgenie`, `Nivel:jornada-ultimate`, `Team:Canais`, `team:canais`, `service:ultimateai-webhook`, `grafana_folder:Experts`), mas o Gabriel não recebeu nenhum alerta da Ultimate. Ou a API key do `ATENDIMENTO CANAIS` é de uma integração que não é a dele (antiga, de outro time ou sem a ação de abrir IP), ou o alerta chegou e ficou como P3, sem destaque. As duas coisas precisam ser corrigidas.

- Em 04/11/2026 o Gabriel buscou `source: Grafana AND tags: "team:canais"` no JSM Ops e não achou nada. A busca está coerente com o que o Grafana envia, mas só cobre os alertas dos times que ele enxerga. A checagem definitiva são os logs da integração dona da API key do `ATENDIMENTO CANAIS`.

## Prioridade: só P1/P2 abre IP

- Segundo o **Gabriel Egydio** (responsável pelo JSM Ops e pela integração alertas → IP), o JSM Ops só abre o IP automaticamente quando o alerta chega como **P1 ou P2**. Alerta que chega como P3 fica só no JSM Ops.
- No dia 03/11 só chegaram ao time de Canais dois alertas, os dois via integração do **Stackdriver** e como P3, por isso não viraram IP. Eram de CPU e memória do serviço `contabilizei-crm-atendimento-zendesk`, outro assunto. Nenhum alerta da Ultimate vindo do Grafana chegou ao Jira.
- No Grafana, nenhum contact point opsgenie usa `overridePriority` (verificado em 04/11/2026), então a prioridade não vem da anotação `og_priority`. As 106 regras de notas têm o label `severity` (`critical` ou `warning`, uma regra de cada por SLI) e enviam as tags como `both`. Hipótese ainda não confirmada: a integração do POC Centralizador converte `severity=critical` em P1/P2.
- As 9 regras do `ATENDIMENTO CANAIS` (Ultimate, CSAT, CPU do Postgres, HTTP Error %, dependências) **não têm o label `severity`**: só `Contact`, `Team`/`team`, `Nivel` e `service`. Sem ele, chegariam como P3 (o padrão).
- Como corrigir: definir a prioridade dos alertas de Canais (pelo label `severity: critical`, no padrão do centralizador, ou com `overridePriority: true` e a anotação `og_priority: P1|P2`) e mandá-los por uma integração que chegue ao JSM Ops do time. Confirmar com o Gabriel qual dos dois caminhos a integração aceita e se a API key do `ATENDIMENTO CANAIS` ainda é usada.

## Armadilha: "Unused" na tela de contact points

- Na tela de contact points (`/alerting/notifications`), o selo **Unused** só considera as **notification policies**. Ele ignora as regras que escolhem o contact point direto, pelo roteamento simplificado (`notification_settings.receiver`), que é como o Grafana da CTBZ funciona: nenhuma policy aponta para os contact points de atendimento.
- Por isso, `ATENDIMENTO CANAIS` aparece como Unused mesmo sendo usado por 9 regras e tendo enviado hoje sem erro (verificado em 04/11/2026). O mesmo acontece com `CTBZ-ALERT-POC-CENTRALIZADOR-ATENDIMENTO` (6 regras, Google Chat) e `Radar Atendimento` (6 regras, Google Chat). Para saber se um contact point está mesmo em uso, ver as regras (`/api/v1/provisioning/alert-rules`) e a última entrega (`/api/alertmanager/grafana/config/api/v1/receivers`).

## Acessos

- Responsável pelo JSM Ops e pela abertura automática de IP: **Gabriel Egydio**.
- **Opsgenie × JSM Ops:** é o mesmo produto em duas fases. O Opsgenie standalone (`*.app.opsgenie.com`, API `api.opsgenie.com`) está sendo descontinuado pela Atlassian, e as funções dele passaram para o JSM Ops, dentro do Jira. A API foi mantida compatível, então o tipo de contact point no Grafana continua se chamando `opsgenie`. O que define o destino é a `apiUrl`: todos os contact points opsgenie da CTBZ apontam para `api.atlassian.com/jsm/ops/...`, ou seja, para o JSM Ops.
- **JSM Ops** = Jira Service Management Operations, o antigo Opsgenie, que a Atlassian incorporou ao Jira Service Management. É um módulo dentro do próprio site Jira (https://contabilizeicontabilidade.atlassian.net/jira/ops), não outra plataforma. Ele cuida de alertas, plantão (on-call), escalonamento e integrações (cada integração tem uma API key e regras de ação, como abrir um IP). Para acessar, é preciso uma licença de agente do Jira Service Management e ser membro do time de Ops dono da integração. Quem concede é o admin do site Atlassian ou do JSM.
- No Grafana, a conta do Glener é `Viewer` (org Contabilizei): dá para ler regras, contact points e histórico pela API (`/api/v1/provisioning/alert-rules`, `/api/v1/provisioning/contact-points`, `/api/v1/rules/history?ruleUID=...&from=&to=`, com a sessão do navegador), mas não editar.
- A tela de alertas do JSM Ops (`/jira/ops/alerts`) não carrega para a conta do Glener ("Não foi possível carregar os alertas"): sem acesso ao JSM Ops.
- A configuração dos alertas não está versionada em nenhum repositório de `~/repositories`.
