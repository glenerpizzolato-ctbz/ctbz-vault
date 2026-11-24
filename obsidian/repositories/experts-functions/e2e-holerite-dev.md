---
name: experts-functions-e2e-holerite-dev
description: "Teste E2E em dev do e-mail de holerite: script que publica no functions.email-holerites e confere function, email_replications, PDFs no bucket, e-mail renderizado, status do envio e o caso sem colaborador válido"
metadata:
  type: reference
tags:
  - experts-functions
  - email-service
  - e2e
criado_em: 2026-11-24
---

# E2E do e-mail de holerite em dev

Script: [[scripts/e2e_holerite_dev.py]] (`~/ctbz-vault/obsidian/repositories/experts-functions/scripts/e2e_holerite_dev.py`). Fica só no vault, fora do repositório, por decisão de 24/11/2026 (PRD-178571, sub-task de testes PRD-178575).


O script publica eventos no tópico `functions.email-holerites` de `contabilizei-experts-dev` e confere cada salto até o email-service:

1. O log da function com o `emailId`.
2. A linha em `email_replications`: template `exp-email-holerite-v1`, remetente, assunto, variáveis, opt-out e um anexo por colaborador válido.
3. Os PDFs no bucket do email-service.
4. O e-mail renderizado (HTML e PNG).
5. O status final do envio.
6. A ausência de envio quando nenhum colaborador é válido.

Em dev, o status final do envio é `FAILED`: desde 20/08/2026, a HubSpot de dev recusa o domínio do remetente com o erro 421. O script trata esse caso como esperado. A entrega na caixa de entrada é validada em prd.

## Subscription própria e DLQ (PRD-178821)

O script [[scripts/e2e_holerite_sub_dlq_dev.py]] testa a `function-email-holerites-sub`, com ack de 600 s e DLQ depois de 10 tentativas. Ele importa o `e2e_holerite_dev.py` e tem dois casos, `--cases slow,dlq`:

- **slow**: manda N colaboradores (`--employees`) e confere que houve uma única requisição, um único log "Holerites enviados" e um único registro em `email_replications`.
- **dlq**: manda um PDF gigante, que o `file-upload` recusa por passar de 10 MB. Confere que a mensagem chega à `functions.email-holerites.dlq-sub` com `CloudPubSubDeadLetterSourceDeliveryCount=10` e que houve 10 requisições, sem envio. O publish é pela REST, porque o `gcloud --message` não aceita alguns MB.

Os casos usam a contagem de requisições da function na janela do teste, então não rode dois ao mesmo tempo. A mensagem leva de 8 a 10 minutos para chegar à DLQ, por causa do backoff de 10 a 600 s.

> [!WARNING] `function-html-to-pdf` de dev estoura a memória com 4 ou mais PDFs
> Em dev, o `function-html-to-pdf` roda com `max_instances=1`, `container_concurrency=100` e 512 Mi. Em prd é `container_concurrency=1` com até 100 instâncias. Com 4 ou mais colaboradores, os PDFs gerados em paralelo dão "Out-of-memory event detected in container", e a function responde 503. Depois de três rodadas assim, em 24/11/2026, a instância travou: toda chamada passou a levar 504 em 120 s, mesmo com 2 PDFs. O `deploy-dev` sem diff não recria a revisão, e o usuário não tem `artifactregistry.repositories.downloadArtifacts` no `contabilizei-tools-production` para forçar uma com `gcloud run services update`. Em dev, teste a folha com no máximo 2 ou 3 colaboradores.

## Pré-requisitos

- `gcloud` autenticado, com permissão para:
  - publicar em Pub/Sub em `contabilizei-experts-dev`;
  - ler o Cloud Logging;
  - ler o bucket `ctbz-email-service-dev-storage`.
- O proxy do banco `sql_atendimento_dev` de pé, com o serviço `dev_atendimento_canais_email_service` no `~/.pg_service.conf`.
- `pdftotext` instalado. O `google-chrome` é opcional e só serve para gerar o print do e-mail.
- O deploy da branch em dev, feito pelo job `deploy-dev` da pipeline.

## Como rodar

```sh
python3 ~/ctbz-vault/obsidian/repositories/experts-functions/scripts/e2e_holerite_dev.py --to seu.email@contabilizei.com.br
```

As evidências ficam em `e2e-out/<run>/`: o payload, os PDFs, `email.html`, `email.png` e `report.md`. O processo sai com código 1 se algum passo falhar.

Saída: as evidências ficam em `e2e-out/<run>/` no diretório em que o script roda. Usar `--out` apontando para o scratchpad ou para `/tmp`.

Relacionado: [[templates-mandrill-holerite-e-guias]], [[migrar-template-do-mandrill]], [[smtp-dev-hubspot-dominio]], [[PRD-178571]].

## Execuções

- **2026-11-24, run `20261124134723`: 17/17 OK.**
  - Versão: branch `feat/PRD-178571` (imagem `experts-functions:0.1.20-5ddb53e5-dev`, revisão `function-email-holerites-00010-zzj`), subida pela pipeline 3108775736 com `DEPLOY=true` e `DEPLOY_FROM_MR=false`.
  - O `context` falha com "Utilize DEPLOY_FROM_MR ou deploys isolados" se só passar `DEPLOY=true`, porque o `DEPLOY_FROM_MR=true` vem de variável herdada.
  - `service-account-dev` e `deploy-dev` são manuais nessa pipeline.
  - Resultado: emailId `23460480395007272`, dois PDFs corretos (o colaborador só com `BASE_CALCULO` ficou de fora), `FAILED` pelo 421 conhecido da HubSpot de dev e nenhum envio para a folha sem colaborador válido.
  - Evidências no comentário da PRD-178575.
- **2026-11-24, subscription própria e DLQ, PRD-178827**:
  - Caminho feliz 17/17 (run `20261124192741`).
  - DLQ OK nas 3 runs (40, 12 e 4 colaboradores): 10 tentativas cada, de 8 a 10 minutos até a DLQ, sem envio.
  - Requisições de 47,6 s, 19,8 s e 23,2 s sem nenhuma reentrega simultânea.
  - Ficou pendente o envio com sucesso acima de 10 s, por causa do OOM do `html-to-pdf` de dev.
  - Evidências no comentário da PRD-178827.
