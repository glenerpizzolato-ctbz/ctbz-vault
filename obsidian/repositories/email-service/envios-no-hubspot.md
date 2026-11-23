---
name: email-service-envios-no-hubspot
description: "Como os e-mails do email-service aparecem (ou não) na HubSpot: só SMTP API, sem tag/header/evento; um token SMTP para todos os apps; portal do token (47852359) diferente do portal dos tokens de API que temos (21138480); onde o time da HubSpot deve procurar"
metadata:
  type: reference
tags:
  - email-service
  - hubspot
  - smtp
analisado_em: 2026-11-23
---

# Envios do email-service na HubSpot

Levantamento de 2026-11-23, motivado pela reclamação de que os envios do e-mail de guia avulsa (template `d8d1c1cb-4c1e-4e62-ba9c-217817d6e33e`, `exp-email-guia-imposto-avulsa-v1`, app `experts-service`) não aparecem na HubSpot. Ver também [[templates-mandrill-holerite-e-guias]].

## Como o envio chega à HubSpot

- O email-service só usa a **API SMTP transacional** da HubSpot (`src/infra/smtp/hubspot-smtp.ts`, nodemailer em `smtp.hubapi.com:465`, credenciais `HUBSPOT_STMP_LOGIN`/`HUBSPOT_STMP_PASSWORD`). O HTML é montado no próprio serviço a partir de `email_templates`.
- **Não vai nada que identifique o template na HubSpot**: nem header `X-HubSpot-*`, nem tag, nem nome do template, nem evento customizado. Só `from`, `to`, `subject`, `html` e anexos.
- Todos os apps usam a mesma credencial SMTP, então na HubSpot tudo cai sob o mesmo token SMTP (o "campaign name" dele). Em 30 dias até 23/11/2026: `microsservico-agrupamento-guias` (~25 mil, vários templates de agrupamento), `experts-service` (8.962, guia avulsa), `super-app` (OTP). O que distingue a guia avulsa lá dentro é o **assunto** "Sua empresa tem uma nova guia de imposto disponível".
- A guia avulsa não tem anexo (`attachments: []` no experts-service; nenhum dos ~19 mil envios em prd tem anexo).
- Remetente: `Equipe Contabilizei Experts <atendimento.experts@…>`; o domínio é trocado pelo `CTBZ_EMAIL_DOMAIN` do `buildFrom`. O `messageId` que a HubSpot devolve nos logs de prd termina em `@contabilizei.com.br`, sinal de que em prd o domínio é `contabilizei.com.br` (que tem DKIM para os portais 47852359 e 21138480), e não `ctbz.com.br`.

## Evidências de que os envios saem

- `email_replications` (`prd_atendimento_canais_email_service`): 18.952 envios do template com o assunto da guia, status `SENT` (aceito pelo SMTP da HubSpot), de 18/09 a 23/11/2026; 8 `PENDING` em novembro.
- Log do container `email-service` (projeto `contabilizei-prod-01`, namespace `atendimento-canais-prd`): `Email sent successfully via SMTP` com `emailId` e `messageId`, por exemplo às 13:20 de 23/11/2026.

## Portais HubSpot (armadilha)

- **21138480**: portal dos tokens que temos em `experts-bruno/hubspot/.env` (`hubspot_token_prod` e `hubspot_token_sandbox` apontam os dois para ele, conferido em `/account-info/v3/details`). Tem os contatos (CRM/marketing) e eventos `pe21138480_*` (ex: `cnpj_ativado`).
- **47852359**: número do login SMTP de prd Eventos customizados com prefixo `pe47852359_` voltam "Invalid event type" na API do 21138480, ou seja, são portais diferentes.
- **48394222**: único portal com DKIM em `ctbz.com.br`.
- Nos contatos dos destinatários de 23/11/2026 no portal **21138480**, `hs_email_last_send_date` não registra o envio do dia: o e-mail não fica registrado nesse portal. Se o time procura lá, não vai achar.
- Os tokens que temos não têm os escopos `transactional-email` (listar tokens SMTP) nem `marketing.email.read` (eventos de e-mail). Não há token nosso para o portal 47852359.

## Onde procurar na HubSpot (para quem tem acesso ao portal do token SMTP)

1. Entrar no portal do token SMTP (Hub ID 47852359, conferir no menu da conta, canto superior direito).
2. Engrenagem (Configurações) > Marketing > E-mail > aba **SMTP**: passar o mouse no token > Ações > **Ver detalhes** mostra o desempenho de todos os envios do token (enviados, entregues, aberturas, cliques, bounces). Ali aparece também o "campaign name" do token e se ele cria contatos.
3. Contato: buscar o destinatário pelo e-mail nesse portal e olhar a linha do tempo de atividades. Só aparece se o token foi criado com "Criar contatos automaticamente para os destinatários"; a doc da HubSpot não garante o registro na linha do tempo para SMTP.
4. Para separar a guia avulsa dos outros envios do mesmo token: filtrar pelo assunto. A HubSpot não guarda o HTML enviado.

## Se quiserem rastrear por template na HubSpot

Opções de evolução, não implementadas: um token SMTP por aplicação/fluxo (o "campaign name" vira o identificador), ou publicar um evento customizado de e-mail pelo `hubspot-proxy`.
