---
name: zendeskapp-whatsapp-ativo-projeto-x-atendimento
description: "Mapa de ponta a ponta do WhatsApp ativo pelo app do Zendesk: o que o Projeto do template (mensagem_ativa_template.squad), o Atendimento do envio (mensagem_ativa.integracao) e a categoria da Meta definem (WABA, número, filas, agente, categoria, validade, fluxo do bot na resposta, opt-out)"
metadata:
  type: reference
tags:
  - zendeskapp-whatsapp-ativo
  - atendimento-zendesk
  - whatsapp-ativo
atualizado_em: 2026-11-19
---

# Projeto do template x Atendimento do envio

Página visual com diagramas e simulador: [[mapa-whatsapp-ativo]] (https://claude.ai/artifact/6igTX8xWFNasBTFaBEDDzP) (retrato de 19/11/2026, app `db1bdc9`, backend `fc5b2fe3f`).

## As três chaves

- **Projeto** (cadastro, `ModalAddTemplate` → `CreateWhatsappTemplateService`): vira `integration` para criar o template na Meta (`sunshine.createTemplate(dto.integration)`, ou seja, define a **WABA** onde ele existe) e `mensagem_ativa_template.squad`. Também define em quais Atendimentos o template aparece (`template.squad === getSquad(atendimento)`) e o opt-out `SURVEY` (squad `SURVEY`). Não define o número de saída.
- **Atendimento** (envio individual/massivo): é a `integracao`. Define o número (`APP_MODULES_WHATSAPP_ATIVO_INTEGRATIONS_JSON` no configmap `atendimento-zendesk-prd`), as filas, se oferece agente (só CORE, EXPERTS, REPRESENTANTES), a `categoria` (`mapearCategoriaAtivo`), a validade (48 h em REPRESENTANTES, 24 h nos demais) e o fluxo do bot que reconhece a resposta.
- **Categoria Meta** (`mensagem_ativa_template.categoria`, atualizada pelo `template_category_update`): custo e opt-out MARKETING/TRANSACTIONAL quando não é pesquisa.

## Squad do template é espelho da integração? Não

Mesmo vocabulário (`IntegracaoWhatsapp`), mas não é espelho. O backend nunca compara `mensagem_ativa_template.squad` com a `integracao` do envio (a validação busca o template só pelo nome): a ligação é só o filtro `getSquad` da tela. No cadastro, o valor só escolhe a WABA e fica gravado; número, filas e resposta saem da `integracao` de cada envio. `getSquad` não é identidade (INBOUND/REPRESENTANTES → EXPERTS), há projetos sem Atendimento e a mitigação troca a integração no worker.

## Filas

`BuscarFilasService`: CORE, BANK, OUVIDORIA e CORRETORA buscam grupos dinâmicos em `zendesk_grupos` (fluxo BASICO_PADRAO/BANK/OUVIDORIA/CORRETORA, canal WhatsApp, `habilitadoWhatsppAtivo`, com roteamento cadastrado); os demais na tabela `fila` (`atendimento = X`, nome com `[WHATSAPP]`).

## Resposta do cliente

`MensagemAtivaRepository.buscarMensagensAtivas`: fluxo ESPECIAIS procura por `categoria` em `CategoriasEspeciais` (WORKER_CSAT, REPRESENTANTES_ATIVO, JUMP, INBOUND, CSA, ATIVACAO_MIGRACAO, FLOW, ATIVOS_WORKFLOW); fluxos de `TipoFluxoBotMain` procuram `integracao IN (fluxo, MITIGACAO)`; os demais `integracao = fluxo`. Sempre dentro de `criado_em + validade_em_minutos`. `nome_grupo` + `agente_retorno` viram a tag de roteamento (agente online com capacidade recebe direto).

## Armadilhas

- Projetos RESERVA, REPRESENTANTES, INBOUND, JUMP e MITIGACAO aparecem no cadastro, mas nenhum Atendimento lista esses squads (`getSquad` devolve EXPERTS para INBOUND/REPRESENTANTES; RESERVA não está na lista de Atendimentos). Templates desses projetos só saem por API.
- INBOUND e REPRESENTANTES listam templates do projeto EXPERTS.
- "Pesquisa com Workflow" grava `squad = ATIVOS_WORKFLOW`: apesar do nome, não cai no opt-out `SURVEY`.
- O massivo não grava `mensagem_ativa.squad` (o individual grava `squad = integracao`).
- Integração na WABA Main + telefone em `flag_tel_mitigacao` → `integracao = MITIGACAO` (número de mitigação).

Opt-out em detalhe: [[whatsapp-ativo-finalidade-optout]]. Permissões: [[permissoes-por-grupo]].
