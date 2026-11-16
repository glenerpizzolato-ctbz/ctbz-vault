---
name: alerta-webhook-ultimate-scanner
description: "Causa do alerta diário 'UltimateAI - Webhook respondendo erro' (20h–21h30, valor 82): varredura automática externa (IPs AWS sa-east-1) no Cloud Run ultimateai-webhook, de 30/09 a 25/10/2026; parou sozinha e não era problema do bot"
metadata:
  type: project
tags:
  - incidentes
  - alertas
  - grafana
  - ultimate
  - seguranca
---

# Alerta "Webhook Ultimate respondendo erro": era um scanner externo

Análise de 16/11/2026 do alerta `UltimateAI - Webhook respondendo erro (≥20 em 10 min)` (4xx/5xx de `run.googleapis.com/request_count` no Cloud Run `ultimateai-webhook`, projeto `atendimento-canais-prd`), que disparava quase todo dia entre 20h35 e 21h30, quase sempre com o valor 82.

## Conclusão

Não é erro do webhook nem dos bots da Ultimate. É uma **varredura automática externa** que passava uma vez por dia pela URL pública antiga do serviço (`ultimateai-webhook-5qax7l65va-uc.a.run.app`), procurando arquivos e endpoints expostos. O serviço responde 404 para todos, e cada passada gerava exatamente **82 respostas 404** (mais 40 respostas 302, que o alerta não conta) em 10 a 30 segundos. Daí o valor fixo 82.

- **Período:** todos os dias de 30/09 a 25/10/2026 (só 13/10 sem passada). Desde 26/10 não houve mais nenhuma rajada até 16/11.
- **Horário:** ia ficando mais tarde a cada dia, em BRT: 18:44 (30/09), ~20:10–20:50 (02 a 16/10), 21:02–21:30 (17 a 25/10). O alerta tem janela de 10 min, por isso aparecia "entre 20h35 e 21h30".
- **Origem:** IPs AWS de São Paulo (`18.230.236.25`, `56.125.122.178`, `54.94.120.3` e IPv6 `2600:1f1e:d58::/48`), com user agent de navegador aleatório a cada requisição.
- **O que buscava:** `/.env`, `/.git/config`, `/.claude/`, swagger/openapi (`/swagger.json`, `/openapi.json`, `/api-docs`, `/swagger-ui/index.html` etc.), `/actuator`, `/server_info` e endpoints de servidor MCP (`/mcp`, `/mcp/`, `/api/mcp`, `/sse`). É um padrão de scanner atrás de segredos expostos e servidores MCP abertos. Nada foi encontrado: tudo respondeu 404.
- **Por que parou:** não se sabe. Em 26/10 às 15:10 houve um deploy (revisão `00010-hrt`, só a troca da imagem base pela correção da [[cve-2026-111497-node2shell]]), que não mexeu em rotas nem no ingress. O mais provável é o scanner ter mudado de alvo ou de agenda por conta própria.

## Outros erros fora do padrão (pontuais, não diários)

- 30/10 15:37: 6× 500 no `POST /webhook` vindos da Ultimate (`216.198.18.x`, axios).
- 05/11 18:18 e 06/11 17:11: 8 e 4× 429 no `POST /webhook` vindos da Ultimate (limite de taxa).
- 06/11, 13/11 e 15/11: poucos 404 de scanners internos de segurança (`public-swagger-inventory/1.0`, `Farol-ASPM`, `farol-surface`).

Nenhum desses passa do limiar de 20 em 10 min.

## Como foi medido

- Logs de request do Cloud Run (`log_name:"run.googleapis.com%2Frequests"`, `httpRequest.status>=400`), que guardam só 30 dias (a partir de 17/10).
- Métrica `run.googleapis.com/request_count` por `response_code`, alinhada por minuto, pela API do Cloud Monitoring, para cobrir desde 30/09.

## O que fazer com o alerta

- Como o ruído parou sozinho, o alerta pode ficar como está. Se o scanner voltar, a correção é **contar só a rota real** (`POST /webhook`) ou ignorar 404, porque o 404 em rota inexistente é de varredura, não de falha.
- O serviço segue com `ingress: all` e duas URLs públicas (a antiga `-5qax7l65va-uc` e a nova `-852985851006`). A Ultimate usa a nova (`/webhook`), e o scanner só usou a antiga. Isso pode ser endurecido à parte, sem urgência.

Relacionado: [[limpeza-alertas-canais]], [[proposta-ajuste-alerta-ultimate-ip]], [[abertura-automatica-ip-grafana]].
