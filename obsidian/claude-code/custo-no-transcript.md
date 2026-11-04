---
name: custo-no-transcript
description: Onde o custo de uma sessão aparece no transcript .jsonl do Claude Code (cost-state só no fim da sessão) e como calcular o custo em tempo real pelos tokens de cada mensagem
metadata:
  type: reference
---

# Custo da sessão no transcript do Claude Code

- O custo acumulado da sessão fica em linhas `{"type":"cost-state","totalCostUSD":...,"modelUsage":{...}}` do `.jsonl` (ver [[sessoes-e-resume]] para onde ficam os arquivos). Essas linhas não têm `timestamp`.
- **Armadilha:** o `cost-state` só é gravado quando a sessão termina (sai do `claude`), às vezes também em pontos intermediários (ex: ao retomar). Durante a sessão ele não existe: quem lê só o `cost-state` vê US$ 0 em toda sessão que ainda está rodando. Conferido no Claude Code 2.1.312 (out/2026).
- Para ter o custo em tempo real, somar o uso de cada linha `"type":"assistant"`: `message.model` e `message.usage` (`input_tokens`, `output_tokens`, `cache_read_input_tokens`, `cache_creation_input_tokens`, com `cache_creation.ephemeral_1h_input_tokens`/`ephemeral_5m_input_tokens`) vezes o preço do modelo.
- A mesma mensagem aparece em várias linhas `assistant` (uma por bloco de conteúdo, com o mesmo `message.id`): deduplicar por `message.id`, senão o custo é contado 2 a 3 vezes.
- As linhas `api-request` trazem o modelo e os parâmetros da chamada, mas não o uso nem o custo.
- A mesma mensagem também se repete **entre arquivos**: a sessão retomada copia o histórico para o `.jsonl` novo (em out/2026: 16,9 mil linhas `assistant` para 8,7 mil ids). Deduplicar globalmente, não só por arquivo.
- Conta do custo: input × preço de input; escrita do cache × 1,25 (TTL de 5 min) ou × 2 (TTL de 1 h, em `cache_creation.ephemeral_1h_input_tokens`); leitura do cache × 0,1 do input (0,05 no Opus 5.5, 0,025 no Fable/Mythos 5.1); output × preço de output; `usage.speed == "fast"` custa o dobro. Fica a preço de tabela da API, não o que a assinatura cobra.
- Chamadas `claude -p --no-session-persistence` não gravam transcript: o custo delas só existe no `total_cost_usd` do JSON de resultado.
- Implementado no BahCode (`ide-bahcode`, `src/spend.rs`): a barra mostra os tokens e o custo do dia, e o modal mostra 7 dias, 30 dias, total e recorde.
