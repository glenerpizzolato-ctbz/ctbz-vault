---
name: roteamento-n1-ativacao-soci
description: "Roteamento do bot WhatsApp Expert/BP no encaminhamento para N1 Ativação por status do SOCI (jiraStatus): drops atuais na Ultimate (Entrega 02, prd) com nome e id dos grupos do Zendesk, e o que muda na Entrega 03 (PRD-176172)"
metadata:
  type: reference
tags:
  - ultimate-as-a-code
  - ultimate
  - zendesk
---

# Roteamento N1 Ativação por status do SOCI

Os drops ficam no dashboard da Ultimate (fluxo de encaminhamento N1 Ativação), não no repo. A decisão usa o `jiraStatus` que o `plataforma-crm-web` devolve nos dados gerais do bot. Épico [[PRD-154606]]; Entrega 02 [[PRD-157501]]; Entrega 03 [[PRD-176172]].

## Versão atual em prd (Entrega 02, conferida em 2026-11-16)

Tabela informada pelo Glener; nomes dos grupos conferidos no Zendesk de prd pela skill `buscar-grupo-zendesk`. Pronta para colar no Google Chat (bloco de código):

```
+-------+-------------------------------+----------------------------------------------+
| Bloco | Status SOCI                   | Grupo ZD                                     |
+-------+-------------------------------+----------------------------------------------+
| 1     | Aguardando Cliente Cadastro   | Experts/BP: Cadastro [Ativação] [Whatsapp]   |
|       | Aguardando Formatura          | (28283501432220)                             |
|       | EM_ANALISE                    |                                              |
|       | PENDENCIA                     |                                              |
|       | REFAZER - ESCRITÓRIO VIRTUAL  |                                              |
|       | Refazer Pré-Cadastro          |                                              |
+-------+-------------------------------+----------------------------------------------+
| 2     | Ag Análise MT                 | Experts/BP: Pré CNPJ - Módulo tributário     |
|       | Ag Assinatura Cliente MT      | [Ativação] [WhatsApp] (30023019944860)       |
|       | Ag Assinatura Contador        |                                              |
|       | Aguardando DBE MT             |                                              |
|       | Aguardando Ecac               |                                              |
|       | Erro Ag Assinatura MT         |                                              |
|       | Erro Preenchimento MT         |                                              |
|       | Gerar DBE MT                  |                                              |
|       | Preenchimento Cliente MT      |                                              |
|       | Preenchimento MT              |                                              |
|       | Processo Adm MT               |                                              |
|       | Protocolo no Ecac             |                                              |
+-------+-------------------------------+----------------------------------------------+
| 3     | Em Stand-by                   | Experts/BP: Pós Vendas [Ativação] [Whatsapp] |
|       | Iniciado                      | (28283527238556)                             |
|       | NAO_INICIADO                  |                                              |
|       | Pós Vendas                    |                                              |
+-------+-------------------------------+----------------------------------------------+
| 4     | [FSP] Follow Assinatura       | Experts/BP: Pré CNPJ [Ativação] [Whatsapp]   |
|       | [SEVEN] Aguardando Assinatura | (28283155272220)                             |
|       | [SEVEN] Exigência             |                                              |
|       | [SEVEN] Exigência/Pendência   |                                              |
|       | Aguardando assinatura         |                                              |
|       | Aguardando Cliente            |                                              |
|       | Aguardando pagamento          |                                              |
|       | Aguardando Protocolo          |                                              |
|       | Em exigência                  |                                              |
|       | Enviar Docusign               |                                              |
|       | Enviar processo ao cliente    |                                              |
|       | Erro Docusign                 |                                              |
+-------+-------------------------------+----------------------------------------------+
| 5     | Qualquer outro status (ELSE)  | Experts: Atendimento [Ativação] [Whatsapp]   |
|       |                               | (5318551320604) + tag sys_grupo_ativacao_exp |
|       |                               | BP: Atendimento [Ativação] [Whatsapp]        |
|       |                               | (5318551320604)                              |
+-------+-------------------------------+----------------------------------------------+
```

- O grupo do bloco 2 (`Pré CNPJ - Módulo tributário`, 30023019944860) já está em uso em prd desde 2026-09-02; não é novidade da Entrega 03, embora o card diga que os status MT "saem do grupo antigo".

## Grupos da Entrega 03 em prd (conferidos em 2026-11-16)

| Grupo | ID | Criado |
| --- | --- | --- |
| AIDA Geral [WhatsApp] [BP] | 22427993443100 | 2025-09-18 |
| Onboarding [Experts] | 5318567086108 | 2022-07-11 |
| Pré CNPJ - Assinatura JC [Ativação] [WhatsApp] | 30023034651676 | 2026-09-02 |
| Retenção Abertura [Ativação] [WhatsApp] | 29996619254940 | 2026-09-01 |

## Diff Entrega 02 → 03

Relatório com o diff por status e os conflitos: artefato "Roteamento N1 Ativação V1 x V2" (https://claude.ai/artifact/VWvyR3BBU2nhUTwNYqrMgC) e PDF em `~/Downloads/roteamento-n1-ativacao-v1-v2.pdf`. Resumo: 19 status ficam onde estão, 7 de assinatura/protocolo vão de Pré CNPJ para Assinatura JC, 8 caem no ELSE e 8 entram (Cadastro, Consulta MT (Auto), Erro Análise MT, [SEVEN] AGUARDANDO PAGAMENTO, [SEVEN] Aguardando Protocolo, Protocolar JC, Solicita Reembolso e Finalizado por plano).

## De onde vem o `statusJira` no fluxo de processos (conferido no código em 2026-11-16)

O bot usa duas rotas do `atendimento-zendesk` (controller `whatsapp-identifcacao-processos.controller.ts`):

1. `GET /bots/whatsapp/identificacao/processos/contagem/{telefone}` chama `contabilizei-abertura` `GET /integracao/twilio/processo/telefone/{telefone}`. A Abertura busca as **empresas da Abertura cujo sócio tem esse telefone** (`empresaDAO.getByManyTelefonesSocio`) e devolve o `ProcessoAbertura` de cada uma. O `atendimento-zendesk` **descarta os processos com status `FINALIZADO`** (`StatusProcessoParaExclusao`) e separa Experts x outros planos pelo `plano` (`categoriaPlano` do processo).
2. `GET /bots/whatsapp/identificacao/processos/dados/{idProcesso}/telefone/{telefone}` chama `GET /integracao/twilio/{idProcesso}/processo` e resume o processo (`statusJira`, `plano`, `idJira`, empresa etc.).

- `statusJira` = `ProcessoAbertura.status`, entidade do **Datastore** (Objectify `@Entity @Cache`) no projeto `contabilizei-abertura`. Quem grava é o `JiraSyncService` (`atualizaValoresCamposAbertura`), que copia o status da issue SOCI do Jira e ainda atualiza a macro etapa, o histórico de status e a etapa da central/HubSpot.
- O vínculo é **telefone do sócio → empresa da Abertura → processo**, não CNPJ nem o `ticketing-service`. O `ticketing-service` (banco `prd_issue_ticketing`, tickets por CNPJ) só é usado pelo `atendimento-zendesk` na timeline. Mexer nele não muda o roteamento.
- Não há cache no `atendimento-zendesk` nem na Abertura além do `@Cache` do Objectify, que é write-through quando o save passa pela aplicação. Uma edição direta no Datastore pelo console deixa o memcache desatualizado. O cache de 3 h é só do `plataforma-crm-web` (`AberturaFacade.consultarProcessoPorId`, chave por `idProcesso`), usado no caminho de empresa já ativa (dados gerais), não neste.
- Consequência: um processo **Finalizado** nunca chega na rota de dados por esse caminho, porque a contagem o descarta. Os drops de Finalizado (AIDA BP / Onboarding Experts) só são alcançáveis se o Finalizado vier por outro caminho (dados gerais da empresa no `plataforma-crm-web`).

## Testar mudando o status de uma issue SOCI em prd (avaliado em 2026-11-16)

- O MCP do Atlassian lê o projeto SOCI e lista as transições com o usuário do Glener (ex: SOCI-562684).
- O fluxo do SOCI não deixa pular para qualquer status. A partir de **Finalizado**, só existe uma transição que muda de status, para **Aguardando Finalização**. As outras 13 voltam para Finalizado e disparam ações reais, como criar cards FIN (pagamento de taxa), PLA, CIT, Controle e Auditoria Pós CNPJ e solicitar enquadramento.
- Por isso, **não usar issue SOCI de cliente real para teste**: a mudança vai para a Abertura pelo `JiraSyncService` (macro etapa, histórico, HubSpot) e as transições criam trabalho para outros times. Para testar em prd, é preciso um processo e uma issue SOCI de teste criados pelo time da Abertura, com o telefone de teste como sócio.

## Drop depois da IA (observado em 2026-11-24)

- **BP também passa pelos drops:** o BP em abertura vai primeiro para a AIDA [Ativação] [BP]; quando ela transfere para humano, o ticket cai no drop do status (ex: ticket 30426186, `Aguardando Cliente (Prefeitura)`, fora do mapa → Atendimento [Ativação]). O mesmo vale para Experts no rollout da IA.
- **A transferência da IA nem sempre segue o status:** ticket 30426058 (BP, SOCI-576142 em `Em Stand-by` desde 10/11, `[SOCI] Etapa do Processo = Cadastro`) caiu em Cadastro em vez do ELSE. Provável transferência pela etapa; conferir no log da Ultimate.
- Para validar um ticket: skill `validar-drop-ativacao` ([[trilha-chamadas-bot-load-balancer]]).
