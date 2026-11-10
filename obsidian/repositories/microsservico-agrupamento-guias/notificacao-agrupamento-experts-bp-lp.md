---
name: notificacao-agrupamento-experts-bp-lp
description: "Como funciona a notificação do agrupamento de guias por e-mail e WhatsApp no microsservico-agrupamento-guias, separando os fluxos de Experts SN, Experts LP e BP LP (crons, tópicos, roteamento por pertenceBpLp/pertenceExpLp, services comuns e específicos)"
metadata:
  type: reference
tags:
  - microsservico-agrupamento-guias
  - notificacao
  - whatsapp
  - email
  - bp-lp
sistemas:
  - microsservico-agrupamento-guias
  - email-service
  - emissor-whatsapp
atualizado_em: 2026-11-10
---

# Notificação do agrupamento de guias: Experts SN, Experts LP e BP LP

O agrupamento de guias é notificado por e-mail e por WhatsApp para três públicos: clientes Experts no Simples e demais regimes (Experts SN), clientes Experts no Lucro Presumido (Experts LP) e clientes do plano básico padrão (BP) no Lucro Presumido (BP LP). Os fluxos compartilham a infraestrutura e só se separam na hora de montar a mensagem.

## Fluxo

1. **Crons/rotas separadas por público:** `NotificacaoGrupoGuiaExpSnJobImpl`, `NotificacaoGrupoGuiaExpLpJobImpl` e `NotificacaoGrupoGuiaBpLpJobImpl` (`executaEmail` e `executaWhatsapp`) buscam os `grupo_guia` elegíveis no `GrupoGuiaService` (`buscarGruposGuiaElegiveisNotificacao{ExpSn,ExpLp,BpLp}{Email,Wpp}`). Rotas `GET /notificacao/envia-lote/grupo-guia/{exp-sn,exp-lp,bp-lp}/{EMAIL,WHATSAPP}`, crons `ms-agrupamento-guias-cron-notify-{email,wpp}-{exp-sn,exp-lp,bp-lp}`. Experts é plano `EXPERT_ESSENCIAL`/`EXPERT_PRO` ou nulo (legado); Experts LP é regime `LUCRO_PRESUMIDO` e Experts SN, os demais regimes, inclusive o nulo. A rota antiga `/experts/{EMAIL,WHATSAPP}` dispara SN e LP juntos, só para a transição das crons (separação no MR !90).
2. **Mesmo tópico para todos os públicos:** cada elegível é publicado como `NotificacaoDTO(id, tipo)` no tópico de e-mail (`NotificacaoEmailGrupoGuiaPublisher`) ou de WhatsApp (`NotificacaoWhatsappGrupoGuiaPublisher`). Não existe tópico próprio do BP LP.
3. **Consumer único** chama `NotificacaoServiceImpl.notificaGrupoGuiaEmail` / `notificaGrupoGuiaWhatsApp`, que fazem a elegibilidade (competência atual, status agrupado, tem guia, ainda não notificado com sucesso naquele tipo) e criam o `controle_notificacao`.
4. **Roteamento:** `grupoGuia.pertenceBpLp()` (regime `LUCRO_PRESUMIDO` e plano em `PagtoPlanoCategoria.BP`: BASICO, AVANCADO, PREMIUM, MULTIBENEFICIOS) e, no e-mail, `grupoGuia.pertenceExpLp()` (regime `LUCRO_PRESUMIDO` e plano fora do BP) decidem o service específico. Os demais casos vão para Experts (SN). No WhatsApp, Experts LP ainda usa o service de Experts (sem template próprio definido).

## Services por canal

| Canal | Comum | Experts (SN) | Experts LP | BP LP |
| --- | --- | --- | --- | --- |
| E-mail | `EnvioEmailAgrupamentoService` (anexo, descrição do imposto, publicação) | `NotificacaoRequestServiceImpl` (template por diagnóstico) | `NotificacaoRequestExpLpServiceImpl` (template `templateAgrupamentoExpertsLpUuid`, sem diagnóstico) | `NotificacaoRequestBpLpServiceImpl` (template `templateAgrupamentoBpLpUuid`) |
| WhatsApp | `EnvioWhatsAppAgrupamentoService` (só `enviaNotificacao`: publica no tópico do ativo e preenche o `externalId`) | `WhatsAppRequestServiceImpl` (template por diagnóstico, fila `Assessores/Hubs [WHATSAPP]`, integração `EXPERTS`, categoria `JUMP`) | o mesmo de Experts | `WhatsAppRequestBpLpServiceImpl` (template `TemplateWhatsAppBp.GRUPO_GUIA_IMPOSTOS_BP_LP`, `bpm_empacotamento_guias_impostos` sem parâmetros, fila `AIDA Geral [WhatsApp] [BP]`, integração `EXPERTS` e categoria `JUMP` como em Experts) |

## Particularidades

- **BP LP não tem diagnóstico de aumento de imposto:** só Experts consulta `DiagnosticoAumentoImpostoQueryService` e troca o template conforme `MotivosDiagnosticoNotificacao.EXPERTS`. O diagnóstico do BP é outra notificação (`enviaNotificacaoDiagnosticoBp` / `NotificacaoDiagnosticoBpServiceImpl`, enums `TemplateWhatsAppBp`), sem relação com o agrupamento.
- Cada service específico monta o próprio `WhatsAppRequestDTO` (`requestWhatsBuilder`): no review do MR !88 foi recusado um builder comum com muitos parâmetros. Os dois enviam opt-out `TAX`, `debounceToBusinessHour = true`, `squad = squad-engenharia-canais` e `autor = microsservico-agrupamento-guias`.
- Padrão adotado: um service por público, sem flag/booleano escolhendo o caminho. Só vai para o service comum o que é idêntico e não exige um monte de parâmetros para variar o comportamento.
- **Opt-out de e-mail (PRD-174790):** o `EnviarEmailRequestDTO` tem `optoutPurpose` e `cnpj` obrigatórios (não compila sem), sem valor padrão: cada builder informa `optoutPurpose = EnviarEmailRequestDTO.OPTOUT_PURPOSE_TAX` explicitamente ao lado do `cnpj`, para a finalidade ficar visível no envio (pedido do dev no MR !95; um padrão no DTO foi achado pouco visível). O CNPJ sai do `EnvioEmailAgrupamentoService.getCnpjSemMascara` (só letras/dígitos, maiúsculo), calculado uma vez **antes de publicar o anexo** (para não deixar anexo órfão) e repassado ao builder: o comum `buildSendEmailDTO`, o default do `NotificacaoRequestServiceImpl` e os 7 do `EmailTemplateService` (recebem `cnpj` por parâmetro). O `publicaEmail` só publica o DTO inteiro, sem `copy` (pedido no review do MR !95).
- **Callback de e-mail é lido com Gson:** status desconhecido vira `null` (não quebra) e cai no `else` → `FALHA`. Era o que acontecia com `BLOCKED_OPTOUT` até o PRD-174790; agora ele vira `BLOQUEADA_OPTOUT` sem motivo, igual ao WhatsApp. Campos snake_case (`failure_reason`) precisam de `@SerializedName`.
- **`BLOQUEADA_OPTOUT` não é renotificado pelas crons:** as queries `buscarGruposGuiaElegiveis*` excluem qualquer `controle_notificacao` existente do tipo, seja qual for o status.
- **`nomeGuia` do e-mail = lista de todas as guias e parcelas do PDF** (Experts SN, Experts LP e BP LP, pelo `EnvioEmailAgrupamentoService.getNomeGuia`, a partir da branch `feat/lista-guias-email-agrupamento`, empilhada sobre o MR !97 de parcelas): o `NotificacaoServiceImpl.getDocumentos` converte cada `itemGrupoGuiaList` em `DocumentoAgrupavel`, tira as avulsas (igual ao `ArquivoServiceImpl.agrupaArquivosPDF`) e manda `NotificacaoRequestDTO.documentos` (`DocumentoNotificacaoDTO(descricao, numeroParcela, totalParcelas)`). A descrição é a do enum `Imposto` (ex: `SIMPLES` → `DAS SIMPLES`, `CSLL` → `DARF CSLL`), ou o nome cru quando a parcela traz um imposto fora do enum. O "x de y" vem do `nrPrestacao` da parcela (`001/060` → parcela 1 de 60); a guia não tem parcela e mostra só a descrição. Cada linha é `<descrição> - parcela x de y`, ordenada por descrição e número da parcela, separadas por `<br>`: nos 3 templates de prod (`exp-email-agrupamento-guias-default-v4`, `exp-empacotamento-lp`, `bpm-empacotamento-lp`, tabela `email_templates` do banco `email_service`) o `{{nomeGuia}}` fica sozinho num `<p>` depois de "Confira abaixo as guias disponíveis:", e o email-service (`replaceHtmlVariables`) substitui o texto cru, sem escapar HTML, então `\n` não quebraria a linha. Sem documento, lança `NotificacaoEmailException` ("Campo nomeGuia obrigatorio..."). Antes era só a descrição da "primeira" guia do `Set` (sem `@OrderBy`, ordem não garantida), e o antigo `getImpostos` quebrava (`requireNotNull(controleGuia)`) com parcela no agrupamento. Os 7 templates de diagnóstico do `EmailTemplateServiceImpl` continuam sem `nomeGuia`. No `agrupamento-guias-service` a regra antiga continua (`EnvioEmailService.nomeGuia`: `agrupamento.guias[0].imposto` mapeado em `IMPOSTO_DESCRICAO`).
- **Formato real da parcela em dev (2026-11-10), diferente da fixture do !97:** a única parcela vinda do sistema de impostos (`controle_parcelas.id = 1`) tem `nr_prestacao = '22'` (só o número, **sem o total**), `imposto` nulo, `imposto_list = {SIMPLES}` e `tipo_parcelamento = PGFN_SIMPLES`; a fixture `evento-parcela-completa.json` usa `nrPrestacao = "001/060"` e `imposto = "SIMPLES"`. Com o dado real, o `getNomeGuia` sai só com a descrição crua (`PGFN_SIMPLES`), sem "parcela x de y": o total de parcelas não chega no evento. Para testar, o grupo 3 de dev (Experts SN, 202610, CNPJ 51596322000186) ganhou duas parcelas de teste (`sistema_origem = 'teste-PRD-176358'`, `id_parcela` 9900000000000301/311), uma em cada formato, com os itens 9 e 10 do `item_grupo_guia`.
- **WhatsApp quebra com parcela (MR !97, achado em 2026-11-10):** `MetadadosGuiaFactory.from` (metadados do evento HubSpot) faz `requireNotNull(it.controleGuia)` em todo item do grupo; item de parcela não tem `controleGuia`, então qualquer grupo com parcela termina em `FALHA / ERRO_DESCONHECIDO` ("Required value was null") no WhatsApp de Experts e de BP LP. O WhatsApp BP LP só considera os planos AVANCADO, PREMIUM e MULTIBENEFICIOS (BASICO fica de fora).
- Histórico: e-mail do BP LP em PRD-170837 (MR !87), WhatsApp do BP LP em PRD-170836 (MR !88).
