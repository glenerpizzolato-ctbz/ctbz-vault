---
name: causa-raiz-zendesk-ai-agents-2026-11-03
description: Causa raiz informada pela Zendesk para a queda dos AI Agents (Ultimate) em 03/11/2026 (IP-4361) - rotação de segredo entre serviços que não propagou, HTTP 401, recuperação por região
metadata:
  type: project
tags: [incidentes, zendesk, ultimate, IP-4361]
---

# Causa raiz da Zendesk: AI Agents fora em 03/11/2026 (IP-4361)

Fonte: "Zendesk Event Analysis - AI Agents are unresponsive" e "A note from Zendesk CCO about the AI Agents service interruption", PDFs recebidos pelo chamado nº 15459846 em 06/11/2026. Incidente 10525 na status page. A RCA pública ainda vai sair na central de ajuda da Zendesk.

## Em palavras simples

Os serviços internos dos AI Agents usam um segredo compartilhado para assinar e validar os tokens com que conversam entre si. Às 10:20 UTC (07:20 BRT) a Zendesk rotacionou esse segredo, mas ele não se propagou para todos os serviços. Com valores diferentes, um serviço passou a recusar as chamadas do outro (HTTP 401): o bot caía em fallback (o nosso "Technical Error"), não escalava para humano e o painel ficava em loop de recarga. A correção foi reiniciar todos os serviços, em fases, para propagar o segredo. Segundo a Zendesk, foi problema de disponibilidade, não de segurança.

## Horários (BRT = UTC-3)

- 07:20: rotação do segredo e início dos erros. 07:25: primeiros tickets de clientes. 07:55: confirmado que o segredo não propagou.
- 08:00: tentativa de ressincronizar o segredo manualmente, sem sucesso. 08:15: decidido reiniciar todos os serviços.
- Infra antiga no GCP: reinício na UE às 08:20 e nos EUA às 08:40; normal às 09:10.
- Infra ZOS (AWS), por pod: UE de 09:12 a 11:00 (pods 17, 18, 29, 31, 28); Américas de 10:55 a 11:45 (pods 13, 19, 20, 23, 27); APAC de 11:48 a 12:10 (pods 25, 30, 15).
- 12:20: todos os testes automáticos verdes, tudo normal.

## Relação com o que vimos do nosso lado

- Nosso `Technical Error` no ultimateai-webhook começou às 08:10 BRT, e o alerta do Grafana ficou disparado até 11:14:30. O fim bate com a recuperação das Américas no ZOS (10:55–11:45), mas a Zendesk não disse em qual pod está a nossa instância.
- O nosso "normalizado" às ~12:15–12:28 é a confirmação do time (actions voltando), um pouco depois do fim do lado deles.

## Ação da Zendesk e nossa

- Zendesk: revisar o runbook de rotação de segredos (conferir a propagação em todos os serviços e regiões, documentar os reinícios e checar os erros de autenticação antes de concluir a rotação). Status: agendado.
- Recomendação ao cliente: nenhuma.
- Registrado no [post-mortem](https://outline.ctbz.com.br/doc/ip-4361-r3NlcCxCiH) (causa raiz, linha do tempo e item de ação) e no comentário de 06/11 do IP-4361.

## Por que não teve runbook nem ajuste centralizado do nosso lado (decisão de 06/11/2026)

A única mitigação do nosso lado foi trocar a mensagem de erro dos bots por uma mais instrutiva, o que é simples e levou ~6 min (09:34–09:40 BRT). Por isso o runbook e o failover saíram do post-mortem e do IP-4381. Se alguém perguntar "por que trocar em N lugares e não em um só?": o próprio incidente limitou as funções da Ultimate. Com a comunicação entre os serviços dela falhando (HTTP 401), um ajuste centralizado, como uma chamada de API para trocar a mensagem em todos os bots de uma vez, também não funcionaria. A troca manual bot a bot era o caminho disponível.

Ver também [[processo-incidentes-ip]], [[abertura-automatica-ip-grafana]], [[eventos-de-erro-ultimate]].
