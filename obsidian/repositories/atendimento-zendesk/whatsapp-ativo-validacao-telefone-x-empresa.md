---
name: whatsapp-ativo-validacao-telefone-x-empresa
description: "O WhatsApp ativo não confere se o telefone de destino pertence à empresa (CNPJ) do envio: telefone e empresa são validados separadamente; só o link ativo usa um telefone do próprio cadastro"
metadata:
  type: reference
tags:
  - atendimento-zendesk
  - whatsapp-ativo
  - validacao
sistemas:
  - atendimento-zendesk
  - plataforma-crm-web
---

# WhatsApp ativo: telefone x empresa

Conferido no `origin/master` (95587b09f) em 2026-11-13. **Não há validação de que o `destino` pertence ao `cnpj`** em nenhum caminho do ativo.

- **Ativo individual/tópico** (`ValidarWhatsappAtivoService.validar`, `src/domain/whatsapp-ativo/messaging/services/validar-whatsapp-ativo/validar-whatsapp-ativo.service.ts`): o telefone só passa pelo formato (`TelefoneUtil.validarTelefone`, libphonenumber, ou BSUID). O CNPJ, se vier, busca os dados no plataforma-crm-web (`DadosClienteWhatsappAtivoService.buscar`) e o `validarDadosClienteWhatsappAtivo` barra empresa não encontrada, inativa (exceto Expert) e plano inelegível (Básico só autopilot/comércio), além do dia útil. A resposta traz `listaTelefones`, mas ela não é comparada com o `destino`. Sem `cnpj` (ou categoria `ATIVACAO_MIGRACAO`), nem a empresa é validada.
- **Massivo** (`RowValidatorService`): só formato do telefone, dígito do CNPJ (ou `processoAberturaId`) e variáveis do template, por linha.
- **Link ativo** (`EnviarLinkAtivoService`): é o único que liga os dois, mas porque não recebe telefone: usa `dados.listaTelefones[0].numero` da empresa.
- No app do Zendesk (`zendeskapp-whatsapp-ativo`, individual), a `listaTelefones` vem do back (`zendeskapps/whatsapp-ativo/individual`) para o agente escolher, mas o back não confere no envio se o número escolhido está nela (o front não foi conferido).
- O que o bot faz com o retorno do ativo (e por que o plano não é checado nele): [[retorno-ativo-plano-sem-whatsapp]].
- Para checar manualmente o vínculo, a rota `buscar-por-telefone-e-cnpj` da plataforma-crm-web (skill `autenticar-empresa-whatsapp`) é a que o bot usa.
