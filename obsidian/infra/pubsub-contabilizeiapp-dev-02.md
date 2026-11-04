---
name: pubsub-contabilizeiapp-dev-02
description: "Tópicos e subscriptions do Pub/Sub em contabilizeiapp-dev-02 (App Contabilizei, dev) com consumidor e repositórios que citam cada um"
metadata:
  type: reference
tags:
  - infra
  - pubsub
atualizado_em: 2026-10-09
---

# Pub/Sub: contabilizeiapp-dev-02

App Contabilizei, dev. Fotografia de 2026-10-09. Formato: tópico → subscriptions (tipo e consumidor) · repositórios que citam o nome do tópico/subscription em `~/repositories` (`config:` = repos de configuração que citam quase tudo). Ver [[_infra-indice]] para o significado de cada campo.

- **`alteracao-empresa`** · repos: contabilizei-back-core, plataforma-back-worker, plataforma-central-rotinas, plataforma-faturamento-worker, plataforma-fopag-worker, plataforma-importacao-notas-worker, plataforma-monolito, plataforma-web
- **`cloud-builds`**
- **`comercio-20-topic-empresas-inativas`** · repos: contabilizei-back-core, plataforma-fopag-worker, plataforma-importacao-notas-worker
- **`comercio-notify-evento-cancelamento`** · repos: contabilizei-back-core, plataforma-fopag-worker, plataforma-importacao-notas-worker
    - `comercio-notify-evento-cancelamento-sub` (pull)
- **`empresa-alterada`** · repos: contabilizei-back-core, plataforma-importacao-notas-worker
    - `empresa-alterada-sub-codigos-tributarios` (pull, consumidor provável `empresa-alterada`, DLQ `empresa-alterada-dlq-codigos-tributarios`)
- **`empresa-alterada-dlq-codigos-tributarios`**
    - `empresa-alterada-dlq-sub-codigos-tributarios` (pull, consumidor provável `empresa-alterada-dlq`)
- **`empresa-ativada`** · repos: contabilizei-back-core, plataforma-importacao-notas-worker
    - `empresa-ativada-sub-codigos-tributarios` (pull, consumidor provável `empresa-ativada`, DLQ `empresa-ativada-dlq-codigos-tributarios`)
    - `empresa-ativada-sub-gestao-eventos-snh` (pull, consumidor provável `empresa-ativada`, DLQ `empresa-ativada-dlq-gestao-eventos-snh`)
- **`empresa-ativada-dlq-codigos-tributarios`**
    - `empresa-ativada-dlq-sub-codigos-tributarios` (pull, consumidor provável `empresa-ativada-dlq`)
- **`empresa-ativada-dlq-gestao-eventos-snh`**
- **`notas-worker.bcast.nfs-concluida`** · repos: experts-nfs, plataforma-importacao-notas-worker
    - `notas-worker.bcast.nfs-concluida-sub-apurador-ibs-cbs` (pull, consumidor provável `notas-worker.bcast.nfs-concluida`, DLQ `notas-worker.bcast.nfs-concluida-dlq-apurador-ibs-cbs`)
- **`notas-worker.bcast.nfs-concluida-dlq-apurador-ibs-cbs`**
    - `notas-worker.bcast.nfs-concluida-dlq-sub-apurador-ibs-cbs` (pull, consumidor provável `notas-worker.bcast.nfs-concluida-dlq`)
- **`processar-upload-inss`**
    - `dados.processar-upload-inss` (push → App Engine `contabilizei-back-worker` /rest/worker/impostopagar/auth/processaCallbackInss)
- **`salvar-xml-nfse`**
