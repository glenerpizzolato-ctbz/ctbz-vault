---
name: whatsapp-ativo-telefone-internacional
description: "WhatsApp ativo não é enviado para número internacional: a validação aceita qualquer DDI, mas no envio à Sunshine o destino passa por formatarTelefoneBrasileiro, que devolve null para número não-BR (só BSUID escapa)"
metadata:
  type: reference
tags:
  - atendimento-zendesk
  - whatsapp-ativo
  - telefone-internacional
sistemas:
  - atendimento-zendesk
  - zendeskapp-whatsapp-ativo
---

# WhatsApp ativo e telefone internacional

Conferido no `origin/master` em 2026-11-13.

- **Validação de entrada** (`TelefoneUtil.validarTelefone` = `isValidPhoneNumber` do libphonenumber): aceita número de qualquer país, desde que venha com `+DDI`. Usada no `ValidarWhatsappAtivoService.validarTelefone` (lança `TelefoneInvalidoException` / `TELEFONE_INVALIDO`) e no `RowValidatorService` do massivo (CSV). Sem `+`, o `TelefoneUtil.formatar` assume `BR`.
- **Envio de fato** (`EnviarAtivoService.enviarNotificacaoWhatsapp`, `src/domain/whatsapp-ativo/messaging/services/enviar-ativo/enviar-ativo.service.ts`): faz `destinationId = TelefoneUtil.formatarTelefoneBrasileiro(destinationId)`, que retorna `null` quando `parsed.country !== 'BR'` (há teste: "deve retornar null caso o telefone seja internacional"). Só BSUID passa direto. Resultado: o ativo para número internacional passa na validação, mas o POST de notificação vai com `destinationId: null` e falha na Sunshine, em vez de ser barrado com erro claro.
- **Front** (`zendeskapp-whatsapp-ativo`): o massivo mostra `TELEFONE_INVALIDO` como "O Telefone fornecido ou é inválido ou é um número internacional" (texto herdado; hoje o back só barra inválido). O individual ganhou seletor de país (DDI via libphonenumber, `country-codes.ts`), mas o envio continua preso ao BR pelo ponto acima.
- Contexto: a stack modela telefone como Brasil (ACR PRD-162752); o cadastro de telefone internacional é o PRC [[PRD-172999 - Cadastro de telefone internacional]].
