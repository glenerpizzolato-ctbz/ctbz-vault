---
name: ouvidoria-origens-fora-do-horario
description: "Todas as origens que levam um ticket às filas de Ouvidoria (número exclusivo, Super-Ouvidoria do sentinela no WhatsApp principal/Avisos/chat web, botão Reclamação/Elogio do chat, Feedback Experts, inativos, Bank, macro manual, e-mail/Reclame Aqui) e o que acontece com cada uma fora do expediente (seg a sex 9h–18h)"
metadata:
  type: reference
tags:
  - ultimate
  - ouvidoria
  - horario
  - sentinela-atendimento
---

# Origens da Ouvidoria e o comportamento fora do expediente

Levantado em 2026-11-24 pela tabela `tickets` do `prd_crm_atendimento_zendesk` (tickets com `id > 30100000`, criados de 29/10 a 24/11/2026, cujo grupo atual tem "Ouvidoria" no nome), cruzada com as tags de cada caminho e com o código do `sentinela-atendimento` (`6c09351`, 11/11/2026). "Fora do horário" = antes das 9h ou a partir das 18h em dia útil, fim de semana e feriado. O horário considerado é o de **criação** do ticket, não o da transferência.

Versão visual em PDF (mapa dentro x fora do horário, conclusões, grupos e onde acontece cada drop: bot/reply da Ultimate, arquivo do sentinela/widget, integração, regra de horário, grupo e tags): `~/Downloads/ouvidoria-origens-fora-do-horario.pdf`, gerado com Chrome headless a partir de `~/Downloads/ouvidoria-origens-fora-do-horario.html`.

IDs dos grupos: Ouvidoria [WhatsApp] [Ouvidoria] `20122706111516`, Ouvidoria [WhatsApp] [BP] [Experts] `14918792967068`, Ouvidoria [Chat] [BP] `14918795937052`, CS - Ouvidoria `360000072159`, AIDA Geral 24/7 [Chat] [BP] `23609820337948`, AIDA Geral 24/7 [WhatsApp] [BP] `23609834550556`, Contabilizei Bank [Chat] [Bank] `14918551005980`.

## Tabela

| # | Origem | Como chega na Ouvidoria | Fila destino | Fora do horário | Volume no período (horário / fora) |
| --- | --- | --- | --- | --- | --- |
| 1 | **Número exclusivo da Ouvidoria** (41) 4141-0099, bot `[prod] ctbz wpp ouvidoria` (inclui retorno do ativo `ouvidoria_geral`) | Menu de desidratação ([[PRD-173035]]): "Fazer reclamação" e cliente não identificado transbordam; "Quero atendimento"/"Outro assunto" indicam o canal oficial | `Ouvidoria [WhatsApp] [Ouvidoria]` | **Sem menu**: mensagem de fora do horário, tag `sys_ouvidoria_fora_de_horario` e ticket direto na fila, sem IA nem Corujão; humano responde no próximo dia útil. Vale para feriado. Ver [[ouvidoria-fora-do-horario]] | 216 / 58 (7 de retorno de ativo, 7 no fds) |
| 2 | **Super-Ouvidoria (sentinela) no WhatsApp principal** (41) 4101-0021 | Cliente da lista da Super-Ouvidoria, ticket com IA/bot (não com humano) e mensagem classificada num tema que casa com o motivo dele → transferência automática pela API (`sys_super_ouvidoria_transferido`) | `Ouvidoria [WhatsApp] [BP] [Experts]` | **Não transfere**: o `TransferDecisionService` checa o horário de operação (`sentinela_app_settings/sentinela_operating_hours`, 9h–18h, `outside_operating_hours`). O cliente segue com a AIDA/fila em que está; a regra é reavaliada a cada nova mensagem classificada e transfere quando cair no horário. **Não trata feriado** (só dia da semana) | 228 / 10 (os de "fora" foram criados de madrugada/7h–8h e transferidos depois das 9h) |
| 3 | **Super-Ouvidoria no WhatsApp Avisos** (41) 9813-0400 | Igual à 2 | `Ouvidoria [WhatsApp] [BP] [Experts]` | Igual à 2 | 22 / 0 |
| 4 | **Super-Ouvidoria no chat web** (widget) | Igual à 2 | `Ouvidoria [WhatsApp] [BP] [Experts]` (2 em `Ouvidoria [Chat] [BP]`) | Igual à 2 | 57 / 3 |
| 5 | **Chat web, botão "Reclamação/Elogio"** (fluxo Contabilidade, cliente elegível pela `elegivel-auditoria`) | Tags `sys_grupo_ouvidoria`/`sys_tema_ouvidoria` nas `conversationTags` (ver [[widget-tags-roteamento-ouvidoria]]) | `Ouvidoria [Chat] [BP]` | **Das 18h em diante e no fds vai para a IA** (`AIDA Geral 24/7 [Chat] [BP]`: 35 de 35 nos dias úteis após 18h, 9 de 9 no fds). Antes das 9h ainda caiu na Ouvidoria (6 entre 7h e 9h, 1 à 1h): a janela do chat parece começar antes das 9h | 32 / 7 na Ouvidoria (+48 fora do horário na IA) |
| 6 | **WhatsApp principal, Experts → Feedback** (`Wpp Exp \| Feedback Business Hour v03`) | Reclamação/elogio/sugestão/troca de assessor (`sys_*_ouvidoria_exp`) | `Ouvidoria [WhatsApp] [BP] [Experts]` | **Nenhum caso fora do horário**, em nenhuma fila: o diálogo é o de "Business Hour", então fora do horário o Experts não chega a esse menu (vai para o fluxo noturno, ver [[corujao-fila-noturna-experts]]). A confirmar no dialogue builder | 17 / 0 |
| 7 | **WhatsApp principal, clientes inativos → "Fazer reclamação"** ([[PRD-173036]]) | Tags `metric_inat_*_outro_reclamacao` | `Ouvidoria [WhatsApp] [BP] [Experts]` | **Nenhum caso fora do horário**: 52 tickets do fluxo de inativos fora do horário, todos para AIDA ou filas operacionais, nenhum com "Fazer reclamação". Volume baixo para concluir (1,9% escolhem reclamação no horário): a confirmar no dialogue builder | 25 / 0 |
| 8 | **WhatsApp principal, Conta PJ (Bank) → "Reclamação/Elogio"** (tema 762) | Roteamento por tema do atendimento-zendesk devolve `sys_grupo_bot_ouvidoria` (ver [[tags-ouvidoria-whatsapp-ultimate]]) | `Ouvidoria [WhatsApp] [Ouvidoria]` | **Vai para a IA**: os 4 casos fora do horário foram 3 para `AIDA Geral 24/7 [Chat] [BP]` e 1 para `Contabilizei Bank [Chat] [Bank]` | 4 / 0 na Ouvidoria |
| 9 | **Transferência manual pelo atendente** (macro com `ticket_transbordado_para_off_ouvidoria`, ou troca de grupo), no WhatsApp principal, Financeiro (11) 5026-5417 e chat | Atendente transfere o ticket | `Ouvidoria [WhatsApp] [BP] [Experts]` (alguns em `[Ouvidoria]`/`[Chat] [BP]`) | Depende de haver atendente: fora do horário quase não ocorre (1 caso às 19:34). Fica na fila até o próximo dia útil | ~60 / 4 |
| 10 | **Canais assíncronos**: e-mail `ouvidoria@`, Reclame Aqui (Droz, `Serviço Web`), formulário web/Typeform, conversa paralela e follow-up de ticket fechado | Criação direta do ticket | `CS - Ouvidoria` | **Sem regra de horário**: o ticket entra na fila a qualquer hora e é tratado no próximo dia útil (é assíncrono por natureza) | ~730 / ~320 |

## Conclusões

- Só o **número exclusivo** (1) e os **canais assíncronos** (10) deixam o cliente esperando a Ouvidoria fora do horário; o número avisa o cliente, o assíncrono não precisa.
- Nos canais com bot (chat web e WhatsApp principal), fora do horário a reclamação vai para a **IA (AIDA 24/7)** ou não chega ao menu de Ouvidoria. A Super-Ouvidoria do sentinela segura a transferência até as 9h.
- Pontos de atenção: o sentinela **não trata feriado** (transfere num feriado em dia útil, com a fila sem time); o botão do chat leva à fila da Ouvidoria **entre 7h e 9h** e de madrugada, sem aviso de fora do horário.
- Para fechar 6 e 7 com certeza, ler os replies do `[prod] ctbz wpp main` pelo dashboard ([[dashboard-read-api]], com aprovação). O mesmo vale para o `[prod] ctbz chat main` (5), para achar a janela do roteador de horário.

## Como reproduzir

Classificação por origem (filtrar sempre por `id`, senão dá timeout):

```sql
select case
  when integration_id='6825e5a4fae003c31efe9eb2' then 'numero ouvidoria'
  when 'sys_super_ouvidoria_transferido' = any(tags) then 'sentinela '||integration_id
  when tags && array['metric_inat_inad_outro_reclamacao','metric_inat_canc_outro_reclamacao','metric_inat_baixa_outro_reclamacao'] then 'inativos'
  when tags && array['sys_reclamacao_ouvidoria_exp','sys_elogio_ouvidoria_exp','sys_sugestao_ouvidoria_exp','sys_trocaasessor_ouvidoria_exp'] then 'experts feedback'
  when 'sys_grupo_bot_ouvidoria' = any(tags) then 'bank'
  when tags && array['sys_grupo_ouvidoria','sys_tema_ouvidoria'] then 'chat botao'
  else coalesce(integration_id, via) end origem,
  case when extract(isodow from created_at at time zone 'America/Sao_Paulo')>5 then 'fds'
       when extract(hour from created_at at time zone 'America/Sao_Paulo') between 9 and 17 then 'horario' else 'fora' end janela,
  group_name, count(*)
from tickets where id > 30100000 and group_name ilike '%ouvidoria%' group by 1,2,3;
```

Para ver para onde um caminho vai fora do horário, trocar o filtro de grupo pelas tags do caminho e agrupar pelo `group_name`.

Integrações: `66214c2bd6c1a9194bf900ed` WhatsApp principal (41) 4101-0021, `663132c8d9cb85278bfda6df` Avisos (41) 9813-0400, `6a4fd34d1b972688c659346c` Financeiro (11) 5026-5417, `5d66b9d108eb4e0010c2a542` Mitigação (41) 9972-0167, `6825e5a4fae003c31efe9eb2` Ouvidoria (41) 4141-0099, `66ab8fcdaed5868f72d0acbf` chat web (Native Messaging). O número sai da tag `businessphone:` do ticket.
