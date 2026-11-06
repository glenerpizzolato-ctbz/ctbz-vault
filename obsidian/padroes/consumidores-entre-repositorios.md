---
name: consumidores-entre-repositorios
description: Registrar no vault quem consome cada contrato (rota, tópico, evento, tabela) de um repositório, para a revisão de MRs achar quebra de fluxo dependente
metadata:
  type: reference
tags:
  - padroes
  - mr-review
---

# Consumidores entre repositórios

A revisão de MRs do BahCode (a do grupo, a auto-revisão e a avaliação das threads) procura **quebra de fluxo dependente**: se o diff muda um contrato que outro repositório consome. Ela acha o consumidor pelo vault (as notas do repo, o catálogo `infra/` e as pastas `repositories/<outro>/` que citam a rota ou o tópico) e confirma no código dele, em `~/repositories/<consumidor>`. Sem registro no vault, ela ainda pode achar pelo `Grep` no código, mas o vault é o atalho.

Origem: um MR do `contato-service` mudou o contrato de `POST /api/v1/optouts`, e um colega apontou em thread que ia quebrar a tela de contato do `atendimento-canais-admin`, que consome a rota.

Como registrar:

- **No consumidor:** na nota do fluxo, citar o repositório provedor pelo nome e o contrato exato (método e path, tópico, evento, tabela) e o arquivo que o usa. Ex.: `atendimento-canais-admin/optout-tela-contato` (`POST /api/v1/optouts` do `contato-service`, por `useRegistrarOptout.ts`).
- **No provedor:** uma seção `## Consumidores` no índice do repo, uma linha por consumidor: o repositório, o contrato e a nota do consumidor.
- Tópicos, filas e serviços do GCP já têm consumidores no catálogo `infra/` (gerado pela skill `atualizar-catalogo-gcp`).
