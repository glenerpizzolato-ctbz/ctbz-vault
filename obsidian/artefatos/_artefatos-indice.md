---
name: artefatos-indice
description: "Índice dos artefatos do Claude (páginas publicadas em claude.ai/artifact) que valem a pena guardar: uma nota por artefato com link, assunto, fontes e o HTML versionado em arquivos/"
metadata:
  type: reference
tags:
  - artefatos-indice
---

# Artefatos

Páginas geradas pelo Claude e publicadas como artefato (claude.ai/artifact) que viraram referência. Cada artefato tem uma nota `<slug>.md` (link, o que mostra, retrato de quando, fontes, notas relacionadas) e o HTML-fonte em `arquivos/<slug>.html`, para republicar no mesmo link ou recriar se o link se perder.

Para atualizar: editar `arquivos/<slug>.html` e publicar com a ferramenta Artifact passando o `url` da nota (mantém o link); depois atualizar `atualizado_em` e o resumo da nota.

Para **compartilhar com o time** (HTML Share: como publicar, versões, marcações, assinaturas e permissões), ver [[compartilhar-com-o-time]].

## WhatsApp ativo

- [[mapa-whatsapp-ativo|Mapa do WhatsApp Ativo]] — Projeto do template (squad) x Atendimento do envio (integracao): quais templates aparecem, como cada campo do envio é preenchido, número de saída, resposta e opt-out, com simulador

## Avisos e Mensagens

- [[plano-api-avisos|Plano da API de Avisos e Mensagens]] — Regras de destinatários em OU de E (protótipo), persistência em JSONB, contrato REST, motor único e MRs do PRD-179459

## Holerite / Experts

- [[fluxo-holerite-email|Fluxo do Holerite por E-mail]] — BPMN do envio de hoje (function → html-to-pdf → Mandrill) x proposta (function → html-to-pdf → email-service/HubSpot), com pré-requisitos e riscos
