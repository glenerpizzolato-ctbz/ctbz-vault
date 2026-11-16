---
name: smtp-dev-hubspot-dominio
description: "Por que o email-service de dev não entrega: o portal HubSpot da credencial SMTP de dev (51348990) não tem ctbz.com.br conectado como domínio de envio (421 no DATA)"
metadata:
  type: project
tags:
  - email-service
  - hubspot
  - smtp
---

# SMTP de dev recusado pela HubSpot (421 connected email sending domain)

Diagnóstico de 2026-11-16 (work-item #54).

- **Sintoma**: todo envio em dev falha com `421 The from domain should be a connected email sending domain … - hssmtp`, classificado como `REJECTED` (permanente, sem retry). Logs: projeto `contabilizei-dev-01`, namespace `atendimento-canais-dev`, container `email-service`.
- **Linha do tempo (banco `dev_atendimento_canais_email_service`, tabela `email_replications`)**: último `SENT` em 2026-05-28, primeiro `FAILED` em 2026-08-20, com o mesmo remetente (`Equipe Contabilizei Experts <atendimento.experts@…>`, reescrito para `@ctbz.com.br` pelo `buildFrom`). Entre essas datas o único commit foi o bump do zezu-core 0.12 → 0.13.1; a lógica de domínio (`CTBZ_EMAIL_DOMAIN`, recorte do prefixo) é de março. Ou seja, **não foi mudança de código**.
- **Reprodução local** com a credencial DEV do `.env` (`…@51348990.smtp.hubspot.net`): `AUTH` ok, `MAIL FROM`/`RCPT TO` ok, e o 421 vem só no comando `DATA` (a HubSpot valida o cabeçalho `From` do corpo). Credencial válida, o problema é o domínio no portal.
- **DNS**: os CNAMEs de DKIM da HubSpot são por portal (`hs1-<id>._domainkey.<domínio>`). `ctbz.com.br` só tem DKIM para o portal `48394222` (e o SPF inclui `48394222.spf08.hubspotemail.net`); não há registro para `51348990` (dev) nem para `47852359` (número do login SMTP de prd). `contabilizei.com.br` tem DKIM para `47852359` e `21138480`. Prd envia normalmente com `ctbz.com.br`.
- **Conclusão**: o portal HubSpot de dev (51348990) não tem `ctbz.com.br` conectado/verificado como domínio de envio (ou perdeu a conexão entre jun e ago/2026). Pedido ao time dono da HubSpot: conectar `ctbz.com.br` (ou outro domínio de teste) no portal 51348990 e publicar os CNAMEs de DKIM que a HubSpot gerar, ou informar quais domínios já estão conectados nele para apontar o `CTBZ_EMAIL_DOMAIN` de dev.
- Pendente: confirmar no secret do deployment de dev (cluster privado, precisa de VPN) que o login é o mesmo do `.env` local.
