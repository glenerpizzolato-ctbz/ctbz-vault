---
name: email-service-teste-banco-fora
description: "Como testar em dev a retentativa da validação com o banco fora, sem derrubar a instância compartilhada: rodar a branch localmente e derrubar só o proxy local"
metadata:
  type: reference
tags:
  - email-service
  - testes
---

# Testar a validação com o banco fora (dev)

A instância de dev (`atendimento-canais-dev:us-central1:atendimento-canais`) é compartilhada com os outros serviços de canais: não reiniciar nem bloquear o banco para testar.

Em vez disso, rodar a branch localmente: o `.env` local aponta para o banco de dev pelo proxy em `localhost:5433` (`sql_atendimento_dev`) e o Pub/Sub de `atendimento-canais-dev`. O pool do Postgres conecta sob demanda (sem I/O no boot), então o app sobe com o proxy derrubado, e a falha é real (`ECONNREFUSED`), só para o processo local.

1. Tirar o pod de dev da disputa pela `email-service.p2p.send-email.sub` (cada mensagem vai para um só assinante; o pod de dev costuma rodar a imagem do último MR, mas com o banco dele no ar validaria a mensagem). O deployment tem um ScaledObject do KEDA com mínimo 1, então `kubectl scale --replicas=0` é desfeito: pausar o KEDA em 0 com `kubectl --context gke_contabilizei-dev-01_us-central1-a_contabilizei-private-cluster-dev-01 -n atendimento-canais-dev annotate scaledobject email-service autoscaling.keda.sh/paused-replicas=0 --overwrite` e, no fim, remover a anotação (`autoscaling.keda.sh/paused-replicas-`). Cluster privado: precisa de VPN. Atenção: o contexto padrão do `kubectl` pode ser o de prod; sempre passar `--context`.
2. Subir local (`pnpm dev`) e derrubar o proxy: `zsh -ic '_sql_proxy_kill_alias sql_atendimento_dev'`.
3. Publicar um envio válido em `email-service.p2p.send-email` (dev), ex: `node ~/dotfiles/src/google/publish-topic.google.js topic=email-service.p2p.send-email`, com `template_id` de um template que exista em dev.
4. Ver no log local `error processing send email message` com `deliveryAttempt` 1, 2, 3… (backoff da subscription: 10s a 600s, 5 tentativas, DLQ `email-service.p2p.send-email.dlq`).
5. Cenário recuperação: subir o proxy (`zsh -ic '_sql_proxy_start_alias sql_atendimento_dev'`) antes da 5ª tentativa e ver a mensagem validar e seguir (`email_replications` com o `id` = messageId, status `SENT`).
6. Cenário esgotado: deixar o proxy fora até a 5ª tentativa; o callback `INVALID_PAYLOAD` com `failure_reason: VALIDATION_HANDLER_ERROR` é publicado e a mensagem aparece em `email-service.p2p.send-email.dlq.inspect.sub` (`gcloud pubsub subscriptions pull … --project=atendimento-canais-dev` sem `--auto-ack`).
7. Voltar as réplicas do deployment de dev.

## Armadilhas vistas no teste de 09/11/2026 (PRD-175906)

- **A DLQ dá outro messageId** à mensagem: procurar pelo payload ou por `CloudPubSubDeadLetterSourceTopicPublishTime`, não pelo id original.
- **`pull` sem ack reserva a mensagem por 600s** (`ackDeadlineSeconds` da `…dlq.inspect.sub`): um loop de `pull` esconde a mensagem dos `pull` seguintes por 10 minutos. Para confirmar sem ler, usar a métrica `pubsub.googleapis.com/subscription/dead_letter_message_count` da subscription de origem (API do Cloud Monitoring).
- **O SMTP do HubSpot de dev recusa o remetente** (`421 The from domain should be a connected email sending domain`): nenhum envio sai `SENT` em dev desde maio/2026, então o teste vai até `email_replications` + dispatch, não até a caixa de entrada.
- Para a callback não ir a um serviço real, publicar com `application` de teste (ex: `teste-prd-175906`).
- Evidências com prints: renderizar o log em HTML e capturar com `google-chrome --headless=new --screenshot=… --window-size=1500,860 file://…` (sem ferramenta de print de tela no X11 desta máquina).
