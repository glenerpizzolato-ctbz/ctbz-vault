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

Plano do back-end do Cadastro de Avisos e Mensagens no `atendimento-zendesk` ([[PRD-179459]], sub-task PRD-179410, épico [[PRD-164638]]). Versão enxuta de 27/11/2026, com 7 seções curtas:

1. **Rota principal**: `GET /zendeskapps/warnings-and-messages/tickets/:ticketId/avisos`. É a rota central, por decisão do usuário em 27/11/2026. Ela vai do ticket (tabela `tickets`, ou a API do Zendesk se ele ainda não sincronizou) aos dados atuais do cliente e do guardião, avalia as mensagens no ar (em memória, recarregadas quando alguém salva) e ordena pela RN22.
2. **Regras**: OU de E, com é/não é. É a forma do protótipo (`ruleHitsC`/`condHits`): sem aninhamento livre, mas expressa qualquer combinação. São 16 critérios, com um motor único.
3. **Persistência**: `regras jsonb` (`{schemaVersion, rules:[{conds:[{criterio, op, valores}]}]}`), com as colunas derivadas `criterios[]` e `planos[]` para os filtros, `versao` para concorrência e histórico só de inserção. Tabelas normalizadas e JSON Logic foram descartadas.
4. **Rotas**: consulta por ticket, CRUD de `/mensagens` (sem exclusão, com `PATCH /status` e `/historico`), `/criterios/:id/valores`, `/planilhas` e `/alcance`. Os caminhos são proposta e ainda serão combinados com o PRD-179460. O `GET /criterios` (catálogo servido pela API) foi retirado: a lista dos 16 critérios fica fixa no front.
5. **Alcance e planilha**:
   - O alcance é calculado por `POST /alcance` com debounce de cerca de 300 ms, contando sobre um retrato da base de clientes. Nada é gravado.
   - A planilha é lida e descartada, **sem bucket**. Só o nome do arquivo e os aceitos entram na regra; os recusados voltam com o motivo.
6. **MRs**: 7, com a consulta por ticket em 3º.
7. **Em aberto**: a fonte dos dados do cliente e a base do alcance; o processo de abertura de um ticket sem CNPJ; os grupos de Publicador e Leitor; o que fazer quando a fonte cai.

O que é RN e o que é proposta: só o alcance tem RN numerada (RN14). Planilha e valores dos critérios vêm de outras seções da especificação (tabela "Critérios disponíveis" e "Considerações"). Os caminhos e formatos das rotas são proposta, inclusive o da consulta.

Atualizar quando os pontos em aberto forem decididos ou se o contrato mudar na conversa com o front.

Relacionado: [[_atendimento-zendesk-indice|atendimento-zendesk]], [[PRD-179459]], [[PRD-179460]], [[PRD-179389]].
