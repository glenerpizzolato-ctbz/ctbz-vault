---
name: plano-api-avisos
description: "Artefato Plano da API de Avisos e Mensagens (PRD-179459): as regras de destinatários do protótipo são OU de E com é/não é (forma normal disjuntiva, sem aninhamento livre); persistência recomendada em JSONB com schemaVersion e colunas derivadas; contrato REST com regras no formato gravado + catálogo de critérios; motor único para consulta e alcance; sequência de MRs e pontos em aberto"
metadata:
  type: reference
tags:
  - artefatos
  - atendimento-zendesk
  - avisos-e-mensagens
link: https://claude.ai/artifact/7mfamWLKVGnosybWnbo3Pe
arquivo: arquivos/plano-api-avisos.html
criado_em: 2026-11-27
atualizado_em: 2026-11-27
retrato: "atendimento-zendesk e20a15a20 (master) · protótipo 'Cadastro de Avisos e Mensagens — versão final.html' · descrição do PRD-179389 (backup de 26/11/2026) com RN01–RN22"
---

# Plano da API de Avisos e Mensagens

Plano do back-end do Cadastro de Avisos e Mensagens no `atendimento-zendesk` ([[PRD-179459]], sub-task PRD-179410, épico [[PRD-164638]]).

A página mostra:

- **Rota principal**: `GET /zendeskapps/warnings-and-messages/tickets/:ticketId/avisos` (decisão do usuário em 27/11/2026: a consulta por ticket é a rota central; a listagem com filtros existe para o cadastro). O ticket sai da tabela `tickets` (espelho do Zendesk: `organization_cnpj`, `organization_plano`, `assignee_id`, `group_id`), com a API do Zendesk como reserva quando ele ainda não sincronizou. As mensagens no ar ficam compiladas em memória e são recarregadas quando alguém salva, com a versão do conjunto guardada no Redis. Os dados do cliente têm cache curto. A página traz o formato da resposta e os casos de erro da especificação.
- **Forma das regras no protótipo**: a mensagem tem regras somadas com OU. Cada regra junta critérios com E, e cada critério tem a relação é/não é e valores que valem como OU entre si (`ruleHitsC`/`condHits` no protótipo). Não há if/else aninhado livre: é forma normal disjuntiva, que expressa qualquer combinação. Inclui a tabela de semântica (dado ausente: `é` → falso, `não é` → verdadeiro; status calculado; ordem RN22) e o catálogo dos 16 critérios.
- **Persistência**: recomendada a coluna `regras jsonb` (`{schemaVersion, rules:[{conds:[{criterio, op, valores}]}]}`) validada por Zod, com colunas derivadas (`criterios[]`, `planos[]`, `termos_busca`) para os filtros da lista. Tabelas normalizadas e árvore genérica (JSON Logic) foram descartadas. Modelo das tabelas `avisos_mensagens` e `avisos_mensagens_historico`.
- **Contrato REST**: o detalhe devolve `rules` no mesmo formato gravado (com rótulos resolvidos) e o front monta a tela pelo `GET /criterios`; a lista traz `resumo` e alcance. Tabela com as 12 rotas e o papel de cada uma.
- **Motor de regras**: catálogo (um item por critério com `test`) → `RuleEngine` (`validate`, `matches`, `describe`) → contextos de cliente e guardião, usado pela consulta por ticket e pelo alcance. Alcance recomendado sobre uma base de clientes em memória/Redis; alternativa `toSql`.
- **Sequência de 7 MRs** (a consulta por ticket vem logo depois do motor) e os pontos em aberto (ticket de cliente em ativação sem CNPJ, fonte dos dados do cliente, grupos dos papéis, fonte fora do ar, tamanho da base).

Conclusão principal: guardar as regras como JSON em OU de E, que é o formato que o front já monta, e ter um único motor com catálogo de critérios, em vez dos ifs do `ValidarRestricaoService` dos bots.

Atualizar quando os pontos em aberto forem decididos ou se o modelo mudar na implementação.

Relacionado: [[_atendimento-zendesk-indice|atendimento-zendesk]], [[PRD-179459]], [[PRD-179460]], [[PRD-179389]].
