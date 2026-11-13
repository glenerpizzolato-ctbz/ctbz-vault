---
name: 2026-11-13-mapa-retorno-ativo-ultimate
description: "Mapeamento do retorno de mensagem ativa nos bots main e fina + avisos da Ultimate de prd, que mostrou que o plano do cliente não é checado no retorno, e documentação da leitura segura da Ultimate como código"
metadata:
  type: project
tags:
  - performance
titulo: "Mapa do retorno de ativo nos bots da Ultimate e brecha de plano"
data: 2026-11-13
periodo: 2026QD3
categorias: [processo, qualidade]
impacto: medio
fontes: ["[[retorno-ativo-plano-sem-whatsapp]]", "[[_ultimate-as-a-code-indice]]"]
---

# Mapa do retorno de ativo nos bots da Ultimate e brecha de plano

## Contexto

O time precisava saber o que acontece quando um cliente de plano sem WhatsApp (Básico) responde a uma mensagem ativa, e se forçar o envio encaminha o cliente para atendimento humano ou IA. O fluxo vivia só no dashboard da Ultimate; o mapa em código (`ultimate-as-a-code`) tinha só o welcome reply.

## O que fiz

- Li os bots `[prod] ctbz wpp main` e `[prod] ctbz wpp fina + avisos` pelas rotas internas de leitura do dashboard (com aprovação, sem alterar nada), seguindo o grafo a partir do welcome (147 replies alcançáveis no main), e cruzei com o código do `atendimento-zendesk`, os logs do GKE (fluxos consultados) e o banco de prd (grupos).
- Documentei a leitura segura da API do dashboard e preenchi os ids de prd no `ultimate-as-a-code`, além do mapa nó a nó do retorno de ativo.
- Criei a pasta `mensagem-ativa` no vault e publiquei um explicativo com os dois fluxos (artefato e PDF).

## Resultado

- Ficou claro que o plano só é barrado no envio, e só quando o ativo vai com `cnpj`: no retorno, os dois bots consultam o ativo antes da checagem de plano, e o fina + avisos não tem bloqueio de plano em nenhum caminho (até sem ativo escala para a AIDA Geral).
- O `ultimate-as-a-code` passou a compilar o welcome reply para prd, e qualquer pessoa do time consegue repetir a leitura dos bots com o guia.

## Evidências

- [[retorno-ativo-plano-sem-whatsapp]]
- [[_ultimate-as-a-code-indice]] (branch `docs/mapa-mensagem-ativa` no `ultimate-as-a-code`)
- Artefato: https://claude.ai/artifact/XLQY4YwhSjyWT7PD5Rwf4n
