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
  - "[[PRD-176094 - Ticket de chat web cai na Ouvidoria sem o cliente pedir]]"
atualizado_em: 2026-11-10
---

# Desidratação da Ouvidoria e menu da Super Ouvidoria

- **Período:** 2026QD3 · **Categorias:** outros-times, entrega · **Impacto:** medio

## Contexto

Muitos contatos caíam na Ouvidoria sem necessidade e sobrecarregavam o time (demanda da própria Ouvidoria).

## O que fiz

No número exclusivo da Super Ouvidoria, implementei na Ultimate um menu que aponta o canal oficial de cada plano e transborda só reclamações; criei a área `OUVIDORIA` na autenticação do atendimento-zendesk (!165) para autenticar Expert e as flags de vínculo (empresa ativa, inativa, em abertura) sem quebrar a autenticação (!176); documentei como destravar conversa presa na Ultimate.

Em 2026-11-10, investiguei a ACR PRD-176094, sobre tickets do chat web que caíam na Ouvidoria. Pelos audits do Zendesk e pelo metadata do Sunshine, encontrei a origem real da tag `sys_grupo_ouvidoria`: as `conversationTags` do widget do chat web, gravadas no botão Reclamação/Elogio e reenviadas a partir do `localStorage`. O diagnóstico automático (Bolt) e o card apontavam como causa a integração da Ultimate, que só repassa esse metadata.

Em 2026-11-11, no ticket 30176681 da mesma ACR, expliquei as mensagens de erro de autenticação que apareciam antes do log da Ultimate: cruzando os logs do `atendimento-zendesk` e do `atz-worker-webhooks`, mostrei que a primeira abertura do chat ficou anônima por uma corrida entre o `loginUser` e o `openChat` no widget (duas conversas no Sunshine, juntadas pelo Zendesk depois do login), um defeito separado da causa da Ouvidoria.

## Resultado

Só as reclamações de fato chegam à Ouvidoria pelo número exclusivo.

Na ACR PRD-176094, dimensionei o problema em 142 tickets com a tag de ouvidoria de 25/10 a 10/11 (133 do chat web) e documentei a causa e o próximo passo para o time do widget.

Em 2026-11-11, aprofundei a mesma ACR: sem chamar a API de prod do Zendesk, reconstruí pelos logs do `atendimento-zendesk` e pelos eventos no BigQuery a navegação dos clientes no widget antes da Ultimate. Com isso, descartei duas hipóteses levantadas pelo time: o incidente da Ultimate de 03/11 (o comportamento é diário e estável antes e depois, 34 casos mapeados em 4 dias) e um erro na API de elegibilidade da ouvidoria (sem alteração desde set/2025; mostrei com dados que ela só exibe o botão, contrapondo a análise de um colega). Separei causa direta (clique em "Reclamação/Elogio") de causa contribuinte (regra de elegibilidade das 24h, que dobrou o público no dia seguinte ao incidente) e documentei tudo no Jira com a planilha dos casos.

## Evidências

- [[PRD-173035]]
- [[PRD-174558]]
- [[PRD-173036]]
- [[PRD-174256]]
- [[categoria-plano-autenticacao-whatsapp]]
- [[destravar-atendimento-ultimate]]
- [[PRD-176094 - Ticket de chat web cai na Ouvidoria sem o cliente pedir]] · https://contabilizeicontabilidade.atlassian.net/browse/PRD-176094
