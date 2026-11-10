---
name: rodar-testes-localmente-microsservico-agrupamento-guias
description: "Como rodar os testes e a aplicação do microsservico-agrupamento-guias localmente quando o contabilizei-sso-client novo (3.0.9+) só existe no registry Maven do GitLab e o Artifactory devolve 403"
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

**Solução definitiva (feita em 2026-11-10):** baixar o artefato uma vez para o `~/.m2` pelo `glab` autenticado. O pacote fica no projeto `ctbz/devops/recursos/packages` (id `66189044`):

```bash
D=~/.m2/repository/br/com/contabilizei/contabilizei-sso-client/3.0.9; mkdir -p $D && cd $D
for f in contabilizei-sso-client-3.0.9.pom contabilizei-sso-client-3.0.9.jar; do
  glab api "projects/66189044/packages/maven/br/com/contabilizei/contabilizei-sso-client/3.0.9/$f" > $f
done
rm -f *.lastUpdated _remote.repositories
```

Depois disso, `./mvnw test` e `SPRING_PROFILES_ACTIVE=local ./mvnw spring-boot:run` funcionam sem `GITLAB_MAVEN_PACKAGES_URL`. Vale para qualquer lib `br.com.contabilizei` que só esteja no registry do GitLab (listar versões: `glab api "groups/ctbz/packages?package_name=<artifactId>&package_type=maven"`).

Paliativo, se não der para baixar: os testes não usam o SSO, então dá para rodar com uma versão que já está no `~/.m2`, offline: `./mvnw -o test -Dcontabilizei-sso-client.version=3.0.5`. O override é só local.

Armadilha: o repo principal pode continuar rodando normalmente enquanto a worktree falha, porque o checkout principal pode estar num master anterior ao bump (ex: `d48dada1`, com 3.0.2 em cache) e a worktree num commit posterior.

## application-local.yml para rodar contra dev

O `application-local.yml` commitado aponta para o Postgres do docker-compose (`localhost:5432`). A versão do usuário que roda contra o banco de dev (proxy `sql_atendimento_dev`, `localhost:5433/ms_agrupamento_guias`) e consome as subscriptions reais de `atendimento-canais-dev` fica num **stash do repo principal** (`stash@{0}` de 2026-10-30, "WIP on master: 25bae7bd"; o stash é compartilhado com as worktrees). Para levar a uma worktree sem aplicar o stash: `git show <sha-do-stash>:src/main/resources/application-local.yml > src/main/resources/application-local.yml`. Esse stash é anterior ao !97: acrescentar `processarParcela` (`subscription: ms-agrupamento-guias.sub.processar-parcela`, `project: atendimento-canais-dev`). Consumir as subs reais de dev compete com o pod de dev pelas mensagens. O arquivo tem credenciais: nunca commitar.

## PubSubInitConfig contra o Pub/Sub real de dev (a partir do !97)

O `PubSubInitConfig` (`@Profile("local")`) cria no `project-id` global os tópicos e subscriptions que não encontrar. No master ele só garante `processarGuiaImposto`, `agruparGuiasEmpresa` e `agruparGuiasEmpresaRetry` (que existem em `atendimento-canais-dev`). O !97 (PRD-167515) ampliou para 9 pares (parcela, notificações, callbacks) mais os tópicos de `enviarAnexoEmail`, `enviarEmail` e `enviarAtivoWhatsapp`, pensando no emulador: os callbacks só têm `topic` no `application-local.yml` do !97. Rodando com o yml de dev (sem `emulator-host`), sobe com `NullPointerException` em `PubSubInitConfig.<init>` (`enviarEmailCallback.topic` nulo); e, preenchendo os tópicos, ele criaria cópias soltas em `atendimento-canais-dev` de tópicos que moram em outros projetos (`processar-parcela` em `contabilizei-impostos-teste`; `atendimento-zendesk.envio-whatsapp-ativo` e `atendimento-zendesk.whatsapp-ativo-status` em `contabilizei-crm-dev`). Correção local (não commitada): `@ConditionalOnProperty("spring.cloud.gcp.pubsub.emulator-host")` na classe, para o init só rodar com emulador. Todas as subscriptions `ms-agrupamento-guias.sub.*` já existem em dev.

## Receber de verdade o e-mail do agrupamento (local, envio em prod)

Em dev o e-mail nunca chega: o email-service de dev responde no callback `FAILED` / `REJECTED` com `421 The from domain should be a connected email sending domain ... - hssmtp` (o SMTP/HubSpot de dev não tem o domínio do remetente conectado), e o `controle_notificacao` vira `FALHA / ERRO_CALLBACK_ENVIO_EMAIL`. Para receber, rodar local com o banco de dev e apontar **só o envio** para prod no `application-local.yml`:

- `enviarAnexoEmail.project` e `enviarEmail.project` = `atendimento-canais-prd` (os **dois**: o anexo sobe no email-service e o envio referencia o id dele; anexo em dev + envio em prod não fecha). A ADC do usuário tem `pubsub.topics.publish` nesses tópicos de prod.
- Template de prod no `templateAgrupamento*Uuid` do público (Experts SN `123ccd0f-9b37-4912-98c7-277a1473f1a2`).
- `notificacaoGrupoGuiaEmail` numa fila só do app local (`ms-agrupamento-guias.p2p.notifies-email-local` / `ms-agrupamento-guias.sub.notifies-email-local`, criados em `atendimento-canais-dev` em 2026-11-10): a fila normal `notifies-email` é consumida também pelo pod de dev, que pode pegar a mensagem e mandar pelo SMTP de dev.
- O callback de prod volta no tópico de prod, que o app local não consome: o controle fica sem o status final.
- A rota de lote ignora grupos que já têm qualquer `controle_notificacao` do tipo: apagar o registro anterior do grupo de teste antes de disparar de novo.
