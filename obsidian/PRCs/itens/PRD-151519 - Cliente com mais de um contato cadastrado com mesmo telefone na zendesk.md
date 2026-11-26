---
name: prc-zendesk-contatos-duplicados-mesmo-telefone
description: PRC — cliente com mais de um contato cadastrado com o mesmo telefone na Zendesk; causa (ticket ignorado/perdido) e como descobrir e mesclar via front admin
metadata:
  type: reference
tags:
  - prc
canal:
  - wpp
dominio:
  - atendimento
sistemas:
  - zendesk
  - atendimento-canais-admin
acr:
  - PRD-151519
ocorrencias:
  - PRC-154451
qtd_ocorrencias: 1
ultima_ocorrencia: 2026-11-05
---

# Cliente com mais de um contato cadastrado com mesmo telefone na zendesk

## Sintoma / possíveis causas

- Cliente está sendo **ignorado** no atendimento: **ticket aberto perdido**
  (o ticket fica vinculado a um contato "bifurcado" e não ao contato principal do cliente).

## Como descobrir

1. Acessar o front admin (precisa ser pelo front, pois exige permissão de admin na Zendesk):
   `https://admin.ctbz.com.br/api/atendimento-canais/sustentacao/zendesk/usuarios`
2. Pesquisar pelos últimos 8 dígitos do telefone do cliente, com `*` na frente:
   `*${ULTIMOS_8_DIGITOS_TELEFONE_CLIENTE}`
3. Verificar se aparece mais de um contato para o mesmo telefone.

## Como resolver

- **Mesclar** os contatos pelo próprio front admin.

> [!warning] Duplicado com `external_id` não mescla em prod
> A Zendesk recusa com "enquanto ele tiver uma ID externa" (o front do admin só mostra erro/422). Limpar o `external_id` do duplicado pela API e mesclar de novo: ver [[sustentacao-zendesk-merge-usuarios]].

> [!warning] Cuidado antes de mesclar
> Os contatos que bifurcam (os que serão mesclados no principal) devem ter
> **apenas telefone cadastrado** — **sem organização** e **sem e-mail**.
> Caso contrário, não podem ser mesclados.

## A correção na Zendesk pode ser desfeita

O `plataforma-back-worker` sincroniza o usuário da Zendesk achado pelo **e-mail do responsável** da empresa, gravando o nome e o telefone do responsável da plataforma. Se o responsável na plataforma mistura dados de duas pessoas, a sincronização (ex: quando alguém entra na plataforma com a empresa) renomeia de novo o contato corrigido. Antes de dar o PRC como resolvido, conferir o cadastro do responsável na plataforma e os logs (ver [[sincronizacao-usuario-zendesk]]). Caso: PRC-155281 (2026-11-24). Quando o certo é trocar o responsável (outro sócio), o processo é SSO primeiro e depois admin `man-responsavel`, e o SSO aceita um e-mail por CPF; editar no SSO exige permissão de escrita (ver a seção "Troca de responsável" de [[sincronizacao-usuario-zendesk]]). Se o PRC só pede a troca do responsável, sem problema de contato na Zendesk, é indevido (Onboarding e Retenção): ver [[Indevido - Troca do responsável da empresa (Onboarding e Retenção)]].

## Troca de e-mail: dois usuários na Zendesk (e-mail antigo e novo)

Quando o cliente troca o e-mail do responsável na plataforma e continua recebendo no antigo, a Zendesk pode ter dois usuários da mesma pessoa na mesma organização (um com o e-mail antigo, outro com o novo). Para validar se os envios do canal off já vão para o novo, consultar pela API (coleção `~/repositories/experts-bruno/zendesk-api`, só GET) os tickets de cada usuário (`/users/<id>/tickets/requested.json?sort_by=created_at&sort_order=desc`) e da organização (`search type:ticket organization:<id> created>AAAA-MM-DD`) e ver em qual requester caíram os tickets `via=api`/`email` depois da troca. Armadilhas:

- Tickets proativos (ex: `WINBACK - AJUDA`, via api) podem vir de **outra empresa** do mesmo CPF (CNPJ antigo/inativo no corpo do ticket), que ainda tem o e-mail antigo como responsável: a troca na empresa atual não corrige esses.
- E-mail de marketing (convite de live etc.) não passa pela Zendesk (HubSpot): não aparece nos tickets.
- Caso PRC-154451 (2026-11-24): usuários 1275653644 (antigo) e 362718497699 (novo) na mesma org; nenhum ticket off criado depois de 05/11, então ainda sem evidência de envio pelo novo. O merge pelo admin voltou 422 porque o duplicado tinha `external_id` (ID externa do SSO); limpando o `external_id` pela API, o merge passou (antigo mesclado no novo, hotmail virou e-mail secundário, 40 tickets migrados). Ver [[sustentacao-zendesk-merge-usuarios]].

## ACR para vincular

PRCs que caem nesse problema devem ser vinculadas à ACR:
[PRD-151519](https://contabilizeicontabilidade.atlassian.net/browse/PRD-151519)
— Desincronização de Dados de Contato: Atualização de E-mail do Responsável

## Como fechar o PRC

- Link `Problem/Incident`: `inwardIssue` = PRD-151519, `outwardIssue` = PRC (o PRC *is caused by* a ACR).
- Atribuir ao Glener, comentar (cadastro da plataforma já correto + usuários duplicados mesclados na Zendesk) e, de `To-do`, `Started` (61) → `Solved` (121) com: Classificação N3 (`customfield_18430`) Expert - Projetos `31450`; Devido `22182` (`customfield_19805`); Funcionalidade (`customfield_18681`) Atendimento - Usuários `32047`; Grau do Impacto (`customfield_19493`) `20698`; Ofensor (`customfield_21097`) `zendesk_usuario_duplicado`; Resolução (`customfield_18429`) Correção de dados da base `17918`; Tipo (`customfield_18460`) Suporte a operação `18048`. Usado no PRC-154451 (2026-11-24).
