---
name: whatsapp-ativo-fora-do-horario-comercial
description: "O que acontece com um WhatsApp ativo com debounceToBusinessHour disparado fora do horário comercial (ex: agrupamento de guias no dia 15 em fim de semana): fica em retentativa até segunda 9h, mas a validade de 24h conta do criado_em e a resposta do cliente deixa de ser ligada ao ativo"
metadata:
  type: reference
tags:
  - atendimento-zendesk
  - whatsapp-ativo
  - microsservico-agrupamento-guias
sistemas:
  - atendimento-zendesk
  - microsservico-agrupamento-guias
atualizado_em: 2026-11-11
---

# WhatsApp ativo fora do horário comercial (debounceToBusinessHour)

## Como funciona

- Com `debounceToBusinessHour = true`, o `EnviarAtivoService.executar` chama `ValidarWhatsappAtivoService.validarDebounceToBusinessHour`, que barra sábado e domingo (`validarDiaUtil`) e fora das 9h às 18h59 de São Paulo (`validarHorarioEnvioPermitido`). Feriado não é considerado.
- A barreira lança `HorarioInvalidoException`, que **não** está em `validationErrors`: a mensagem sofre nack e volta pelo Pub/Sub. A subscription `atendimento-zendesk.envio-whatsapp-ativo-sub` (projeto `contabilizei-crm`) tem backoff de 10s a 600s, retenção de 7 dias e nenhuma DLQ. Sem `retryLimit`, a retentativa não tem limite (só `ATIVACAO_MIGRACAO` tem teto padrão, 100). Assim a mensagem fica em `PROCESSANDO` até o próximo horário válido e sai a partir de segunda às 9h. Com volume grande, o semáforo espalha o envio por dias.
- A linha de `mensagem_ativa` é criada na **primeira** tentativa (`createOrAddRetry`); as retentativas só incrementam `retentativas`, sem mexer em `criado_em`.

## Armadilha: a resposta do cliente não é ligada ao ativo

`MensagemAtivaRepository.buscarMensagensAtivas` (bot, quando o cliente responde) só acha ativos com `criado_em + validade_em_minutos >= now()`. A validade padrão é 1440 min (24h) e o `microsservico-agrupamento-guias` não manda `validadeEmMinutos`. Num disparo de sábado ou domingo, a janela vence antes do envio de segunda, então a resposta do cliente não é reconhecida como resposta ao ativo: não vira `RESPONDIDA` e não é roteada pela fila/agente do ativo (`Assessores/Hubs [WHATSAPP]`).

Evidência (template `exp%empacot%`, banco `prd_crm_atendimento_zendesk`):

| dia 15 | dia | ativos | entregues | RESPONDIDA |
| --- | --- | --- | --- | --- |
| 2026-07-15 | qua | 19170 | 16793 | 4046 |
| 2026-08-15 | **sáb** | 21455 | 18906 | **2** |
| 2026-09-15 | ter | 20120 | 17151 | 3996 |
| 2026-10-15 | qui | 20342 | 18325 | 4286 |

Em 2026-08-15, todos os ativos foram criados no sábado entre 9h e 15h (crons de WhatsApp às 9h e às 15h do dia 15 ao 19), com média de 384 retentativas (máximo 1890), e saíram de 2026-08-17 9h até 08-20.

Correções possíveis: o agrupamento mandar `validadeEmMinutos` maior (ex: 4320, que cobre um fim de semana), o atendimento-zendesk contar a validade a partir do envio (`SOLICITADA`) em vez do `criado_em`, ou a cron do agrupamento pular fim de semana.

Aplicado (2026-11-11) no `agrupamento-guias-service`: o `EnvioWhatsappService` manda `validadeEmMinutos: 4320` (`VALIDADE_WHATSAPP_EM_MINUTOS`), branch `fix/whatsapp-validade-fim-de-semana`. O consumer do atendimento-zendesk já repassa o campo para a `mensagem_ativa` (`enviar-ativo.service.ts`), sem mudança lá. O `microsservico-agrupamento-guias` (Kotlin) ainda precisa da mesma correção enquanto for ele que dispara em prod.
