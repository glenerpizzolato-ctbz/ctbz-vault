---
name: ultimate-indice
description: "Índice do domínio Ultimate: bots de WhatsApp na Ultimate (Zendesk AI agents), roteamento para grupos do Zendesk, endpoints que os fluxos chamam e testes"
metadata:
  type: reference
tags:
  - ultimate-indice
---

# Ultimate

Notas sobre os bots da Ultimate (Zendesk AI agents): fluxos do dialogue builder, roteamento para grupos do Zendesk, endpoints do `atendimento-zendesk` que os fluxos chamam e como testar. O código versionado fica em [[_ultimate-as-a-code-indice|ultimate-as-a-code]].

## Testes e diagnóstico

- [[testar-bot-whatsapp]] — receita para testar o bot em prd com o WhatsApp do Glener: envio no segundo :30, ticket e grupo pela API, fechar sem CSAT, GIF sem vazar conversas, evidência no Jira (scripts em `ultimate/scripts/`)
- [[endpoints-autenticacao-bot]] — endpoints de identificação do bot: empresa (buscar-por-telefone, consulta CNPJ com `emailAssessorOngoing`/`jiraStatus`/`jiraFinalizado`) e processos de abertura (contagem/dados)

## Roteamento N1 Ativação (segmentação N1/N2)

- [[roteamento-n1-ativacao-soci]] — drops por status do SOCI: tabela V1 em prd (pronta para Google Chat), grupos da Entrega 03, diff V1 x V2 (artefato + PDF), conflitos e origem do `statusJira`
- [[testes-roteamento-n1-ativacao]] — plano de testes da Entrega 03 (PRD-177631), por que o teste em prd travou, caminhos e regras de segurança
- [[backup-roteamento-n1-ativacao-v1]] — backup JSON (dialogue builder) do bloco de `statusJira` da V1 (Entrega 02), para rollback da PRD-176172

## Ativação (processo de abertura / SOCI)

- [[ativacao-processos-abertura-teste]] — admin da Abertura (https://admin.contabilizei.com/abertura/sistema-admin/#/processosabertura); processos de teste em prd (SOCI-255767, SOCI-255830): ids, plano, como apontar o telefone do sócio para o seu e consultar como o bot
- [[menu-inic-experts-ramificacoes]] — Menu Inic Experts: `aberturaEmpresa` → tickets → `jiraFinalizado`; Finalizado vai para o menu completo e o Experts Grupo Padrão, não para a Ativação Inbound
- [[rollout-ia-ativacao]] — `flagRolloutIAAtivExp` (~42%, segundo do relógio ≤ 24) e `flagRolloutAtivacaoInboundBP` (100%) calculadas na integração `[zd-fns] GET | config env`; decidem se a conversa de abertura vai para a AIDA Ativação

## Endpoints dos fluxos

- [[validar-email-tomador-nfs]] — `POST .../experts/nfs/tomadores/email/validar`: só checa formato com regex não ancorada; sempre 200 com `isValido`. Origem do `emailAssessorOngoing` (integração `[pltf-crm] GET | consulta CNPJ`, `empresaLogada.assessor`)

- [[logs-conversa-ultimate]] — URL dos conversation logs do dashboard (botId + período + `platformConversationId` do Sunshine, tirado da tag `conversationid:` do ticket)

## Relacionadas

- [[processo-abertura-teste]] (contabilizei-abertura) — criar e manipular processo de abertura de teste
- [[abertura|Informed captain da Abertura]] — Alessandro Voigt Cigoline
- [[dashboard-read-api]] (ultimate-as-a-code) — ler bots/replies de prd pela API do dashboard
- [[zendesk-sunco-prod-politica]] — IA não acessa Zendesk/Sunco de prd
