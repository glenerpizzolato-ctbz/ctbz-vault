---
name: tests-indice
description: "Hub dos roteiros de teste (preparação de massa, como disparar fluxos e conferir resultado) por domínio e por repositório"
metadata:
  type: reference
tags:
  - tests-indice
---

# Testes

Roteiros para preparar massa de teste, disparar fluxos e conferir o resultado nos sistemas da Contabilizei, principalmente em dev. Uma nota por roteiro em `itens/`.

## Visões

- [[ctbz/tests/_por-dominio|Por domínio]]
- [[ctbz/tests/_por-repositorio|Por repositório]]

## Estrutura

- `itens/<slug>.md`: um roteiro por nota, com o front-matter `dominio` (lista), `repositorios` (lista), `ambiente` e `atualizado_em`.
- Novo roteiro: criar a nota em `itens/` e adicioná-la nas duas visões.

## Vocabulário

- **dominio:** mesmo vocabulário de [[ctbz/PRDs/_prds-indice|PRDs]]: `atendimento`, `copilot`, `csat`, `impostos`, `monitoria-ia`, `notas-fiscais`, `notificacoes`, `plataforma`, `ultimate`
- **repositorios:** nome do repositório em `~/repositories` (ou `dotfiles` para scripts próprios)
- **ambiente:** `local`, `dev`, `prd`
