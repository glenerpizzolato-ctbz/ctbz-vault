---
name: deploy-dev-e-prd
description: "Como subir o atendimento-zendesk em dev (via branch develop, pipeline manual com DEPLOY=true) e em prd; a doc oficial fica no README do repo"
metadata:
  type: reference
tags:
  - atendimento-zendesk
  - deploy
---

# Deploy do atendimento-zendesk em dev e prd

A doc oficial fica no `README.md` do repositório, seção "Fluxo de branches e deploy (GitLab)" (subseções "Subir em dev", "Subir em produção" e "Subir só alguns serviços"). O `.context/workflows/development-workflows.md` ainda fala de Bitbucket e está desatualizado.

## Dev

- Existe **um único ambiente de dev** para os 15 serviços (web e 14 workers), e ele sobe **só da branch `develop`**. Subir de outra branch sobrescreve o que outra pessoa está testando.
- A `develop` nunca vai para a `master`: o MR para a `master` é sempre da sua branch.
- Passo a passo:
  1. Mergear a sua branch na `develop`: `git switch develop && git pull && git merge <sua-branch> && git push`.
  2. Push na `develop` não dispara pipeline. Em **Build → Pipelines → Run pipeline**, escolher a `develop` com a variável `DEPLOY` = `true`.
  3. Rodar os jobs manuais nesta ordem: `service-account-dev`, `migrations-run-dev` e `helm-deploy-gke-dev`.
- Para subir só alguns serviços, clicar no **nome** do job `helm-deploy-gke-dev` (o ▶ do desenho roda sem variável e sobe os 15) e preencher `GKE_SERVICES_ONLY` com nomes do ambiente, ex: `atendimento-zendesk-dev` (o web, que serve as rotas de bots). Nome com sufixo `-prd` no job de dev falha antes de mexer em qualquer serviço.

## Prd

Na pipeline da `master` gerada pelo merge, rodar `service-account-prd`, `migrations-run-prd` (se der `invalid_grant: Invalid JWT Signature`, esperar 1 minuto e dar retry) e `helm-deploy-gke-prd`. Nunca rodar `migrations-rollback-*`.

Para conferir depois onde o deploy foi parar e a saúde do serviço, ver [[deploy-saude-pos-deploy]].

## Armadilha: rebase da feature pela develop

Para testar em dev, a feature é mergeada **na** `develop`, nunca rebaseada **sobre** ela. Rebasear a feature pela `develop` traz para o MR os mais de 130 commits da `develop` (aconteceu no !176, PRD-174256, em 2026-11-04). Para desfazer numa worktree, onde a `master` está em uso no checkout principal e o `git switch master` falha, não é preciso trocar de branch: `git rebase --onto origin/master <último commit da develop> <branch>` replanta só os commits da feature. Depois, `git push --force-with-lease=<branch>:<sha antigo>`.
