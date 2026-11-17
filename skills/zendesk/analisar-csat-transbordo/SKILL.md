---
name: analisar-csat-transbordo
description: Analisa, para um ou N tickets do Zendesk, por que o CSAT Transbordo segurou ou não a pesquisa CSAT (segurar a pesquisa até o ticket off de acompanhamento/Jira ser resolvido) - monta o checklist das regras que o ticket passou e onde foi bloqueado, diz a causa concreta e gera uma planilha (CSV) com causa descoberta sim/não, código e texto da causa, mais um relatório em Markdown. Cobre os dois motores (experts-service até ~12/11/2026 e survey-service depois), lendo os logs do Cloud Logging e os bancos de prod só leitura (ticketing, experts_service, atendimento-zendesk), sem chamar a API de prod do Zendesk. Use quando o usuário perguntar por que a pesquisa CSAT saiu num atendimento transbordado, por que um ticket não transbordou, pedir para analisar tickets de um PRC de CSAT/transbordo ou levantar a causa em lote.
argument-hint: "<tickets: ids ou links do Zendesk> [freshness: 30d] [saida]"
---

# Analisar o CSAT Transbordo de tickets do Zendesk

O transbordo segura a pesquisa CSAT de um atendimento humano quando o pedido do cliente foi para um ticket off de acompanhamento (com Jira, em Experts, ou conversa paralela, em BPMP). A pesquisa (FUP) só sai quando o ticket off ou o Jira é resolvido. As regras completas estão no vault, em `csat/csat-transbordo-regras.md` (`~/ctbz-vault/obsidian/csat/`): ler a nota antes de interpretar um caso fora do comum.

O script `scripts/analisar_csat_transbordo.py` faz a análise toda:

1. Lê os logs de decisão do CSAT no projeto `contabilizei-prod-01`:
    - `experts-service` (namespace `experts-prd`, flow `csat-engine`): o motor legado, até o cutover de ~12/11/2026. Ele loga cada regra, inclusive cada Jira descartado e o motivo.
    - `survey-service` (namespace `atendimento-canais-prd`, job `csat.request`): o motor atual. Ele só loga o desfecho (`CSAT DISPATCHED|HELD|SKIPPED`, `CSAT ignorado: …`, `CSAT agendado/descartado`), então as regras do transbordo são reavaliadas pelo script com os dados dos bancos.
    - `zendesk-agents` (namespace `crm-prd`, "is closed or solved"): dá o horário do solved. O `survey-service` não loga o `enable_transbordo`, e o script o infere pelo atraso entre o solved e a decisão (com a flag, o job espera 10 min).
2. Consulta os bancos de prod, só leitura:
    - `prd_issue_ticketing` (`ticket_jira`): os Jiras do CNPJ, no estado atual.
    - `prd_experts_experts_service` (`survey_csat_sent`, `ticket_transbordo`): o que foi enviado e os transbordos. As linhas do `survey-service` são espelhadas aí, com `survey_service_id`.
    - `prd_crm_atendimento_zendesk` (`tickets`): o ticket pai e os tickets do CNPJ abertos depois dele (candidatos a ticket off, com via e grupo).
3. Classifica cada ticket com um código de causa e grava a planilha e o relatório.

## Como rodar

1. Subir os proxies que não estiverem de pé (conferir antes com `ss -ltn | grep -E ':544[457]'` e anotar quais já estavam): `zsh -ic '_sql_proxy_start_alias sql_issue_prd'` (5447), `sql_exp_prd` (5445) e `sql_crm_prd` (5444). Esperar as portas abrirem.
2. Rodar (aceita ids ou links, separados por espaço, ou um arquivo com `--file`):

    ```bash
    python3 -I ~/.claude/skills/analisar-csat-transbordo/scripts/analisar_csat_transbordo.py 30257371 30349105 [--file ids.txt] [--freshness 30d] [--out ~/Downloads/csat-transbordo.csv]
    ```

    - `--freshness` é a janela de logs (padrão `30d`, que é a retenção do bucket `_Default`). Uma janela menor deixa a consulta mais rápida: o tempo vai quase todo nas leituras do Cloud Logging (~2 min por lote de 15 tickets).
    - A saída é sempre em `~/Downloads`: `~/Downloads/csat-transbordo-<data>.csv`, com o relatório `.md` ao lado. Só passar `--out` se o usuário pedir outro lugar.
    - `--no-db` usa só os logs (sem reavaliar Jiras e tickets off).
3. Derrubar só os proxies que o passo 1 subiu: `zsh -ic '_sql_proxy_kill_alias sql_<dominio>_prd'`.
4. Confirmar as causas que dependem do histórico do Jira (ver abaixo) e responder ao usuário.

## Depois de rodar

- Mostrar o resumo que o script imprime (por ticket: motor, origem, CSAT enviado, transbordo segurou e a causa) e os caminhos da planilha e do relatório. Para um ticket só, resumir o checklist do `.md` (o que passou e onde bloqueou).
- **Confirmar no Jira o que mudou depois do motor.** O `ticket_jira` guarda só o estado atual. Nos códigos `DUE_DATE_PREENCHIDO_APOS_MOTOR`, `JIRA_ESTADO_MUDOU` e nos que dizem "o Jira mudou depois do motor", abrir o changelog com o MCP do Atlassian (`getJiraIssue`, `cloudId: contabilizeicontabilidade.atlassian.net`, `fields: ["duedate","status","created"]`, `expand: "changelog"`) e comparar o horário de cada mudança (`duedate`, `status`, `Demanda preventiva`) com o "motor decidiu". O `due_date` dos EXPBKO é preenchido pelo usuário "SVC - Experts" (automação de SLA, `[SLA] Retorno da automação` passa de `SEM_SLA` para `VIGENTE`), só depois que o BKO preenche o "Tipo de Solicitação".
- Se o ticket informado é a resposta do cliente à pesquisa (`TICKET_DE_RESPOSTA_CSAT`) ou o ticket off (`TICKET_OFF_DO_TRANSBORDO`), a causa do vazamento está no atendimento que o script aponta: incluí-lo na rodada se não estiver.
- Quando os tickets vierem de um PRC (atendimento, ticket off e resposta do mesmo caso), gerar um arquivo só daquele PRC (`--out ~/Downloads/csat-transbordo-<PRC>-<data>.csv`) e acrescentar no topo do `.md` uma seção "Conclusão" com a causa raiz e o que o changelog do Jira confirmou.
- A planilha tem CNPJ e e-mail de atendente: fica na máquina do usuário. Só publicar ou enviar para outro lugar se ele pedir. No Google Sheets, importar com "Converter texto em números" desmarcado, senão o CNPJ perde os zeros.
- Causa nova ou regra que mudou no código: atualizar a nota de regras no vault e, se for o caso, o script (padrões de log em `P`, `SS_*` e `SKIP_REASONS`; projetos em `JIRA_PROJECTS`).

## Colunas da planilha

`ticket_id`, `link_zendesk`, `motor` (`experts-service`/`survey-service`), `cnpj`, `source`, `enable_transbordo` (`true`, `false`, `true (inferido)`, `?`), `ticket_criado_em`, `solved_em`, `motor_decidiu_em`, `execucoes_motor`, `csat_enviado`, `regra_envio`, `transbordo_segurou`, `causa_descoberta` (`sim`/`não`), `codigo_causa`, `causa`, `detalhe_jiras` (cada Jira do CNPJ, o estado atual e a regra que o barra), `tickets_off_candidatos`, `ticket_transbordo_do_ticket`, `survey_csat_sent`, `checklist` (`R01 OK ; R02 OK ; … ; DEC LIBEROU`) e `observacoes`. Datas em BRT.

## Códigos de causa

| Código | Causa descoberta | O que significa |
|---|---|---|
| `TRANSBORDO_SEGUROU` | sim | o transbordo funcionou: a pesquisa foi segurada |
| `DUE_DATE_PREENCHIDO_APOS_MOTOR` | sim | o Jira EXPBKO estava sem `due_date` quando o motor rodou; a automação de SLA preencheu depois (corrida com o atraso de 10 min) |
| `JIRA_SEM_DUE_DATE`, `DUE_DATE_ACIMA_48H` | sim | EXPBKO sem `due_date` ou com prazo acima de 48h |
| `DEMANDA_PREVENTIVA`, `DEMANDA_PREVENTIVA_VAZIA` | sim | campo "Demanda preventiva" = Sim, ou vazio (vazio também descarta) |
| `JIRA_PROJETO_NAO_ELEGIVEL` | sim | o Jira não é EXPBKO nem NFEXP |
| `JIRA_CRIADO_APOS_MOTOR` | sim | o Jira foi aberto depois de o motor decidir |
| `JIRA_ANTERIOR_AO_ATENDIMENTO` | sim | o Jira é anterior ao ticket do atendimento |
| `JIRA_JA_RESOLVIDO` | sim | o Jira já estava fechado |
| `BPMP_TICKET_OFF_VIA_DIFERENTE` | sim | BPMP: o ticket off não foi aberto via "Conversa paralela" |
| `BPMP_TICKET_OFF_APOS_MOTOR` | sim | BPMP: o ticket off foi aberto depois do motor (BPMP não tem atraso) |
| `FLAG_ENABLE_TRANSBORDO_DESLIGADA` | sim | o gatilho mandou `enable_transbordo=false` |
| `ORIGEM_FORA_DO_TRANSBORDO` | sim | a origem não é `HUMAN_EXPERTS` nem `HUMAN_BPMP` |
| `CSAT_NAO_ELEGIVEL` | sim | a pesquisa nem saiu (quarentena, conta genérica, telefone, janela de expediente…) |
| `TICKET_DE_RESPOSTA_CSAT` | sim | o id informado é a resposta à pesquisa; analisar o ticket pai indicado |
| `TICKET_OFF_DO_TRANSBORDO` | sim | o id informado é o ticket off (acompanhamento do Jira/conversa paralela), não o atendimento: diz se havia transbordo e se o FUP saiu, e aponta o atendimento |
| `CSAT_POR_OUTRO_FLUXO` | sim | a pesquisa saiu por outro fluxo, fora do motor do ticket humano |
| `ERRO_NO_MOTOR` | sim | o motor falhou |
| `JIRA_ESTADO_MUDOU` | não | hoje o Jira passaria, mas mudou depois do motor: confirmar no changelog |
| `SEM_JIRA_PARA_O_CNPJ`, `BPMP_SEM_TICKET_OFF` | não | não há Jira/ticket off do CNPJ depois do atendimento (aberto com outro CNPJ, sem CNPJ, ou não houve) |
| `CSAT_AGENDADO_EXPEDIENTE` | não | pedido agendado para a abertura do expediente, sem decisão ainda |
| `SEM_LOG_DO_MOTOR`, `INDETERMINADO` | não | sem dados suficientes: olhar o caso à mão |

## Armadilhas

- **Dois motores.** O script escolhe o que decidiu por último. Durante o cutover os dois podem ter rodado para o mesmo ticket: a nota em `observacoes` avisa quando há mais de uma execução.
- **`enable_transbordo` no survey-service é inferido.** Com flag e transbordo por Jira, a decisão sai 10 min depois do solved. Para BPMP não há atraso, e a flag fica `?`: se a causa sair `BPMP_SEM_TICKET_OFF`, a flag desligada também explicaria.
- **Estado atual x estado no momento do motor.** O motor do survey-service não loga quais Jiras viu. O script reavalia com o estado de hoje e marca quando o Jira foi atualizado depois da decisão. Nesse caso, confirmar no changelog antes de afirmar a causa.
- **Qualquer PENDING do CNPJ segura.** Um transbordo `PENDING` de outro ticket do mesmo CNPJ segura a pesquisa. As `observacoes` listam os `ticket_transbordo` do CNPJ em ±30 dias.
- **Candidatos a ticket off** são os tickets do CNPJ abertos até 7 dias depois do atendimento, sem os follow-ups (`Ticket fechado`) e sem os tickets de resposta da pesquisa (grupo com "CSAT").
- **Logs do survey-service** têm `ticketId` no `jsonPayload`. Se o formato mudar (ex: nova mensagem de desfecho), ajustar `SS_OUTCOME`/`SS_IGNORED`/`SS_DISCARDED`.
