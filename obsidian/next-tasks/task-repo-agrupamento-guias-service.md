---
name: task-repo-agrupamento-guias-service
description: "Criar repositório agrupamento-guias-service (notificações)"
metadata:
  type: project
tags:
  - next-task
titulo: "Criar repositório agrupamento-guias-service (notificações)"
tipo: tarefa
tema: novos-repositorios
dominio:
  - impostos
  - notificacoes
  - plataforma
origem: planilha
---

# Criar repositório agrupamento-guias-service (notificações)

Criar o serviço responsável apenas pelas notificações de guias; a parte de agrupamento fica no repositório atual (ms-agrupamento-guias), que será migrado para o time de impostos.

> Texto original na planilha: "criar repo agrupamento-guias-service"

## Notas

<!-- Detalhes, decisões, PRD criado a partir desta tarefa. -->

- 2026-10-15: serviço criado localmente em `~/repositories/agrupamento-guias-service` (Zezu, padrão do email-service), com toda a notificação portada do Kotlin, testes com 100% de cobertura, collection Bruno e terraform (crons pausados). Falta: repositório no GitLab, deploy/Kong, `terraform apply` e a virada. Detalhes em [[arquitetura-e-migracao]].
