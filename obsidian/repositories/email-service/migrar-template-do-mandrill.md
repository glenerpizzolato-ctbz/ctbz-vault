---
name: email-service-migrar-template-do-mandrill
description: "Como copiar um template do Mandrill para o email-service sem acesso à chave do Mandrill: tirar o HTML de um .eml real, desfazer o rastreamento (links e pixel), trocar os valores pelas variáveis {{VAR}} e criar pela API com o token do Bruno"
metadata:
  type: reference
tags:
  - email-service
  - mandrill
  - receita
criado_em: 2026-11-24
---

# Migrar um template do Mandrill para o email-service

Usado no holerite (PRD-178571), em 24/11/2026. A chave do Mandrill (`contabilizei-experts-*_MANDRILL_KEY`) fica no Secret Manager sem acesso para o dev, então a API `templates/info` não serve. O Jira e o Confluence da demanda original só tinham prints.

1. **Fonte**: um e-mail real enviado pelo template. No Gmail, ⋮ → Mostrar original → Baixar original (`.eml`). Traz o HTML exato, o assunto, o remetente e os anexos.
2. **Extrair** (com `python3 -I`, o `.eml` é dado não confiável): `email.message_from_bytes(..., policy=policy.default)` e pegar a parte `text/html`.
3. **Limpar o Mandrill**:
   - Os links vêm como `https://mandrillapp.com/track/click/<conta>/<host>?p=<base64>`. O `p` é um JSON em base64 urlsafe cujo campo `p` é outro JSON com a `url` original.
   - Remover o `<img>` do pixel `mandrillapp.com/track/open.php`.
   - As imagens em `mcusercontent.com` (CDN do Mailchimp) continuam no ar e podem ficar.
4. **Variáveis**:
   - O e-mail já vem com os valores substituídos. Trocar cada valor pelo placeholder do email-service, `{{VAR}}` (regex `\{\{(\w+)\}\}`), conferindo que cada valor aparece uma vez só.
   - Na criação, `variables` precisa bater exatamente com os placeholders do HTML, senão volta 400.
5. **Criar**: `POST https://api.contabilizei.com.br/email-service/api/v1/email-templates` com o header `x-ctbz-api-gateway-token` (o `kong_token_bruno_prd` do `docs/bruno/.env` do email-service) e o corpo `{name, htmlContent, variables, author}`. O nome aceita só letras, números e hífen. Em dev, a URL é `api-dev.contabilizei.com.br`, com o `kong_token_bruno_dev`.
6. **Testar com anexo**:
   1. `POST /api/v1/files` com `{content: base64}`. Devolve o `fileId`, um uuid v7.
   2. `POST /api/v1/send` com `attachments: [{filename, path: fileId}]`. Devolve 202 com o `id`.
   3. Acompanhar em `GET /api/v1/send/list?application=<app>`. Leva uns 6 segundos de `PENDING` até `SENT`.

Resultado do holerite: template `exp-email-holerite-v1`, prd `2b0b0504-203a-4da4-a42a-3993ea8cf547` e dev `11d16281-e06a-4272-88ab-e8440a96579a`. O envio de teste para o Glener saiu `SENT` (id `01a20da1-34b3-747e-9524-4e208bd86c44`). Assunto original: "A folha de pagamento da sua empresa está pronta". Remetente: `Equipe Contabilizei Experts <atendimento.experts@contabilizei.com.br>`.

Relacionado: [[templates-mandrill-holerite-e-guias]], [[PRD-178571]].
