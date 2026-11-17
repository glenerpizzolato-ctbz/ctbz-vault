---
name: 2026-11-16-testes-e2e-roteamento-n1-ativacao
description: "Testes E2E em prd do roteamento N1 Ativação por status do SOCI (PRD-176172) conduzidos com agente de IA: Jira → Abertura → WhatsApp → Zendesk → evidência no card, com descobertas que destravaram e corrigiram o plano de testes"
metadata:
  type: project
tags:
  - performance
titulo: "Testes E2E do roteamento N1 Ativação por SOCI conduzidos com IA"
data: 2026-11-16
periodo: 2026QD3
categorias: [ia, qualidade, processo, seguranca]
atualizado_em: 2026-11-17
impacto: medio
fontes: ["[[testes-roteamento-n1-ativacao]]", "[[roteamento-n1-ativacao-soci]]", "[[rollout-ia-ativacao]]", "[[ativacao-processos-abertura-teste]]", "[[menu-inic-experts-ramificacoes]]"]
---

# Testes E2E do roteamento N1 Ativação por SOCI conduzidos com IA

## Contexto

A Entrega 03 da segmentação N1/N2 (PRD-176172) mudou na Ultimate o grupo do Zendesk de cada status do SOCI, com grupos novos (Módulo tributário, Assinatura JC, Retenção…). Testar em prd exige um processo de abertura ligado ao telefone de teste, mudar o status do SOCI a cada cenário, conversar com o bot pelo WhatsApp e conferir o grupo do ticket.

## O que fiz

- Conduzi com o Claude Code o ciclo completo por cenário: transição do SOCI pelo MCP do Jira → conferência do `statusJira` nas rotas do bot → conversa no WhatsApp Web → leitura do grupo pela API do Zendesk → fechamento do ticket sem CSAT → comentário com GIF no card de testes (PRD-177631).
- Descobertas que destravaram o teste: o `statusJira` vem do Datastore da Abertura (não do `prd_issue_ticketing`); o vínculo é pelo telefone do sócio; o plano do processo é trocado por rota pública da Abertura; a IA de Ativação Experts entra por rollout aleatório pelo segundo do relógio (~42%) e a de BP em 100%; os gatilhos de CSAT só respeitam `sys_csat_survey_sent`.
- Cuidei de privacidade: recorte dos GIFs para não vazar as conversas pessoais do WhatsApp; substituição de uma evidência que vazou.
- Diagrama das ramificações do Menu Inic e diff V1 x V2 (artefatos) mostrando que o caso Finalizado não passa pelos drops de Ativação.

## Resultado

- 5 cenários validados em prd com evidência no card (Cadastro, Pré CNPJ, Módulo tributário, ELSE/Atendimento, Assinatura JC), todos no grupo esperado.
- Um ponto de atenção encontrado: o ELSE do Experts deixou de adicionar a tag `sys_grupo_ativacao_exp`.
- Ciclo, armadilhas e ferramentas documentados no vault para os próximos testes de Ativação.

- **2026-11-17, PRD-176795 (BP N1/N2):** mesmo método aplicado ao roteamento BP com canário por telefone em prd: 3 cenários de inbound sem empresa e 4 de empresa ativa OK (B1/B2/B3 + regressão Experts). Achados que mudaram a solução: o retorno de ativo (cerca de 4,3 mil tickets desde 10/11) passava por outro caminho que não tinha sido ajustado; `jiraFinalizado` sozinho mandaria cerca de 26 mil empresas de migração para a Ativação, o que levou à regra `aberturaEmpresa && !jiraFinalizado` (cerca de 1,8 mil empresas). Também foi validado que o impersonate do `bots-api` traz os dados reais do CRM, o que destravou massa para estados que não dá para forçar. No caminho apareceram pontos de segurança: rotas sem autenticação de usuário no impersonate (`bots-api`) e em rotas que alteram `jiraFinalizado` (`plataforma-web` e monolito).

## Evidências

- Card de testes: https://contabilizeicontabilidade.atlassian.net/browse/PRD-177631
- Notas: [[testes-roteamento-n1-ativacao]], [[rollout-ia-ativacao]], [[ativacao-processos-abertura-teste]], [[menu-inic-experts-ramificacoes]], [[logs-conversa-ultimate]]

- PRD-176795 / sub-task de testes PRD-177894 (comentários de evidência, incluindo 29777959); [[testes-roteamento-bp-n1-n2]], [[empresa-teste-bp-ativa]]
