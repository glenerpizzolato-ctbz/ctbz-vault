---
name: agrupamento-guias-service-arquitetura-e-migracao
description: "Arquitetura do agrupamento-guias-service: notificação por segmento (exp/bp × simples/lp × email/wpp) com rota + tópico + consumer pull por segmento, banco próprio só com notifications, evento autocontido; origem no microsservico-agrupamento-guias e armadilhas"
metadata:
  type: project
tags:
  - agrupamento-guias-service
  - microsservico-agrupamento-guias
  - notificacao
  - zezu
sistemas:
  - agrupamento-guias-service
  - microsservico-agrupamento-guias
  - email-service
  - atendimento-zendesk
atualizado_em: 2026-10-15
---

# agrupamento-guias-service: arquitetura

Serviço Node/Zezu (padrão do `email-service`) que notifica (e-mail e WhatsApp) o agrupamento de guias. Nasceu como cópia da parte de notificação do `microsservico-agrupamento-guias` (Kotlin) e, em 2026-10-15, foi refeito num desenho mais simples (mergeado na `main` local, ainda sem remote), a pedido do Glener.

## Desenho atual (refeito em 2026-10-15)

- **Segmento = público × regime × canal**: `exp`/`bp`, `simples`/`lp`, `email`/`wpp` → 8 segmentos. Cada um tem rota `POST /notifica/<publico>/<regime>/<canal>`, tópico `agrupamento-guias-service.p2p.notifica-<seg>` e subscription pull `agrupamento-guias-service.sub.notifica-<seg>` (terraform com `for_each`; padrão em [[pubsub-nomenclatura]]). Com `IS_LOCAL=true` os consumers usam as subs `-local`, criadas só no terraform de dev. Rota e consumer recebem o mesmo corpo e chamam o mesmo usecase.
- **Sem lote, sem scheduler**: chegam N eventos e cada um notifica separado. O evento é autocontido (id do agrupamento, idEmpresa, cnpj, competência, `path` do PDF, contato, guias, diagnóstico opcional): o serviço não lê nada de outro banco.
- **Banco próprio, uma tabela por canal**: `notifications_email` (com `recipient_email`) e `notifications_wpp` (com `recipient_phone`); colunas em inglês, `grouping_id` (id do agrupamento), `plan` (enum `PagtoPlanoCategoria` do Kotlin, nulo em Experts sem plano) e `tax_regime` (enum `RegimeTributario`: `LUCRO_PRESUMIDO`, `SIMPLES`, `MEI`), vindos do evento (`planoPagamento`, `regimeTributario`), `tax_increase_diagnosis_{id,type,payload}` só quando o diagnóstico definiu o template, sem payload cru do evento. Migrations drizzle-kit em `migrations/`. Substitui `controle_notificacao`. Status: `PENDING`, `SUCCESS`, `FAILED`, `BLOCKED_OPTOUT`, `INCOMPLETE_DATA`. Já notificado = existe `PENDING`/`SUCCESS`/`BLOCKED_OPTOUT` do agrupamento na tabela do canal.
- **Um service por público + regime + canal** (8, ex: `ExpSimplesEmailService`), cada um monta o próprio template e as variáveis; comum em `EnvioEmailService`/`EnvioWhatsappService`. Preferência do Glener: nada de helper de variáveis de template nem variáveis/"fonte" no JSON de config (tentado e descartado em 2026-10-15).
- **BP Simples** (e-mail e WhatsApp) ainda não implementado: o service de envio só loga `method dont supported or dont implemented` e não grava nada.
- **Mantidos**: callbacks do email-service e do WhatsApp ativo (agora atualizando `notifications`). **Removidos**: lote/scheduler, diagnóstico BP, consulta do diagnóstico, `enviou-notificacao-agrupamento` (usada pelo experts-service) e `POST /notificacao`.
- Nomes: "grupo_guia" virou "agrupamento" no código, rotas e tópicos; só a chave `id_grupo_guia` dos metadados do WhatsApp ficou, por ser contrato com o HubSpot/experts-service.

- **Templates de e-mail** em `src/config/email-templates/{dev,prd}.json` (padrão de JSON por ambiente dos zendeskapps, `environments/zcli.apps.config.{dev,prod}.json`), só nome + UUID, organizados por público → regime, com chaves padronizadas `templateEmail<Publico><Regime>Padrao` ou `templateEmail<Publico><Regime>Diagnostico<Motivo>` (ex: `templateEmailExpSimplesDiagnosticoAumentoFaturamento`), cada uma com `name` (documentação) + `id`; `null` = ainda não criado. No código o mapa é achatado por nome. Diagnóstico de aumento de imposto só existe no regime Simples (Experts e BP), confirmado pelo Glener em 2026-10-15: os segmentos LP ignoram o diagnóstico (e-mail e WhatsApp), e o JSON tem `templateEmail{Exp,Bp}SimplesDiagnostico<Motivo>` (os de BP ainda `null`, BP Simples não implementado). Hoje existem só ExpSimplesPadrao (`exp-email-agrupamento-guias-default-v4`), ExpSimplesDiagnosticoAumentoFaturamento (`exp-email-agrupamento-guias-diag-fatur-v1`) e BpLpPadrao (`agrupamento-guias-bp-lp-v2`); em prd os outros motivos só têm versões `-test-N`.

## Decisões que continuam

- **Identidade**: `agrupamento-guias-service` no `application` do e-mail e no `autor` do WhatsApp; as subscriptions de callback filtram por ela.
- **Worker**: `LockedPubsubWorker` (trava por messageId no Redis por 4h, sempre ack). Os 8 consumers ficam num registro só (`notificaWorkers`) com instância própria do usecase.

## Armadilhas

- Nome ↔ UUID dos templates do email-service: `psql -w service=<dev|prd>_atendimento_canais_email_service -c "select id, name from email_templates where name ilike '%agrupamento%'"`.

- `pnpm install` precisa de token do Artifact Registry (`@contabilizei-private`). Sem mexer no `~/.npmrc`: gerar um npmrc temporário com `//us-central1-npm.pkg.dev/contabilizei-tools-production/npm/:_authToken=$(gcloud auth print-access-token)` e rodar `NPM_CONFIG_USERCONFIG=<arquivo> npx -y pnpm@11.2.2 install` (variável `npm_config_//...` no env não funciona).
- Awilix em modo estrito: worker singleton não pode depender de usecase registrado como transiente (rota precisa do logger da request) — dá `AwilixResolutionError ... shorter lifetime than its ancestor`. E o `modules.spec` estoura memória (OOM) ao tentar imprimir esse erro: para ver a mensagem, envolver o `resolve` num try/catch e logar só `message`.
- Testes de DAO usam o Drizzle real sobre um client `pg` falso (`src/test-utils/fake-db.ts`, linhas em `rowMode: 'array'`), o que valida o SQL gerado.

## Pendências

- Criar repositório no GitLab, deploy, banco próprio (secret `DATABASE_URL`) e rodar `pnpm db:migrate`; `terraform apply`.
- Definir o conteúdo do BP Simples.
- O experts-service consultava `enviou-notificacao-agrupamento`, que saiu: precisa de alternativa se ainda for usada.

Relacionado: [[notificacao-agrupamento-experts-bp-lp]] (como a notificação funcionava no Kotlin).
