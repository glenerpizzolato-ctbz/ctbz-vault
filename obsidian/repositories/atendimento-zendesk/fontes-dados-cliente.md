---
name: fontes-dados-cliente
description: "De onde o atendimento-zendesk tira cada dado do cliente (plano, status, regime, ramo, município/UF, CNAE, natureza jurídica, tipo de contrato, certificadora, processo de abertura, grupos do guardião): clients prontos (crm-web, plataforma, Zendesk) para 1 cliente e BigQuery para a base inteira, com as lacunas"
metadata:
  type: reference
tags:
  - atendimento-zendesk
  - avisos-e-mensagens
  - dados-cliente
repositorio: atendimento-zendesk
---

# Fontes de dados do cliente no atendimento-zendesk

Levantado em 27/11/2026 para o motor de regras de avisos e mensagens ([[PRD-179459]], artefato [[plano-api-avisos]]), sobre o `master` @ `e20a15a20`. Serve para qualquer funcionalidade que precise de atributos do cliente.

## Um cliente (dados atuais, por API)

| Dado | Fonte | Client em `src/infra/clients/` |
|---|---|---|
| Plano, status (ATIVO/INATIVO), regime, ramos (COMERCIO/SERVICO), `codMunicipioIbge`, razão social | crm-web `GET /auth/atendimento/v2/bots/whatsapp/dados-cliente/basico-padrao?cnpj=&telefone=` | `plataforma-crm-web/dados-cliente-basico-padrao` |
| Os mesmos dados para Experts (mais `abertura`, `assessor`, `vencimentoCertificado`) | crm-web `.../dados-cliente/experts` | `plataforma-crm-web/dados-clientes-experts` |
| Processo de abertura pelo telefone (reserva; o principal são as tags, abaixo), com `id` e `abertura` | crm-web `GET /auth/atendimento/processo/telefone?telefone=` | `plataforma-crm-web/dados-cliente-abertura` |
| Certificadora (só `CERTISIGN` ou `SOLUTI`) | crm-web `GET /auth/atendimento/v2/bots/core/dados-cliente/certificado/emissor?cnpj=` | `plataforma-crm-web/buscar-dados-integracoes` |
| Empresa completa (endereço, plano `categoriaV2`, regime, status) e o `id` interno | plataforma (contabilizeiapp) `GET /empresa/auth/getByCnpj` | `plataforma-notas-worker/empresas` |
| CNAEs da empresa | plataforma `GET /nfse/rest/cnae-empresa/listar/{idEmpresa}` | `plataforma-notas-worker/cnaes` |
| Municípios atendidos (lista para seletor) | crm-web `.../apps/gerenciamento-faqs/municipios` | `plataforma-crm-web/municipios-atendidos` |
| Dados da Receita (razão social, UF, IBGE, situação cadastral), sem natureza jurídica | heimdall `ms-consulta-simples` | `heimdall/ms-consulta-simples/consulta-cnpj` |
| Processo de abertura por CPF ou `uidc` (não por id) | contabilizei-abertura `/integracao/twilio/processo/cpf|uidc/...` | `contabilizei-abertura/dados-cliente-abertura` |
| Ticket por id; grupos de um usuário; lista de grupos; agentes | Zendesk `api/v2/tickets/:id`, `users/:id/group_memberships`, `groups`, `users` | `zendesk/buscar-ticket-por-id`, `zendesk/agent-groups`, `zendesk/grupos-atendimento-zendesk`, `zendesk/agentes` |

## Processo de abertura de um ticket sem CNPJ

O caminho principal são as **tags do ticket** (dica de um colega, conferida em 27/11/2026):

- `processo_id:<N>`: gravada pelo WhatsApp ativo (`mapProcessoIdTag` em `src/infra/util/whatsapp-mensagem-ativa.util.ts`).
- `processo:<N>`: lida pelo `ObterProcessoDoTicketService` (`src/domain/tickets/services/obter-processo-do-ticket/`), usado ao sincronizar a organização após o ticket ser criado. Não é gravada por este repositório (vem de fora, provavelmente do bot ou de gatilho).
- **Armadilha:** o `ObterProcessoDoTicketService` procura `tag.includes('processo:')`, que não casa com `processo_id:<N>`. Quem precisar do processo tem que aceitar os dois padrões.
- Amostra de prod (últimos 20 mil tickets, 25–27/11/2026, tabela `tickets`): 2.394 com `processo_id:`, 237 com `processo:`, 36 com as duas (sempre o mesmo número). Dos 4.839 tickets sem `organization_cnpj`, 2.040 tinham uma das tags, todos de WhatsApp. Os sem CNPJ e sem tag vêm de e-mail, formulário web e Serviço Web (914/715/404) e 715 de WhatsApp. 555 tickets com CNPJ também tinham a tag.
- Reserva: crm-web `processo/telefone` pelo `requester_phone`.
- A consulta com `created_at` na tabela `tickets` estoura o statement timeout em prod; usar `ORDER BY id DESC LIMIT N`.

A tabela local `tickets` já espelha o ticket com `organization_cnpj`, `organization_plano`, `assignee_id`, `group_id` e `requester_phone`.

## Base inteira (para contar e filtrar)

- `contabilizei-dataflow.saude_empresa.empresa` tem `cnpj`, `plano`, `status`, `regime_tributario`, `uf`, `municipio`, `ibge`, `cnae_principal` (com `periodo`).
- `contabilizei-dataflow.dw_contabilizeiapp.Empresa` tem `naturezaJuridica`, `abertura` (bool: abertura x migração), `status`, `regimeTributario`, `utilizaCertificadoDigital`.
- `contabilizei-contabilake.operacao_cliente.cnae_empresas` (já lido pelo painel-sync).
- O `src/domain/painel-sync` já tem o motor que copia tabelas do BigQuery para o Postgres por manifest. O banco `painel-assessor` (`dim_cliente`, `dim_cnae`, `dim_certificado`) cobre **só a carteira Experts**: não serve como base geral.

## Lacunas

- Natureza jurídica e tipo de contrato (abertura x migração) não têm API: só o BigQuery (D-1).
- Certificadora: a API só distingue Certisign e Soluti; não há fonte geral para GVS, outra ou sem certificado.
- Status "Em migração" e "Migrada" não aparecem nas fontes acima: falta descobrir o campo.
- Não há busca de processo de abertura por id.
- O `back-worker` (`/experts/dados-empresa`) não é chamado direto pelo atendimento-zendesk: só o `experts-nfs` o usa.
