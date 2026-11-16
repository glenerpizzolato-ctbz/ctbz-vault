---
name: 2026-11-16-relatorio-notificacoes-dia-15
description: "Skill que gera, só com leitura em prod, o relatório das notificações do agrupamento de guias do dia 15 por segmento e canal, cruzando o controle do agrupamento com o status real do WhatsApp ativo, para compartilhar com o time"
metadata:
  type: project
tags:
  - performance
titulo: "Relatório automatizado das notificações do agrupamento (dia 15)"
data: 2026-11-16
periodo: 2026QD3
categorias: [ia, qualidade]
impacto: medio
fontes: ["[[relatorio-notificacoes-dia-15]]", "[[notificacao-agrupamento-experts-bp-lp]]"]
---

# Relatório automatizado das notificações do agrupamento (dia 15)

## Contexto

Todo dia 15 o agrupamento de guias notifica ~25 mil clientes por e-mail e WhatsApp, em três públicos (Experts Simples, Experts LP e BP LP). Não havia uma forma rápida de saber se todos receberam, o que estava em trânsito e o que faltava enviar, e o WhatsApp sai sob demanda do horário comercial.

## O que fiz

Criei a skill `relatorio-notificacoes-agrupamento`, que lê só em modo leitura o banco do agrupamento e o `mensagem_ativa` do atendimento-zendesk, aplica as mesmas regras de elegibilidade das crons e gera um resumo para o chat, um artefato para o time e um PDF, com veredito por segmento × canal, próxima cron, falhas e alertas.

## Resultado

Relatório em ~40 s. Na primeira foto (competência 10/2026, dia 15 num domingo) mostrou o e-mail ~100% enviado nos três públicos e ~24 mil WhatsApps na fila do horário comercial. Também revelou que o controle do agrupamento não reflete o WhatsApp real (2.091 `AGUARDANDO_NOTIFICACAO` sem callback em 09/2026) e grupos que nunca são notificados (22 `SEM_ARQUIVO_GUIA_AVULSA`, 560 `GUIAS_AGUARDANDO_GERACAO`).

## Evidências

- [[relatorio-notificacoes-dia-15]] (nota do relatório e histórico de execuções)
- Skill em `~/ctbz-vault/skills/impostos/relatorio-notificacoes-agrupamento/`
