---
name: padroes-indice
description: "Índice de padrões e convenções do time (nomenclatura de recursos, organização de código) que valem para qualquer serviço"
metadata:
  type: reference
tags:
  - padroes-indice
---

# Padrões do time

Convenções que valem para qualquer serviço, uma nota por padrão.

- [[pubsub-nomenclatura|Nomenclatura de Pub/Sub]] — tópico `<serviço>.p2p.<nome>`, subscription `<serviço>.sub.<nome>` e sufixo `-local` na execução local
- [[whatsapp-limites-botoes|Limites de botões no WhatsApp]] — botão de resposta 20 caracteres, linha de lista 24 (Ultimate/Zendesk e Meta)
- [[rotina-deploy-separada|Rotina separada para o deploy]] — fechar o card da feature e abrir uma Rotina só para o deploy em prd (mesmo épico, status To-do), para não ocupar cycle time
- [[jira-transicoes-passo-a-passo|Transições do Jira uma por vez]] — em todos os cards, mudar o status transição por transição pelo workflow (ex: To-do → Started → Finished), com os ids conhecidos; sub-task de código é do tipo Desenvolvimento (e como converter)
- [[jira-anexar-imagens-comentario|Anexar imagens em comentário do Jira]] — subir arquivos locais pelo MCP da Atlassian (uploadAttachmentToJiraIssue + curl) e embuti-los num comentário com inlineFileId
- [[sonar-duplicacao-codigo-novo|Sonar: duplicação em código novo]] — gate de 6% em código novo: diagnosticar pelo MCP (`search_duplicated_files`), mexer em arquivo antigo o torna código novo, literais não quebram duplicação; extrair o idêntico para um service comum
- [[pipeline-repo-novo-sem-variaveis-ci|Repo novo sem variáveis de CI]] — pipeline sem build/lint/test e Sonar do MR com cobertura 0%; copiar as variáveis de um repo do mesmo tipo
- [[commit-push-automatico|Commit e push automáticos]] — em branch de trabalho ou com MR aberto, terminar o pedido já commitando, dando push e atualizando o MR, sem perguntar
- [[sonar-cobertura-branches-kotlin|Sonar: cobertura de branches em Kotlin]] — gate de 90% de branches no código novo; safe calls, let/takeIf e lambdas inline geram ramos inalcançáveis; diagnosticar com jacoco.xml × git diff e trocar por orEmpty/!!
- [[create-secret-value-cifrao|Secret com `$` no create-secret-value]] — ao gravar secret pelo job `create-secret-value` do `vault-roleset`, duplicar cada `$` do valor (`$$`); com um só, o valor gravado sai diferente e a autenticação falha (ex: 401 no Kong)
- [[sonar-cobertura-excluida-no-runner|Sonar: 0% em código testado]] — `new_coverage` 0.0 com teste existente: o arquivo está nas exclusões de cobertura do runner (vitest/jest/jacoco) e não entra no relatório importado pelo Sonar
- [[consumidores-entre-repositorios|Consumidores entre repositórios]] — registrar quem consome cada rota, tópico ou tabela (no consumidor e na seção Consumidores do provedor), para a revisão de MRs achar quebra de fluxo dependente
