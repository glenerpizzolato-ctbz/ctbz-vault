---
name: menu-inic-experts-ramificacoes
description: "Ramificações do reply Wpp Exp | Menu Inic v56 (bot wpp main prd): aberturaEmpresa, tickets abertos, jiraFinalizado, menu completo → validar e-mail Ongoing → Experts Grupo Padrão; menu sem Jira → Ativação Inbound (drops SOCI). Onde entra o caso Finalizado da PRD-176172"
metadata:
  type: reference
tags:
  - ultimate
  - ativacao
  - roteamento
---

# Menu Inic Experts: ramificações

Lido em 2026-11-16 no reply `Wpp Exp | Menu Inic v56 | 172337 from 162644` (`6ad788b768e0b901e98023ce`) do bot `[prod] ctbz wpp main`, pela API de leitura do dashboard ([[dashboard-read-api]]). Diagrama: artefato "Menu Inic Experts: ramificações" (https://claude.ai/artifact/6y9ef5ufcvPswRe2UP1Koo).

- Depois de carteira, horário comercial e mensagens de aviso: `COND aberturaEmpresa`.
  - `false` (empresa não está em abertura) → menu completo (concierge se `FLAGS_V2` inclui `allow_concierge_experts`, grupo `29190745372444`; senão allowlist NF → menu com Emitir NF / **Falar com Assessor** / Serviços rápidos / Saúde e Conta PJ / Reclame / Informe).
  - `true` → `[atnd-zd] GET | status tickets by CNPJ`: se `ticketsAbertosQuantidade > 0` → `Pointer | Status Tickets`; senão → `COND jiraFinalizado`:
    - `true` → **mesmo menu completo da empresa ativa**;
    - `false` → menu sem Jira (2 Falar com minha Assessoria → `Pointer | Ativacao Inbound - Wpp Shared`, onde ficam os drops por `statusJira` da [[roteamento-n1-ativacao-soci|PRD-176172]]; 3 Plano de saúde e 4 Conta PJ → validar e-mail Ongoing → grupo padrão; 5 → Router Business Hours);
    - vazio → "Sistema temporariamente indisponível".
- **Falar com Assessor** (nó `6a6a04c9767f8e68efdda948`) → integração `Contabilizei - Experts - Validar Email - Ongoing` ([[validar-email-tomador-nfs|emailAssessorOngoing]]) → `isValidoValidarEmail` true → flag `EXP_TRIAGEM_IA` (true → `Escalate | Triagem IA - Wpp Exp [C]`; false → escala); inválido → escala. A escala vai para **`Experts - Grupo Padrão [WHATSAPP] [Experts]` (15320473247900)**.
- **Consequência para a PRD-176172:** cliente com Jira Finalizado nunca passa pela Ativação Inbound: ele vai para o menu completo e termina no Experts Grupo Padrão. O pedido da PRD (Finalizado → Onboarding [Experts] / AIDA Geral [BP]) precisa ser feito no ramo `jiraFinalizado = true` (ou depois do Validar Email Ongoing), e não nos drops de Ativação.
