---
name: endpoints-autenticacao-bot
description: "Endpoints que o bot WhatsApp Experts (Ultimate) usa para identificar o cliente: empresa por telefone/CNPJ (plataforma-crm-web via consulta CNPJ: plano, jiraStatus, jiraFinalizado, abertura, assessor/emailAssessorOngoing) e processos de abertura por telefone (atendimento-zendesk → Abertura); como chamar e o que cada um devolve"
metadata:
  type: reference
tags:
  - ultimate
  - autenticacao
  - atendimento-zendesk
  - plataforma-crm-web
---

# Endpoints de autenticação/identificação do bot

Conferido em 2026-11-16 (código e dashboard). Todos passam pelo API gateway (Kong) do atendimento; as credenciais (url e `x-api-key`) vêm da cloud function `zendeskbot-config` e ficam em cache na skill `buscar-empresas-por-telefone` (`scripts/bots_api.py`: `credentials('prd')`, `gateway_headers`).

## Empresa (cliente já com CNPJ)

| Integração na Ultimate | Rota | O que devolve |
| --- | --- | --- |
| `[pltf-crm] POST \| count CNPJs (only count) - Shared` | `…/plataforma/atendimento/v2/bots/whatsapp/dados-cliente/buscar-por-telefone` (`plataforma-crm-web`) | empresas do telefone (ativas/rascunho, inativas, qualquer status; BP x Experts). Skill `buscar-empresas-por-telefone` |
| `[pltf-crm] GET \| consulta CNPJ - Shared` (`673b8c73da41e7fc95e7a4bf`, no reply `Wpp Shared \| Id Empresa Auth v02`) | `POST …/dados-cliente/buscar-por-telefone-e-cnpj` (`BuscarDadosGeralWhatsAppBotFacade`) | `empresaLogada`: `categoriaPlano`, `jiraStatus` → `statusJira`, `jiraFinalizado`, `abertura` → `aberturaEmpresa`, `assessor` → **`emailAssessorOngoing`** ([[validar-email-tomador-nfs]]), regime, município etc. |
| autenticação básico/padrão | `…/fluxo/interacao/api/v1/bots/whatsapp/autenticacao/basico-padrao` (`atendimento-zendesk`) | statusBot, fluxos por área. Skill `autenticar-empresa-whatsapp`; sem CNPJ responde 500 |

- `jiraStatus` só vem quando a empresa tem `idProcesso` e `identificarEmpresaAbertura()` é verdadeiro; vem da Abertura com cache de 3 h por `idProcesso` (`AberturaFacade.consultarProcessoPorId`).

## Processo de abertura (sem empresa ativa)

Base: `/atendimento/zendesk/bots/whatsapp/fluxo/interacao/api/v1/bots/whatsapp/identificacao/processos` (`atendimento-zendesk`, **GET**). Bruno: `experts-bruno/ultimate-ai-bots/bots/wpp-main/id_abertura/`.

- `GET /contagem/{+55telefone}` → Abertura `integracao/twilio/processo/telefone/{tel}` (empresas da Abertura cujo **sócio** tem o telefone). Descarta status `FINALIZADO`; separa `experts` x `basicoPadraoMultibeneficios` pelo plano do processo; o bot usa o primeiro de `listasIDs.total` (`primeiroIdProcessoListTotal`, `idProcessoExperts`, `totalProcessosAberturaListTotal`).
- `GET /dados/{idProcesso}/telefone/{+55telefone}` → Abertura `integracao/twilio/{id}/processo`: `statusJira` (= `ProcessoAbertura.status`), `plano`, `idJira`, empresa, assessor. Não confere se o telefone é do processo.
- Sem cache no `atendimento-zendesk`. Detalhes da cadeia e do sync com o Jira: [[roteamento-n1-ativacao-soci]].

## Config

- `[zd-fns] GET | config env - Shared` (`668c345bc2932ebcec62a717`): carrega a config do bot e calcula os rollouts da IA de Ativação ([[rollout-ia-ativacao]]).
