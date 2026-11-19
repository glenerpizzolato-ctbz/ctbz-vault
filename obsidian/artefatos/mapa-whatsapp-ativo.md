---
name: mapa-whatsapp-ativo
description: "Artefato Mapa do WhatsApp Ativo: diagramas interativos de Projeto do template (squad) x Atendimento do envio (integracao) e de como o Atendimento preenche os campos do envio (categoria, validade, fila, agente, número, fluxo da resposta, opt-out)"
metadata:
  type: reference
tags:
  - artefatos
  - whatsapp-ativo
  - zendeskapp-whatsapp-ativo
  - atendimento-zendesk
link: https://claude.ai/artifact/6igTX8xWFNasBTFaBEDDzP
arquivo: arquivos/mapa-whatsapp-ativo.html
html_share: "" # pendente: gerado em ~/Downloads/mapa-whatsapp-ativo.html em 19/11/2026
criado_em: 2026-11-19
atualizado_em: 2026-11-19
retrato: "zendeskapp-whatsapp-ativo origin/master db1bdc9 · atendimento-zendesk master fc5b2fe3f · configmap atendimento-zendesk-prd"
---

# Mapa do WhatsApp Ativo

Link: https://claude.ai/artifact/6igTX8xWFNasBTFaBEDDzP (privado; compartilhar pelo menu Share). Fonte: [arquivos/mapa-whatsapp-ativo.html](arquivos/mapa-whatsapp-ativo.html).

## O que mostra

- **Qual Projeto aparece em qual Atendimento**: diagrama bipartido do filtro `getSquad` da tela, colorido pelo número de saída; projetos sem Atendimento marcados "só API".
- **O que o Atendimento preenche em cada envio**: coordenadas paralelas Atendimento → squad listado → `categoria` → fluxo da resposta → número, com a ficha do envio (o que a tela manda, o que `mensagem_ativa` grava e o efeito no envio/resposta).
- O que o squad (cadastro) e a integração (envio) controlam, a esteira do cadastro à resposta, simulador Projeto x Atendimento, tabela de referência por Atendimento e armadilhas.

## Conclusão principal

O squad do template não é espelho do Atendimento: mesmo vocabulário (`IntegracaoWhatsapp`), mas a ligação é só o filtro da tela; o backend nunca compara `template.squad` com a `integracao`. Detalhes em [[projeto-x-atendimento]].

## Quando atualizar

Ao mudar `getSquad`, `mapearCategoriaAtivo`, `mapearValidadeEmMinutos`, `BuscarFilasService`, `CategoriasEspeciais`/`TipoFluxoBotMain`, a lista de Atendimentos/Projetos do app ou o `APP_MODULES_WHATSAPP_ATIVO_INTEGRATIONS_JSON`. Os dados ficam nas constantes no topo do `<script>` do HTML.

Relacionadas: [[projeto-x-atendimento]], [[whatsapp-ativo-finalidade-optout]], [[permissoes-por-grupo]].
