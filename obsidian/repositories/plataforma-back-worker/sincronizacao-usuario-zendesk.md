---
name: sincronizacao-usuario-zendesk
description: "O plataforma-back-worker (módulo contabilizei-back-worker no App Engine) sobrescreve o usuário da Zendesk achado pelo e-mail do responsável da empresa: nome, telefone e WhatsApp vêm da plataforma; desfaz correções manuais de contatos; como achar nos logs"
metadata:
  type: reference
tags:
  - plataforma-back-worker
  - zendesk
---

# Sincronização do usuário da Zendesk pelo responsável da empresa

`CriarOuAtualizarUsuarioFacade` (`src/main/java/br/com/contabilizei/worker/zendesk/facade/`), disparada por `IdentificarDuplicidadeDeAtualizacoesFacade`, roda no módulo `contabilizei-back-worker` do App Engine (projeto `contabilizeiapp`):

1. Acha a organização da empresa na Zendesk.
2. Acha o usuário por `ZendeskService.obterUsuario`: `search.json?query=type:user email:<e-mail do responsável da empresa>` e pega o primeiro resultado.
3. Faz `PUT` nesse usuário com o payload da plataforma: `name` (nome do responsável), `email`, `phone`, `whatsapp`, `organization_id` e `user_fields.mensalidades_atraso`. Sem usuário, cria um.

**Armadilha:** o usuário é achado pelo **e-mail**, mas o nome e o telefone vêm do **responsável na plataforma**. Se o cadastro do responsável mistura dados de duas pessoas (ex: nome de um sócio e e-mail genérico da empresa), qualquer correção manual na Zendesk é desfeita na próxima sincronização: o usuário que ficou com aquele e-mail é renomeado com o nome do responsável. A sincronização é disparada, por exemplo, quando alguém entra na plataforma com a empresa (inclusive um admin interno acessando como a empresa). A correção definitiva é no cadastro do responsável na plataforma, não só na Zendesk.

## Como achar nos logs (sem a API de prd da Zendesk)

```
gcloud logging read '"<CNPJ>" AND ("Iniciando atualização do usuário Zendesk" OR "Usuário Zendesk atualizado")' --project contabilizeiapp --freshness=3d --format='value(timestamp,textPayload)'
```

O "Iniciando atualização" traz o JSON enviado (nome, e-mail, telefone); o "atualizado com sucesso" traz o id do usuário da Zendesk. Na mesma janela, `Usuario Logado - Email: ... CNPJ: ...` no mesmo projeto mostra quem estava logado. As edições feitas pelo front admin de sustentação ficam no log `zendesk-sustentacao-audit` do `atendimento-canais-admin-prd` (projeto `atendimento-canais-prd`, `jsonPayload.acao`, `operador`, `alteracoes`).

## Quem alterou o cadastro da empresa na plataforma

O monolito (`default` do App Engine, projeto `contabilizeiapp`) grava um `CHANGETRACE` a cada alteração de entidade, com o operador e o antes/depois de cada campo. Nos logs não aparece nenhuma escrita da Zendesk na empresa (a sincronização conhecida vai da plataforma para a Zendesk): se um campo mudou na plataforma, procurar o autor aqui.

```
gcloud logging read '"CHANGETRACE" AND "<id da empresa>"' --project contabilizeiapp --freshness=30d --format='value(timestamp,textPayload)'
```

Mais rápido: buscar pelo valor antigo do campo (ex: `"<e-mail antigo>"`), que traz o CHANGETRACE, as buscas do admin e as publicações em `EMPRESA_ALTERADA`/`UPDATE_EMPRESA`.

Caso real: PRC-155281 (2026-11-24), KLASS PLATAFORMA DE APOIO A EDUCACAO (CNPJ 69686282000129): a identidade `contato@klass.app.br` foi movida para o usuário do CESAR às 15:34 e, às 15:49, a sincronização renomeou esse usuário para GUSTAVO MATTOS REMIAO (o responsável na plataforma tem esse nome com o e-mail `contato@klass.app.br`). O e-mail do responsável foi trocado de `rmg.joal@proton.me` para `contato@klass.app.br` pelo admin em 19/11/2026 08:03 (BRT) por jackson.jesus@contabilizei.com.br (CHANGETRACE), cinco dias antes dos ajustes na Zendesk.

## Troca de responsável da empresa (SSO + admin)

Processo oficial (apresentação "Verificações no SSO"): primeiro no SSO (https://sso.contabilizei.com/sistema-admin/#/, abas Usuários e Empresas, IP liberado em https://libera-meu-ip.ctbz.com.br/ com "SSO" e "contabilizei-sso"), depois no admin em `#/man-responsavel`. O SSO aceita um e-mail por CPF: para dar a um responsável novo o e-mail de outro usuário, antes é preciso trocar o e-mail do usuário antigo. A edição do e-mail do responsável no admin (`edit-empresa`) também altera o e-mail do usuário no SSO (no PRC-155281, o usuário do SSO foi atualizado no mesmo minuto do CHANGETRACE). Editar usuário no SSO exige permissão de escrita: sem ela, o confirmar volta "Operação não autorizada" e nada é gravado (visto em 2026-11-24 com o login do Glener).

PRC que só pede a troca do responsável (sem problema de contato na Zendesk) é de Onboarding e Retenção: devolver como indevido, com a orientação acima no comentário (ver [[Indevido - Troca do responsável da empresa (Onboarding e Retenção)]]).
