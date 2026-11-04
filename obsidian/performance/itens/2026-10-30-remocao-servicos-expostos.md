---
name: 2026-10-30-remocao-servicos-expostos
description: "Remoção de serviços Cloud Run esquecidos e expostos na internet"
metadata:
  type: project
tags:
  - performance
titulo: "Remoção de serviços Cloud Run esquecidos e expostos na internet"
data: 2026-10-30
periodo: 2026QD3
categorias:
  - seguranca
  - qualidade
impacto: alto
fontes:
  - "[[atendimento-canais-admin/build-e-deploy]]"
  - "[[file-transcriber/build-e-imagem]]"
  - "[[cve-2026-111497-node2shell]]"
---

# Remoção de serviços Cloud Run esquecidos e expostos na internet

- **Período:** 2026QD3 · **Categorias:** seguranca, qualidade · **Impacto:** alto

## Contexto

O Wiz apontou como P2 grau A (anônimo na internet) o `atendimento-canais-admin-dev` no `aida-stg`, e havia outro avulso (`file-transcriber` sem sufixo), ambos com imagens vulneráveis.

## O que fiz

Analisei 90 dias de logs (só scanners buscando `/.env` e `/@fs/etc/passwd`) e confirmei que nenhum repositório, Pub/Sub ou scheduler apontava para eles; removi os serviços em vez de corrigi-los e documentei a causa raiz (`build.sh` sem `--project` e terraform legado que os recriaria).

## Resultado

Duas superfícies de ataque eliminadas e causa raiz registrada para não se repetir.

## Evidências

- [[atendimento-canais-admin/build-e-deploy]]
- [[file-transcriber/build-e-imagem]]
- [[cve-2026-111497-node2shell]]
