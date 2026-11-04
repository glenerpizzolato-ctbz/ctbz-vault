---
name: 2026-10-30-ouvidoria-desidratacao
description: "Desidratação da Ouvidoria e menu da Super Ouvidoria"
metadata:
  type: project
tags:
  - performance
titulo: "Desidratação da Ouvidoria e menu da Super Ouvidoria"
data: 2026-10-30
periodo: 2026QD3
categorias:
  - outros-times
  - entrega
impacto: medio
fontes:
  - "[[PRD-173035]]"
  - "[[PRD-174558]]"
  - "[[PRD-173036]]"
  - "[[PRD-174256]]"
  - "[[categoria-plano-autenticacao-whatsapp]]"
  - "[[destravar-atendimento-ultimate]]"
---

# Desidratação da Ouvidoria e menu da Super Ouvidoria

- **Período:** 2026QD3 · **Categorias:** outros-times, entrega · **Impacto:** medio

## Contexto

Muitos contatos caíam na Ouvidoria sem necessidade e sobrecarregavam o time (demanda da própria Ouvidoria).

## O que fiz

No número exclusivo da Super Ouvidoria, implementei na Ultimate um menu que aponta o canal oficial de cada plano e transborda só reclamações; criei a área `OUVIDORIA` na autenticação do atendimento-zendesk (!165) para autenticar Expert e as flags de vínculo (empresa ativa, inativa, em abertura) sem quebrar a autenticação (!176); documentei como destravar conversa presa na Ultimate.

## Resultado

Só as reclamações de fato chegam à Ouvidoria pelo número exclusivo.

## Evidências

- [[PRD-173035]]
- [[PRD-174558]]
- [[PRD-173036]]
- [[PRD-174256]]
- [[categoria-plano-autenticacao-whatsapp]]
- [[destravar-atendimento-ultimate]]
