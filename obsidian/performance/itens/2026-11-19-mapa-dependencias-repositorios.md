---
name: 2026-11-19-mapa-dependencias-repositorios
description: "Mapa de dependências por repositório no vault (o que consome e quem o consome), com levantamento automático pelo código em 123 repositórios e a regra de os agentes confirmarem e espelharem cada contrato, usado pela revisão de MRs para achar quebra de fluxo dependente"
metadata:
  type: project
tags:
  - performance
titulo: "Mapa de dependências entre repositórios no vault, mantido pelos agentes"
data: 2026-11-19
periodo: 2026QD3
categorias: [processo, ia, qualidade]
impacto: medio
fontes: ["[[dependencias-entre-repositorios]]", "[[dependencias-contato-service]]", "[[2026-11-04-auto-approve-mrs]]"]
---

# Mapa de dependências entre repositórios no vault, mantido pelos agentes

## Contexto

O vault guardava dependências entre repositórios em três lugares soltos: o catálogo GCP (`infra/`, gerado, só tópicos, filas e serviços), um grafo manual de chamadas de Canais/Experts/AIDA (fotografia de um colega, sem o contrato) e uma seção `## Consumidores` que só um repositório (de 127) tinha. A revisão de MRs que procura quebra de fluxo dependente dependia dessas notas para achar quem consome o contrato que o diff muda.

## O que fiz

- Defini o padrão: cada repositório tem a nota `dependencias-<repo>.md`, com **Consome** (repositórios internos, libs internas, infra GCP, bancos e dados, terceiros) e **Consumido por**, uma linha por contrato confirmado no código, sempre espelhada nas duas pontas.
- Criei a skill `mapear-dependencias`, com um script que gera o levantamento automático de candidatos: cruza por nome os 129 repositórios clonados (com cache por HEAD), lê os manifestos (libs internas, drivers de banco, SDKs de terceiros), os hosts de terceiros no código, as tabelas do BigQuery citadas, o catálogo `infra/` e o grafo manual. O script só reescreve o bloco automático e não toca no que foi confirmado.
- Gerei a nota nos 123 repositórios do vault (mais `meta-webhooks`, que entrou no vault), confirmei no código as dependências do `contato-service` (6 dependências e 5 consumidores com o contrato) e espelhei nos consumidores.
- Coloquei a regra nas instruções dos agentes (criar a nota ao começar num repositório, registrar e espelhar cada dependência confirmada, ler o Consumido por antes de mudar um contrato) e fiz a revisão de MRs do BahCode ler primeiro o Consumido por.

## Resultado

- De 1 para 123 repositórios com mapa de dependências; a varredura completa leva ~8 s.
- A revisão de MRs passa a ter um lugar fixo para achar consumidores, que cresce sozinho conforme o trabalho em cada repositório confirma as dependências.

## Evidências

- [[dependencias-entre-repositorios]] (padrão) e [[dependencias-contato-service]] (exemplo confirmado)
- Skill `mapear-dependencias` (`~/ctbz-vault/skills/repositorios/`), commits `a07c839`, `fb4ad43`, `1f214b3` e `7c72bfe` do ctbz-vault
- Commit `3cdc4e6` do ide-bahcode (prompts da quebra de fluxo dependente)
