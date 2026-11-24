---
name: prc-indevido-troca-responsavel-empresa
description: PRC — pedido para trocar o responsável (sócio) da empresa ou os dados dele chega a nós, mas é de Onboarding e Retenção; fechar como indevido (squad errada) com a orientação padrão - a própria operação faz pelo SSO e depois admin man-responsavel, e a Zendesk só é atualizada depois que a plataforma estiver correta
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
acr:
  - PRD-77741
ocorrencias:
  - PRC-155281
qtd_ocorrencias: 1
ultima_ocorrencia: 2026-11-16
---

# Troca do responsável da empresa - indevido (Onboarding e Retenção)

## Sintoma

O PRC pede para trocar o responsável da empresa (ex: outro sócio passa a ser o responsável) ou alterar as informações dele (nome, e-mail, CPF, telefone). Esse pedido **não é da Engenharia Canais**: teoricamente é do time de **Onboarding e Retenção**, e a orientação que eles dão é a mesma do processo oficial, que o próprio atendimento consegue executar pelos nossos sistemas.

Não confundir com o caso em que o contato da Zendesk está errado por causa do cadastro do responsável (ver [[PRD-151519 - Cliente com mais de um contato cadastrado com mesmo telefone na zendesk]] e [[sincronizacao-usuario-zendesk]]): aí o problema chega como contato/ticket errado na Zendesk e é nosso.

## Como resolver

Devolver como **indevido**, sem fazer a troca:

1. Comentar no PRC com o texto padrão abaixo.
2. Vincular à ACR de indevidos do time, **PRD-77741** ("[Atendimento] [Expert] PRC's indevidos.", tipo Rotina, já arquivada, mas é a que o time usa: mais de 450 PRCs vinculados), link `Problem/Incident` com o PRC *is caused by* PRD-77741 (`createJiraIssueLink` com `inwardIssue: PRD-77741`, `outwardIssue: <PRC>`). Existe também a PRD-163003 ("Orientações de Processos que Podem Ser Realizados em Nossos Sistemas"), mas é do squad Onboarding e Retenção.
3. Atribuir ao Glener (`assignee` = `{"accountId": "712020:71b4f148-e139-4098-b2b0-0fe4e7a37cf1"}` no `editJiraIssue`).
4. Fechar com `Solved` (saindo de `To-do`, passar antes por `Started`, 61; depois `Solved`, 121), com:
   - Devido ou Indevido? (`customfield_19805`): **Indevido** (`22183`)
   - Resolução do chamado (`customfield_18429`): **Envio de orientações (indevido)** (`17921`)
   - Tipo de chamado (`customfield_18460`): Suporte a operação (`18048`)
   - Classificação do chamado (N3) (`customfield_18430`): Experts - CRM → Indevido (`39474` / `39475`)
   - Funcionalidade (`customfield_18681`): Atendimento - WhatsApp (`28568`) ou Atendimento - E-mail (`28569`), conforme o canal
   - Grau do Impacto (`customfield_19493`): Alto - Impactou Operação (`20700`)
   - Ofensor do Chamado (`customfield_21097`, labels): `crm_chamado_indevido_canais`
   - Os 7 campos vão direto no `transitionJiraIssue` do `Solved` (121); de `Em Andamento` ele sai sem passar por outra transição.

### Comentário padrão

> Olá! Vamos fechar este chamado como **indevido**, pois a squad está errada: a troca/alteração do responsável da empresa é do time de **Onboarding e Retenção**, e não da Engenharia Canais.
>
> A própria operação consegue fazer essa alteração pelos nossos sistemas, que é a mesma orientação que o time de Onboarding e Retenção costuma dar:
>
> 1. Primeiro no SSO: https://docs.google.com/presentation/d/1ICG8L4P4IQVNChxLFO5Q7kQRTUWW5e2f4emirJRkoDo/edit?usp=sharing
> 2. Depois no Responsável na plataforma: https://admin.ctbz.com.br/#/man-responsavel
>
> A Zendesk só deve ser atualizada depois que o cadastro na plataforma estiver correto: o contato da Zendesk é sincronizado a partir do responsável da plataforma, então uma correção feita só na Zendesk é sobrescrita na próxima sincronização.

Por que a Zendesk vem por último: o `plataforma-back-worker` regrava o nome e o telefone do usuário da Zendesk com os dados do responsável da plataforma, achando o usuário pelo e-mail do responsável (ver [[sincronizacao-usuario-zendesk]]). Detalhes do processo (SSO aceita um e-mail por CPF, permissão de escrita no SSO, efeito na Zendesk) na seção "Troca de responsável da empresa" de [[sincronizacao-usuario-zendesk]].

## Ocorrências

- PRC-155281 (KLASS PLATAFORMA DE APOIO A EDUCACAO LTDA, aberto em 2026-11-16, fechado em 2026-11-24): sócio pedia para direcionar os contatos ao outro sócio. Investigamos e ajustamos a Zendesk antes de perceber que era troca de responsável (ver [[sincronizacao-usuario-zendesk]]); o comentário da investigação foi trocado pelo texto padrão e o PRC fechou como indevido na PRD-77741.
