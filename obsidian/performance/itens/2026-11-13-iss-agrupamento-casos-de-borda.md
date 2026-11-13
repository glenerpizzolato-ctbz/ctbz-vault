---
name: 2026-11-13-iss-agrupamento-casos-de-borda
description: "Cruzamento do calendário de ISS por município com as regras da notificação avulsa (experts-service) e do agrupamento de guias, achando a ordem de deploy errada em prod e o risco de ISS em erro travar o grupo inteiro"
metadata:
  type: project
tags:
  - performance
titulo: "ISS no agrupamento: casos de borda por município e ordem de deploy"
data: 2026-11-13
periodo: 2026QD3
categorias: [qualidade]
impacto: alto
fontes: ["[[notificacao-individual-guias-x-agrupamento]]", "[[notificacao-agrupamento-experts-bp-lp]]"]
---

# ISS no agrupamento: casos de borda por município e ordem de deploy

## Contexto

O ISS (4 tipos) passou a ir no agrupamento quando vence a partir do dia 20 (experts-service !152/!153 e microsservico-agrupamento-guias !98). Era preciso garantir que o cliente de cada município recebe o ISS uma vez: avulso ou no grupo.

## O que fiz

Cruzei a planilha de vencimento/entrega de ISS por município com o código dos dois serviços e com as guias reais da competência 10/2026 em prd (`controle_guias`, `grupo_guia`, `task_scheduler`).

## Resultado

- Descobri que o experts-service com a regra entrou em prod em 13/11 às 12:58 UTC com o !98 ainda aberto: sem o agrupamento em prod antes da montagem de 15/11, todo ISS ≥ 20 liberado a partir dali ficaria sem notificação.
- Achei um risco novo: ISS em `ERRO_PROCESSAR_GUIA` deixa o grupo em `GUIAS_COM_ERRO` e o cliente sem nenhuma guia; o ISS agrupável erra 4–8,4% das vezes, contra 0–1,2% dos outros impostos.
- Medi a duplicidade por evento novo depois do grupo (3,7% das guias em 202609) e mostrei que a planilha não cobre vencimentos de 27/11, 30/11 e 04/12.

## Evidências

- [[notificacao-individual-guias-x-agrupamento]] (seção "Cruzamento com o calendário de ISS por município")
- MRs: experts-service !152, !153; microsservico-agrupamento-guias !98
