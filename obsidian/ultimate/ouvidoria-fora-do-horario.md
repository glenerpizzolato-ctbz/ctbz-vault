---
name: ouvidoria-fora-do-horario
description: "Bot da Super Ouvidoria ([prod] ctbz wpp ouvidoria, número (41) 4141-0099) fora do expediente: sem menu, mensagem de fora do horário (seg a sex 9h–18h, exceto feriados), tag sys_ouvidoria_fora_de_horario e ticket direto em Ouvidoria [WhatsApp] [Ouvidoria], sem Corujão nem IA; humano responde no próximo dia útil"
metadata:
  type: reference
tags:
  - ultimate
  - ouvidoria
  - horario
---

# Super Ouvidoria fora do expediente

Levantado em 2026-11-24 pelos dados, sem ler o dialogue builder: tabela `tickets` do `prd_crm_atendimento_zendesk`, integração do número da Ouvidoria `6825e5a4fae003c31efe9eb2`, tickets de 29/10 a 24/11/2026 (desde o deploy do menu de desidratação, [[PRD-173035]]).

## Comportamento

- **Expediente**: segunda a sexta, das 9h às 18h, exceto feriados (texto do bot; o feriado de 02/11 saiu como fora do horário). Os tickets sem a tag vão de 09:02 a 17:46 em dia útil.
- **Fora do expediente**: o bot **não mostra o menu** (Quero atendimento / Fazer reclamação / Outro assunto). À primeira mensagem ele responde "Olá, no momento estamos fora do horário de atendimento do nosso time, que ocorre segunda à sexta das 09h às 18h, exceto em feriados. Peço que aguarde e assim que possível iremos retornar neste número.", grava `sys_ouvidoria_fora_de_horario` (mais `sys_grupo_bot_ouvidoria` e `sys_novo_ouvidoria`) e abre o ticket **em `Ouvidoria [WhatsApp] [Ouvidoria]` (`20122706111516`)**, sem atendente.
- **Não vai para o Corujão** (que é só Experts, ver [[corujao-fila-noturna-experts]]) **nem para IA**. O cliente fica na fila da Ouvidoria até o próximo dia útil. Exemplo: ticket 30416745, mensagem às 21:52 de 23/11 e o atendente respondeu às 09:59 de 24/11, pedindo desculpas pela demora.
- A `sys_encerramento_ia` que aparece em alguns desses tickets é o encerramento automático por IA, não atendimento por IA.
- Números do período: 206 tickets em dia útil das 9h às 18h, todos em `Ouvidoria [WhatsApp] [Ouvidoria]` (mais 1 em `Ouvidoria [WhatsApp] [BP] [Experts]`); 58 em dia útil fora do horário (de 05:53 a 21:53) e 7 no fim de semana, todos em `Ouvidoria [WhatsApp] [Ouvidoria]`.

## Consequência

Fora do horário não há desidratação: quem seria mandado aos canais oficiais pelo menu ("Quero atendimento" / "Outro assunto") vira ticket na fila da Ouvidoria. O roteador de horário (`Wpp Ouvidoria | Hours Router v02`) roda antes do menu. Para confirmar nó a nó, ler o reply no dashboard ([[dashboard-read-api]], com aprovação do usuário).

## Como reproduzir a consulta

```sql
select case when extract(dow from created_at at time zone 'America/Sao_Paulo') in (0,6) then 'fds' else 'util' end d,
       'sys_ouvidoria_fora_de_horario' = any(tags) fora, group_name, count(*)
from tickets where id > 30100000 and integration_id = '6825e5a4fae003c31efe9eb2' group by 1,2,3;
```

Filtrar sempre por `id` (chave): filtros só por `created_at` ou por tags dão timeout.

As demais origens da Ouvidoria (WhatsApp principal, chat web, sentinela, e-mail) e o que cada uma faz fora do horário: [[ouvidoria-origens-fora-do-horario]].
