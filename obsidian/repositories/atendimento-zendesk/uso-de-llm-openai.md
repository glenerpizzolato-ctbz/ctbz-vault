---
name: uso-de-llm-openai
description: "Onde o atendimento-zendesk usa LLM: OpenAI gpt-4o-mini via LangChain 0.0.162 para classificar tema/subtema, decidir encerramento automático e resumir atendimentos"
metadata:
  type: reference
tags:
  - atendimento-zendesk
  - llm
  - openai
repositorio: atendimento-zendesk
---

# Uso de LLM (OpenAI) no atendimento-zendesk

O repositório usa a **OpenAI (`gpt-4o-mini`)** através do **LangChain `0.0.162`** (versão bem antiga, API `langchain/chat_models/openai` e `createStructuredOutputChainFromZod`, com saída estruturada via Zod). A chave vem de `APP_SERVICES_OPENAI_API_KEY` (`app.services.openai.apiKey` na config; `OPENAI_API_KEY` no `environments/.env-local`).

Infra em `src/infra/openai/` (`OpenAIModule`, `OpenAIService`, `LangChainService` e as implementações em `internal/`). Casos de uso:

| Uso | Prompt/chain (`src/infra/openai/internal/`) | Quem chama (`src/domain/`) |
| --- | --- | --- |
| Classificar tema e subtema do atendimento | `classificacao-tema-subtema.ts` | `classificacao-atendimento/services/classificar-tema-subtema` (worker `worker-classificacao-atendimento`) |
| Cortar a conversa por limite de tokens antes de classificar | `langchain-impl.service.ts` (`TokenTextSplitter`) | `classificacao-atendimento/services/limitar-conversa-por-tokens` |
| Detectar a intenção do cliente no encerramento automático | `encerramento-automatico.ts` | `encerramento-automatico/services/processar-intencao-cliente-por-ia` |
| Resumir o atendimento (timeline) | `resumo-atendimento.ts` | `timeline/services/resumir-atendimento` |

Não confundir com o experts-service, que tem o fluxo parecido de "Encerrar com IA" mas usa **Gemini 2.0 Flash via Vertex AI** (ver [[fluxo-encerramento-com-ia]]).
