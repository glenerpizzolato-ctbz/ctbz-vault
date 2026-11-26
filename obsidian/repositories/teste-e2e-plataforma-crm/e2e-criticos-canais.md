---
name: e2e-criticos-canais
description: Testes E2E críticos do squad Canais na métrica de Qualidade (Metabase) ligados às specs do teste-e2e-plataforma-crm, o percentual atual e o que falta (o #3, finalizar atendimento via chat do Fale Conosco, sem a tag @regression desde 2024)
metadata:
  type: reference
tags:
  - teste-e2e-plataforma-crm
  - e2e
  - qualidade
  - canais
repositorio: teste-e2e-plataforma-crm
atualizado_em: 2026-11-26
---

# E2E críticos do squad Canais

Métrica e dashboard: [[metrica-e2e-critico]]. Retrato de 26/11/2026 (extração das 07:05).

## Percentual

- **Executa STG (% criticidade ALTA): 75%** (3 de 4). Meta: 85%.
- Executa STG (% geral): 37,5% (3 de 8 elegíveis; 11 registros excluídos, os E2E antigos da Plataforma Cliente).
- Basta o `test_crm_platform_data_e2e:3` voltar a rodar em stg para o ALTA ir a **100%**.

## Testes do Canais (ativos)

| test_key | Criticidade | Desenv. | Stg | Cenário | Onde está |
| --- | --- | --- | --- | --- | --- |
| `test_crm_platform_data_e2e:3` | ALTO | sim | **não** | Deve finalizar um atendimento via chat do Fale Conosco | `cypress/e2e/autoatendimento/customer-service.cy.js`, **sem `@regression`** |
| `test_crm_platform_data_e2e:4` | ALTO | sim | sim | Deve consultar um atendimento solicitado previamente | `self-service.cy.js` |
| `test_client_platform_data_ui:371` | ALTO | sim | sim | Deve renderizar widget zendesk fale conosco | outro repo (UI da Plataforma Cliente) |
| `test_client_platform_data_ui:372` | ALTO | sim | sim | Deve renderizar tela de autoatendimento ao clicar… | outro repo (UI) |
| `test_client_platform_data_ui:367` | MÉDIO | não | não | Área de chamados e notificações com itens de chamado | não automatizado |
| `test_client_platform_data_ui:370` | MÉDIO | não | não | Navegar para a tela de atendimento específico do chamado | não automatizado |
| `test_client_platform_data_ui:368`, `:369` | BAIXO | não | não | Área de chamados e notificações (sem itens / outras variações) | não automatizado |

Os `test_client_platform_data_e2e:40` a `:50` (Canais) estão `deleted=true`: são os mesmos cenários de autoatendimento migrados para a Plataforma CRM.

## Os demais E2E da Plataforma CRM (outros squads)

| test_key | Squad | Crit. | Stg | Spec |
| --- | --- | --- | --- | --- |
| `:1` histórico do último atendimento | Engajamento | ALTO | sim | `chat-history.cy.js` |
| `:2` voucher do certificado digital | Engajamento | BAIXO | não | `faq.cy.js` (sem tag) |
| `:5` blog encerramento de empresa | Engajamento | MÉDIO | não | `faq.cy.js` (sem tag) |
| `:6` assistente inteligente, serviços adicionais | Engajamento | ALTO | sim | `self-service.cy.js` |
| `:7` gerar novo atendimento (ticket) | Engajamento | ALTO | sim | `self-service.cy.js` (intermitente) |
| `:8` segunda via da fatura | Billing | MÉDIO | não | `invoice.cy.js` (sem tag) |
| `:9` blog certificado já adquirido | Engajamento | BAIXO | não | `faq.cy.js` (sem tag) |
| `:10` contatos dos canais de atendimento | Engajamento | ALTO | sim | `self-service.cy.js` |
| `:11` informe de rendimentos para download | Contábil | BAIXO | não | `self-service.cy.js` (sem tag) |
| `:12` assistente inteligente, mensalidade | Billing | MÉDIO | sim | `invoice.cy.js` |
| `:13` assistente inteligente, informe de rendimentos | Contábil | BAIXO | sim | `self-service.cy.js` |

## O #3 ainda faz sentido?

Sim. O cenário é a entrada principal do chat web: home → botão "Fale conosco" (iframe `iframe-helpdesk`) → Contabilidade → "Quero falar sobre um novo assunto" → tema Impostos / subtema "Quanto vou pagar de imposto (DAS/DARF)…" → FAQ → "Não, ainda preciso de ajuda" → menu de canais (Chat e Email) → Chat → abre o Zendesk Messaging (iframe "Janela de mensagens") e fecha. Pelo [mapa do widget](https://claude.ai/artifact/K9Gd5f9VbosysyYTG8kfgR) ([[widget-tags-roteamento-ouvidoria]]) esse caminho existe; no `master` do widget de 18/11/2026 continuam os `data-testid` (`primary-btn`, `confirm-theme-button`, `confirm-subtheme-button`, `channel-btn`) e os textos ("Quero falar sobre um novo assunto", "ainda preciso de ajuda", "Como você quer falar conosco?").

Histórico: a tag `@regression` saiu em 31/10/2024 (commit `f8482fe`, "removed tag regression from failed test") e não voltou; desde então o teste não roda na pipeline (o job filtra `@regression+@autoatendimento`).

Riscos para ele voltar a passar:

- Flag ConfigCat `ATENDIMENTO_BOT_ULTIMATE_PARA_IA_CHAT`: ligada, a Contabilidade pula tema/subtema e vai direto aos canais. Em stg, os outros testes com tema/subtema e o mesmo usuário (`crm`) passam, então a flag não atinge esse usuário lá.
- Chat só aparece com `elegivelChat` (plano sem "Expert").
- Textos do FAQ de Impostos e do bot (fixture `system-complete-service-through-contact-us.json`, comparação exata e na ordem).
- O passo final depende do Zendesk Messaging do sandbox abrir no iframe e do botão `aria-label="Fechar"`.
- Ouvidoria: se o usuário ficar elegível (ticket nas últimas 24 h, por exemplo do `self-service`), aparece o menu "Atendimento / Reclamação/Elogio" antes dos temas.

Rodar: [[rodar-testes-e2e-plataforma-crm]] (precisa da VPN para stg).
