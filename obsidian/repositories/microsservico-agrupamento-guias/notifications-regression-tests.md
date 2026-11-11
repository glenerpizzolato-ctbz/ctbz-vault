---
name: notifications-regression-tests
description: "Playbook de testes de regressão das notificações do microsservico-agrupamento-guias em DEV (e-mail, WhatsApp, diagnóstico Experts e BP, crons/buscas de elegibilidade, callbacks): fluxo, regras, catálogo de cenários por público e plano (Simples e Lucro Presumido), massa sintética, como disparar, verificar e limpar"
metadata:
  type: reference
tags:
  - microsservico-agrupamento-guias
  - notificacao
  - testes
  - regressao
sistemas:
  - microsservico-agrupamento-guias
  - email-service
  - atendimento-zendesk
skill: regressao-notificacoes-agrupamento
atualizado_em: 2026-11-10
---

# Testes de regressão das notificações do agrupamento

Serve para **aprender** como as notificações do agrupamento funcionam e para **validar se algo parou de funcionar**: cada cenário tem a massa, a rota que o dispara e o resultado esperado. A execução é automatizada pela skill `regressao-notificacoes-agrupamento` (`~/ctbz-vault/skills/impostos/regressao-notificacoes-agrupamento/`), cujo script `regressao.py` gera a massa, checa os destinos, dispara as rotas, compara o resultado com o esperado e limpa. Primeira execução completa: PRD-176360 (2026-11-10), durante o PRD-176358.

> [!IMPORTANT]
> **Regra do contato de teste:** toda notificação de teste vai **só** para `glener.pizzolato@contabilizei.com.br` e o telefone `55996981032`, que ficam no `grupo_guia.contato` (e no `diagnostico_aumento_imposto.contato`) da massa. Nunca, em hipótese alguma, disparar para outro e-mail ou telefone. As rotas de lote alcançam **todos** os elegíveis da competência, então antes de qualquer disparo rodar `regressao.py checar`: ele lista cada destino de cada rota e falha se houver contato diferente; o `disparar` roda a mesma checagem e se recusa a seguir. Se aparecer um registro alheio, isolar (ex: mudar o status dele) em vez de relaxar a checagem.

## Fluxo em uma página

1. **Cron** (Cloud Scheduler de `atendimento-canais-{dev,prd}`) chama a rota de lote do público.
2. **Rota de lote** busca os `grupo_guia` elegíveis (`GrupoGuiaRepository.buscarGruposGuiaElegiveisNotificacao*`) e publica `{"id", "tipo"}` no tópico `ms-agrupamento-guias.p2p.notifies-email` ou `notifies-wpp`.
3. **Consumer** chama `NotificacaoServiceImpl.notificaGrupoGuiaEmail` / `notificaGrupoGuiaWhatsApp`: valida competência atual, status `SUCESSO_AGRUPAMENTO`, ter item, contato e não ter SUCESSO anterior do tipo; cria o `controle_notificacao` (`AGUARDANDO_NOTIFICACAO`).
4. **Roteamento:** `pertenceBpLp()` (LP + plano BP) → BP LP; `pertenceExpLp()` (LP + plano fora do BP) → Experts LP; senão Experts SN.
5. **E-mail:** publica o PDF do grupo (`grupo_guia.path`) no `email-service.p2p.file-upload` e o envio no `email-service.p2p.send-email` com o template do público e `nomeGuia` (lista dos documentos, ver [[notificacao-agrupamento-experts-bp-lp]]). **WhatsApp:** publica no tópico do ativo do atendimento-zendesk.
6. **Callback** atualiza o controle: e-mail `SENT` → `SUCESSO`, `FAILED` → `FALHA / ERRO_CALLBACK_ENVIO_EMAIL`, `BLOCKED_OPTOUT` → `BLOQUEADA_OPTOUT`; WhatsApp `ENVIADA/ENTREGUE/RESPONDIDA` → `SUCESSO`, `ERRO` → `FALHA / ERRO_CALLBACK_ENVIO_WHATSAPP`, `BLOQUEADA_OPTOUT` → `BLOQUEADA_OPTOUT`.

Diagnóstico BP é outro fluxo: a rota `diagnostico/envia-lote/bp` lê `diagnostico_aumento_imposto` (não o grupo) e manda WhatsApp de diagnóstico.

## Crons (Cloud Scheduler, America/Sao_Paulo)

Conferido com `gcloud scheduler jobs list` em 2026-11-10 (o catálogo `infra/schedulers.md` ainda tinha as antigas `experts/*`).

| Job | Cron | Rota | DEV | PRD |
| --- | --- | --- | --- | --- |
| `ms-agrupamento-guias-cron-notify-email-exp-sn` | `0 03,12 15-19 * *` | `exp-sn/EMAIL` | ativo | ativo |
| `ms-agrupamento-guias-cron-notify-email-exp-lp` | `0 05,14 15-19 * *` | `exp-lp/EMAIL` | ativo | ativo |
| `ms-agrupamento-guias-cron-notify-email-bp-lp` | `0 04,13 15-19 * *` | `bp-lp/EMAIL` | ativo | **PAUSED** |
| `ms-agrupamento-guias-cron-notify-wpp-exp-sn` | `0 09,15 15-19 * *` | `exp-sn/WHATSAPP` | ativo | ativo |
| `ms-agrupamento-guias-cron-notify-wpp-exp-lp` | `0 09,15 15-19 * *` | `exp-lp/WHATSAPP` | ativo | ativo |
| `ms-agrupamento-guias-cron-notify-wpp-bp-lp` | `0 10 15-19 * *` | `bp-lp/WHATSAPP` | ativo | **PAUSED** |
| `ms-agrupamento-guias-cron-reprocess-group` | `30 02 16-19 * *` | `agrupamento-guias/reprocessa-erros` | ativo | ativo |

Rotas sob `/notificacao/envia-lote/grupo-guia/`. Não há cron para `diagnostico/envia-lote/bp` (disparo manual). A rota antiga `experts/{EMAIL,WHATSAPP}` (SN + LP juntos) ainda existe, só para a transição. Em DEV as crons rodam sozinhas nos dias 15 a 19: a massa de teste é alcançada por elas também (com a regra do contato, sem risco).

## Busca de elegibilidade (o que cada rota pega)

Competência = `PeriodoApuracaoUtils.periodoAtual()` (mês anterior ao corrente), `status = 'SUCESSO_AGRUPAMENTO'` e nenhum `controle_notificacao` do mesmo tipo, **em qualquer status** (por isso um teste repetido exige apagar o controle anterior do grupo).

| Rota | Regime | Plano |
| --- | --- | --- |
| `exp-sn/EMAIL` e `/WHATSAPP` | nulo ou ≠ `LUCRO_PRESUMIDO` | `EXPERT_ESSENCIAL`, `EXPERT_PRO` |
| `exp-lp/EMAIL` e `/WHATSAPP` | `LUCRO_PRESUMIDO` | `EXPERT_ESSENCIAL`, `EXPERT_PRO` |
| `bp-lp/EMAIL` | `LUCRO_PRESUMIDO` | `BASICO`, `AVANCADO`, `PREMIUM`, `MULTIBENEFICIOS` |
| `bp-lp/WHATSAPP` | `LUCRO_PRESUMIDO` | `AVANCADO`, `PREMIUM`, `MULTIBENEFICIOS` (BASICO fica fora) |
| `diagnostico/envia-lote/bp` | — | diagnóstico com `plano NOT LIKE 'EXPERT%'`, guia (`id_guia`) da competência e CNPJ sem nenhum `controle_notificacao` no mês; um por CNPJ, até 500 |

Consequências que os cenários cobrem: plano **nulo** (legado) não entra em nenhuma busca; BP no **Simples** não é notificado pelo agrupamento; competência anterior e status de erro ficam fora.

## Templates esperados

| Público | E-mail DEV | E-mail PRD | WhatsApp |
| --- | --- | --- | --- |
| Experts SN | `8d278fab…` | `123ccd0f…` (`exp-email-agrupamento-guias-default-v4`) | `experts_empacotamento_guias_impostosb` |
| Experts SN com diagnóstico `AUMENTO_FATURAMENTO` | `7c837342…` | `1daac9af…` | `exp_guias_diag_fatur_01` |
| Experts LP | `8d278fab…` (DEV usa o de SN) | `873da0a6…` (`exp-empacotamento-lp`) | `experts_empacotamento_guias_impostosb` |
| BP LP | `c9085510…` | `6f8764b7…` (`bpm-empacotamento-lp`) | `bpm_empacotamento_guias_impostos` |
| Diagnóstico BP `AUMENTO_FATURAMENTO` | — | — | `bp_diag_fatur_02` |

Só `AUMENTO_FATURAMENTO` está habilitado (`MotivosDiagnosticoNotificacao.EXPERTS` e `.BP`); os outros 6 motivos (`DESENQUADRAMENTO_FATOR_R`, `MUDANCA_FAIXA_SIMPLES_*`, `PROPORCAO_*`) são ignorados: Experts cai no template padrão, BP nem notifica. O diagnóstico Experts é achado por CNPJ + competência da guia (`id_guia` em `controle_guias`) e `plano LIKE 'EXPERT%'`. O template de aumento de faturamento exige `faturamentoAnterior`, `faturamentoAtual` e `porcentagemAumento` no `resultado` (sem um deles: `FALHA / ERRO_ENVIO_EMAIL`).

Como os diagnósticos nascem (fora do teste, para entender): no processamento da guia (`ProcessarMensagemGuiaServiceImpl`), se o valor variou entre 10% e 200% e a empresa está ATIVA, no Simples, sem folha e sem sócio com duplo vínculo; o primeiro diagnóstico positivo (fator R, faixas, proporções…) é gravado.

## Catálogo de cenários

`regressao.py cenarios` imprime este catálogo a partir do código (fonte da verdade do esperado). `nomeGuia` com `<br>` entre as linhas.

### Experts SN (Simples)

| ID | Massa | E-mail esperado | WhatsApp esperado |
| --- | --- | --- | --- |
| SN-01 | 1 guia SIMPLES | `DAS SIMPLES` | padrão Experts |
| SN-02 | SIMPLES, ISS, INSS_EMPRESA, INSS_PRO_LABORE (EXPERT_ESSENCIAL) | `DAM ISS<br>DAS SIMPLES<br>INSS<br>INSS` (ordenado; descrição repetida aparece 2x) | padrão |
| SN-03 | 1 parcela `SIMPLES` `003/060` | `Parcelamento DAS - parcela 3 de 60` | padrão ⚠️ |
| SN-04 | parcelas `PGFN_SIMPLES` `22`, `SIMPLES` `012/060` e `001/060`, `PREVIDENCIARIO_INSS` sem nr, tipo nulo `5/10` | `Parcelamento - parcela 5 de 10<br>Parcelamento DAS - parcela 1 de 60<br>Parcelamento DAS - parcela 12 de 60<br>Parcelamento PGFN DAS - parcela 22<br>Parcelamento Previdenciário` | padrão ⚠️ |
| SN-05 | guia SIMPLES + guia ISS avulsa (`EMISSAO_PENDENTE`) + parcela `005/060` | `DAS SIMPLES<br>Parcelamento DAS - parcela 5 de 60` (avulsa fora) | padrão ⚠️ |
| SN-06 | guia + parcela + diagnóstico `AUMENTO_FATURAMENTO` | template de diagnóstico, sem `nomeGuia` | `exp_guias_diag_fatur_01` ⚠️ |
| SN-07 | só guia avulsa (`EMISSAO_FUTURA`) | `FALHA / ERRO_ENVIO_EMAIL` ("Campo nomeGuia obrigatorio") | padrão |
| SN-08 | regime nulo (legado), EXPERT_PRO | `DAS SIMPLES` | padrão |
| SN-09 | plano nulo (legado) | não elegível | não elegível |
| SN-10 | diagnóstico `DESENQUADRAMENTO_FATOR_R` (não habilitado) | template padrão com `DAS SIMPLES` | padrão |
| SN-11 | contato sem e-mail | `DADOS_INCOMPLETO` | padrão |
| SN-12 | competência anterior | não elegível | não elegível |
| SN-13 | status `GUIAS_COM_ERRO` | não elegível | não elegível |
| SN-14 | já tem e-mail `SUCESSO` | não elegível | padrão |

### Experts LP (Lucro Presumido)

| ID | Massa | E-mail esperado | WhatsApp esperado |
| --- | --- | --- | --- |
| LP-01 | CSLL, IRPJ_16, PIS, COFINS, ISS | `DAM ISS<br>DARF COFINS<br>DARF CSLL<br>DARF_IRPJ<br>PIS` (todas, não só uma) | padrão Experts |
| LP-02 | parcelas `DARF_UNIFICADO` e `PGFN_DEMAIS_DEBITOS` `004/024` (EXPERT_ESSENCIAL) | `Parcelamento DARF Unificado - parcela 4 de 24<br>Parcelamento PGFN Demais Débitos - parcela 4 de 24` | padrão ⚠️ |
| LP-03 | CSLL, PIS + parcela `PREVIDENCIARIO_INSS` `010/060` | `DARF CSLL<br>PIS<br>Parcelamento Previdenciário - parcela 10 de 60` | padrão ⚠️ |

### BP LP (Lucro Presumido, plano básico padrão)

| ID | Massa | E-mail esperado | WhatsApp esperado |
| --- | --- | --- | --- |
| BP-01 | BASICO: CSLL, IRPJ_16, COFINS | `DARF COFINS<br>DARF CSLL<br>DARF_IRPJ` | não elegível (BASICO) |
| BP-02 | AVANCADO: parcela `PGFN_PREVIDENCIARIO_INSS` `007/030` | `Parcelamento PGFN Previdenciário - parcela 7 de 30` | `bpm_empacotamento_guias_impostos` ⚠️ |
| BP-03 | MULTIBENEFICIOS: PIS, COFINS + parcelas `PGFN_SIMPLES` `15` e `DIVIDA_ATIVA` `002/012` | `DARF COFINS<br>PIS<br>Parcelamento Dívida Ativa - parcela 2 de 12<br>Parcelamento PGFN DAS - parcela 15` | BP ⚠️ |
| BP-04 | PREMIUM: PIS | `PIS` | BP |
| BP-05 | BASICO no Simples | não elegível | não elegível |

### Diagnóstico BP

| ID | Massa | Esperado |
| --- | --- | --- |
| DBP-01 | diagnóstico `AUMENTO_FATURAMENTO`, plano BASICO, guia da competência | WhatsApp `bp_diag_fatur_02` |
| DBP-02 | diagnóstico `PROPORCAO_ANEXOS` (não habilitado) | ignorado |

⚠️ = grupo com parcela: o WhatsApp falha com `FALHA / ERRO_DESCONHECIDO` ("Required value was null") até a correção da **PRD-176440** (`MetadadosGuiaFactory` exigia `controleGuia` em todo item). O verificador marca como `BUG` enquanto isso; depois da correção, esses cenários têm de dar `OK`. Correção na branch `fix/PRD-176440` (sobre o !97, commit `89e7249d`, ainda sem MR): os metadados do HubSpot passam a considerar só as guias do grupo (contrato de guias do atendimento-zendesk) e ignoram as parcelas.

## Execução

Deploy em dev: no pipeline do MR é manual (`service-account-dev` e depois `helm-deploy-gke-dev`, que fica `skipped` até o play) e troca a versão do pod de dev compartilhado, então combinar antes; no merge para o master, o pipeline do master faz `service-account-dev`, `terraform-resources-dev`, `helm-deploy-gke-dev` **e `helm-deploy-gke-prd`** (visto em 2026-11-11 no merge do !101: dev e prd na mesma rodada). Para conferir que o pod trocou, olhar no Cloud Logging o ReplicaSet novo (`microsservico-agrupamento-guias-<hash>-*`) e o `Started MicrosservicoAgrupamentoGuiasApplicationKt` depois do horário do deploy. Pré-requisitos: proxy de dev do atendimento (`sql_atendimento_dev`, serviço `dev_atendimento_canais_ms_agrupamento_guias`), `gcloud` autenticado (logs em `contabilizei-dev-01`) e o token do api-gateway de dev numa variável de ambiente (`DECK_BRUNO_EXPERTS_TO_MICROSSERVICO_AGRUPAMENTO_GUIAS_DEV`, do `docs/bruno/.env` do repo; ver `apis/`). O pod de dev precisa estar com a branch a testar.

```bash
R=~/ctbz-vault/skills/impostos/regressao-notificacoes-agrupamento/scripts/regressao.py
python3 -I $R limpar --aplicar                 # zera massa anterior
python3 -I $R massa --aplicar                  # cria os grupos (competência atual)
python3 -I $R checar                           # quem cada rota alcançaria; falha se houver contato fora do de teste
export TK=...                                  # token do api-gateway de dev
INICIO=$(date -u +%FT%TZ)
python3 -I $R disparar --token-env TK --rotas email
python3 -I $R disparar --token-env TK --rotas whatsapp,diagnostico-bp
sleep 60
python3 -I $R verificar --desde $INICIO        # OK / BUG / FALHA por cenário e canal; sai com 1 se houver FALHA
python3 -I $R limpar --aplicar                 # ao terminar
```

Para disparar só uma rota sem alcançar os outros grupos (ex: reproduzir um cenário), mudar temporariamente o `status` dos outros grupos de teste para `PROCESSANDO` e voltar depois.

## Como ler o resultado

- **E-mail em DEV nunca chega:** o SMTP de dev rejeita (`421 The from domain should be a connected email sending domain - hssmtp`), e o controle termina em `FALHA / ERRO_CALLBACK_ENVIO_EMAIL`. O que valida é o `sendEmailDTO` no log do pod (`templateId` e `nomeGuia`) e o `email_replications` do email-service de dev (`dev_atendimento_canais_email_service`). Para receber o e-mail de verdade: app local com banco de dev e só o envio em prod, ver [[rodar-testes-localmente]].
- **Quebra de linha:** renderizar o HTML do template (`email_templates.html_content` do email-service) com as `variables` de um `email_replications` e tirar print (Chrome headless). O `{{nomeGuia}}` fica num `<p>`; `<br>` literal no print é regressão.
- **WhatsApp em DEV chega** no telefone de teste (o callback do ativo volta `SUCESSO`).
- **Metadados do WhatsApp (evento do HubSpot):** o pod não loga o `metadados` do `WhatsAppRequestDTO`. Para conferir as chaves ([[metadados-whatsapp-hubspot]]), ler o que o atendimento-zendesk gravou: `mensagem_ativa.metadados` (`jsonb`) no banco de dev do atendimento-zendesk (`service=dev_crm_atendimento_zendesk`, proxy `sql_crm_dev`, porta 5434), filtrando `doc_tipo = 'cnpj' and doc_valor like '990000%'` (CNPJs da massa) e `criado_em >= <início>`; o status fica em `mensagem_ativa_status` (FK `id_mensagem`). O esperado sai do banco do agrupamento (itens → `controle_guias`/`controle_parcelas`); as datas são `timestamp without time zone`, lidas em UTC pela JVM e formatadas em America/Sao_Paulo. Chave nova só chega ao HubSpot se estiver na whitelist `METADADOS_NA_WHITELIST` do `EventoHubspotAtivoService` do atendimento-zendesk e declarada no evento.
- Evidências viram comentário na sub-task de testes do card (logs + banco + prints), como na PRD-176360.

## Armadilhas

- Rotas de lote alcançam tudo o que for elegível: sempre `checar` antes.
- Qualquer `controle_notificacao` do tipo (até FALHA) tira o grupo da busca: para repetir, apagar o controle do grupo.
- **Token entre aspas no `.env`:** no `docs/bruno/.env`, o `DECK_BRUNO_EXPERTS_TO_MICROSSERVICO_AGRUPAMENTO_GUIAS_DEV` está entre aspas. Um `grep … | cut -d= -f2-` leva as aspas para o header `x-ctbz-api-gateway-token`, e o api-gateway responde **401 Unauthorized**. Tirar as aspas antes de exportar: `v="${v#\"}"; v="${v%\"}"; export TK="$v"`. Sem o header, a resposta é `No API key found in request`.
- **SN-11 x WhatsApp:** o catálogo espera `ENVIA` no WhatsApp do contato sem e-mail, mas desde 2026-10-15 (`1a956143`/`cdfcba3a`) `ContatoDTO.fromJson`, do WhatsApp, chama `fromJsonEmail` e exige e-mail. O WhatsApp fica `DADOS_INCOMPLETO` ("campo email obrigatório"). Visto em 2026-11-11, sem decisão ainda: ou é bug ou o catálogo precisa mudar.
- **Mesma data de vencimento em toda a massa:** `massa` grava guias e parcelas com o mesmo `data_para_pagamento`/`vencimento` (agora + 10 dias). Para provar uma regra de "menor vencimento", antecipar a data de um documento da massa e reenviar só aquele grupo, apagando o controle do tipo.
- **Grupo fora da massa com o contato de teste:** em dev, o grupo 3 (`id_empresa` 5775972832378880, testes da PRD-176358) usa o contato de teste e entra no `exp-sn/WHATSAPP`. O `checar` passa, porque o contato é o de teste, mas o grupo ganha controle. Para não sujá-lo, pôr `status='PROCESSANDO'` durante o disparo e voltar para `SUCESSO_AGRUPAMENTO` depois.
- O PDF anexado é o `grupo_guia.path` (já mesclado), não os documentos: a massa reaproveita arquivos reais de dev, então o conteúdo do PDF não bate com a lista (só a lista é validada).
- O diagnóstico de teste precisa da guia (`id_guia`) em `controle_guias` na competência, senão não é achado.
- `PubSubInitConfig` e `application-local.yml` ao rodar local contra dev: ver [[rodar-testes-localmente]].

## Histórico de execuções

- **2026-11-11 (PRD-176511/PRD-176512, !101 já no master em dev):** só a rota WhatsApp, conferindo os `metadados` em `mensagem_ativa.metadados` do atendimento-zendesk de dev contra o esperado calculado do banco. Os 16 grupos enviados deram OK (só guias, só parcelas, misto, Experts e BP LP), e o menor vencimento entre guia e parcela foi confirmado com um reenvio do LP-03. O SN-11 ficou em `DADOS_INCOMPLETO` (ver armadilhas). Evidências na pasta `tests/w4t` da feature do BahCode.

- **2026-11-10 (PRD-176358, MR !99, sobre o !97):** 13 grupos (versão inicial deste catálogo). E-mail OK em todos os públicos; WhatsApp com parcela falhou → PRD-176440. Evidências na PRD-176360. Depois do review do !99 a descrição da parcela passou a ser a do `TipoParcelamento` (o esperado acima já reflete isso).

- **Grupo só com guia avulsa em prd (2026-11-11, grupo `671875`):** o mesmo cenário do SN-07 aconteceu de verdade. O único item era uma guia `SIMPLES` em `EMISSAO_FUTURA`, e o e-mail terminou em `FALHA / ERRO_ENVIO_EMAIL`, com o log `NotificacaoEmailException: Notificação <idControle> Campo nomeGuia obrigatorio...`. O WhatsApp do mesmo grupo foi enviado, porque não lista as guias, e a elegibilidade (`isGrupoPossuiGuia`) só confere se há item, não se há item não avulso. Para investigar: `item_grupo_guia` join `controle_guias` pelo `grupo_guia_id`, e o log `ERROR` do container `microsservico-agrupamento-guias` no `contabilizei-prod-01`.
