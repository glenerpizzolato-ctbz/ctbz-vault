---
name: dependencias-plataforma-app-config
description: "Dependências do plataforma-app-config: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - plataforma-app-config
repositorio: plataforma-app-config
---

# Dependências do plataforma-app-config

O que o `plataforma-app-config` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

## Consome

### Repositórios internos

_Nada confirmado ainda._

### Libs internas

_Nada confirmado ainda._

### Infra GCP

_Nada confirmado ainda._

### Bancos e dados

_Nada confirmado ainda._

### Terceiros

_Nada confirmado ainda._

## Consumido por

Quem consome os contratos deste repositório; a revisão de MRs confere se o diff quebra algum deles.

_Nada confirmado ainda._

<!-- deps:auto:inicio (gerado por mapear-dependencias; não editar à mão) -->

## Levantamento automático

Gerado em 2026-11-19 sobre `master` @ `c1853e6` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.

### Repositórios que este cita

- `plataforma-web` (1×): `src/main/webapp/WEB-INF/dispatch.xml:33`
- `plataforma-central-rotinas` (1×): `src/main/webapp/WEB-INF/queue.xml:1463`

### Repositórios que citam este

_Nenhum._

### Libs internas

- `br.com.contabilizei:contabilizei-back-parent` (`pom.xml`)

### Infra GCP (catálogo [[por-repositorio]], de 2026-10-09)

- **Fila Cloud Tasks**: `aceite-portabilidade-queue`, `acesso-simples-queue`, `agendamento-importacao-notas-queue`, `agendamento-queue`, `alterar-regime-empresa`, `ativacao-contabil-histocio`, `ativacao-empresa`, `ativar-empresa-mei`, `atualizacao-cnae-anexo-massivo-queue`, `atualizar-campos-jira-processo-migracao-queue`, `atualizar-contratos-empresa-queue`, `auditoria-das-queue`, `backup-kind-queue`, `backup-queue`, `bank-integration-first-of-month-run`, `bigquery-exporter-queue`, `cadastro-automatico-queue`, `calcular-grupo-nota-tomada-queue`, `calculo-faturamento-queue`, `call-back-obrigacao`, `carregar-notificar-faturamento-zero`, `carregarDados-queue`, `central-rotinas-queue`, `certificado-digital`, `cnae-queue`, `cnd-queue`, `cobranca-avulsa-jira`, `comunicacao-fechamento-balanco`, `conciliador-escrituracao-reenvio-eventos`, `conclusao-importacao-comercio-queue`, `conclusao-importacao-queue`, `correcao-movimentacao`, `criar-obrigacao`, `criar-obrigacao-defis`, `crm-custom`, `darf-pagamento`, `das-pagamento`, `das-queue`, `dte-queue`, `email-boas-vindas-csa`, `email-follow-certificado`, `emissao-nota-fiscal-contabilizei`, `empresa-queue`, `enviar-email-finalizacao-abertura-queue`, `escrituracao-processamento-evento`, `escrituracao-queue`, `ev-custom`, `execucao-importacao-comercio-queue`, `execucao-importacao-queue`, `fast-obrigacao-queue`, `faturamento-queue`, `fechamento-exercicio`, `fechamento-exercicio-auto`, `fintech-criacao-contas`, `fintech-processos-consultas`, `firebase-callback-queue`, `fiscal-queue`, `folha-atualizacao-colaborador`, `folha-atualizacao-tipo-folha`, `folha-cancelamento`, `folha-coloca-em-calculo`, `folha-criacao-movimento`, `folha-criacao-novo-colaborador`, `folha-dispara-integracoes`, `folha-distribuicao-prolabore`, `folha-empresa-persistencia`, `folha-evento-finalizacao`, `folha-executa-calculo`, `folha-finalizacao`, `folha-finalizacao-desmembramento`, `folha-finalizacao-mes-atual`, `folha-geracao`, `folha-gerar-avulsa`, `folha-historico-prolabore`, `folha-importacao`, `folha-movimentos`, `folha-notificacao-data-limite-queue`, `folha-notificacao-dissidio-fopag-queue`, `folha-notificacao-ferias-fopag-queue`, `folha-notificacao-holerite-queue`, `folha-notificacao-queue`, `folha-qualidade-cadastral`, `folha-queue`, `folha-totais-decimo-terceiro`, `folha-totalizacao`, `gerar-arquivo-obrigacao`, `gerar-pdf-aceite-queue`, `gps-pagamento`, `importacao-automatica-nfse-queue`, `importacao-automatica-notas-tomadas-queue`, `importacao-comercio-queue`, `importacao-ofx`, `importacao-queue`, `imposto-comercio-queue`, `iss-queue`, `jira-queue`, `limpar-mes-contabil`, `lucro-presumido-queue`, `mes-contabil-queue`, `mobile-bff-default`, `mobile-default`, `modulo-impostos-queue`, `nfe-entrada-queue`, `notificacao-queue`, `notificacao-worker-queue`, `obrigacao-agendamento`, `obrigacao-queue`, `obrigacao-queue-manual`, `obrigacao-recibo-impostos-queue`, `obrigacoes-core-fast-queue`, `obrigacoes-core-queue`, `obrigacoes-iss-poa-finalizacao-queue`, `obrigacoes-iss-poa-transmissao-queue`, `obrigacoes-iss-rj-queue`, `optimize-queue`, `pagamentos-service-queue`, `particionamento-notas-queue`, `pendencia-exclusao-simples-nacional-queue`, `pesquisa-usuario-queue`, `processa-lancamento-contabil-bk-queue`, `processamento-dctfweb`, `processamento-ecd`, `processamento-impostos-queue`, `processamento-mit`, `processamento-paginacao-dctfweb`, `processamento-paginacao-ecd`, `processamento-paginacao-mit`, `processar-elegibilidade-defis`, `processar-recibo-obrigacao`, `processar-transmissao-queue`, `push-notification`, `qc-queue`, `qc-queue-slow`, `recibo-queue`, `regime-tributario-queue`, `relatorio-contabil-queue`, `salvar-novo-onboarding-queue`, `sedex-queue`, `simulador-plano-saude`, `simular-gatilho-processar-empresa-defis`, `simular-gatilho-processar-lote-defis`, `sincronizar-contabil-queue`, `tarefas-depois-fechamento-queue`, `transmitir-obrigacao`, `upload-obrigacao`, `validacao-comercio-queue`, `validacao-importacao-queue`, `validacao-queue`, `verificador-pendencias-queue`, `verificar-prefeitura-queue`, `zendesk-queue`, `zendesk-sincronizar-organizacao-queue`, `zendesk-sincronizar-usuario-queue`

### Bancos e dados

_Nenhum driver ou dataset achado._

### Terceiros

_Nenhum SDK ou host de terceiro achado._

<!-- deps:auto:fim -->
