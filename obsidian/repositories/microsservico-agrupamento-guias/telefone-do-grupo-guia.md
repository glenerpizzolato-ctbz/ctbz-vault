---
name: telefone-do-grupo-guia
description: De onde vem o telefone gravado em grupo_guia.contato (usado no WhatsApp do agrupamento) — telefone principal da Empresa no monolito, publicado pelo plataforma-faturamento-worker
metadata:
  type: reference
tags: [microsservico-agrupamento-guias, plataforma-faturamento-worker, agrupamento-guias]
---

# Telefone do `grupo_guia`

O telefone para onde vai o WhatsApp do agrupamento é decidido **no publicador do evento**, não no microsserviço: o microsserviço só copia o que chega.

1. **Publicação** (`plataforma-faturamento-worker`, `AgrupamentoGuiasFacade.enviaMsAgrupamentoGuia`/`buildDto`): só para empresas com plano `EXPERT_ESSENCIAL`, monta o `EmpacotamentoGuiasDTO` com `responsavel`/`email` do `empresa.getResponsavel()` e `telefone(empresa.getNumeroTelefonePrincipal())`, e publica no tópico `agrupar-guias-empresa` (projeto `contabilizei-impostos`).
2. **Regra do telefone principal** (`contabilizei-back-core`, `Empresa.getTelefonePrincipal()`): primeiro telefone da `listaTelefone` da empresa com tipo `COMERCIAL`; se não houver, o primeiro `CELULAR`; se não houver, o primeiro da lista, qualquer tipo. `getNumeroTelefonePrincipal()` devolve só o `numero` (sem DDI), ou `""` se a empresa não tiver telefone. É o telefone **da empresa**, não o do responsável/sócio.
3. **Gravação** (`microsservico-agrupamento-guias`, `AgrupamentoGuiasConsumer` na sub `ms-agrupamento-guias.sub.agrupar-guias` → `GrupoGuiaServiceImpl.criaGrupoGuia`): grava `contato` (jsonb) = `{nome: dto.responsavel, email: dto.email, telefone: dto.telefone}`. A rota `POST /agrupamento-guias` aceita o mesmo DTO manualmente.
4. **Envio**: `ContatoDTO.fromJson` exige telefone não vazio (senão `DADOS_INCOMPLETO`) e o WhatsApp sai com `destino = "+55" + celular`.

## Armadilhas

- O contato **congela na criação** do `grupo_guia`: o `reprocessar` (status de erro ou sem guia) reaproveita o registro e não atualiza `contato`; outra mensagem para a mesma empresa/período com grupo existente cai em `AgrupamentoJaExisteException`. Trocar o telefone na empresa depois do agrupamento não muda o destino daquela competência.
- Se a empresa tiver telefone fixo cadastrado como `COMERCIAL`, ele ganha do `CELULAR` e o WhatsApp vai para o fixo.
- O fluxo de diagnóstico de aumento de imposto (`DiagnosticoAumentoImpostoRecordServiceImpl`) resolve o telefone por outra regra parecida, `DadosEmpresaResponseDTO.resolverTelefone()` (primeiro `COMERCIAL`, depois `CELULAR`, sem fallback para outro tipo), a partir dos dados da empresa vindos da API.
