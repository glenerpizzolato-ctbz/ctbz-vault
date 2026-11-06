---
name: 2026-11-04-auto-approve-mrs
description: "Auto-approve de MRs do time com revisão por IA e regras restritivas (BahCode)"
metadata:
  type: project
tags:
  - performance
titulo: "Auto-approve de MRs do time com revisão por IA e regras restritivas"
data: 2026-11-04
periodo: 2026QD3
categorias:
  - ia
  - processo
impacto: medio
fontes:
  - "[[2026-11-04-skills-fluxo-desenvolvimento]]"
---

# Auto-approve de MRs do time com revisão por IA e regras restritivas

- **Período:** 2026QD3 · **Categorias:** ia, processo · **Impacto:** medio

## Contexto

Revisar MRs pequenos e limpos do time consome tempo, mas aprovar sozinho exige travas para não aprovar MR de bot, MR grande ou com problema.

## O que fiz

No BahCode, a revisão automática do Claude passou a dar uma nota de 0 a 100 para segurança, aderência a ADRs, qualidade de código e testes. Em cima dela criei o auto-approve (desligado por padrão), que só aprova quando todas as regras ligadas passam: MR do grupo do time, autor que eu sigo no GitLab (exclui Duo e bots de IA), menos de 10 arquivos, pipeline verde e sem threads, revisão sem nenhuma sugestão e confiabilidade de pelo menos 85%. Regra que não pôde ser conferida conta como reprovada. Cada aprovação fica registrada num sino com o link do MR, o modal do MR mostra as notas e o que cada regra viu, e tudo é configurável. Os prompts do Claude (MRs, PRCs e Attention) passaram a ser editáveis pela tela de Configurações.

Em 2026-11-06 a revisão ganhou a checagem de **quebra de fluxo dependente**, nos MRs do time, nos meus e na avaliação das threads: o Claude lê o vault e os repositórios clonados, acha quem consome o contrato que o diff muda (rota, tópico, evento, tabela) e confirma no código do consumidor, apontando o arquivo:linha que quebra e como manter compatível. Nasceu de um caso real: um MR meu no `contato-service` que ia quebrar a tela de contato do `atendimento-canais-admin`, apontado por um colega em thread. Criei também a convenção de registrar consumidores no vault ([[consumidores-entre-repositorios]]).

## Resultado

Aprovação automática auditável e conservadora para MRs triviais do time; o ganho em número de MRs ainda não foi medido.

## Evidências

- Branch `feat/mr-auto-approve` do ide-bahcode (commits `e0dbb4d`, `62c45c9`, `56b3da5`)
- [[2026-11-04-skills-fluxo-desenvolvimento]]
- Commit `b00e66a` do ide-bahcode (quebra de fluxo dependente) e [[consumidores-entre-repositorios]]
