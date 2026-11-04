---
name: 2026-11-03-incidente-ip-4361-ultimate
description: "Incidente IP-4361 nos bots de WhatsApp: diagnóstico e post-mortem"
metadata:
  type: project
tags:
  - performance
titulo: "Incidente IP-4361 nos bots de WhatsApp: diagnóstico e post-mortem"
data: 2026-11-03
periodo: 2026QD3
categorias:
  - incidente
  - outros-times
impacto: alto
fontes:
  - "[[processo-incidentes-ip]]"
  - "[[eventos-de-erro-ultimate]]"
  - "[[monitor-mensagens-sistema-indisponivel]]"
  - "[[abertura-automatica-ip-grafana]]"
---

# Incidente IP-4361 nos bots de WhatsApp: diagnóstico e post-mortem

- **Período:** 2026QD3 · **Categorias:** incidente, outros-times · **Impacto:** alto

## Contexto

Em 2026-11-03 os bots da Ultimate entraram em erro em massa: coincidiram um incidente da Zendesk nos AI Agents e o enum novo `PRECOS_2027` em 8 planos, que quebrava serviços do nosso lado.

## O que fiz

Separei as duas causas pelos eventos do `ultimateai-webhook` (`Technical Error` ~2.100 em 30 min da Zendesk; `Action Failed` de ~1/h para ~110/h nosso), mapeei as versões do texto de erro, registrei o relato, escrevi o post-mortem no Outline e resolvi o IP. Mostrei que o monitor de mensagens de erro pegava só 1 de 5 variantes e que o alerta do Grafana (08:18) não abriu o IP automaticamente por falha na integração do JSM Ops (aberto à mão às 08:59).

## Resultado

Incidente documentado e fechado, textos de contingência revertidos (PRD-175013) e dois gaps de monitoramento identificados com causa.

## Evidências

- [[processo-incidentes-ip]]
- [[eventos-de-erro-ultimate]]
- [[monitor-mensagens-sistema-indisponivel]]
- [[abertura-automatica-ip-grafana]]
- Jira: [PRD-175013](https://contabilizeicontabilidade.atlassian.net/browse/PRD-175013)

## Desdobramento: abertura automática de IP (04/11/2026)

- Investiguei por que o alerta do Grafana, que disparou às 08:18, não abriu o IP sozinho. Mapeei o caminho Grafana → JSM Ops → IP, comparei a configuração com a do time de notas (que abre IP) e descobri que a integração de Canais no JSM Ops não existia e que as regras chegariam como P3, por não terem `severity`. Com o Gabriel Egydio, a integração foi criada, e abri o chamado EC-1704 (Engenharia Cross) para criarem o contact point. Nota: [[abertura-automatica-ip-grafana]].

## Atualização 04/11/2026: chat web nos alertas

Descobri que o bot do chat web (`[prod] ctbz chat main`) nunca mandava eventos ao `ultimateai-webhook`: nos 30 dias anteriores, nenhuma chamada dele chegou ao serviço, nem recusada. O webhook dele estava desativado na Ultimate. Depois de ativado, validei o evento de teste no log e conferi que as 7 regras do Grafana cobrem qualquer bot. Assim, o chat web (866 conversas afetadas no incidente) passou a ter alerta em tempo real sem mudar código. A ação foi registrada no post-mortem e no plano de ação [IP-4381](https://contabilizeicontabilidade.atlassian.net/browse/IP-4381).
