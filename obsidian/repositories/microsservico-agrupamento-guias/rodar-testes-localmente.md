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
atualizado_em: 2026-11-12
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
- Template de prod no `templateAgrupamento*Uuid` do público (Experts SN `25d1382f-2afc-42de-8b55-088ee67841a9`, `default-v5`).
- `notificacaoGrupoGuiaEmail` numa fila só do app local (`ms-agrupamento-guias.p2p.notifies-email-local` / `ms-agrupamento-guias.sub.notifies-email-local`, criados em `atendimento-canais-dev` em 2026-11-10): a fila normal `notifies-email` é consumida também pelo pod de dev, que pode pegar a mensagem e mandar pelo SMTP de dev.
- O callback de prod volta no tópico de prod, que o app local não consome: o controle fica sem o status final.
- A rota de lote ignora grupos que já têm qualquer `controle_notificacao` do tipo: apagar o registro anterior do grupo de teste antes de disparar de novo.

## Validar troca de template de e-mail (local)

Usado na PRD-177099 (2026-11-12). Quando o MR só troca `template*Uuid` nos `application-{dev,prod}.yml`, o caminho mais barato e mais fiel é local com envio em prod (seção acima), sem trocar o pod de dev compartilhado:

1. `application-local.yml` a partir do stash (`git show stash@{0}:src/main/resources/application-local.yml > src/main/resources/application-local.yml`, stash "WIP on master: 25bae7bd"; ele tem as credenciais de dev embutidas, então não precisa de `SSO_APP_SECRET`/`HEIMDALL_*` no ambiente). O arquivo é **rastreado no git** (a versão commitada é a do emulador): restaurar com `git checkout --` no fim.
2. Acrescentar `processarParcela`; pôr `notificacaoGrupoGuiaEmail` em `ms-agrupamento-guias.p2p.notifies-email-local` / `ms-agrupamento-guias.sub.notifies-email-local`; `enviarAnexoEmail.project` e `enviarEmail.project` = `atendimento-canais-prd`; e os `template*Uuid` com os UUIDs **de prod** do MR (o email-service de prod não conhece os de dev).
3. `PubSubInitConfig` com `@ConditionalOnProperty("spring.cloud.gcp.pubsub.emulator-host")` (só local).
4. Subir com `SPRING_PROFILES_ACTIVE=local SERVER_PORT=<PORT da worktree> ./mvnw spring-boot:run` (o `application.yml` fixa `server.port: 8080`; precisa do Redis em `localhost:6379`). Não há auth na app: as rotas de lote são `GET localhost:<porta>/notificacao/envia-lote/grupo-guia/{exp-sn,exp-lp,bp-lp}/EMAIL` (o `/agrupamento-guias` é prefixo do api-gateway).
5. Massa da skill de regressão, `checar`, e deixar em `PROCESSANDO` todo grupo de teste que não deve receber (inclusive o grupo 3 de dev), para mandar só um e-mail por público.
6. Conferir: log local `construção do DTO… templateId=…`, `email_replications` de prod (`template_id`, `to`, `status`, só leitura) e a caixa de entrada. O `controle_notificacao` fica sem status final (o callback volta no tópico de prod).

Para parar o app, matar pelo PID (`ss -ltnp | grep :<porta>`): um `pkill -f "spring-boot:run"` rodado pelo shell do agente casa com a própria linha de comando e derruba o shell junto.

Permissão: `pubsub.topics.publish` nos tópicos do email-service de prod dá para conferir sem publicar, com `POST https://pubsub.googleapis.com/v1/projects/atendimento-canais-prd/topics/<topico>:testIamPermissions` e o body `{"permissions":["pubsub.topics.publish"]}` (token do `gcloud auth print-access-token`).

## Rodar uma classe de teste só

Com classe que tem `@Nested`, `./mvnw test -Dtest=MetadadosGuiaFactoryTest` pode não rodar a classe e deixar em `target/surefire-reports` o relatório de uma execução antiga (visto em 2026-11-11: o arquivo tinha horário da véspera). Usar um padrão com curinga e conferir o horário do relatório: `./mvnw test -Dtest='MetadadosGuiaFactoryTest*' -Dsurefire.failIfNoSpecifiedTests=false`.
