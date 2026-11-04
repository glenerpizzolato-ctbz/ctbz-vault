---
name: 2026-10-27-skills-diagnostico-teste-bots
description: "Skills de diagnóstico e teste dos bots de WhatsApp"
metadata:
  type: project
tags:
  - performance
titulo: "Skills de diagnóstico e teste dos bots de WhatsApp"
data: 2026-10-27
periodo: 2026QD3
categorias:
  - ia
  - qualidade
impacto: medio
fontes:
  - "[[api-gateway-bots-whatsapp]]"
  - "[[status-empresa-bigquery]]"
  - "[[rotas-busca-empresa]]"
---

# Skills de diagnóstico e teste dos bots de WhatsApp

- **Período:** 2026QD3 · **Categorias:** ia, qualidade · **Impacto:** medio

## Contexto

Diagnosticar por que o bot não reconhecia um cliente exigia chamar o gateway com chave copiada à mão, e testar em prd deixava tickets nas filas da Zendesk.

## O que fiz

Criei skills que autenticam e consultam empresas como o próprio bot (`buscar-empresas-por-telefone`, `autenticar-empresa-whatsapp`, sem expor segredos), buscam massa de teste por plano no BigQuery (`buscar-empresas-por-plano`) e fecham só os tickets do meu usuário de teste (`fechar-tickets-teste-zendesk`). Também destravei o token do monolito em dev e documentei o passo a passo.

## Resultado

Diagnóstico do bot em prd e dev a partir de telefone ou CNPJ, massa de teste reutilizável e testes em prd sem sujar as filas dos times.

## Evidências

- [[api-gateway-bots-whatsapp]]
- [[status-empresa-bigquery]]
- [[rotas-busca-empresa]]
