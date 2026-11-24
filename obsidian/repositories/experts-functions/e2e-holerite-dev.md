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
