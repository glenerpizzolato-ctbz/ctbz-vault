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

## Limites da plataforma

- [[whatsapp-limites-botoes|Limites de botões no WhatsApp]] — botão de resposta 20 caracteres, linha de lista 24 (Ultimate/Zendesk e Meta)

## Testes e diagnóstico

- [[ouvidoria-origens-fora-do-horario]] — todas as origens que levam às filas de Ouvidoria (número exclusivo, Super-Ouvidoria do sentinela, botão do chat, Feedback Experts, inativos, Bank, macro, e-mail/Reclame Aqui) e o que cada uma faz fora do expediente
- [[ouvidoria-fora-do-horario]] — Super Ouvidoria fora do expediente (seg a sex 9h–18h): sem menu, mensagem de fora do horário, tag `sys_ouvidoria_fora_de_horario` e ticket direto na fila Ouvidoria [WhatsApp] [Ouvidoria]; sem Corujão nem IA
- [[corujao-fila-noturna-experts]] — Corujão (fila noturna Experts): entradas (cron 22:30 do atendimento-zendesk, reroute do bots-api, Ultimate), saída 09:05 para o Default, critérios, IDs de grupo e pontos frágeis
- [[testar-bot-whatsapp]] — receita para testar o bot em prd com o WhatsApp do Glener: envio no segundo :30, ticket e grupo pela API, fechar sem CSAT, GIF sem vazar conversas, evidência no Jira (scripts em `ultimate/scripts/`)
- [[endpoints-autenticacao-bot]] — endpoints de identificação do bot: empresa (buscar-por-telefone, consulta CNPJ com `emailAssessorOngoing`/`jiraStatus`/`jiraFinalizado`) e processos de abertura (contagem/dados)

## Roteamento N1 Ativação (segmentação N1/N2)

- [[roteamento-n1-ativacao-soci]] — drops por status do SOCI: tabela V1 em prd (pronta para Google Chat), grupos da Entrega 03, diff V1 x V2 (artefato + PDF), conflitos e origem do `statusJira`
- [[testes-roteamento-n1-ativacao]] — plano de testes da Entrega 03 (PRD-177631), por que o teste em prd travou, caminhos e regras de segurança
- [[testes-roteamento-bp-n1-n2]] — plano de testes da PRD-176795 (BP WhatsApp: SOCI/migração não finalizados → AIDA 24/7 Ativação BP, senão AIDA Geral 24/7 BP): matriz, regressões, massa e pontos em aberto
- [[backup-roteamento-n1-ativacao-v1]] — backup JSON (dialogue builder) do bloco de `statusJira` da V1 (Entrega 02), para rollback da PRD-176172

## Ativação (processo de abertura / SOCI)

- [[ativacao-processos-abertura-teste]] — admin da Abertura (https://admin.contabilizei.com/abertura/sistema-admin/#/processosabertura); processos de teste em prd (SOCI-255767, SOCI-255830): ids, plano, como apontar o telefone do sócio para o seu e consultar como o bot
- [[empresa-teste-bp-ativa]] — empresa de testes BP ativa em prd (CNPJ 51596322000186, AVANCADO) ligada ao telefone de teste; campos de autenticação que o bot recebe (abertura, jiraFinalizado)
- [[menu-inic-experts-ramificacoes]] — Menu Inic Experts: `aberturaEmpresa` → tickets → `jiraFinalizado`; Finalizado vai para o menu completo e o Experts Grupo Padrão, não para a Ativação Inbound
- [[rollout-ia-ativacao]] — `flagRolloutIAAtivExp` (~42%, segundo do relógio ≤ 24) e `flagRolloutAtivacaoInboundBP` (100%) calculadas na integração `[zd-fns] GET | config env`; decidem se a conversa de abertura vai para a AIDA Ativação

## CSAT

- [[csat-quero-atendimento-ramificacoes]] — destinos do "Quero atendimento" no Wpp Exp | CSAT v19 (FUP → Business Hours; retorno → ReRoute/Init session/Concierge/Business Hours/reautenticação) e como ler o dialogue builder pela API

## Endpoints dos fluxos

- [[validar-email-tomador-nfs]] — `POST .../experts/nfs/tomadores/email/validar`: só checa formato com regex não ancorada; sempre 200 com `isValido`. Origem do `emailAssessorOngoing` (integração `[pltf-crm] GET | consulta CNPJ`, `empresaLogada.assessor`)

- [[logs-conversa-ultimate]] — URL dos conversation logs do dashboard (botId + período + `platformConversationId` do Sunshine, tirado da tag `conversationid:` do ticket)

## Relacionadas

- [[processo-abertura-teste]] (contabilizei-abertura) — criar e manipular processo de abertura de teste
- [[abertura|Informed captain da Abertura]] — Alessandro Voigt Cigoline
- [[dashboard-read-api]] (ultimate-as-a-code) — ler bots/replies de prd pela API do dashboard
- [[zendesk-sunco-prod-politica]] — IA não acessa Zendesk/Sunco de prd
