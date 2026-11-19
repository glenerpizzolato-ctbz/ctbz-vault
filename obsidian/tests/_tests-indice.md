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

- [[tests/_por-dominio|Por domínio]]
- [[tests/_por-repositorio|Por repositório]]

## Regras gerais

- **Testes de WhatsApp: não acessar o WhatsApp Web do Glener.** O Claude não abre o WhatsApp Web (claude-in-chrome), não lê conversas e não envia mensagens. Pedir ao Glener para enviar ou responder (texto exato e, se importar, o momento) e aguardar a confirmação dele antes de seguir; conferir o resultado pelo Zendesk e pela Ultimate. Receita em [[testar-bot-whatsapp]].

## Estrutura

- `itens/<slug>.md`: um roteiro por nota, com o front-matter `dominio` (lista), `repositorios` (lista), `ambiente` e `atualizado_em`.
- Novo roteiro: criar a nota em `itens/` e adicioná-la nas duas visões.

## Vocabulário

- **dominio:** mesmo vocabulário de [[PRDs/_prds-indice|PRDs]]: `atendimento`, `copilot`, `csat`, `impostos`, `monitoria-ia`, `notas-fiscais`, `notificacoes`, `plataforma`, `ultimate`
- **repositorios:** nome do repositório em `~/repositories` (ou `dotfiles`/`ctbz-vault` para scripts e skills próprios)
- **ambiente:** `local`, `dev`, `prd`
