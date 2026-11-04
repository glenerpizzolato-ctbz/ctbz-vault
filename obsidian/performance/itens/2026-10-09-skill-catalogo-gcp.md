---
name: 2026-10-09-skill-catalogo-gcp
description: "Catálogo GCP automatizado com IA (skill atualizar-catalogo-gcp)"
metadata:
  type: project
tags:
  - performance
titulo: "Catálogo GCP automatizado com IA (skill atualizar-catalogo-gcp)"
data: 2026-10-09
periodo: 2026QD3
categorias:
  - ia
  - processo
  - outros-times
impacto: alto
fontes:
  - "[[_infra-indice]]"
  - "[[por-repositorio]]"
---

# Catálogo GCP automatizado com IA (skill atualizar-catalogo-gcp)

- **Período:** 2026QD3 · **Categorias:** ia, processo, outros-times · **Impacto:** alto

## Contexto

Ninguém sabia com facilidade onde cada serviço, tópico, subscription, scheduler ou fila rodava entre os projetos GCP dos domínios, nem quem consumia cada tópico.

## O que fiz

Criei uma skill com script (`build_catalog.py`) que lista pelas APIs Pub/Sub, Scheduler, Cloud Tasks, Cloud Run/functions e GKE de todos os projetos, cruza cada recurso com os repositórios que o citam, deduz o consumidor pela convenção de nomes e gera as notas do vault com visão reversa por repositório.

## Resultado

Catálogo cobrindo Atendimento/Canais, Experts, AIDA, CRM, App, Impostos, Issue e Fintech; é a fonte usada para localizar serviços em investigações (ex: CVE node2shell).

## Evidências

- [[_infra-indice]]
- [[por-repositorio]]
