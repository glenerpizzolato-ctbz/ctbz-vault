---
name: 2026-11-05-opportunities-scan
description: "Varredura diária com IA em busca de oportunidades de melhoria (aba Opportunities do BahCode)"
metadata:
  type: project
tags:
  - performance
titulo: "Varredura diária com IA de oportunidades de melhoria (Opportunities)"
data: 2026-11-05
periodo: 2026QD3
categorias:
  - ia
  - processo
impacto: medio
fontes:
  - "[[2026-11-04-auto-approve-mrs]]"
  - "[[2026-11-04-vault-conhecimento-time]]"
---

# Varredura diária com IA de oportunidades de melhoria (Opportunities)

- **Período:** 2026QD3 · **Categorias:** ia, processo · **Impacto:** medio

## Contexto

As melhorias que mais renderam ao time nasceram de alguém notar um trabalho manual repetido: a tela de telefone internacional (muito usada em PRCs), a tela de gestão de e-mails para o CRM, o resumo automático de alertas, o lembrete automático de MRs parados, o repo de webhooks com os logs de erro da Ultimate e a aba de Sustentação no admin para ajustes de PRCs na Zendesk. Esse olhar dependia de acaso.

## O que fiz

Criei no BahCode a aba Opportunities (grupo Scanning): uma varredura automática, uma vez por dia, em que o Claude, só leitura, lê os vaults (PRCs com mais ocorrências, retros, próximas tarefas, infra, incidentes) e as minhas sessões interativas recentes do Claude, e devolve até 5 oportunidades de automação, observabilidade, ferramenta ou processo, com impacto, esforço, se usa IA, problema, evidência concreta e proposta, sem repetir as já levantadas. Prompt (com os exemplos reais do time), modelo, intervalo, fontes e liga/desliga ficam na tela de Configurações; cada oportunidade pode ser marcada como feita ou descartada.

## Resultado

A primeira varredura levou 1 minuto, custou US$ 0,25 e trouxe 5 oportunidades com evidência do vault, entre elas: alertas do Grafana como código (configuração hoje não versionada e só editável pelo DevOps), recuperação automática dos e-mails do atendimento.experts retidos no spam (5 ocorrências de PRC num mês, dependendo de uma pessoa com acesso à caixa), gate de saúde pós-deploy na pipeline central e a criação automática das sub-tarefas do plano de ação dos IPs a partir do post-mortem.

## Evidências

- Commit `6f890f9` do ide-bahcode (`feat(opportunities)`)
- [[2026-11-04-auto-approve-mrs]]
