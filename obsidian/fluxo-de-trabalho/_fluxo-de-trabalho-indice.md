---
name: fluxo-de-trabalho-indice
description: "Índice do fluxo de trabalho do time: como conduzir cards do Jira, MRs, commits, deploy e evidências de teste"
metadata:
  type: reference
tags:
  - fluxo-de-trabalho-indice
---

# Fluxo de trabalho

Como o time trabalha no dia a dia: transições e tipos de card no Jira, evidências de teste, commits, MRs e revisão, deploy. Uma nota por regra.

- [[rotina-deploy-separada|Rotina separada para o deploy]] — fechar o card da feature e abrir uma Rotina só para o deploy em prd (mesmo épico, status To-do), para não ocupar cycle time
- [[jira-transicoes-passo-a-passo|Transições do Jira uma por vez]] — em todos os cards, mudar o status transição por transição pelo workflow (ex: To-do → Started → Finished), com os ids conhecidos; sub-task de código é do tipo Desenvolvimento, a chamada de rotina é sempre Subtarefa (e como converter)
- [[jira-anexar-imagens-comentario|Evidências de teste no Jira]] — um comentário por cenário (mais o resumo), imagem inline logo abaixo do texto que a cita (nunca tudo como anexo no fim); upload pelo MCP da Atlassian (uploadAttachmentToJiraIssue + curl) e nó media-single no HTML; gerar PNG de evidência em texto
- [[commit-push-automatico|Commit e push automáticos]] — em branch de trabalho ou com MR aberto, terminar o pedido já commitando, dando push e atualizando o MR, sem perguntar
- [[gitlab-work-item-status|Status de work-item no GitLab]] — To do / In progress / Done é o widget STATUS via GraphQL (`workItemUpdate` com `statusWidget`), não label
- [[threads-mr-resolver-ao-responder|Resolver threads de MR ao responder]] — ao validar e responder threads de revisão (pessoas ou bots), resolver cada uma em seguida, sem deixá-la aberta
- [[gitlab-duo-requested-changes|GitLab Duo em requested changes]] — corrigir e resolver não basta: pedir revisão de novo ao Duo para ele aprovar e liberar o MR
- [[mr-pequeno-nao-dividir|MR pequeno não se divide]] — com poucos arquivos (até ~5 arquivos/~200 linhas), um MR só, sem forçar a corrente em branch chaining; como desfazer a corrente no BahCode
- [[resultado-de-teste-na-subtask-e2e|Resultado de teste na sub-task E2E]] — evidências de teste vão como comentário na sub-task de teste E2E do card, não no PRD principal
- [[metrica-e2e-critico|Métrica de E2E crítico]] — link do dashboard GE Qualidade – Automação (Metabase), o que a meta de 85% mede (gauge % criticidade ALTA em stg), por que um teste "desenvolvido" não conta e como tirar a lista de um squad pela API
