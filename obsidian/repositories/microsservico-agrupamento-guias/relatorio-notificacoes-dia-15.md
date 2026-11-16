---
name: relatorio-notificacoes-dia-15
description: "Relatório das notificações do agrupamento de guias em prod (rodada do dia 15): de onde vêm os números (grupo_guia, controle_notificacao, mensagem_ativa), regras de elegibilidade das crons, como ler cada status, quando rodar, armadilhas descobertas, migração para o agrupamento-guias-service e histórico de execuções da skill relatorio-notificacoes-agrupamento"
metadata:
  type: reference
tags:
  - microsservico-agrupamento-guias
  - agrupamento-guias-service
  - notificacao
  - relatorio
sistemas:
  - microsservico-agrupamento-guias
  - atendimento-zendesk
skill: relatorio-notificacoes-agrupamento
atualizado_em: 2026-11-16
---

# Relatório das notificações do dia 15

Executado pela skill `relatorio-notificacoes-agrupamento` (`~/ctbz-vault/skills/impostos/relatorio-notificacoes-agrupamento/`, script `relatorio.py`). Só leitura em prod. Responde, por segmento × canal: quantos deveriam receber, quantos receberam, o que está em trânsito, o que falta e quando a próxima cron roda.

## De onde vêm os números

- **Universo**: `grupo_guia` da competência (`periodo_apuracao` = mês anterior ao dia 15), banco `prd_atendimento_canais_ms_agrupamento_guias` (proxy `sql_atendimento_prd`, 5443).
- **Segmento** (igual às queries `buscarGruposGuiaElegiveisNotificacao*` do `GrupoGuiaRepository`, conferidas em 2026-11-16 no commit `25bb8ce9`): Experts = plano `EXPERT_ESSENCIAL`/`EXPERT_PRO` (**plano nulo não entra**); Experts LP = Experts + regime `LUCRO_PRESUMIDO`; Experts SN = Experts com regime nulo ou diferente de LP; BP LP = `BASICO`/`AVANCADO`/`PREMIUM`/`MULTIBENEFICIOS` + LP. WhatsApp BP LP exclui o `BASICO`. BP no Simples e plano nulo não têm notificação.
- **Elegível** = `status = 'SUCESSO_AGRUPAMENTO'` no segmento. A cron só pega quem não tem nenhum `controle_notificacao` do tipo (qualquer status), então `FALHA`, `DADOS_INCOMPLETO` e `BLOQUEADA_OPTOUT` nunca são renotificados pelas crons.
- **Status do controle**: último `controle_notificacao` do grupo por tipo (`EMAIL`/`WHATSAPP`). Valores: `SUCESSO`, `AGUARDANDO_NOTIFICACAO` (publicado, sem callback), `FALHA` (+ `motivo`), `DADOS_INCOMPLETO`, `BLOQUEADA_OPTOUT`. `created_at` é UTC sem fuso.
- **WhatsApp real**: `controle_notificacao.external_id` = `mensagem_ativa.id_message_broker` (banco `prd_crm_atendimento_zendesk`, proxy `sql_crm_prd`, 5444), filtrando `autor = 'microsservico-agrupamento-guias'`; status = último `mensagem_ativa_status` (`PROCESSANDO`, `SOLICITADA`, `ENVIADA`, `ENTREGUE`, `RESPONDIDA`, `ERRO`, `BLOQUEADA_OPTOUT`). O cruzamento é feito no script (bancos diferentes).

## Filtros

O relatório pode sair por público (`--publico exp|bp`), regime (`--regime simples|lp`), canal (`--canal email|wpp`), plano (`--plano`) e competência (`--competencia AAAAMM` ou `--data` do dia da rodada). O filtro de segmento e plano vai no SQL do `grupo_guia`; o de canal tira as consultas do canal que ficou de fora. Detalhes e exemplos no `SKILL.md`.

## Como ler

- **Concluído**: todos os elegíveis enviados (WhatsApp: entregue/respondido), sem falha nem contato faltando.
- **Em andamento**: há elegível sem notificação com cron ainda por rodar, ou mensagens em trânsito (e-mail aguardando callback, WhatsApp `PROCESSANDO`/`SOLICITADA`).
- **Concluído com perdas**: terminou, mas com falhas ou contato incompleto (até 2%).
- **Precisa de ação**: elegível sem notificação e sem cron restante (só disparo manual), falhas acima de 2% ou mais de 0,5% de WhatsApp com controle e sem registro no ativo (mensagem perdida entre o agrupamento e o atendimento-zendesk).
- `PROCESSANDO` em massa no fim de semana é esperado: o ativo só envia em dia útil das 9h às 19h ([[whatsapp-ativo-fora-do-horario-comercial]]) e espalha o envio pelo semáforo.
- Os alertas fixos também apontam `SUCESSO_AGRUPAMENTO_SEM_ARQUIVO_GUIA_AVULSA` (as crons não pegam) e `GUIAS_AGUARDANDO_GERACAO` (nunca reprocessado, ver PRC `PRD-174011`).

## Armadilhas descobertas (2026-11-16)

- O controle do agrupamento não é a verdade do WhatsApp: na competência 202609 ficaram **2.091** `AGUARDANDO_NOTIFICACAO` que nunca receberam callback. Por isso o relatório usa o status do `mensagem_ativa`.
- `DADOS_INCOMPLETO` não publica nada (sem `external_id`): não contar como "sem registro no ativo".
- **Uma foto só por cartão de WhatsApp.** Enquanto o ativo envia, os callbacks mudam o `controle_notificacao` de `AGUARDANDO_NOTIFICACAO` para `SUCESSO`/`FALHA` em segundos. Montar o cartão juntando a consulta da matriz com a do cruzamento dava soma diferente dos elegíveis; agora o cartão sai de uma consulta só, e cada elegível cai numa categoria só (uma `FALHA` de callback é `ERRO` no ativo, não duas falhas). `FALHA` com motivo `DADOS_INCOMPLETO` conta como sem contato.
- A busca no `mensagem_ativa` usa como início o primeiro `created_at` dos controles de WhatsApp da competência, porque testes manuais podem ter rodado dias antes do dia 15.

## Quando rodar

Ver a seção "Quando rodar" do `SKILL.md`: dia 15 ~10h30 e ~16h; se o dia 15 cair no fim de semana, no próximo dia útil ~11h e ~16h; fechamento no dia 19 depois das 16h.

## Migração para o agrupamento-guias-service

Em 2026-11-16 o `agrupamento-guias-service` ainda não está em prod (sem tópicos no catálogo de `atendimento-canais-prd`, sem banco no `.pg_service.conf`) e o microsservico não publica para ele. Quando assumir:

- Criar a conexão do banco dele no DBeaver/`.pg_service.conf` e trocar a leitura do status por `notifications_email`/`notifications_wpp` (`grouping_id`, `status`, `error_reason`, `external_id`, `template`, `plan`, `tax_regime`), mapeando `SUCCESS`→enviado, `PENDING`→em trânsito, `FAILED`→falha, `BLOCKED_OPTOUT`, `INCOMPLETE_DATA`→sem contato.
- `--autor agrupamento-guias-service` no cruzamento do WhatsApp.
- O universo e a elegibilidade continuam no `grupo_guia` do microsservico, que segue fazendo o agrupamento; quem publica o evento por segmento passa a decidir o "falta enviar" (o service não tem cron nem lote).
- BP Simples entra como segmento quando for implementado.

## Histórico de execuções

| Quando | Competência | Resultado | Artefato |
| --- | --- | --- | --- |
| 2026-11-16 09:09 | 202610 | Primeira execução publicada. E-mail: Exp SN 99,9% (2 a enviar na rodada das 12h), Exp LP 100% (1 sem contato), BP LP 100%. WhatsApp começando a sair às 9h depois do domingo: ~6,7% entregue, ~22,3 mil na fila do ativo, falhas de 1,2% a 1,7%, quase todas erro de entrega da Meta ("healthy ecosystem engagement" e número inalcançável, ver PRC `PRD-134632`). | https://claude.ai/artifact/8Hf8ipe1ZupmPm8nHhCPmy |
| 2026-11-16 09:06 | 202609 (filtro BP LP · WhatsApp) | Teste dos filtros. Resultado final da competência 09: 1.470 de 1.739 entregues (84,5%) e **234 falhas** (13,5%, quase todas erro no ativo), bem acima dos Experts: vale investigar os erros do WhatsApp BP. | — |
| 2026-11-16 09:00 | 202610 | Teste da skill (não publicado). Dia 15 caiu no domingo: e-mail ~100% nos 3 segmentos; WhatsApp ~24,2 mil em `PROCESSANDO` saindo a partir de segunda 9h; 22 `SEM_ARQUIVO_GUIA_AVULSA` e 560 `GUIAS_AGUARDANDO_GERACAO` fora da notificação. | — |
