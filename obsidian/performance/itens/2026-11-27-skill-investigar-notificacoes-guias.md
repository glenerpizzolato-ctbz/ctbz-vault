---
name: 2026-11-27-skill-investigar-notificacoes-guias
description: "Skill investigar-notificacoes-guias-empresa: diagnostica por CNPJ e competência por que o cliente não recebeu a notificação do agrupamento de guias ou a avulsa; achou a causa do PRC-153307 que o Fiscal não tinha conseguido por falta de logs"
metadata:
  type: project
tags:
  - performance
titulo: "Diagnóstico por CNPJ das notificações de guias não recebidas (skill investigar-notificacoes-guias-empresa)"
data: 2026-11-27
periodo: 2026QD3
categorias: [ia, ajuda-outros-times, qualidade]
impacto: medio
fontes: ["[[PRD-174011 - Cliente não recebe notificação do agrupamento de guias]]"]
---

# Diagnóstico por CNPJ das notificações de guias não recebidas

## Contexto

PRC-153307: cliente Experts reclamou de não ter recebido o empacotamento das guias em 04, 05, 06 e 10/2026. O Fiscal e o CRM não acharam a causa porque os logs só guardam 30 dias, e o chamado passou por três times antes de chegar à Engenharia Canais.

## O que fiz

- Investiguei só pelos bancos (agrupamento, experts-service, WhatsApp ativo) e pelo BigQuery, sem depender de log.
- Criei a skill `investigar-notificacoes-guias-empresa` (script Python, só leitura em prod), que cruza grupo, histórico, itens, guias, controle de notificação, WhatsApp ativo, avulsas do experts-service e o plano mês a mês, e classifica cada competência com a causa e o que fazer. Validada com o CNPJ do PRC-153307 e com o do PRC-151642.

## Resultado

- Causa achada em ~20 s por execução: 04–06/2026 a empresa estava no plano AVANCADO (fora do agrupamento na época); 10/2026 uma DARF duplicada órfã travou o grupo. Nenhum dos dois casos tinha avulsa (explicado pelo "buraco de silêncio" do experts-service).
- Causa nova registrada no playbook (empresa sem grupo por plano), que o roteiro anterior não cobria.

## Evidências

- PRC-153307, playbook [[PRD-174011 - Cliente não recebe notificação do agrupamento de guias]].
- Skill em `~/ctbz-vault/skills/impostos/investigar-notificacoes-guias-empresa/`.
