---
name: por-repositorio
description: "Visão reversa do catálogo GCP: para cada repositório em ~/repositories, os tópicos, subscriptions, schedulers, filas e serviços que ele cita"
metadata:
  type: reference
tags:
  - infra
  - repositorios
atualizado_em: 2026-10-09
---

# Recursos GCP por repositório

Fotografia de 2026-10-09. Para cada repositório local em `~/repositories`, os nomes de recursos GCP que aparecem no código (busca por token exato). Citar não diz se o repo publica ou consome: abrir o código para confirmar. Repositórios de configuração (citam quase tudo) ficam no fim, só com a contagem.

## aida-back

- **Tópico**: `aida-ticket-tema`, `atendimento-zendesk-atualizar-ticket`, `atendimento-zendesk-enviar-mensagem-sunshine`, `dl-zendesk-webhooks-tickets`, `test-topic`
- **Subscription**: `dl-zendesk-webhooks-tickets`
- **Fila Cloud Tasks**: `aida-analise-mensagem-travada`, `aida-analise-transferencia`, `aida-autopilot`, `aida-autopilot-new-message`, `aida-classifier`, `aida-controle-ticket`, `aida-despedida`, `aida-encerramento`, `aida-extratos`, `aida-funcoes-agendadas`, `aida-jobs-default`, `aida-message-separator`, `aida-nf-emissao`, `aida-nf-emissao-callback`, `aida-processamento-msg`, `aida-queue`, `aida-router-fila`, `aida-score`, `aida-simulador`, `aida-tag`, `aida-temperature`, `aida-transference`, `aida-update-ticket`, `aida-ura-inteligente`, `certificado-digital`
- **Cloud Run / function**: `arquivos-fator-r`, `experts-nfs`, `find_situacao_voucher`

## aida-classifier

- **Tópico**: `aida-classifier-classification-event`
- **Fila Cloud Tasks**: `aida-classifier`

## atendimento-api-gateway

- **Tópico**: `atendimento-zendesk-atualizar-ticket`, `zendesk-webhooks-capacidade-agentes`, `zendesk-webhooks-conversations`, `zendesk-webhooks-events-tickets`, `zendesk-webhooks-messages`, `zendesk-webhooks-notifications`, `zendesk-webhooks-pesquisa-satisfacao`, `zendesk-webhooks-retorno-desconexao-sem-interacao`, `zendesk-webhooks-tickets`
- **Subscription**: `zendesk-webhooks-tickets`
- **Fila Cloud Tasks**: `emissor-whatsapp`
- **Cloud Run / function**: `atendimento-front`, `contabilizei-crm-webhooks`, `emissor-whatsapp`, `historico-atendimento`

## atendimento-canais-admin

- **Fila Cloud Tasks**: `certificado-digital`, `notas-recorrentes`
- **Cloud Run / function**: `atendimento-canais-admin-dev`, `bots-api`, `experts-nfs`, `monitoria-ia-web`

## atendimento-zendesk

- **Tópico**: `atendimento-zendesk-agregador-conversa`, `atendimento-zendesk-atualizar-registro-ticket-formalizacao-sem-interacao`, `atendimento-zendesk-atualizar-ticket`, `atendimento-zendesk-chat-carregamento-dados-integracoes`, `atendimento-zendesk-classificacao-automatica-fechamento-tickets`, `atendimento-zendesk-criar-ticket`, `atendimento-zendesk-desconexao-atualizar-ticket-na-zendesk`, `atendimento-zendesk-desconexao-cliente-deseja-continuar`, `atendimento-zendesk-desconexao-cliente-nao-deseja-continuar`, `atendimento-zendesk-desconexao-criar-novo-ticket-atendimento`, `atendimento-zendesk-desconexao-envio-de-mensagem-na-conversa`, `atendimento-zendesk-desconexao-manual`, `atendimento-zendesk-desconexao-mensagem-cliente-desconectado`, `atendimento-zendesk-desconexao-reconectar-atendimento-no-mesmo-ticket`, `atendimento-zendesk-encerramento-atualizar-ticket-na-zendesk`, `atendimento-zendesk-encerramento-automatico-executar-ia`, `atendimento-zendesk-encerramento-enviar-para-em-espera`, `atendimento-zendesk-enviar-arquivo-ticket`, `atendimento-zendesk-enviar-mensagem-com-documento`, `atendimento-zendesk-enviar-mensagem-sunshine`, `atendimento-zendesk-full-conversation`, `atendimento-zendesk-notificar-cliente-desconexao`, `atendimento-zendesk-rotina-mensagem-cliente-em-fila`, `atendimento-zendesk-rotina-sincronizacao-agentes`, `atendimento-zendesk-rotina-sincronizacao-grupos`, `atendimento-zendesk-ticket-criado-atualizado-banco-de-dados`, `atendimento-zendesk-whatsapp-ativo-comentario-privado`, `atendimento-zendesk-whatsapp-carregamento-dados-integracoes`, `atendimento-zendesk-whatsapp-experts-carregar-integracoes`, `atendimento-zendesk.envio-whatsapp-ativo`, `atendimento-zendesk.erros.atualizar-ticket`, `atendimento-zendesk.experts.update-assessor-empresa-callback`, `atendimento-zendesk.experts.zendesk-job-pooler`, `atendimento-zendesk.p2p.att-ticket-status`, `atendimento-zendesk.whatsapp-ativo-status`, `bq-contabilizei-data-tb-tickets`, `classificacao-atendimento`, `dashboard-metricas-agentes-sync`, `dashboard-metricas-email-backfill`, `emissor-callback`, `experts.empresa`, `ingestor-streaming`, `jira-inativacao-empresa`, `jira-inativacao-empresa-consultas`, `nfs.non-elegible`, `notificacao-autenticacao-empresa-2fa`, `notificacao-empresa-2fa`, `pesquisa-nps-whatsapp`, `topic-name`, `zendesk-webhooks-capacidade-agentes`, `zendesk-webhooks-conversations`, `zendesk-webhooks-messages`, `zendesk-webhooks-notifications`, `zendesk-webhooks-pesquisa-satisfacao`, `zendesk-webhooks-retorno-desconexao-sem-interacao`, `zendesk-webhooks-users`, `zendeskapps-events-frontends`
- **Subscription**: `atendimento-zendesk.sub.att-ticket-status`
- **Fila Cloud Tasks**: `certificado-digital`, `emissor-whatsapp`, `emissor-whatsapp-massivo`, `feedback-hub`, `pesquisa-nps-whatsapp`
- **Cloud Run / function**: `bots-api`, `emissor-whatsapp`, `emissor-whatsapp-massivo`, `experts-nfs`

## bots-api

- **Tópico**: `atendimento-zendesk-atualizar-ticket`, `atendimento-zendesk-criar-ticket`, `atendimento-zendesk-enviar-mensagem-sunshine`, `atendimento-zendesk-whatsapp-experts-carregar-integracoes`, `atendimento-zendesk.erros.atualizar-ticket`, `bots-api.p2p.nota-fiscal.warmup`, `topic-name`, `zendesk-webhooks-conversations`, `zendesk-webhooks-messages`, `zendesk-webhooks-tickets`
- **Subscription**: `bots-api.encerramento.initialize`, `bots-api.encerramento.on-message`, `bots-api.encerramento.on-ticket-closed`, `bots-api.encerramento.on-ticket-open`, `bots-api.encerramento.on-update-ticket-error`, `bots-api.re-route.ticket`, `bots-api.sub.nota-fiscal.warmup`, `bots-api.sub.ultimate-ai.warmup`, `subscription-name`, `zendesk-webhooks-tickets`
- **Cloud Run / function**: `bots-api`, `experts-nfs`

## canais-adk

- **Tópico**: `atendimento-zendesk-atualizar-ticket`, `contabilizei-agents.bcast.metrics`
- **Fila Cloud Tasks**: `emissor-whatsapp`
- **Cloud Run / function**: `bots-api`, `canais-adk-dev`, `contabilizei-agents`, `emissor-whatsapp`, `experts-nfs`

## cnpj-alfanumerico

- **Fila Cloud Tasks**: `emissor-whatsapp`
- **Cloud Run / function**: `contabilizei-agents`, `emissor-whatsapp`, `experts-nfs`

## contabilizei-abertura

- **Tópico**: `ingestor-streaming`, `topic-name`
- **Fila Cloud Tasks**: `carregarDados-queue`, `certificado-digital`, `zendesk-queue`

## contabilizei-abertura-BB

- **Tópico**: `ingestor-streaming`, `topic-name`
- **Fila Cloud Tasks**: `carregarDados-queue`, `certificado-digital`, `zendesk-queue`

## contabilizei-agents

- **Tópico**: `atendimento-zendesk-atualizar-ticket`, `contabilizei-agents.bcast.metrics`, `contabilizei-agents.p2p.triagem_result`
- **Fila Cloud Tasks**: `emissor-whatsapp`
- **Cloud Run / function**: `bots-api`, `contabilizei-agents`, `emissor-whatsapp`

## contabilizei-back-core

- **Tópico**: `alteracao-empresa`, `audit-inss`, `audit-simples-ecac`, `comercio-20-topic-empresas-inativas`, `comercio-notify-evento-cancelamento`, `consulta-situacao-fiscal`, `consulta-situacao-fiscal-retorno`, `darf-entrada`, `darf-saida`, `dataflow-streaming-eventos-solicitacao-contas`, `empresa-alterada`, `empresa-ativada`, `eventos-solicitacao-contas-crm`, `gerar-das`, `gps-solicita-recalculo`, `mes-contabil-listener`, `notificar-alteracao-inss-darf`, `plataforma.bcast.empresa-alteracao-plano`, `processar-guia-imposto`, `simular-transmissao-pgdas`, `update-empresa`, `update-guia`, `update-guia-batch`, `update-integracao-conta-bancaria`, `verificador-pendencias-divida-ativa`, `verificador-pendencias-divida-ativa-dev`, `verificar-pagamento-darf`, `vinculo-certificado`
- **Subscription**: `dados.darf-saida`
- **Fila Cloud Tasks**: `aceite-portabilidade-queue`, `acesso-simples-queue`, `agendamento-importacao-notas-queue`, `agendamento-queue`, `alterar-regime-empresa`, `ativacao-contabil-histocio`, `ativacao-empresa`, `ativar-empresa-mei`, `atualizar-campos-jira-processo-migracao-queue`, `atualizar-contratos-empresa-queue`, `audit-queue`, `auditoria-das-queue`, `backup-queue`, `bank-integration-first-of-month-run`, `bigquery-exporter-queue`, `cadastro-automatico-queue`, `calcular-grupo-nota-tomada-queue`, `call-back-obrigacao`, `carregar-notificar-faturamento-zero`, `carregarDados-queue`, `certificado-digital`, `cnae-queue`, `cnd-queue`, `cobranca-avulsa-jira`, `conclusao-importacao-comercio-queue`, `conclusao-importacao-queue`, `correcao-movimentacao`, `criar-obrigacao`, `darf-pagamento`, `das-pagamento`, `das-queue`, `dte-queue`, `email-boas-vindas-csa`, `email-follow-certificado`, `emissao-nota-fiscal-contabilizei`, `empresa-queue`, `enviar-email-finalizacao-abertura-queue`, `escrituracao-processamento-evento`, `escrituracao-queue`, `execucao-importacao-comercio-queue`, `execucao-importacao-queue`, `fast-obrigacao-queue`, `faturamento-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `fintech-criacao-contas`, `fintech-processos-consultas`, `firebase-callback-queue`, `fiscal-queue`, `folha-queue`, `gerar-arquivo-obrigacao`, `gerar-pdf-aceite-queue`, `gps-pagamento`, `importacao-automatica-nfse-queue`, `importacao-comercio-queue`, `importacao-ofx`, `importacao-queue`, `imposto-comercio-queue`, `iss-queue`, `jira-queue`, `limpar-mes-contabil`, `lucro-presumido-queue`, `mes-contabil-queue`, `modulo-impostos-queue`, `nfe-entrada-queue`, `notificacao-queue`, `notificacao-worker-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacao-recibo-impostos-queue`, `obrigacoes-core-fast-queue`, `obrigacoes-core-queue`, `optimize-queue`, `pagamentos-service-queue`, `particionamento-notas-queue`, `pendencia-exclusao-simples-nacional-queue`, `processa-lancamento-contabil-bk-queue`, `processamento-impostos-queue`, `processar-recibo-obrigacao`, `processar-transmissao-queue`, `qc-queue`, `qc-queue-slow`, `recibo-queue`, `regime-tributario-queue`, `relatorio-contabil-queue`, `salvar-novo-onboarding-queue`, `sedex-queue`, `sincronizar-contabil-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `verificador-pendencias-queue`, `zendesk-queue`

## contabilizei-crm-webhooks

- **Tópico**: `atendimento-zendesk-atualizar-ticket`, `test-topic`, `twilio-webhooks-messages`, `twilio-webhooks-messages-local`, `twilio-webhooks-tasks`, `twilio-webhooks-tasks-local`, `zendesk-webhooks-agents`, `zendesk-webhooks-capacidade-agentes`, `zendesk-webhooks-comments`, `zendesk-webhooks-conversations`, `zendesk-webhooks-events-tickets`, `zendesk-webhooks-notifications`, `zendesk-webhooks-pesquisa-satisfacao`, `zendesk-webhooks-retorno-desconexao-sem-interacao`, `zendesk-webhooks-tickets`, `zendesk-webhooks-tickets-new`, `zendesk-webhooks-users`
- **Subscription**: `zendesk-webhooks-tickets`
- **Cloud Run / function**: `contabilizei-crm-webhooks`

## contabilizei-crm-widget-window

- **Fila Cloud Tasks**: `certificado-digital`

## contabilizei-front

- **Fila Cloud Tasks**: `certificado-digital`, `fechamento-exercicio`

## contabilizei-front-admin

- **Fila Cloud Tasks**: `fechamento-exercicio`

## contabilizei-front-vue

- **Fila Cloud Tasks**: `certificado-digital`

## contabilizei-guias

- **Tópico**: `audit-inss`, `audit-simples-ecac`, `buscar-baixa-das`, `buscar-baixa-das-anterior`, `callback-plataforma-confirmar-mes`, `callback-plataforma-confirmar-mes-dev`, `callback-plataforma-confirmar-mes-homol`, `callback.plataforma`, `cobranca.recalculo.guia`, `confirmar-mes-lucro-presumido`, `darf-entrada`, `emitir-parcela`, `emitir-parcela-pgfn`, `finalizar-importacao-lucro-presumido`, `gerar-darf-inss-avulsa`, `gerar-das-avulsa`, `gerar-guia-darf`, `gerar-guia-das`, `gerar-iss`, `gerar-tfe`, `ingestor-streaming`, `notificacao.recalculo.guia`, `notificacao.vencimento.guia`, `notificacao.vencimento.parcela`, `notificar-liberacao-guia-tfe`, `notificar-liberacao-guias-compra`, `notificar-liberacao-guias-compra-homol`, `notificar-liberacao-parcela-guia`, `processar-guia-imposto`, `recalcular-guia-das`, `recalculo-iss`, `rpa-regularize-pgfn`, `rpa-simples-nacional-teste`, `test-topic`, `verificar-cancelamento-parcelamento`, `verificar-pagamento`, `verificar-pagamento-darf`, `verificar-pagamento-tfe`, `verificar-sincronizacao-empresa-lote`, `verificar-sincronizacao-parcelamento`
- **Subscription**: `dados.darf-saida`, `notificacao.recalculo.guia`, `notificacao.vencimento.parcela`, `notificar-liberacao-parcela-guia`

## contabilizei-impostos

- **Tópico**: `calcula-impostos-nota-tomada`, `callback.plataforma`, `efetivar-perfil-fator-r`, `importar-guias-empresa`
- **Subscription**: `dados.processar-impostos-push`

## contabilizei-movimentacao-back

- **Fila Cloud Tasks**: `correcao-movimentacao`

## contabilizei-pagamentos

- **Tópico**: `processar-faturas`
- **Fila Cloud Tasks**: `audit-queue`, `push-notification`

## contato-service

- **Tópico**: `contato-service.topic.on-message-event-meta`, `contato-service.topic.on-message-event-meta.dlq`
- **Subscription**: `contato-service.sub.on-message-event-meta`, `contato-service.sub.on-message-event-meta.dlq`

## ctbzapp-utils

- **Fila Cloud Tasks**: `agendamento-queue`, `notificacao-queue`, `zendesk-queue`

## email-service

- **Tópico**: `email-service.p2p.file-upload`, `email-service.p2p.file-upload.dlq`, `email-service.p2p.send-email`, `email-service.p2p.send-email-callback`, `email-service.p2p.send-email-callback.dlq`, `email-service.p2p.send-email-validated`, `email-service.p2p.send-email-validated.dlq`, `email-service.p2p.send-email.dlq`, `test-topic`
- **Subscription**: `email-service.p2p.file-upload.dlq.inspect.sub`, `email-service.p2p.file-upload.sub`, `email-service.p2p.send-email-callback.dlq.inspect.sub`, `email-service.p2p.send-email-callback.invalid-payload.sub`, `email-service.p2p.send-email-callback.replication-not-found.sub`, `email-service.p2p.send-email-callback.smtp-unavailable.sub`, `email-service.p2p.send-email-callback.update-db.sub`, `email-service.p2p.send-email-callback.validation-error.sub`, `email-service.p2p.send-email-validated.dlq.inspect.sub`, `email-service.p2p.send-email-validated.enqueue-dispatch.sub`, `email-service.p2p.send-email-validated.replicate-record.sub`, `email-service.p2p.send-email.dlq.inspect.sub`, `email-service.p2p.send-email.sub`
- **Cloud Run / function**: `bots-api`

## emissor-whatsapp

- **Tópico**: `emissor-massivo-check-issuance`, `emissor-massivo-processar`, `emissor-massivo-reports`, `twilio-metrics-flow`
- **Subscription**: `emissor-massivo-processar`, `emissor-massivo-reports`, `twilio-metrics-flow`
- **Fila Cloud Tasks**: `emissor-whatsapp`, `emissor-whatsapp-massivo`
- **Cloud Run / function**: `emissor-whatsapp`, `emissor-whatsapp-massivo`

## emissor-whatsapp-reports

- **Fila Cloud Tasks**: `emissor-whatsapp`
- **Cloud Run / function**: `emissor-whatsapp`, `emissor-whatsapp-reports`

## experts-admin

- **Cloud Run / function**: `bots-api`

## experts-alertas

- **Cloud Run / function**: `experts-alertas`

## experts-api-gateway

- **Fila Cloud Tasks**: `emissor-whatsapp`, `emissor-whatsapp-massivo`, `experts-zendesk`
- **Cloud Run / function**: `emissor-whatsapp`, `emissor-whatsapp-massivo`, `emissor-whatsapp-reports`, `experts-api-gateway`, `experts-async-publisher`, `experts-nfs`, `experts-twilio-metrics`, `experts-zendesk`

## experts-async-publisher

- **Cloud Run / function**: `experts-async-publisher`

## experts-bruno

- **Tópico**: `twilio-webhooks-channels`, `zendesk-webhooks-notifications`
- **Fila Cloud Tasks**: `feedback-hub`
- **Cloud Run / function**: `check-numerical-answer`, `compare-values`, `experts-alertas`, `experts-nfs`, `multiply-two-string-values`, `return-element-at-index`, `return-list-property`, `validate-date`, `zendeskbot-conditional`, `zendeskbot-config`, `zendeskbot-delay`, `zendeskbot-loop`, `zendeskbot-parse-string-to-number`, `zendeskbot-validate-finantial-value`

## experts-contabil

- **Tópico**: `fintech.update-extrato`
- **Scheduler**: `cashflow-generate`
- **Fila Cloud Tasks**: `cashflow-generate`
- **Cloud Run / function**: `experts-contabil`

## experts-dominios-functions

- **Tópico**: `expired-twilio-tasks`, `functions.email-holerites`, `functions.ia-desvio-conduta.single-from-batch`, `functions.ia-desvio-conduta.single_chat-from-batch`, `functions.p2p.email-sender`, `functions.pendencias-oportunidades`, `twilio-republish-evts-from-crm`, `twilio-webhooks-tasks`
- **Subscription**: `functions.ia-desvio-conduta.single-from-batch.3-5-turbo-0125-temp0-sub`, `functions.ia-desvio-conduta.single-from-batch.4o-temp0-sub`, `functions.ia-desvio-conduta.single-from-evt.system-deleted.4o-sub`, `functions.ia-desvio-conduta.single-from-evt.task-completed.4o-sub`, `functions.ia-desvio-conduta.single_chat-from-batch-sub`, `tw-tasks-republish-to-experts-sub`
- **Scheduler**: `pendencias-oportunidades-scheduler`
- **Cloud Run / function**: `function-email-holerites`, `function-email-sender`, `function-html-to-pdf`, `function-pendencias-oportunidades`, `html-to-pdf`

## experts-drawio

- **Tópico**: `atendimento-zendesk-ticket-criado-atualizado-banco-de-dados`, `emissor-individual-emitir`, `emissor-massivo-check-issuance`, `emissor-massivo-processar`, `emissor-massivo-reports`, `expired-twilio-tasks`, `twilio-republish-evts-from-crm`, `twilio-webhooks-tasks`, `zendesk-tickets-callback`, `zendesk-tickets-upsert`, `zendesk-webhooks-tickets`
- **Subscription**: `emissor-individual-emitir`, `emissor-massivo-processar`, `emissor-massivo-reports`, `tw-tasks-republish-to-experts-sub`, `zendesk-webhooks-tickets`, `zendesk-webhooks-tickets-atendimento-zendesk-sub`
- **Fila Cloud Tasks**: `emissor-whatsapp`, `emissor-whatsapp-massivo`, `experts-zendesk`
- **Cloud Run / function**: `atendimento-api-gateway`, `contabilizei-crm-suporte-webhooks`, `contabilizei-crm-webhooks`, `emissor-whatsapp`, `emissor-whatsapp-massivo`, `emissor-whatsapp-reports`, `experts-alertas`, `experts-api-gateway`, `experts-async-publisher`, `experts-contabil`, `experts-nfs`, `experts-twilio-metrics`, `experts-zendesk`, `function-pendencias-oportunidades`

## experts-excalidraw

- **Cloud Run / function**: `function-email-holerites`, `html-to-pdf`

## experts-functions

- **Tópico**: `expired-twilio-tasks`, `functions.email-holerites`, `functions.ia-desvio-conduta.single-from-batch`, `functions.ia-desvio-conduta.single_chat-from-batch`, `functions.p2p.email-sender`, `functions.pendencias-oportunidades`, `twilio-republish-evts-from-crm`, `twilio-webhooks-tasks`
- **Subscription**: `functions.ia-desvio-conduta.single-from-batch.3-5-turbo-0125-temp0-sub`, `functions.ia-desvio-conduta.single-from-batch.4o-temp0-sub`, `functions.ia-desvio-conduta.single-from-evt.system-deleted.4o-sub`, `functions.ia-desvio-conduta.single-from-evt.task-completed.4o-sub`, `functions.ia-desvio-conduta.single_chat-from-batch-sub`, `tw-tasks-republish-to-experts-sub`
- **Scheduler**: `pendencias-oportunidades-scheduler`
- **Cloud Run / function**: `function-email-holerites`, `function-email-sender`, `function-html-to-pdf`, `function-pendencias-oportunidades`, `html-to-pdf`

## experts-ms-nps

- **Tópico**: `experts.assessor`, `nps.p2p.save`, `test-topic`
- **Subscription**: `plataforma.save-nps-sub`

## experts-nfs

- **Tópico**: `atendimento-zendesk.envio-whatsapp-ativo`, `emissor-callback`, `emissor-experts`, `emissor-massivo-reports`, `experts-nfs.bcast.nfs.result`, `experts-nfs.dead-letter`, `experts-nfs.p2p.create-nfs-jira`, `experts-nfs.p2p.nfs.retroativa`, `nfs.non-elegible`, `notas-worker.bcast.nfs-concluida`, `test-topic`
- **Subscription**: `emissor-massivo-reports`, `experts-nfs.sub.ack-nfs-recorrente`, `experts-nfs.sub.create-nfs-jira`, `experts-nfs.sub.emissor-callback.google-chat`, `experts-nfs.sub.emissor-callback.massivo`, `experts-nfs.sub.emissor-callback.whatsapp`, `experts-nfs.sub.nfs-concluida`, `experts-nfs.sub.nfs-jira.send-whatsapp-message`, `experts-nfs.sub.nfs-jira.update-issue`, `experts-nfs.sub.nfs.non-elegible.google-chat`, `experts-nfs.sub.nfs.retroativa`, `experts-nfs.sub.nfs.retroativa.google-chat`, `experts-nfs.sub.v3.emissor-callback.massivo`, `experts-nfs.sub.v3.emissor-callback.result`, `experts-nfs.sub.v3.emissor-callback.whatsapp-message`
- **Scheduler**: `experts-nfs-monitoring-check-queue`
- **Fila Cloud Tasks**: `emissor-experts`, `emissor-experts-pooler`, `emissor-whatsapp`, `notas-recorrentes`
- **Cloud Run / function**: `emissor-whatsapp`, `experts-nfs`

## experts-scripts

- **Fila Cloud Tasks**: `certificado-digital`, `notas-recorrentes`

## experts-service

- **Tópico**: `atendimento-zendesk-atualizar-ticket`, `atendimento-zendesk-ticket-criado-atualizado-banco-de-dados`, `atendimento-zendesk.envio-whatsapp-ativo`, `atendimento-zendesk.erros.atualizar-ticket`, `email-service.p2p.send-email`, `experts-service.bcast.csat-response`, `experts-service.dead-letters`, `experts-service.p2p.csat-fup-sla-16h`, `experts-service.p2p.feedback-hub.create-jira-issue`, `experts.assessor`, `experts.empresa`, `p2p.update-assessor-empresa`, `plataforma.bcast.empresa-alteracao-plano`, `processar-guia-imposto`, `test-topic`, `ticketing.bcast.ticket-jira`, `ticketing.bcast.v2.ticket-jira`, `zendesk-trigger.p2p.csat-survey`, `zendesk-webhooks-conversations`, `zendesk-webhooks-tickets`
- **Subscription**: `experts-service.p2p.update-assessor-empresa.sub`, `experts-service.sub.csat-fup-sla-16h`, `experts-service.sub.csat-fup.ticket-off-closed`, `experts-service.sub.csat-fup.ticket-off-merged`, `experts-service.sub.desconexao.create`, `experts-service.sub.desconexao.evalutate-message-ia`, `experts-service.sub.desconexao.ticket-update-error`, `experts-service.sub.feedback-hub.create-jira-issue`, `experts-service.sub.guia-imposto`, `experts-service.sub.guia-imposto-local`, `experts-service.sub.plataforma-alteracao-plano`, `experts-service.sub.run-survey-engine`, `experts-service.sub.send-csat-fup-atendimento`, `experts-service.sub.ticket-transbordo.ticket-jira-v1`, `experts-service.sub.ticket-transbordo.ticket-jira-v2`, `experts.empresa__experts-service__events-consumer-sub`, `plataforma.update-assessor-empresa-sub`, `zendesk-webhooks-tickets`
- **Scheduler**: `executar_task_scheduler`
- **Fila Cloud Tasks**: `emissor-whatsapp-massivo`, `feedback-hub`
- **Cloud Run / function**: `bots-api`, `emissor-whatsapp-massivo`

## experts-tarefas-assessor

- **Tópico**: `submit-single-wpp-message`, `test-topic`, `zendesk-tickets-callback`, `zendesk-tickets-upsert`
- **Scheduler**: `tarefas-organicas`
- **Fila Cloud Tasks**: `experts-zendesk`
- **Cloud Run / function**: `experts-zendesk`

## experts-twilio

- **Tópico**: `jira-troca-assessor-elogio-sugestao`, `nfs.instabilidade-prefeitura`, `nfs.non-elegible`, `twilio-metrics-flow`, `zendesk-tickets-upsert`
- **Subscription**: `twilio-metrics-flow`
- **Fila Cloud Tasks**: `emissor-whatsapp-massivo`, `feedback-hub`
- **Cloud Run / function**: `emissor-whatsapp-massivo`, `experts-alertas`, `experts-contabil`

## experts-twilio-flows

- **Tópico**: `twilio-metrics-flow`
- **Subscription**: `twilio-metrics-flow`
- **Fila Cloud Tasks**: `emissor-whatsapp`, `feedback-hub`
- **Cloud Run / function**: `emissor-whatsapp`

## experts-zendesk

- **Tópico**: `submit-single-wpp-message`, `test-topic`, `zendesk-tickets-callback`, `zendesk-tickets-upsert`
- **Scheduler**: `tarefas-organicas`
- **Fila Cloud Tasks**: `experts-zendesk`
- **Cloud Run / function**: `experts-zendesk`

## file-transcriber

- **Tópico**: `experts.assessor`, `file-transcriber.bcast.transcription`
- **Fila Cloud Tasks**: `file-transcriber-v2`
- **Cloud Run / function**: `file-transcriber`

## fintech-payments

- **Tópico**: `contabilizei-bank.agendar-pagamento`, `contabilizei-bank.cancelar-agendamento`, `contabilizei-bank.hubspot-events-input`, `contabilizei-bank.retentativa-pagamento-imediato`, `fintech-crm.enviar-email`, `fintech-crm.enviar-google-chat`, `fintech-crm.enviar-push-notification`, `payments.criar-lote-pagamento-recorrente`, `payments.enviar-dados-lote-para-fintech-web`, `payments.notificacao-email-pagamento-recorrente`, `payments.pagar-lote-recorrente`
- **Subscription**: `atualizar-forma-pagamento-fintech-payments-sub`, `contabilizei-bank.atualizar-conta-alias-fintech-payments-sub`, `contabilizei-bank.notificar-agendamento-cancelado-sub`, `payments.criar-lote-recorrente-sub`, `payments.enviar-dados-lote-para-fintech-web-sub`, `payments.notificacao-email-pagamento-recorrente-sub`, `payments.pagar-lote-recorrente-sub`, `sub.processar-controle-debito-guia-payments`, `sub.processar-faturas-payments`, `sub.processar-guia-imposto-payments`, `sub.update-empresa-payments`

## firestore-to-bigquery

- **Fila Cloud Tasks**: `emissor-whatsapp`, `notas-recorrentes`
- **Cloud Run / function**: `emissor-whatsapp`

## html-to-pdf

- **Cloud Run / function**: `html-to-pdf`

## js-libraries

- **Tópico**: `atendimento-zendesk.envio-whatsapp-ativo`, `experts-service.p2p.feedback-hub.create-jira-issue`, `test-topic`
- **Fila Cloud Tasks**: `feedback-hub`
- **Cloud Run / function**: `bots-api`

## k8s-configmap

- **Tópico**: `classificacao-atendimento`, `fintech-crm.enviar-email`, `fintech-crm.enviar-push-notification`, `fintech-recebiveis.notificacao-015`, `fintech-recebiveis.retorno-liquidacao`, `fintech-recebiveis.retorno-registro-antecipacao-precontratada`, `parcelamento-rpa-callback`, `rpa-regularize-pgfn`, `rpa-simples-nacional`, `verificar-cancelamento-parcelamento-retorno`
- **Subscription**: `dataflow-batch-service`, `fintech-recebiveis.agendar-liquidacao-sub`, `fintech-recebiveis.registrar-antecipacao-precontratada-sub`, `rpa-regularize-pgfn-sub`, `rpa-regularize-pgfn-teste-sub`, `rpa-simples-nacional-sub`, `rpa-simples-nacional-teste-sub`
- **Cloud Run / function**: `bots-api`, `contabilizei-agents`

## kong-config

- **Tópico**: `atendimento-zendesk-atualizar-ticket`, `zendesk-webhooks-agents`, `zendesk-webhooks-capacidade-agentes`, `zendesk-webhooks-comments`, `zendesk-webhooks-conversations`, `zendesk-webhooks-events-tickets`, `zendesk-webhooks-messages`, `zendesk-webhooks-notifications`, `zendesk-webhooks-pesquisa-satisfacao`, `zendesk-webhooks-retorno-desconexao-sem-interacao`, `zendesk-webhooks-tickets`, `zendesk-webhooks-tickets-new`, `zendesk-webhooks-users`
- **Subscription**: `dataflow-batch-service`, `zendesk-webhooks-tickets`
- **Cloud Run / function**: `bots-api`, `contabilizei-comprovante-rendimentos`, `contabilizei-crm-webhooks`, `experts-async-publisher`

## mcp-notas-fiscais

- **Fila Cloud Tasks**: `emissor-whatsapp`
- **Cloud Run / function**: `contabilizei-agents`, `emissor-whatsapp`, `experts-nfs`

## microsservico-agrupamento-guias

- **Tópico**: `agrupar-guias-empresa`, `agrupar-guias-empresa-retry`, `atendimento-zendesk.envio-whatsapp-ativo`, `atendimento-zendesk.whatsapp-ativo-status`, `email-service.p2p.file-upload`, `email-service.p2p.send-email`, `email-service.p2p.send-email-callback`, `ms-agrupamento-guias.p2p.agrupar-guias-retry`, `ms-agrupamento-guias.p2p.notificacao-diagnostico-bp`, `ms-agrupamento-guias.p2p.notifies-email`, `ms-agrupamento-guias.p2p.notifies-wpp`, `notificacao-grupo-guia-email`, `notificacao-grupo-guia-whatsapp`, `notificacao-guia-email`, `processar-guia-imposto`
- **Subscription**: `ms-agrupamento-guias.sub.agrupar-guias`, `ms-agrupamento-guias.sub.agrupar-guias-retry`, `ms-agrupamento-guias.sub.notificacao-diagnostico-bp`, `ms-agrupamento-guias.sub.notificacao-diagnostico-bp-local`, `ms-agrupamento-guias.sub.notifies-email`, `ms-agrupamento-guias.sub.notifies-wpp`, `ms-agrupamento-guias.sub.processar-guia`, `ms-agrupamento-guias.sub.send-email-callback`, `ms-agrupamento-guias.sub.send-wpp-callback`, `sub.agrupar-guias-empresa`, `sub.agrupar-guias-empresa-retry`, `sub.notificacao-grupo-guia-email`, `sub.notificacao-grupo-guia-whatsapp`, `sub.processar-guia-imposto-impostos`
- **Scheduler**: `ms-agrupamento-guias-cron-notify-email-bp-lp`, `ms-agrupamento-guias-cron-notify-email-exp-lp`, `ms-agrupamento-guias-cron-notify-email-exp-sn`, `ms-agrupamento-guias-cron-notify-wpp-bp-lp`, `ms-agrupamento-guias-cron-notify-wpp-exp-lp`, `ms-agrupamento-guias-cron-notify-wpp-exp-sn`, `ms-agrupamento-guias-cron-reprocess-group`

## monitoria-ia

- **Tópico**: `atendimento-zendesk-full-conversation`, `file-transcriber.bcast.transcription`, `zendesk-webhooks-tickets`
- **Subscription**: `monitoria-ia-aggregator.sub.transcriptions`, `monitoria-ia-parser.sub.zendesk-full-conversation`, `zendesk-webhooks-tickets`
- **Fila Cloud Tasks**: `monitoria-ia-agregador`, `monitoria-ia-executor`
- **Cloud Run / function**: `contabilizei-crm-suporte-webhooks`, `file-transcriber`, `monitoria-ia-aggregator`, `monitoria-ia-executor`, `monitoria-ia-parser`, `monitoria-ia-web`

## ms-relatorio-faturamento

- **Tópico**: `experts.assessor`, `relatorio-faturamento.p2p.processing`, `test-topic`
- **Subscription**: `relatorio-faturamento.p2p.processing-sub`
- **Cloud Run / function**: `html-to-pdf`

## oi-contabilizei-functions

- **Tópico**: `zendesk-criar-ticket`

## pipeline

- **Tópico**: `alarme-abertura-conta`, `alarme-autopilot`, `alarme-importacao-extrato`, `alarme-tickets-fintech`, `alarme-votos-nps`, `atendimento-zendesk-atualizar-ticket`, `ativar-collections`, `autopilot-desligamento-clientes-inelegiveis`, `autopilot-liberacao-novos-clientes`, `bs2-sync-conta`, `classificacao-atendimento`, `contabilizei-bank.webhook-dock`, `desativar-collections`, `financeiro-chat-payments`, `gerar-das`, `oferta-da-payments`, `oferta-da-payments-debito`, `twilio-webhooks-messages`, `twilio-webhooks-tasks`, `zendesk-webhooks-agents`, `zendesk-webhooks-capacidade-agentes`, `zendesk-webhooks-comments`, `zendesk-webhooks-conversations`, `zendesk-webhooks-events-tickets`, `zendesk-webhooks-notifications`, `zendesk-webhooks-pesquisa-satisfacao`, `zendesk-webhooks-retorno-desconexao-sem-interacao`, `zendesk-webhooks-tickets`, `zendesk-webhooks-tickets-new`, `zendesk-webhooks-users`
- **Subscription**: `contato-service.sub.on-message-event-meta`, `dados.buscar-baixa-das-anterior-dev`, `dados.buscar-baixa-das-anterior-prod`, `dados.buscar-baixa-das-dev`, `dados.buscar-baixa-das-prod`, `dataflow-batch-service`, `email-service.p2p.send-email.sub`, `experts-service.sub.desconexao.evalutate-message-ia`, `zendesk-agents.sub.tickets`, `zendesk-webhooks-tickets`
- **Fila Cloud Tasks**: `aida-classifier`, `aida-memoria-process`, `certificado-digital`, `experts-zendesk`, `simulador-plano-saude`
- **Cloud Run / function**: `aida-back-dev`, `aida-classifier-prd-api`, `aida-classifier-stg-api`, `arquivos-fator-r`, `atendimento-api-gateway`, `atendimento-api-gateway-dev`, `atendimento-api-gateway-prd`, `bots-api`, `contabilizei-agents`, `contabilizei-comprovante-rendimentos`, `contador-inteligente-dev-api`, `contador-inteligente-stg-api`, `emissor-whatsapp-reports`, `experts-alertas`, `experts-async-publisher`, `experts-nfs`, `experts-zendesk`, `find_situacao_voucher`, `html-to-pdf`, `notify-guias`, `sentinela-atendimento-dev`, `ultimateai-webhook`, `webhook-gitlab`, `zendeskbot-check-numerical-answer`, `zendeskbot-compare-values`, `zendeskbot-conditional`, `zendeskbot-config`, `zendeskbot-delay`, `zendeskbot-loop`, `zendeskbot-multiply-two-string-values`, `zendeskbot-parse-string-to-number`, `zendeskbot-request-delay`, `zendeskbot-return-element-at-index`, `zendeskbot-return-list-property`, `zendeskbot-validate-date`, `zendeskbot-validate-finantial-value`

## plataforma-app-config

- **Fila Cloud Tasks**: `aceite-portabilidade-queue`, `acesso-simples-queue`, `agendamento-importacao-notas-queue`, `agendamento-queue`, `alterar-regime-empresa`, `ativacao-contabil-histocio`, `ativacao-empresa`, `ativar-empresa-mei`, `atualizacao-cnae-anexo-massivo-queue`, `atualizar-campos-jira-processo-migracao-queue`, `atualizar-contratos-empresa-queue`, `auditoria-das-queue`, `backup-kind-queue`, `backup-queue`, `bank-integration-first-of-month-run`, `bigquery-exporter-queue`, `cadastro-automatico-queue`, `calcular-grupo-nota-tomada-queue`, `calculo-faturamento-queue`, `call-back-obrigacao`, `carregar-notificar-faturamento-zero`, `carregarDados-queue`, `central-rotinas-queue`, `certificado-digital`, `cnae-queue`, `cnd-queue`, `cobranca-avulsa-jira`, `comunicacao-fechamento-balanco`, `conciliador-escrituracao-reenvio-eventos`, `conclusao-importacao-comercio-queue`, `conclusao-importacao-queue`, `correcao-movimentacao`, `criar-obrigacao`, `criar-obrigacao-defis`, `crm-custom`, `darf-pagamento`, `das-pagamento`, `das-queue`, `dte-queue`, `email-boas-vindas-csa`, `email-follow-certificado`, `emissao-nota-fiscal-contabilizei`, `empresa-queue`, `enviar-email-finalizacao-abertura-queue`, `escrituracao-processamento-evento`, `escrituracao-queue`, `ev-custom`, `execucao-importacao-comercio-queue`, `execucao-importacao-queue`, `fast-obrigacao-queue`, `faturamento-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `fintech-criacao-contas`, `fintech-processos-consultas`, `firebase-callback-queue`, `fiscal-queue`, `folha-atualizacao-colaborador`, `folha-atualizacao-tipo-folha`, `folha-cancelamento`, `folha-coloca-em-calculo`, `folha-criacao-movimento`, `folha-criacao-novo-colaborador`, `folha-dispara-integracoes`, `folha-distribuicao-prolabore`, `folha-empresa-persistencia`, `folha-evento-finalizacao`, `folha-executa-calculo`, `folha-finalizacao`, `folha-finalizacao-desmembramento`, `folha-finalizacao-mes-atual`, `folha-geracao`, `folha-gerar-avulsa`, `folha-historico-prolabore`, `folha-importacao`, `folha-movimentos`, `folha-notificacao-data-limite-queue`, `folha-notificacao-dissidio-fopag-queue`, `folha-notificacao-ferias-fopag-queue`, `folha-notificacao-holerite-queue`, `folha-notificacao-queue`, `folha-qualidade-cadastral`, `folha-queue`, `folha-totais-decimo-terceiro`, `folha-totalizacao`, `gerar-arquivo-obrigacao`, `gerar-pdf-aceite-queue`, `gps-pagamento`, `importacao-automatica-nfse-queue`, `importacao-automatica-notas-tomadas-queue`, `importacao-comercio-queue`, `importacao-ofx`, `importacao-queue`, `imposto-comercio-queue`, `iss-queue`, `jira-queue`, `limpar-mes-contabil`, `lucro-presumido-queue`, `mes-contabil-queue`, `mobile-bff-default`, `mobile-default`, `modulo-impostos-queue`, `nfe-entrada-queue`, `notificacao-queue`, `notificacao-worker-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacao-recibo-impostos-queue`, `obrigacoes-core-fast-queue`, `obrigacoes-core-queue`, `obrigacoes-iss-poa-finalizacao-queue`, `obrigacoes-iss-poa-transmissao-queue`, `obrigacoes-iss-rj-queue`, `optimize-queue`, `pagamentos-service-queue`, `particionamento-notas-queue`, `pendencia-exclusao-simples-nacional-queue`, `pesquisa-usuario-queue`, `processa-lancamento-contabil-bk-queue`, `processamento-dctfweb`, `processamento-ecd`, `processamento-impostos-queue`, `processamento-mit`, `processamento-paginacao-dctfweb`, `processamento-paginacao-ecd`, `processamento-paginacao-mit`, `processar-elegibilidade-defis`, `processar-recibo-obrigacao`, `processar-transmissao-queue`, `push-notification`, `qc-queue`, `qc-queue-slow`, `recibo-queue`, `regime-tributario-queue`, `relatorio-contabil-queue`, `salvar-novo-onboarding-queue`, `sedex-queue`, `simulador-plano-saude`, `simular-gatilho-processar-empresa-defis`, `simular-gatilho-processar-lote-defis`, `sincronizar-contabil-queue`, `tarefas-depois-fechamento-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `verificador-pendencias-queue`, `verificar-prefeitura-queue`, `zendesk-queue`, `zendesk-sincronizar-organizacao-queue`, `zendesk-sincronizar-usuario-queue`

## plataforma-back-worker

- **Tópico**: `alteracao-empresa`, `audit-pagamentos-tfe`, `audit-parcelamento-especial`, `consultar-tfe`, `experts.empresa`, `gerar-tfe`, `verificador-pendencias`, `verificador-pendencias-cnd`
- **Fila Cloud Tasks**: `acesso-simples-queue`, `agendamento-queue`, `ativacao-empresa`, `bigquery-exporter-queue`, `call-back-obrigacao`, `carregarDados-queue`, `certificado-digital`, `cnae-queue`, `criar-obrigacao`, `darf-pagamento`, `das-pagamento`, `das-queue`, `escrituracao-queue`, `fast-obrigacao-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `folha-queue`, `gerar-arquivo-obrigacao`, `gps-pagamento`, `importacao-queue`, `nfe-entrada-queue`, `notificacao-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacoes-core-queue`, `optimize-queue`, `particionamento-notas-queue`, `processar-recibo-obrigacao`, `recibo-queue`, `regime-tributario-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `zendesk-queue`, `zendesk-sincronizar-organizacao-queue`, `zendesk-sincronizar-usuario-queue`

## plataforma-central-rotinas

- **Tópico**: `alteracao-empresa`, `audit-pagamentos-tfe`, `audit-parcelamento-especial`, `consultar-tfe`, `gerar-tfe`, `verificador-pendencias`, `verificador-pendencias-cnd`
- **Fila Cloud Tasks**: `acesso-simples-queue`, `agendamento-queue`, `ativacao-empresa`, `bigquery-exporter-queue`, `call-back-obrigacao`, `carregarDados-queue`, `certificado-digital`, `cnae-queue`, `criar-obrigacao`, `darf-pagamento`, `das-pagamento`, `das-queue`, `escrituracao-queue`, `fast-obrigacao-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `folha-queue`, `gerar-arquivo-obrigacao`, `gps-pagamento`, `importacao-queue`, `nfe-entrada-queue`, `notificacao-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacoes-core-queue`, `optimize-queue`, `particionamento-notas-queue`, `processar-recibo-obrigacao`, `recibo-queue`, `regime-tributario-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `zendesk-queue`

## plataforma-crm-web

- **Tópico**: `audit-pagamentos-tfe`, `audit-parcelamento-especial`, `consultar-tfe`, `gerar-tfe`, `verificador-pendencias`, `verificador-pendencias-cnd`
- **Fila Cloud Tasks**: `acesso-simples-queue`, `agendamento-queue`, `ativacao-empresa`, `bigquery-exporter-queue`, `call-back-obrigacao`, `carregarDados-queue`, `certificado-digital`, `cnae-queue`, `criar-obrigacao`, `crm-custom`, `darf-pagamento`, `das-pagamento`, `das-queue`, `emissor-whatsapp`, `escrituracao-queue`, `fast-obrigacao-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `folha-queue`, `gerar-arquivo-obrigacao`, `gps-pagamento`, `importacao-queue`, `nfe-entrada-queue`, `notificacao-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacoes-core-queue`, `optimize-queue`, `particionamento-notas-queue`, `processar-recibo-obrigacao`, `recibo-queue`, `regime-tributario-queue`, `simulador-plano-saude`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `zendesk-queue`
- **Cloud Run / function**: `emissor-whatsapp`, `historico-atendimento`

## plataforma-faturamento-worker

- **Tópico**: `agrupar-guias-empresa`, `alteracao-empresa`, `audit-pagamentos-tfe`, `audit-parcelamento-especial`, `calcula-impostos-nota-tomada`, `calcular-impostos-lucro-presumido`, `callback-calculo-impostos-nota-tomada`, `consultar-desenquadramento-dte`, `consultar-tfe`, `criar-empresa-pre-fator-r`, `darf-entrada`, `finalizar-importacao-lucro-presumido`, `gerar-iss`, `gerar-tfe`, `gestao-regime-tributario`, `gps-solicita-recalculo`, `integra-contador`, `migrar-impostos-lucro-presumido`, `recalculo-iss`, `transmitir-pgdas`, `varredura-dte`, `verificador-pendencias`, `verificador-pendencias-cnd`
- **Subscription**: `consulta-enquadramento-final`, `consulta-enquadramento-inicial`, `consulta-solicitacao-enquadramento`, `dados.gerar-iss-retorno`, `solicita-enquadramento`, `troca-regime-tributario-final`, `troca-regime-tributario-lp`, `troca-regime-tributario-restricao-cidade`
- **Fila Cloud Tasks**: `acesso-simples-queue`, `agendamento-queue`, `ativacao-empresa`, `auditoria-das-queue`, `bigquery-exporter-queue`, `calculo-faturamento-queue`, `call-back-obrigacao`, `carregarDados-queue`, `cnae-queue`, `criar-obrigacao`, `darf-pagamento`, `das-pagamento`, `das-queue`, `escrituracao-queue`, `fast-obrigacao-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `folha-queue`, `gerar-arquivo-obrigacao`, `gps-pagamento`, `importacao-queue`, `nfe-entrada-queue`, `notificacao-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacoes-core-queue`, `optimize-queue`, `particionamento-notas-queue`, `processamento-impostos-queue`, `processar-recibo-obrigacao`, `push-notification`, `recibo-queue`, `regime-tributario-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `zendesk-queue`

## plataforma-fopag-worker

- **Tópico**: `alteracao-empresa`, `audit-inss`, `audit-pagamentos-tfe`, `audit-parcelamento-especial`, `audit-simples-ecac`, `comercio-20-topic-empresas-inativas`, `comercio-notify-evento-cancelamento`, `consulta-situacao-fiscal`, `consulta-situacao-fiscal-retorno`, `consultar-tfe`, `darf-entrada`, `darf-saida`, `dataflow-streaming-eventos-solicitacao-contas`, `eventos-solicitacao-contas-crm`, `functions.email-holerites`, `gerar-imposto-composicao-darf-unificado`, `gerar-imposto-folha-fgts`, `gerar-tfe`, `notificar-alteracao-inss-darf`, `processar-guia-imposto`, `simular-transmissao-pgdas`, `update-empresa`, `update-integracao-conta-bancaria`, `verificador-pendencias`, `verificador-pendencias-cnd`, `verificador-pendencias-divida-ativa`, `verificador-pendencias-divida-ativa-dev`, `verificar-pagamento-darf`, `vinculo-certificado`
- **Fila Cloud Tasks**: `acesso-simples-queue`, `agendamento-queue`, `ativacao-empresa`, `bigquery-exporter-queue`, `call-back-obrigacao`, `carregarDados-queue`, `cnae-queue`, `criar-obrigacao`, `darf-pagamento`, `das-pagamento`, `das-queue`, `escrituracao-queue`, `fast-obrigacao-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `folha-queue`, `gerar-arquivo-obrigacao`, `gps-pagamento`, `importacao-queue`, `nfe-entrada-queue`, `notificacao-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacoes-core-queue`, `optimize-queue`, `particionamento-notas-queue`, `processar-recibo-obrigacao`, `recibo-queue`, `regime-tributario-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `zendesk-queue`

## plataforma-importacao-notas-worker

- **Tópico**: `alteracao-empresa`, `audit-inss`, `audit-pagamentos-tfe`, `audit-parcelamento-especial`, `audit-simples-ecac`, `comercio-20-topic-empresas-inativas`, `comercio-notify-evento-cancelamento`, `consulta-situacao-fiscal`, `consulta-situacao-fiscal-retorno`, `consultar-tfe`, `darf-entrada`, `darf-saida`, `dataflow-streaming-eventos-solicitacao-contas`, `empresa-alterada`, `empresa-ativada`, `eventos-solicitacao-contas-crm`, `gerar-tfe`, `mes-contabil-listener`, `notas-worker.bcast.nfs-concluida`, `notificar-alteracao-inss-darf`, `processar-guia-imposto`, `simular-transmissao-pgdas`, `update-empresa`, `update-integracao-conta-bancaria`, `verificador-pendencias`, `verificador-pendencias-cnd`, `verificador-pendencias-divida-ativa`, `verificador-pendencias-divida-ativa-dev`, `verificar-pagamento-darf`, `vinculo-certificado`
- **Fila Cloud Tasks**: `acesso-simples-queue`, `agendamento-queue`, `ativacao-empresa`, `atualizacao-cnae-anexo-massivo-queue`, `bigquery-exporter-queue`, `call-back-obrigacao`, `carregarDados-queue`, `cnae-queue`, `conclusao-importacao-queue`, `criar-obrigacao`, `darf-pagamento`, `das-pagamento`, `das-queue`, `escrituracao-queue`, `fast-obrigacao-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `folha-queue`, `gerar-arquivo-obrigacao`, `gps-pagamento`, `importacao-automatica-notas-tomadas-queue`, `importacao-queue`, `nfe-entrada-queue`, `notas-recorrentes`, `notificacao-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacoes-core-queue`, `optimize-queue`, `particionamento-notas-queue`, `processar-recibo-obrigacao`, `push-notification`, `recibo-queue`, `regime-tributario-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `zendesk-queue`

## plataforma-monolito

- **Tópico**: `alteracao-empresa`, `audit-pagamentos-tfe`, `audit-parcelamento-especial`, `consultar-tfe`, `gerar-tfe`, `verificador-pendencias`, `verificador-pendencias-cnd`
- **Fila Cloud Tasks**: `aceite-portabilidade-queue`, `acesso-simples-queue`, `agendamento-importacao-notas-queue`, `agendamento-queue`, `alterar-regime-empresa`, `ativacao-contabil-histocio`, `ativacao-empresa`, `ativar-empresa-mei`, `atualizar-contratos-empresa-queue`, `auditoria-das-queue`, `backup-kind-queue`, `backup-queue`, `bank-integration-first-of-month-run`, `bigquery-exporter-queue`, `cadastro-automatico-queue`, `call-back-obrigacao`, `carregar-notificar-faturamento-zero`, `carregarDados-queue`, `certificado-digital`, `cnae-queue`, `cnd-queue`, `cobranca-avulsa-jira`, `comunicacao-fechamento-balanco`, `conclusao-importacao-queue`, `correcao-movimentacao`, `criar-obrigacao`, `darf-pagamento`, `das-pagamento`, `das-queue`, `dte-queue`, `email-boas-vindas-csa`, `email-follow-certificado`, `emissao-nota-fiscal-contabilizei`, `empresa-queue`, `enviar-email-finalizacao-abertura-queue`, `escrituracao-processamento-evento`, `escrituracao-queue`, `execucao-importacao-queue`, `fast-obrigacao-queue`, `faturamento-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `fintech-criacao-contas`, `fintech-processos-consultas`, `firebase-callback-queue`, `fiscal-queue`, `folha-queue`, `gerar-arquivo-obrigacao`, `gerar-pdf-aceite-queue`, `gps-pagamento`, `importacao-auto-nfse-queue`, `importacao-ofx`, `importacao-queue`, `imposto-comercio-queue`, `iss-queue`, `jira-queue`, `limpar-mes-contabil`, `lucro-presumido-queue`, `mes-contabil-queue`, `modulo-impostos-queue`, `nfe-entrada-queue`, `notas-recorrentes`, `notificacao-queue`, `notificacao-worker-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacao-recibo-impostos-queue`, `obrigacoes-core-fast-queue`, `obrigacoes-core-queue`, `optimize-queue`, `pagamentos-service-queue`, `particionamento-notas-queue`, `pendencia-exclusao-simples-nacional-queue`, `processa-lancamento-contabil-bk-queue`, `processamento-impostos-queue`, `processar-recibo-obrigacao`, `processar-transmissao-queue`, `qc-queue`, `qc-queue-slow`, `recibo-queue`, `regime-tributario-queue`, `relatorio-contabil-queue`, `salvar-novo-onboarding-queue`, `sedex-queue`, `sincronizar-contabil-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `verificador-pendencias-queue`, `zendesk-queue`

## plataforma-web

- **Tópico**: `alteracao-empresa`, `audit-pagamentos-tfe`, `audit-parcelamento-especial`, `consultar-tfe`, `gerar-tfe`, `verificador-pendencias`, `verificador-pendencias-cnd`, `zendesk-criar-ticket`
- **Fila Cloud Tasks**: `acesso-simples-queue`, `agendamento-queue`, `ativacao-empresa`, `bigquery-exporter-queue`, `call-back-obrigacao`, `carregarDados-queue`, `certificado-digital`, `cnae-queue`, `conclusao-importacao-queue`, `criar-obrigacao`, `darf-pagamento`, `das-pagamento`, `das-queue`, `escrituracao-queue`, `fast-obrigacao-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `fintech-processos-consultas`, `folha-queue`, `gerar-arquivo-obrigacao`, `gps-pagamento`, `importacao-queue`, `nfe-entrada-queue`, `notificacao-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacoes-core-queue`, `optimize-queue`, `particionamento-notas-queue`, `processar-recibo-obrigacao`, `recibo-queue`, `regime-tributario-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `zendesk-queue`

## relacionamento-service

- **Tópico**: `relacionamento.jira-updater`, `relacionamento.jira-updater-v2`

## ticketing-service

- **Tópico**: `ticketing.bcast.dados-gerais-jira-result`, `ticketing.bcast.ticket-jira`, `ticketing.bcast.v2.ticket-jira`, `ticketing.dead-letters`, `ticketing.p2p.add-dados-empresa`, `ticketing.p2p.add-dados-gerais-ticket-jira`, `ticketing.p2p.v1.sla`, `ticketing.p2p.v2.dados-empresa`
- **Subscription**: `ticketing.sub.add-dados-empresa`, `ticketing.sub.add-dados-gerais-ticket-jira`, `ticketing.sub.bq.dados-gerais-jira-result`, `ticketing.sub.upsert-ticket-jira`, `ticketing.sub.v1.sla`, `ticketing.sub.v2.dados-empresa`, `ticketing.sub.v2.upsert-ticket-jira`

## webhook-gitlab

- **Scheduler**: `webhook-gitlab-canais-past-mr-reminder`, `webhook-gitlab-canais-today-mr-needs-attention`, `webhook-gitlab-canais-today-mr-reminder`
- **Cloud Run / function**: `webhook-gitlab`

## zendesk-agents

- **Tópico**: `aida-classifier-classification-event`, `atendimento-zendesk-atualizar-ticket`, `atendimento-zendesk-enviar-mensagem-sunshine`, `contabilizei-agents.bcast.metrics`, `experts-nfs.bcast.nfs.result`, `experts-service.bcast.csat-response`, `file-transcriber.bcast.transcription`, `test-topic`, `zendesk-agents.bcast.etl.agent-latency-results`, `zendesk-atualizar-ticket`, `zendesk-webhooks-conversations`, `zendesk-webhooks-tickets`
- **Subscription**: `subscription-name`, `zendesk-agents.sub.bq.agent-latency-results`, `zendesk-agents.sub.conversations`, `zendesk-agents.sub.etl.agent-latency`, `zendesk-agents.sub.file-transcriber-result`, `zendesk-agents.sub.tickets`, `zendesk-agents.sub.v1.agents-control.on-csat-response`, `zendesk-agents.sub.v1.agents-control.on-metrics`, `zendesk-agents.sub.v1.agents-control.on-ticket-update`, `zendesk-agents.sub.v1.concierge-acknowledge-nf`, `zendesk-agents.sub.v1.copilot-actions`, `zendesk-agents.sub.v1.copilot-actions.dictionary-on-message`, `zendesk-agents.sub.v1.copilot-actions.on-ticket-update`, `zendesk-agents.sub.v1.customer-summary.on-ticket-update`, `zendesk-webhooks-tickets`
- **Cloud Run / function**: `bots-api`, `contabilizei-agents`, `experts-nfs`, `file-transcriber`

## zendeskbot-functions

- **Cloud Run / function**: `check-numerical-answer`, `compare-values`, `multiply-two-string-values`, `return-element-at-index`, `return-list-property`, `validate-date`, `zendeskbot-conditional`, `zendeskbot-config`, `zendeskbot-delay`, `zendeskbot-loop`, `zendeskbot-parse-string-to-number`, `zendeskbot-request-delay`, `zendeskbot-validate-finantial-value`
