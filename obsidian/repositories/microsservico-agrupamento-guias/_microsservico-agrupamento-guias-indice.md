---
name: microsservico-agrupamento-guias-indice
description: "Índice de notas do repositório microsservico-agrupamento-guias: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - microsservico-agrupamento-guias
repositorio: microsservico-agrupamento-guias
caminho: ~/repositories/microsservico-agrupamento-guias
---

# microsservico-agrupamento-guias

Repositório em `~/repositories/microsservico-agrupamento-guias`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[notificacao-agrupamento-experts-bp-lp|Notificação do agrupamento: Experts x BP LP]] — crons, tópicos compartilhados, roteamento por `pertenceBpLp()` e services comuns/específicos de e-mail e WhatsApp
- [[PRD-174011 - Cliente não recebe notificação do agrupamento de guias|PRC: cliente não recebe notificação do agrupamento]] — como investigar por competência (grupo_guia, controle_notificacao, controle_guias) e por que `GUIAS_AGUARDANDO_GERACAO` nunca é retentado
- [[notificacao-individual-guias-x-agrupamento|Convivência com a notificação individual do experts-service]] — `ERRO_NOVA_GUIA` sem renotificar, listas de impostos divergentes e dependência da rota `enviou-notificacao-agrupamento`
- [[telefone-do-grupo-guia|Telefone do grupo_guia]] — telefone principal da Empresa (COMERCIAL > CELULAR > primeiro) definido no plataforma-faturamento-worker e congelado em `grupo_guia.contato`
- [[metadados-whatsapp-hubspot|Metadados do WhatsApp para o HubSpot]] — chaves de grupo, guias e parcelas do `MetadadosGuiaFactory` (evento `whatsapp_ativo`), formatos e quando ficam ausentes
- [[rodar-testes-localmente|Rodar os testes localmente]] — `contabilizei-sso-client` 3.0.9 só no registry do GitLab (403 no Artifactory): baixar o .pom/.jar pelo `glab api` para o `~/.m2`; `application-local` de dev no stash do repo principal ; `-Dtest` com `@Nested` exige curinga; validar troca de template de e-mail local com envio em prod (sem deploy em dev)
- [[notifications-regression-tests|Testes de regressão das notificações]] — fluxo, crons, regras de elegibilidade, templates e catálogo de cenários (Experts SN, Experts LP, BP LP, diagnósticos) com a skill `regressao-notificacoes-agrupamento`; só o contato de teste

- [[replicar-features-no-agrupamento-guias-service|Replicar features no agrupamento-guias-service]] — **regra**: feature de notificação mergeada aqui que não exista no service vira work-item no GitLab dele; como conferir e controle do que já foi aberto

A parte de notificação foi portada para o [[_agrupamento-guias-service-indice|agrupamento-guias-service]] em 2026-10-15 (ver [[arquitetura-e-migracao|arquitetura e migração]]); até a virada, as duas implementações coexistem.

- [[historico-mrs-microsservico-agrupamento-guias|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
