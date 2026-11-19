---
name: dependencias-entre-repositorios
description: Cada repositório tem no vault a nota dependencias-<repo>.md com o que consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, confirmado no código e espelhado no provedor, para a revisão de MRs achar quebra de fluxo dependente
metadata:
  type: reference
tags:
  - padroes
  - mr-review
  - dependencias
---

# Dependências entre repositórios

Cada repositório com pasta no vault tem a nota `repositories/<repo>/dependencias-<repo>.md`, linkada no índice dele: o que o repositório **consome** (outros repositórios, libs internas, infra GCP, bancos e dados, terceiros) e quem o **consome**. Ela cresce conforme trabalhamos no repositório.

Origem: um MR do `contato-service` mudou o contrato de `POST /api/v1/optouts`, e um colega apontou em thread que ia quebrar a tela de contato do `atendimento-canais-admin`, que consome a rota. Desde 2026-11-06 a revisão de MRs do BahCode (a do grupo, a auto-revisão e a avaliação das threads) procura **quebra de fluxo dependente**: se o diff muda um contrato que outro repositório consome. Ela acha o consumidor pelo **Consumido por** da nota do repositório do MR e confirma no código dele, em `~/repositories/<consumidor>`. Sem registro, ela ainda pode achar pelo `Grep`, mas a nota é o atalho. Até 2026-11-19 isso era só uma seção `## Consumidores` no índice do provedor.

## A nota

Duas partes:

1. **Confirmado** (à mão, pelos agentes): `## Consome`, com as subseções Repositórios internos, Libs internas, Infra GCP, Bancos e dados e Terceiros, e `## Consumido por`. Uma linha por contrato, no formato `` - `<outro repo ou serviço>`: <contrato> — por `<arquivo do consumidor>` (<nota do fluxo>) ``. Contrato é o que quebra se mudar: método e path da rota, tópico e quem publica, fila, tabela/coluna, webhook, evento, a função da lib.
2. **Levantamento automático** (entre os marcadores `deps:auto`, gerado pela skill `mapear-dependencias`): os candidatos achados pelo nome no código, nos manifestos, no catálogo `infra/` e no [[grafo-chamadas-canais|grafo manual]]. Nunca editar à mão; o script reescreve só esse bloco.

## Quando registrar

- **Ao trabalhar num repositório** (ler, investigar, mudar), se ele ainda não tem a nota, gerá-la com a skill `mapear-dependencias`.
- **Ao confirmar no código uma dependência** (o client HTTP que chama outro serviço, o tópico que publica ou consome, a tabela que lê de outro sistema, a API externa), escrever a linha em **Consome** e espelhar no **Consumido por** do provedor, na mesma hora. As duas pontas sempre juntas.
- **Ao mudar um contrato**, conferir o **Consumido por** antes, e ao descobrir um consumidor que não estava lá, acrescentá-lo.

## Onde mais há dependências

- [[_infra-indice|Catálogo infra/]] (skill `atualizar-catalogo-gcp`): tópicos, subscriptions, filas, schedulers e serviços com os repositórios que os citam, e a visão reversa [[por-repositorio]]. É a fonte da seção Infra GCP do levantamento.
- [[grafo-chamadas-canais]]: grafo manual de quem chama quem entre Canais, Experts e AIDA, fotografia de 2026-11-11 a conferir no código.
