---
name: fluxo-holerite-email
description: "Artefato Fluxo do Holerite por E-mail: BPMN de cima para baixo (raias por sistema) do envio de hoje (admin → fopag-worker → Pub/Sub → function-email-holerites → html-to-pdf → Mandrill) e da proposta (decidida em 23/11/2026) de manter fopag-worker, tópico, function e html-to-pdf e trocar só o Mandrill pelo email-service (HubSpot), com ganhos, pré-requisitos e riscos"
metadata:
  type: reference
tags:
  - artefatos
  - experts-functions
  - email-service
  - plataforma-fopag-worker
  - holerite
link: https://claude.ai/artifact/3MK3PmSWH5VWzNTgu3hNNm
arquivo: arquivos/fluxo-holerite-email.html
pdf: ~/Downloads/fluxo-holerite-email.pdf
criado_em: 2026-11-23
atualizado_em: 2026-11-23
retrato: "experts-functions abd9e0b · email-service 3642d61 · plataforma-fopag-worker e contabilizei-front-admin no GitLab · Cloud Run/subscriptions de contabilizei-experts-prd · logs da function-email-holerites de 26/10 a 23/11/2026"
---

# Fluxo do Holerite por E-mail

Feature "Envio de holerites por e-mail" (BahCode). A página mostra dois diagramas BPMN de cima para baixo, uma raia (coluna) por sistema, com início/fim, tarefas, decisões, tópicos Pub/Sub e chamadas entre sistemas tracejadas; tarefas novas da proposta marcadas em verde e raias que saem em laranja. Abaixo, ganhos, pré-requisitos e riscos.

O SVG é gerado por script: editar `arquivos/fluxo-holerite-email-gen/bpmn.py` (raias, nós, arestas com coordenadas) e `template.html`, e rodar `python3 bpmn.py template.html ../fluxo-holerite-email.html`. Para o PDF (A3 retrato), envolver o HTML com doctype/head e imprimir com `google-chrome --headless=new --print-to-pdf`.

Resumo dos fluxos:

- **Hoje**: botão "Liberar Folha para o cliente" no admin → REST no `plataforma-fopag-worker` → Pub/Sub `functions.email-holerites` → push HTTP na `function-email-holerites` → `function-html-to-pdf` (1 por colaborador) → API do Mandrill (template `experts-envio-de-holerite`). 1.958 envios para ~1.205 empresas de 26/10 a 23/11/2026, 0 erros no log.
- **Proposta (decisão do usuário em 23/11/2026)**: admin, fopag-worker e tópico continuam iguais; a function continua com a lógica (HTML e PDF pelo `function-html-to-pdf`), mas em vez do Mandrill sobe cada PDF no email-service (rota síncrona de arquivos, devolve `fileId`) e publica o pedido em `email-service.p2p.send-email` (`atendimento-canais-prd`) com `template_id`, `NOME`, `PERIODO` e os `fileIds`. O email-service valida, grava em `email_replications`, baixa os PDFs do GCS e envia pela SMTP da HubSpot. Sai só o template do Mandrill. A versão anterior do desenho (fopag-worker publicando direto no email-service) foi descartada porque a lógica do holerite está na function.

Conclusões principais:

- O email-service não gera PDF: só anexa arquivos enviados antes a ele (`POST /api/v1/files` → `fileId`). Por isso o `function-html-to-pdf` fica no fluxo. Preferir o upload síncrono; no tópico `email-service.p2p.file-upload` o `fileId` é o id da mensagem e o arquivo pode ainda não estar no bucket quando o envio for processado.
- Pré-requisitos: template de holerite no email-service, troca do envio na function, permissões da conta da function (rota de arquivos e publish no tópico de `atendimento-canais-prd`), decidir `optout_purpose`.
- Riscos: conferir como a function (Cloud Run) alcança a rota de arquivos do email-service; reentrega do Pub/Sub após falha sobe os PDFs de novo; na HubSpot o holerite só se separa pelo assunto.

Atualizar quando a proposta for decidida ou implementada, ou se o contrato de envio do email-service mudar.

Relacionado: [[templates-mandrill-holerite-e-guias]], [[envios-no-hubspot]].
