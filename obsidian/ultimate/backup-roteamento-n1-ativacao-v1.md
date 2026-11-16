---
name: backup-roteamento-n1-ativacao-v1
description: "Backup (JSON exportado do dialogue builder) da árvore de roteamento N1 Ativação por status do SOCI na versão da Entrega 02 (V1), antes da PRD-176172, para rollback, já que o fluxo da Ultimate não é versionado"
metadata:
  type: reference
tags:
  - ultimate
  - backup
  - rollback
  - ativacao
arquivo: "backups/2026-11-16-roteamento-n1-ativacao-v1-entrega02.json"
---

# Backup do roteamento N1 Ativação (V1, Entrega 02)

- **Arquivo:** `ultimate/backups/2026-11-16-roteamento-n1-ativacao-v1-entrega02.json` (58 KB, sha256 começa com `db6baddb7e5e3ba7`). Exportado pelo Glener do dialogue builder do bot `[prod] ctbz wpp main` (`66c6220557465548f3ff0d6e`) e salvo em 2026-11-16, como referência de rollback da [[roteamento-n1-ativacao-soci|Entrega 03 (PRD-176172)]].
- **O que é:** o bloco a partir do nó `6afb3f0946b0921fe8a6364b` (`CONDITIONAL_ATTRIBUTE` em `statusJira`), com 37 nós: 15 cenários de condição, 6 condições (1 em `statusJira` e 5 em `plano`, que separam Experts de BP em cada grupo) e 10 escalonamentos.
- **Conteúdo = tabela V1** de [[roteamento-n1-ativacao-soci]]:
  - grupos `28283501432220` Cadastro, `30023019944860` Pré CNPJ - Módulo tributário, `28283527238556` Pós Vendas, `28283155272220` Pré CNPJ e `5318551320604` Atendimento (ELSE), cada um com um escalonamento para Experts e outro para BP;
  - status V1: Aguardando Formatura no Cadastro, Ag Análise MT / Aguardando DBE MT / Aguardando Ecac / Gerar DBE MT / Protocolo no Ecac no MT, Em Stand-by no Pós Vendas, assinatura/protocolo e [SEVEN] Exigência/Pendência no Pré CNPJ;
  - sem os grupos novos da V2 (Assinatura JC `30023034651676`, Retenção `29996619254940`, AIDA BP, Onboarding).
- **Tag do ELSE Experts:** o escalonamento de Experts para `5318551320604` tem a ação `6a3c2b6ca6d3b511dfd4d607` (na V1, a que adiciona `sys_grupo_ativacao_exp`). Nos testes da V2 a tag não apareceu no ELSE ([[testes-roteamento-n1-ativacao]]): conferir se a ação foi mantida no fluxo novo.

## Como usar no rollback

1. No dialogue builder, abrir o reply do encaminhamento N1 Ativação e localizar o bloco de `statusJira`.
2. Usar o JSON como referência para recriar ou colar o bloco (o formato é o da cópia de nós do builder: `nodeType`, `children`, `conditionData`, `textData.escalateTo`, `actionIds`).
3. Conferir depois da troca: grupos de cada ramo, o `plano` Experts/BP e a ação de tag no ELSE de Experts. Validar com um cenário de teste ([[testar-bot-whatsapp]]).
