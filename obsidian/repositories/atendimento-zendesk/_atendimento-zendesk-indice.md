---
name: atendimento-zendesk-indice
description: "Índice de notas do repositório atendimento-zendesk: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - atendimento-zendesk
repositorio: atendimento-zendesk
caminho: ~/repositories/atendimento-zendesk
---

# atendimento-zendesk

Repositório em `~/repositories/atendimento-zendesk`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[categoria-plano-autenticacao-whatsapp]] — valores do enum `categoriaPlano` no endpoint de autenticação basico-padrao do WhatsApp, como o plano do CRM é normalizado e as flags de vínculo da Ouvidoria (empresa ativa/inativa/abertura)
- [[api-gateway-bots-whatsapp]] (em `apis/`) — como chamar a `autenticacao/basico-padrao` pelo gateway (`/atendimento/zendesk/bots/whatsapp/fluxo/interacao`) com a `x-api-key` da `zendeskbot-config`
- [[testes-em-worktree]] — como rodar jest/eslint/prettier numa worktree sem `node_modules` (symlink para o checkout principal) e as suítes que já falham no master
- [[uso-de-llm-openai]] — onde o repo usa LLM (OpenAI gpt-4o-mini via LangChain): classificação de tema/subtema, encerramento automático e resumo de atendimento
- [[monitor-mensagens-sistema-indisponivel]] — monitor que loga quando o cliente recebe mensagem de erro do bot: só textos fixos e case-sensitive (pegou só 1 das 5 variantes de 2026-11-03); linhas NotificarAgente* como fonte completa
- [[historico-mrs-atendimento-zendesk|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
