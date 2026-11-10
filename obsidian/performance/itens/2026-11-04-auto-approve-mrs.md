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
  - seguranca
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

Em 2026-11-10, a partir das skills de revisão de dois colegas do time, a revisão e o auto-approve ganharam a régua deles. A revisão devolve um relatório estruturado (veredito proposto, um check por dimensão, evidência `arquivo:linha` ou URL oficial em cada achado e a cobertura de cada arquivo do diff), conferido depois pelo código: achado crítico sem evidência é rebaixado, arquivo sem cobertura segura a aprovação. Texto do MR passou a ser tratado como dado, e uma instrução escondida vira achado de segurança. Os achados blocker e major de um colega passam por uma validação cética antes de virarem thread, e o comentário com tom fora da régua não vai sozinho. A revisão compara o diff com os critérios do card do Jira e, em diff grande, divide a leitura em subagentes. Novas travas no auto-approve: branch em dia com a base, nenhum job falho (nem `allow_failure`), projetos que nunca aprovam sozinhos, retirada da própria aprovação quando o commit novo não aprovaria, nova tentativa depois de 1 h e teto diário de gasto. As afirmações sobre produção da descrição ("nenhum cliente usa X", "atinge os 27") passaram a ser conferidas no banco de produção por um comando próprio, que só aceita serviço só leitura e consulta de agregação sem dado pessoal, numa transação `READ ONLY`. No caminho, encontrei e corrigi uma falha de segurança: o modo `bypassPermissions` do Claude Code anulava a lista de ferramentas liberadas de todas as chamadas do revisor, então uma instrução escondida num MR podia levar o Claude a rodar qualquer comando; todas passaram a usar `--permission-mode dontAsk`.

## Resultado

Aprovação automática auditável e conservadora para MRs triviais do time; o ganho em número de MRs ainda não foi medido.

## Evidências

- Branch `feat/mr-auto-approve` do ide-bahcode (commits `e0dbb4d`, `62c45c9`, `56b3da5`)
- [[2026-11-04-skills-fluxo-desenvolvimento]]
- Commit `b00e66a` do ide-bahcode (quebra de fluxo dependente) e [[consumidores-entre-repositorios]]
- Commits `8524d69` a `2b6fffb` do ide-bahcode (branch `feat/rest-tab`, 2026-11-10): régua dos revisores do time, conferência em prod e o `--permission-mode dontAsk`
