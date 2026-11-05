---
name: performance-indice
description: "Evidências para o ciclo de performance/promoção: segurança, IA, ajuda a outros times, entregas, incidentes, processo, qualidade e liderança"
metadata:
  type: reference
tags:
  - performance-indice
---

# Evidências de performance

Fonte da verdade das evidências para o ciclo de performance e promoção: tudo que eu fiz e que mostra impacto além do esperado. Os agentes registram aqui **automaticamente, sem perguntar**, assim que algo relevante acontece numa sessão.

## Como usar

- **Registrar:** criar `itens/AAAA-MM-DD-<slug>.md` (data da entrega/ocorrência) com o front-matter abaixo e as seções `Contexto`, `O que fiz`, `Resultado` e `Evidências`, e adicionar a linha na seção da categoria principal neste índice (mais recente primeiro).
- **Mesmo tema, nova ocorrência:** enriquecer a nota existente (nova data em `Resultado`/`Evidências`, `atualizado_em`) em vez de criar outra.
- **Resultado com número sempre que houver:** clientes afetados, tempo economizado, chamados evitados, custo, cobertura. Nunca inventar: sem dado, descrever o efeito qualitativo.
- **Evidências linkáveis:** wikilinks das notas do vault (PRD, PRC, incidente, repositório), links de Jira/MR/post-mortem e quem foi ajudado (time/squad, não dados de clientes).
- **Na hora da avaliação:** filtrar por `periodo` em [[performance.base|Tabela filtrável]] e montar o texto a partir das notas.

## Front-matter

```yaml
name: <slug>
description: "<uma linha>"
metadata:
  type: project
tags:
  - performance
titulo: "<título>"
data: AAAA-MM-DD
periodo: AAAAQDn
categorias: [<uma ou mais do vocabulário>]
impacto: alto | medio
fontes: ["[[PRD-xxxxx]]", "[[nota]]"]
```

## Vocabulário

- **categorias:** `seguranca` (vulnerabilidades, CVEs, riscos de dados/autenticação descobertos ou corrigidos); `ia` (uso bem pensado de IA: produtos com LLM, skills/automações com agentes, avaliação de modelos); `outros-times` (soluções, contribuições ou investigações para outras squads); `entrega` (entregas de impacto de negócio: produtos, fluxos, migrações); `incidente` (participação e solução de incidentes, IPs, post-mortems, levantamento de afetados); `processo` (padrões, playbooks e processos criados para o time); `qualidade` (confiabilidade, observabilidade, débito técnico, custo); `lideranca` (condução de iniciativas, mentoria, compartilhamento de conhecimento).
- **impacto:** `alto` (afeta clientes/negócio ou vários times), `medio` (afeta o time ou um fluxo).
- **periodo:** `AAAAQDn` (quadrimestre: QD1 = jan–abr, QD2 = mai–ago, QD3 = set–dez), igual às [[_prds-indice|PRDs]].

## Evidências

### Segurança

- [[2026-10-30-cve-node2shell|Coordenação da correção da CVE-2026-111497 (node2shell)]] — 2026QD3, impacto alto
- [[2026-10-30-remocao-servicos-expostos|Remoção de serviços Cloud Run esquecidos e expostos na internet]] — 2026QD3, impacto alto
- [[2025-08-26-copilot-lib-vulneravel|Remoção de biblioteca com possível vulnerabilidade no Copilot]] — 2025QD2, impacto medio
- [[2024-07-23-bloqueio-nao-autenticados-ura|Bloqueio de atendimento a clientes não autenticados na URA do WhatsApp]] — 2024QD2, impacto alto

### IA

- [[2026-11-05-opportunities-scan|Varredura diária com IA de oportunidades de melhoria (Opportunities)]] — 2026QD3, impacto medio
- [[2026-11-04-auto-approve-mrs|Auto-approve de MRs do time com revisão por IA e regras restritivas]] — 2026QD3, impacto medio
- [[2026-11-04-skills-fluxo-desenvolvimento|Automação do fluxo de MR com IA (skills mr, comentario, pipe)]] — 2026QD3, impacto medio
- [[2026-11-03-skill-mapear-erros-ultimate|Levantamento de clientes afetados por incidente (skill mapear-erros-ultimate)]] — 2026QD3, impacto alto
- [[2026-10-27-skills-diagnostico-teste-bots|Skills de diagnóstico e teste dos bots de WhatsApp]] — 2026QD3, impacto medio
- [[2026-10-09-skill-catalogo-gcp|Catálogo GCP automatizado com IA (skill atualizar-catalogo-gcp)]] — 2026QD3, impacto alto
- [[2026-10-09-skill-prds-vault|Sincronização das demandas do vault com o Jira (skill atualizar-prds-vault)]] — 2026QD3, impacto medio
- [[2026-03-12-copilot-acoes-emissao-nf|Módulo de ações do Copilot: emissão de NF sugerida por IA]] — 2026QD1, impacto alto
- [[2026-03-06-copilot-semelhanca-carteira-modelo|Copilot: análise de semelhança, expansão para a carteira e troca de modelo]] — 2026QD1, impacto medio
- [[2025-12-22-copilot-envio-automatico-validador|Envio automático de respostas do Copilot com validador de IA]] — 2025QD3, impacto alto
- [[2025-10-10-copilot-acrs-qualidade|ACRs de qualidade das respostas do Copilot]] — 2025QD3, impacto medio
- [[2025-08-07-monitoria-ia|Monitoria de atendimentos com IA]] — 2025QD2, impacto alto
- [[2025-08-05-copilot-experts|Copilot do Zendesk adaptado para o atendimento Experts]] — 2025QD2, impacto alto
- [[2025-03-31-encerramento-automatico-ia|Encerramento automático de atendimentos com IA (Experts)]] — 2025QD1, impacto alto

### Outros times

- [[2026-10-30-pipeline-central-gen2|Correções na pipeline central de devops (DEPLOY_FROM_MR, Go, gen2)]] — 2026QD3, impacto medio
- [[2026-10-30-ouvidoria-desidratacao|Desidratação da Ouvidoria e menu da Super Ouvidoria]] — 2026QD3, impacto medio
- [[2026-05-04-telefone-ativacao|Padronização do telefone na Ativação (outro time)]] — 2026QD2, impacto medio

### Entregas

- [[2026-10-29-agrupamento-guias-bp|Agrupamento de guias para o plano BP (e separação Experts SN/LP)]] — 2026QD3, impacto alto
- [[2026-10-15-agrupamento-guias-service-redesenho|Redesenho da notificação do agrupamento de guias (agrupamento-guias-service)]] — 2026QD3, impacto alto
- [[2026-10-08-opt-out-notificacoes-impostos|Opt-out de notificações de impostos por contato (WhatsApp e e-mail)]] — 2026QD3, impacto alto
- [[2026-09-29-csat-transbordo-contencao|CSAT Transbordo: regras de contenção e tickets travados]] — 2026QD3, impacto alto
- [[2026-09-22-autosservico-admin-templates|Autosserviço para o negócio: atendimento-canais-admin e templates ricos]] — 2026QD3, impacto medio
- [[2026-09-17-clientes-inativos-whatsapp|Atendimento de clientes inativos no WhatsApp do Zendesk]] — 2026QD3, impacto alto
- [[2026-09-17-remocao-escolha-area-ura|Remoção da escolha "Contabilidade/Bank/Corretora" na URA]] — 2026QD3, impacto medio
- [[2026-08-21-explicacao-proativa-das|Explicação proativa da variação de impostos (DAS)]] — 2026QD2, impacto alto
- [[2026-08-07-pesquisas-whatsapp-flows|Pesquisas nativas com WhatsApp Flows]] — 2026QD2, impacto alto
- [[2026-07-22-migracao-agrupamento-guias-gcp|Migração do ms-agrupamento-guias para o GCP de atendimento-canais]] — 2026QD2, impacto alto
- [[2026-07-14-segmentacao-wpp-n1-n2|Segmentação dos fluxos de WhatsApp Expert: N1 Ativação e N2 Onboarding]] — 2026QD2, impacto medio
- [[2026-05-22-cnpj-alfanumerico|Adequação ao CNPJ alfanumérico]] — 2026QD2, impacto alto
- [[2026-01-08-ura-plano-medicos|Nova URA multibenefícios para o Plano Médicos]] — 2026QD1, impacto medio
- [[2025-04-01-ativo-guias-imposto-experts|WhatsApp ativo e e-mail de guias de imposto para Experts]] — 2025QD1, impacto alto
- [[2025-02-19-sinalizacao-clientes-criticos-zendesk|Sinalização de clientes complexos ou críticos no Zendesk]] — 2025QD1, impacto medio
- [[2025-02-07-autoatendimento-documentos-informe|Autoatendimento na URA: documentos e informe de rendimentos]] — 2025QD1, impacto medio
- [[2024-12-27-nf-exterior-ura|Emissão automática de NF para o exterior pela URA]] — 2024QD3, impacto alto
- [[2024-12-09-migracao-twilio-zendesk-sso|Migração do atendimento Experts da Twilio para o Zendesk, com SSO]] — 2024QD3, impacto alto
- [[2024-07-15-holerite-por-email|Envio de holerite por e-mail]] — 2024QD2, impacto medio

### Incidentes

- [[2026-11-03-incidente-ip-4361-ultimate|Incidente IP-4361 nos bots de WhatsApp: diagnóstico e post-mortem]] — 2026QD3, impacto alto
- [[2026-10-28-incidente-deploy-experts-functions|Incidente no deploy de prd do experts-functions e regressão do html-to-pdf]] — 2026QD3, impacto alto
- [[2026-10-28-acrs-notificacoes-qd3|Análise de ACRs de notificações e e-mail (QD3/2026)]] — 2026QD3, impacto medio
- [[2026-04-23-acr-retentativas-ativo|ACR: excesso de retentativas no envio de ativo]] — 2026QD1, impacto medio
- [[2025-12-19-tickets-retidos-corujao|Tickets retidos na transição Corujão → Default]] — 2025QD3, impacto medio

### Processo

- [[2026-10-29-padrao-rotina-deploy|Padrão de rotina separada para o deploy (cycle time)]] — 2026QD3, impacto medio
- [[2026-10-15-padrao-pubsub|Padrão de nomenclatura de Pub/Sub do time]] — 2026QD3, impacto medio
- [[2026-10-01-aviso-mrs-nao-revisados|Aviso automático de MRs não revisados]] — 2026QD3, impacto medio
- [[2026-08-24-playbooks-prc|Base de playbooks de PRC (uma nota por problema)]] — 2026QD2, impacto alto

### Qualidade

- [[2026-11-03-padroes-sonar-pipeline|Padrões de diagnóstico de Sonar e pipeline]] — 2026QD3, impacto medio

### Liderança

- [[2026-11-04-vault-conhecimento-time|Base de conhecimento do time no vault, com skills corporativas]] — 2026QD3, impacto medio
