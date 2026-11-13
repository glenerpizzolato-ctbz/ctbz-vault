---
name: mensagem-ativa-indice
description: "Índice da pasta mensagem-ativa: como o WhatsApp ativo (templates disparados pelo atendimento-zendesk) é enviado, validado e tratado pelos bots da Ultimate quando o cliente responde"
metadata:
  type: reference
tags:
  - mensagem-ativa
  - whatsapp-ativo
---

# Mensagem ativa (WhatsApp ativo)

Conteúdo transversal sobre o ativo: envio e validação no `atendimento-zendesk`, números/integrações e o que os bots da Ultimate fazem com o retorno do cliente. Notas específicas de código continuam na pasta do repositório e são linkadas daqui.

- [[retorno-ativo-plano-sem-whatsapp]] — cliente de plano sem WhatsApp (Básico) que responde a um ativo: o bot consulta o ativo antes da checagem de plano e encaminha (main com "Responder mensagem", fina + avisos direto para IA/humano)
- [[whatsapp-ativo-validacao-telefone-x-empresa]] — o envio não confere se o telefone de destino pertence ao CNPJ
- [[whatsapp-ativo-fora-do-horario-comercial]] — envio fora do horário comercial
- [[whatsapp-ativo-telefone-internacional]] — telefone internacional no ativo
- [[teste-evento-hubspot-whatsapp-ativo]] — teste do evento HubSpot do ativo
