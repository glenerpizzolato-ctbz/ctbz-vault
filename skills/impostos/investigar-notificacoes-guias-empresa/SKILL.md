---
name: investigar-notificacoes-guias-empresa
description: Investiga em PRODUÇÃO (só leitura), para uma empresa (CNPJ), por que ela recebeu ou não as notificações de guias de imposto - a do agrupamento/empacotamento do dia 15 (microsservico-agrupamento-guias, e-mail e WhatsApp) e a avulsa (guia individual do experts-service) - competência a competência. Cruza grupo_guia, histórico de processamento, itens do grupo, controle_guias e controle_notificacao com o WhatsApp ativo, o task_scheduler do experts-service e o plano da empresa mês a mês no BigQuery, e classifica cada mês (enviado, fora do agrupamento pelo plano, sem gatilho, sem guia, aguardando geração, guia duplicada travando, guia alterada, falha de notificação) com o que fazer. Use quando um PRC ou alguém perguntar por que um cliente não recebeu o e-mail/WhatsApp das guias, do empacotamento ou da guia avulsa em algum mês.
argument-hint: "<cnpj> [desde AAAAMM] [ate AAAAMM]"
---

# Investigar notificações de guias de uma empresa

Playbook do problema: `~/ctbz-vault/obsidian/PRCs/itens/PRD-174011 - Cliente não recebe notificação do agrupamento de guias.md` (ler antes; é lá que cada ocorrência é registrada). Fluxos: `~/ctbz-vault/obsidian/repositories/microsservico-agrupamento-guias/notificacao-agrupamento-experts-bp-lp.md` (agrupamento) e `~/ctbz-vault/obsidian/repositories/experts-service/notificacao-individual-guias-x-agrupamento.md` (avulsa e os "buracos de silêncio").

```sh
I() { python3 -I "$HOME/ctbz-vault/skills/impostos/investigar-notificacoes-guias-empresa/scripts/investigar.py" "$@"; }
I 26120247000135                      # últimas 12 competências
I 26120247000135 --desde 202512       # a partir de uma competência
```

Competência é o mês de apuração; o envio do agrupamento é no dia 15 do mês **seguinte** (ex: "não recebi em outubro" = competência 202609). Leva ~20 s. Grava `resumo.md` e `dados.json` em `~/Downloads/investigacoes/notificacoes-guias/<cnpj>/<AAAA-MM-DD_HHMM>/`.

## Regras

- **Prod é só leitura.** O script só faz `SELECT` (serviços `prd_*`, abertos em `default_transaction_read_only`) e `bq query`. Data fix, republicação na rota `envia-empresa-ms-agrupamento-guia/{idEmpresa}` ou disparo manual de notificação: montar e entregar ao usuário, nunca executar.
- **Sem dado de contato** nas saídas e nos comentários do Jira: só CNPJ, ids, status e datas. Não consultar `grupo_guia.contato` nem e-mail/telefone do controle.

## Passos

1. Proxies: `sql_atendimento_prd` (5443, agrupamento) e `sql_exp_prd` (5445, experts-service) obrigatórios; `sql_crm_prd` (5444, WhatsApp ativo) opcional. Conferir com `ss -ltn | grep -E ':544[345]'`; subir só os que faltam (`zsh -ic '_sql_proxy_start_alias sql_atendimento_prd'`) e derrubar no fim só os que você subiu. O BigQuery usa o `bq` do usuário (sem VPN).
2. Rodar `I <cnpj>` com o período do chamado. Sem BigQuery (`--sem-bq`) a causa de plano não é confirmada; sem o 5444 (`--sem-wpp`) o WhatsApp sai só pelo controle.
3. Ler o `resumo.md`: uma linha por competência e o detalhe das que não foram enviadas. Conferir cada causa com a tabela abaixo e completar o que o script não alcança (ver "Limites").
4. Responder no PRC com o histórico por competência (o que foi enviado e por que os outros meses não foram), sem dados de contato. Mostrar o texto ao usuário antes de comentar.
5. Registrar a ocorrência no playbook (`ocorrencias`, `qtd_ocorrencias`, `ultima_ocorrencia` e, se a causa for nova, uma seção) e, se o cliente for exemplo de uma causa nova, acrescentá-la a esta skill.

## Causas

| Código | O que aconteceu | Onde confirmar |
| --- | --- | --- |
| `ENVIADO` / `ENVIADO_PARCIAL` | Grupo notificado (por um ou dois canais). Pode ter virado `ERRO_GUIA_ALTERADA*` depois, sem renotificar | Se o cliente diz que não recebeu: e-mail no email-service/HubSpot pelo `external_id`; WhatsApp pelo status do ativo |
| `FORA_DO_AGRUPAMENTO_PLANO` | Sem grupo porque o plano no dia 15 não era elegível. Até 22/10/2026 (`plataforma-faturamento-worker` `2d62f7b2`) só `EXPERT_ESSENCIAL` era enviado; hoje os lotes são Experts SN/LP, BP LP e BP Simples (BP Simples tem grupo mas não tem notificação) | Plano mês a mês no BigQuery; troca de plano com CS/Faturamento. A avulsa também não sai: o experts-service só notifica plano Experts |
| `SEM_GATILHO` | Plano elegível e guias no microsserviço, mas nenhum grupo nem `historico_processamento_grupo_guia`: a mensagem de `agrupar-guias-empresa` não chegou | Logs do `plataforma-faturamento-worker` (projeto `contabilizei-impostos`, retenção de 30 dias) no dia 15 |
| `SEM_GUIA` | `AGRUPAMENTO_SEM_GUIA` (nenhuma agrupável na montagem; TFE/ISS não contam) ou nenhuma guia no `controle_guias` | Se a plataforma tinha guias antes do dia 15, é falha de sincronização das guias |
| `AGUARDANDO_GERACAO` | Guia sem PDF no dia 15; o grupo nunca é retentado (`ReprocessamentoErrosJobImpl` só pega `ERRO_SISTEMA`/`ERRO_GERACAO_PDF_AGRUPAMENTO`; `AnalisaAlteracaoGuiaServiceImpl.possuiImpactoAgrupamento` ignora guia depois do vencimento ou da virada do mês) | Datas de `REGISTRADO` das guias no resumo |
| `GUIA_TRAVANDO` | Grupo com `path` (PDF gerado) ou imposto duplicado, mas uma guia dentro dele segue sem arquivo (`AGUARDANDO_EMISSAO`): o `EfetivaStatusAgrupamentoServiceImpl` exige PDF de todas | Status da guia (`id_guia`) no sistema de impostos: pedir ao Fiscal (o Datastore de `contabilizei-impostos` dá `PERMISSION_DENIED` para nós). Se cancelada/substituída, o evento não chegou |
| `GUIAS_COM_ERRO` | Guia com `ERRO_PROCESSAR_GUIA`/`FALHA_UPLOAD` trava o grupo | Só sai se a guia mudar de novo |
| `ERRO_GUIA_ALTERADA` | Guias mudaram depois do agrupamento e antes da notificação | Sem renotificação (decisão de Produto) |
| `ERRO_PROCESSAMENTO` | `ERRO_SISTEMA`/`ERRO_GERACAO_PDF_AGRUPAMENTO` | Deveria ser reprocessado pelo job |
| `SEGMENTO_SEM_NOTIFICACAO` | Grupo OK, mas BP Simples, plano nulo ou WhatsApp do BASICO | Esperado |
| `ELEGIVEL_NAO_NOTIFICADO` | `SUCESSO_AGRUPAMENTO` sem controle | Crons dos dias 15 a 19; depois, só disparo manual (skill `relatorio-notificacoes-agrupamento`) |
| `FALHA_NOTIFICACAO` | `FALHA`, `DADOS_INCOMPLETO` ou `BLOQUEADA_OPTOUT` | As crons não renotificam quem já tem controle |

**Avulsa**: para cada mês não enviado, o resumo diz se houve avulsa e por quê não. Guia agrupável (SIMPLES, DARF_UNIFICADO etc.) da competência atual é segurada pelo experts-service até o grupo ter WhatsApp com `SUCESSO`; se o grupo nunca é notificado, a avulsa também não sai (buraco de silêncio). Avulsas de guias fora do agrupamento (ISS com vencimento antes do dia 20, TFE) aparecem numa seção à parte.

## Limites

- O plano vem do snapshot mensal `saude_empresa.empresa` (fim do mês): troca no meio do mês pode aparecer só no mês seguinte. `grupo_guia` só guarda plano e regime a partir de 2026-10.
- `controle_guias.id_arquivo` vem como string vazia (não `NULL`) quando não há PDF; o script usa `nullif(id_arquivo, '')`.
- A tabela de guias do BigQuery citada nas notas antigas (`dw_contabilizei_impostos.Guia`) não existe mais no `contabilizei-dataflow`; o status real da guia no sistema de impostos fica com o Fiscal.
- Logs de aplicação só ficam 30 dias: para meses antigos, a evidência é só o que está nos bancos.

## Exemplos validados

- `26120247000135` (PRC-153307, 2026-11-27): 202603–202605 `FORA_DO_AGRUPAMENTO_PLANO` (AVANCADO de 03 a 06/2026); 202609 `GUIA_TRAVANDO` (DARF_UNIFICADO duplicada `6551924603879424`); demais enviados.
- `03916262000199` (PRC-151642): `SEM_GUIA` e `AGUARDANDO_GERACAO` em vários meses; 202609 enviado e depois `ERRO_GUIA_ALTERADA_RECORRENTE`.
