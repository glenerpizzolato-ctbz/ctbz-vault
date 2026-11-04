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
- O contact point `ATENDIMENTO CANAIS` é só opsgenie (mesma URL do JSM Ops), mas com template `ctbz.message.2`, `sendTagsAs: tags` e `autoClose: false`, e com outra API key/integração no JSM Ops.
- **No IP-4361 (03/11/2026)** a regra OPSGENIE disparou às 08:18:30 (bot `[prod] ctbz wpp main`) e às 08:27+ (fina + avisos), mas nenhum IP foi aberto: o alerta saiu do Grafana e o que falta está do lado do JSM Ops (a integração de `ATENDIMENTO CANAIS` não abre IP como a do POC Centralizador de notas). O IP foi aberto manualmente às 08:59.

## Acessos

- No Grafana, a conta do Glener é `Viewer` (org Contabilizei): dá para ler regras, contact points e histórico pela API (`/api/v1/provisioning/alert-rules`, `/api/v1/provisioning/contact-points`, `/api/v1/rules/history?ruleUID=...&from=&to=`, com a sessão do navegador), mas não editar.
- A tela de alertas do JSM Ops (`/jira/ops/alerts`) não carrega para a conta do Glener ("Não foi possível carregar os alertas"): sem acesso ao JSM Ops.
- A configuração dos alertas não está versionada em nenhum repositório de `~/repositories`.
