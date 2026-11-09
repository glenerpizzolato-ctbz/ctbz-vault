---
name: contagem-processos-abertura-por-telefone
description: "Como a Ultimate conta os processos de abertura de um telefone (GET bots/whatsapp/identificacao/processos/contagem/:telefone): rota da abertura chamada, busca pelo telefone do sócio e exclusão dos processos com statusJira Finalizado"
metadata:
  type: reference
tags:
  - atendimento-zendesk
  - contabilizei-abertura
  - ultimate
---

# Contagem de processos de abertura por telefone (bot da Ultimate)

A Ultimate chama `GET /bots/whatsapp/identificacao/processos/contagem/:telefone` do atendimento-zendesk (`WhatsappIdentificacaoProcessosController`).

## Fluxo

1. `ValidarTelefoneInternacionalHelper`: o telefone **precisa começar com `+`** (senão 400).
2. `TelefoneUtil.formatar` → E.164 e `DadosClienteAberturaService.buscarProcessosPorTelefone` chama o contabilizei-abertura: `GET {abertura}/rest/integracao/twilio/processo/telefone/{telefone}?auth_token=...` (404/400 viram lista vazia).
3. No contabilizei-abertura (`ProcessoAberturaService.getAllProcessosByTelefone`): `MapearTelefonesPlataformaHelper` gera as variantes com e sem o 9 (só quando vem `+55`) e a query é `empresaDAO.getByManyTelefonesSocio` = **`socios.telefone in [...]`**, ou seja, busca pelo **telefone do sócio**, comparação exata só com dígitos.
4. De volta no atendimento-zendesk, `WhatsAppProcessoUtil.contarProcessos` **descarta os processos com `statusJira` = `FINALIZADO`** (`StatusProcessoParaExclusao`) e separa experts x básico/padrão/multibenefícios.

## Armadilha: processo Finalizado conta zero

Se o processo do cliente já foi finalizado no Jira (SOCI em `Finalizado`, empresa ativada), a abertura devolve o processo, mas a contagem volta `total: 0`. É intencional: depois da ativação, o cliente deve ser identificado pela empresa na plataforma (`buscar-por-telefone` da plataforma-crm-web), não pelo processo. O campo "Status do processo" do card (ex: `AG. COMPENSAÇÃO`) não é o que conta: vale o status do card (`statusJira`).

## Armadilha: telefone do sócio gravado errado na abertura

A busca é por igualdade exata em `socios.telefone` (só com/sem o 9). Se o telefone do sócio foi salvo errado no cadastro do processo, a contagem volta 0 enquanto o processo está em andamento, e a empresa também não aparece na plataforma porque ainda não foi ativada: o cliente fica sem nada. O campo `[SOCI] Telefone` do card é gravado pelo usuário `Contabilizei Abertura` e espelha o telefone do sócio da abertura, então o histórico do card mostra o que estava salvo em cada data.

Caso real (conversa de 2026-10-14, analisado em 2026-11-09): telefone `62995455303`, SOCI-564025. Em 2026-10-05 17:48, quando o cadastro foi finalizado, a abertura gravou `69954553032` (o `2` do DDD foi parar no fim, provavelmente erro de digitação/máscara no cadastro). Em 14/10 o card estava em `Preenchimento MT` → `Ag Assinatura Cliente MT` (não Finalizado), mas a busca procurou `[6295455303, 62995455303]` e não achou o processo. Em 19/10 11:14 a abertura gravou `69995455303` (ainda errado), às 11:24 uma analista corrigiu o card para `62995455303` e às 12:06 os "Dados dos sócios" vindos da abertura já traziam o número certo. Ativação em 19/10 e card Finalizado em 20/10 (aí a contagem passa a dar 0 pela exclusão de Finalizado, mas a empresa já aparece ativa na plataforma).

Segundo caso, mesmo padrão (conversa de 2026-10-02): telefone `11964125305`, SOCI-562684 (processo 5164074593943552, Expert Essencial). O card nasceu com `11964125305` e em 2026-10-01 14:38, no cadastro, a abertura gravou **`11958131862`** (outro número, não erro de digitação). Em 02/10 o card passou por `Consultar DBE Auto` → `Aguardando Pagamento (Auto)` → `Aguardando assinatura` (em aberto) e a busca não achou nada. Em 05/10 10:11 uma analista corrigiu o card para `11964125305`, em 06/10 os "Dados dos sócios" da abertura já traziam o número certo, a ativação foi em 06/10 e o card foi Finalizado em 07/10.

Padrão dos dois casos: o `[SOCI] Telefone` nasce com o telefone da venda (o que o cliente usa no WhatsApp) e é **sobrescrito pelo telefone do sócio informado no cadastro** do processo (autor `Contabilizei Abertura`, junto de campos como IRPF/Tipo Endereço). Se o cliente informa outro número ou digita errado, ele some da busca por telefone até alguém corrigir à mão. Para conferir um caso, ler o histórico do card (`listJiraIssueChangelogs`) e ver o valor de `[SOCI] Telefone` e o `status` na data da conversa.

Situação em 2026-11-09: telefone `62995455303`, SOCI-564025 `Finalizado` desde 2026-10-20 (ativação em 2026-10-19). A abertura devolveu o processo (com `+5562995455303` e com `62995455303`); a contagem do bot deu 0; a plataforma achou a empresa ativa (CNPJ 69679731000101, plano AVANCADO) pelo mesmo telefone.

## Como conferir

- Rota da abertura: experts-bruno `contabilizei-abertura/integracao/tw/processo/{telefone}.bru` (token SSO de prd em `.env`, `sso_token_prod`), ou `curl "https://contabilizei-abertura.appspot.com/rest/integracao/twilio/processo/telefone/%2B55<ddd><num>?auth_token=$sso_token_prod"` e olhar o `statusJira` de cada item.
- Empresas do telefone: skill `buscar-empresas-por-telefone`.
