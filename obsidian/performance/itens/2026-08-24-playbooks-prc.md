---
name: 2026-08-24-playbooks-prc
description: "Base de playbooks de PRC (uma nota por problema)"
metadata:
  type: project
tags:
  - performance
titulo: "Base de playbooks de PRC (uma nota por problema)"
data: 2026-08-24
periodo: 2026QD2
categorias:
  - processo
  - qualidade
  - ia
impacto: alto
fontes:
  - "[[_prcs-indice]]"
  - "[[PRD-134632 - Meta não entrega mensagem - healthy ecosystem engagement (131049)]]"
  - "[[PRD-103649 - Cliente recebe notificações WPP com dados de outra empresa]]"
  - "[[PRD-151519 - Cliente com mais de um contato cadastrado com mesmo telefone na zendesk]]"
  - "[[PRD-168944 - Cliente não quer receber pesquisa (CSAT e-ou NPS)]]"
  - "[[PRD-167733 - Cliente não consegue enviar email - cai no spam do atendimento.experts]]"
  - "[[PRD-168171 - Cliente não consegue enviar email - bloqueio de spam no provedor do cliente]]"
  - "[[PRD-174011 - Cliente não recebe notificação do agrupamento de guias]]"
---

# Base de playbooks de PRC (uma nota por problema)

- **Período:** 2026QD2 · **Categorias:** processo, qualidade, ia · **Impacto:** alto

## Contexto

Chamados recorrentes eram reinvestigados do zero a cada ocorrência.

## O que fiz

Criei a base de playbooks de PRC no vault, um por problema, com sintoma, causa, como confirmar e ACR vinculada: Meta barrando ativo (131049), notificação com dados de outra empresa e contatos duplicados, cliente que não quer pesquisa (CSAT/NPS), e-mail que não chega (spam nosso x bloqueio no provedor do cliente) e notificação do agrupamento de guias (com as queries de diagnóstico).

Em 2026-11-13, levei os playbooks da triagem para a resolução: na aba PRCs do BahCode, cada PRC mapeado ganha um plano feito por um agente (Claude) que lê o chamado, o playbook e os tutoriais do vault, confere o que dá em produção só leitura e devolve passos, viabilidade (o agente resolve sozinho ou precisa de uma pessoa), ACR a vincular, comentário e campos de fechamento; um segundo agente executa o plano no Jira (vínculo, comentário, transição) e anota a ocorrência no playbook, com planejamento e resolução automáticos configuráveis.

Em 2026-11-18, a aba virou uma fila de trabalho por problema: os PRCs agrupados pelo playbook que resolve cada um (o que já sabemos resolver), com tags e filtros de etapa (sabemos resolver, plano pronto/errado/não planejado, execução com sucesso/falha/não executada) e um agente Claude por PRC, ao lado do chamado, que confere o playbook e o plano junto com o dev e registra as etapas de volta na aba (inclusive o playbook de um PRC que o mapeamento automático não pegou).

## Resultado

Ocorrências seguintes resolvidas pelo mesmo roteiro: 5 de e-mail que não chega, 3 de pesquisa, 2 de ativo barrado pela Meta. A aba PRCs do BahCode cruza de hora em hora os chamados sem dono com os playbooks e, desde 2026-11-13, planeja e executa a resolução deles (no primeiro teste, o plano do PRC-154406 trouxe ACR, comentário pronto e os campos de fechamento do PRC anterior do mesmo problema). Em 2026-11-18, dos 24 PRCs sem dono do board, 4 caíam em 2 playbooks, todos já com plano, e a fila mostra de cara o que falta em cada etapa.

## Evidências

- [[_prcs-indice]]
- [[PRD-134632 - Meta não entrega mensagem - healthy ecosystem engagement (131049)]]
- [[PRD-103649 - Cliente recebe notificações WPP com dados de outra empresa]]
- [[PRD-151519 - Cliente com mais de um contato cadastrado com mesmo telefone na zendesk]]
- [[PRD-168944 - Cliente não quer receber pesquisa (CSAT e-ou NPS)]]
- [[PRD-167733 - Cliente não consegue enviar email - cai no spam do atendimento.experts]]
- [[PRD-168171 - Cliente não consegue enviar email - bloqueio de spam no provedor do cliente]]
- [[PRD-174011 - Cliente não recebe notificação do agrupamento de guias]]
