---
name: rodar-testes-localmente-microsservico-agrupamento-guias
description: "Como rodar os testes do microsservico-agrupamento-guias localmente quando o contabilizei-sso-client novo (3.0.9+) só existe no registry Maven do GitLab e o Artifactory devolve 403"
metadata:
  type: reference
tags:
  - microsservico-agrupamento-guias
  - maven
  - testes
repositorio: microsservico-agrupamento-guias
atualizado_em: 2026-11-10
---

# Rodar os testes localmente

A partir do `contabilizei-sso-client` 3.0.9 (commit `8bd37199`), o artefato só está no registry Maven do GitLab, que o `pom.xml` lê de `${env.GITLAB_MAVEN_PACKAGES_URL}`. Sem essa variável, o `./mvnw` cai no Artifactory (`ctbz-central`) e falha com `Could not transfer artifact br.com.contabilizei:contabilizei-sso-client:pom:3.0.9 ... 403 Forbidden`.

Os testes não usam o SSO, então dá para rodá-los com uma versão que já está no `~/.m2` (ex: 3.0.5), offline:

```bash
./mvnw -o test -Dcontabilizei-sso-client.version=3.0.5
```

Para rodar uma classe só, `-Dtest=NomeDaClasseTest`. O override é só local: o `pom.xml` continua com a versão nova e a pipeline usa o registry do GitLab.

## application-local.yml para rodar contra dev

O `application-local.yml` commitado aponta para o Postgres do docker-compose (`localhost:5432`). A versão do usuário que roda contra o banco de dev (proxy `sql_atendimento_dev`, `localhost:5433/ms_agrupamento_guias`) e consome as subscriptions reais de `atendimento-canais-dev` fica num **stash do repo principal** (`stash@{0}` de 2026-10-30, "WIP on master: 25bae7bd"; o stash é compartilhado com as worktrees). Para levar a uma worktree sem aplicar o stash: `git show <sha-do-stash>:src/main/resources/application-local.yml > src/main/resources/application-local.yml`. Esse stash é anterior ao !97: acrescentar `processarParcela` (`subscription: ms-agrupamento-guias.sub.processar-parcela`, `project: atendimento-canais-dev`). Consumir as subs reais de dev compete com o pod de dev pelas mensagens. O arquivo tem credenciais: nunca commitar.
