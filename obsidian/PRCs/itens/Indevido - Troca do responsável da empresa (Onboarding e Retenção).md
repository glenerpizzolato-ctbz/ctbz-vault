---
name: prc-indevido-troca-responsavel-empresa
description: PRC — pedido para trocar o responsável (sócio) da empresa ou os dados dele chega a nós, mas é de Onboarding e Retenção; devolver como indevido com a orientação padrão (SSO e depois admin man-responsavel)
metadata:
  type: reference
tags:
  - prc
  - indevido
canal:
  - wpp
  - email
  - chat
dominio:
  - atendimento
sistemas:
  - sso
  - plataforma-admin
acr: []
ocorrencias: []
qtd_ocorrencias: 0
ultima_ocorrencia:
---

# Troca do responsável da empresa - indevido (Onboarding e Retenção)

## Sintoma

O PRC pede para trocar o responsável da empresa (ex: outro sócio passa a ser o responsável) ou alterar as informações dele (nome, e-mail, CPF, telefone). Esse pedido **não é da Engenharia Canais**: teoricamente é do time de **Onboarding e Retenção**, e a orientação que eles dão é a mesma do processo oficial, que o próprio atendimento consegue executar pelos nossos sistemas.

Não confundir com o caso em que o contato da Zendesk está errado por causa do cadastro do responsável (ver [[PRD-151519 - Cliente com mais de um contato cadastrado com mesmo telefone na zendesk]] e [[sincronizacao-usuario-zendesk]]): aí o problema chega como contato/ticket errado na Zendesk e é nosso.

## Como resolver

Devolver como **indevido**, sem fazer a troca:

1. Comentar no PRC com o texto padrão abaixo.
2. Atribuir ao Glener (`assignee` = `{"accountId": "712020:71b4f148-e139-4098-b2b0-0fe4e7a37cf1"}` no `editJiraIssue`).
3. Fechar com `Solved` (saindo de `To-do`, passar antes por `Started`, 61; depois `Solved`, 121), com:
   - Devido ou Indevido? (`customfield_19805`): **Indevido** (`22183`)
   - Resolução do chamado (`customfield_18429`): **Envio de orientações (indevido)** (`17921`)
   - Tipo de chamado (`customfield_18460`): Suporte a operação (`18048`)
   - Os demais obrigatórios (Classificação N3, Funcionalidade, Grau do Impacto, Ofensor) seguem o padrão de [[PRD-168944 - Cliente não quer receber pesquisa (CSAT e-ou NPS)]]; registrar aqui os valores usados na primeira PRC fechada por esse fluxo.

### Comentário padrão

> Olá! Esse tipo de solicitação (troca/alteração do responsável da empresa) pertence ao time de **Onboarding e Retenção**, e não à Engenharia Canais, por isso estamos devolvendo o chamado como indevido.
>
> Geralmente, a orientação que eles dão é que a alteração de informações do responsável da empresa pode ser realizada através dos nossos sistemas:
>
> 1. Primeiro no SSO: https://docs.google.com/presentation/d/1ICG8L4P4IQVNChxLFO5Q7kQRTUWW5e2f4emirJRkoDo/edit?usp=sharing
> 2. Depois no Responsável na plataforma: https://admin.ctbz.com.br/#/man-responsavel

Detalhes do processo (SSO aceita um e-mail por CPF, permissão de escrita no SSO, efeito na Zendesk) na seção "Troca de responsável da empresa" de [[sincronizacao-usuario-zendesk]].

## Ocorrências

_Nenhuma ainda._
