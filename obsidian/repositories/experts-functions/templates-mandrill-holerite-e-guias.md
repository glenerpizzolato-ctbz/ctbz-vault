---
name: experts-functions-templates-mandrill-holerite-e-guias
description: "Templates Mandrill experts-envio-de-holerite (ativo, function email-holerites, disparado pelo admin da FOPAG) e experts-disponibiliza-o-de-guias (sem uso desde 21/09/2026, guia avulsa migrou para o email-service)"
metadata:
  type: reference
tags:
  - experts-functions
  - mandrill
  - email
analisado_em: 2026-11-23
---

# Templates Mandrill: holerite e disponibilização de guias

Levantamento de 2026-11-23 (feature "Envio de holerites por e-mail" no BahCode), para saber se os dois templates do Mandrill ainda são usados, por quais repositórios e quem os consome.

## `experts-envio-de-holerite`: em uso

- **Quem envia**: a function `email-holerites` (`experts-functions`, `functions/email-holerites/src/services/holerite-sender.service.ts`), Cloud Run `function-email-holerites` em `contabilizei-experts-prd`, rota `POST /rhc/folha/notificar`. Gera o PDF de cada holerite pelo `html-to-pdf`, anexa e envia pelo Mandrill (`@experts/mandrill`) com as variáveis `NOME` e `PERIODO`.
- **Gatilho**: botão **"Liberar Folha para o cliente"** na tela Resumo da Folha do admin (`contabilizei-front-admin`, `templates/folha/man-resumo-folha-new.html` → `controller-folha.js` `notificarCliente()`), que chama `GET /fopag/rest/resumo-folha/notificarEmpresaHolerite/{mes}/{ano}/{idEmpresa}` no `plataforma-fopag-worker` (`ResumoFolhaView`, role `FOPAG_WRITER`). A rota faz a notificação de holerite disponível pelo barramento e chama `EnviarEmailHoleritesFacade.enviarHoleritesPorEmail`, que publica no tópico `functions.email-holerites` do projeto `contabilizei-experts` (sub push `eventarc-us-central1-email-holerites-sub-224`). Só publica para empresas com plano que contém "Expert" e só com colaboradores ativos.
- **O cron não manda o e-mail**: a cron de holerite (`NotificadorHoleriteService`, fila `folha-notificacao-holerite-queue`) chama a rota irmã `folha/notificarEmpresaHolerite` (`FolhaJersey`), que só faz o barramento, sem o `EnviarEmailHoleritesFacade`. O e-mail com os PDFs depende do clique no admin.
- **Repositórios vigentes**: `ctbz/obrigacoes/geral/plataforma-fopag-worker` e `ctbz/onboarding-retencao/plataforma/contabilizei-front-admin` no GitLab. Os clones locais em `~/repositories` ainda apontam para o Bitbucket antigo (parados em 2024) e devem ser reclonados do GitLab.
- **Destinatário**: o e-mail do responsável da empresa Experts.
- **Protocolo de cada salto** (conferido em 23/11/2026): admin → fopag-worker por REST (`GET`, síncrono, Restangular); fopag-worker → function por Pub/Sub (tópico `functions.email-holerites` em `contabilizei-experts-prd`, assíncrono); Pub/Sub → function por push HTTP (sub `eventarc-us-central1-email-holerites-sub-224` → `POST /rhc/folha/notificar`); function → `function-html-to-pdf` por REST (`POST` com o HTML, autenticado com identity token do Google via `google-auth-library`, URL na env `URL_HTML_TO_PDF`, uma chamada por colaborador); function → Mandrill pela API HTTPS (`@experts/mandrill`, `messages/send-template`, chave na env `MANDRILL_KEY` via secret).
- **Uso real**: logs de sucesso em prd (retenção começa em 26/10/2026, então "30 dias" na prática são 26/10 a 23/11): **1.958 envios para ~1.205 empresas, 0 erros**. Por mês: 1.042 envios (839 empresas) de 26 a 30/10 e 916 (590 empresas) de 01 a 23/11. Pico em 26/10 (415), 27-28/10 (~220/dia), 03-04/11 (~160/dia) e 10/11 (185); entre os picos fica em 3 a 100 por dia. Por competência: OUTUBRO 1.596, NOVEMBRO 326, SETEMBRO 28, AGOSTO 8. Reenvios são comuns: 742 empresas receberam 1 vez, 312 duas, 96 três e 56 quatro ou mais. 22 envios são da conta de teste "Usuário Demonstração" (CNPJ fictício `YK644N0B000110`). Em 23/11/2026 foram 27 envios para 17 empresas. O volume acompanha a liberação da folha no início do mês.
- **Como contar pelos logs**: filtrar `jsonPayload.message:"function-email-holerites"` no serviço `function-email-holerites` (projeto `contabilizei-experts-prd`); sucesso tem ` INFO ` e falha ` ERROR ` na mensagem, com nome e CNPJ do responsável e o período. Não usar `textPayload:"Holerites"`: a busca não diferencia maiúsculas e pega as linhas de inicialização `start:email-holerites`. As linhas `npm error command sh -c node …` são o desligamento normal do container por ociosidade (SIGTERM), não falha de envio. A function não grava nada em banco nem no BigQuery, então o log é a única fonte do nosso lado; o resto só no painel do Mandrill. Link pronto no console (sucessos de 24/10 a 23/11/2026): https://console.cloud.google.com/logs/query;query=resource.type%3D%22cloud_run_revision%22%0Aresource.labels.service_name%3D%22function-email-holerites%22%0AjsonPayload.message%3A%22Holerites%20enviados%20por%20email%22;startTime=2026-10-24T03:00:00Z;endTime=2026-11-24T03:00:00Z?project=contabilizei-experts-prd
- O `experts-dominios-functions` (Bitbucket `contabilizei-ninjas`, último commit em 28/01/2025) é o repo de origem da function: ela nasceu lá em 21/06/2024 e o repo foi migrado com o histórico para o `experts-functions` no GitLab. A cópia do Bitbucket ficou parada e já diverge do código atual. Em prd, o Cloud Run `function-email-holerites` roda a imagem `experts-functions:0.1.19` (conferido em 23/11/2026), então quem está no ar é o `experts-functions`.

## `experts-disponibiliza-o-de-guias`: sem uso desde 21/09/2026

- **Quem usava**: o `experts-service` (aviso de guia de imposto avulsa, `src/domain/guia-imposto/services/schedule-notification-email-task/`), agendando uma task na `task_scheduler` para o tópico `functions.p2p.email-sender` (function `email-sender`, wrapper de Mandrill sem persistência).
- **Migração**: commit `34100d8` (2026-09-18, Rafael Maestro, `feat(guia-imposto): migrar o e-mail de guia avulsa para o email-service`), já no `master`. O aviso passou a sair pelo `email-service` (tópico `email-service.p2p.send-email`, projeto `atendimento-canais-prd`) com o template `d8d1c1cb-4c1e-4e62-ba9c-217817d6e33e` (`Config.emailService.guiaImpostoTemplateId`), assunto "Sua empresa tem uma nova guia de imposto disponível".
- **Evidência no banco** (`prd_experts_experts_service`, `task_scheduler`): tasks com `template_name = experts-disponibiliza-o-de-guias` vão até 21/09/2026 (9.572 em jul, 7.730 em ago, 5.395 em set) e nenhuma pendente; a partir de então só o template novo (2.242 em set, 9.121 em out, 7.609 em nov até o dia 23).
- **Referências que sobram**: nenhuma no código atual do GitLab (busca no grupo `ctbz`); só no histórico do git e na branch não mergeada do commit `d5752ed` (migração para HubSpot, Gabriel Oliveira), que cita o template num mapeamento.
- **Conclusão**: sem uso, mas não será arquivado no Mandrill: o time não tem acesso ao painel nem à chave (decisão de 24/11/2026, PRD-178574).

## Armadilhas

- A chave do Mandrill de prd fica em `contabilizei-sm-prod` como `contabilizei-experts-prd_MANDRILL_KEY` e o usuário não tem `secretmanager.versions.access` nela, então não dá para consultar `templates/info`/`time-series` da API do Mandrill pelo terminal; a evidência de uso vem dos logs e da `task_scheduler`.
- Os logs da `function-email-sender` não trazem o nome do template, então não servem para medir uso por template.
- Os clones locais do `plataforma-fopag-worker` e do `contabilizei-front-admin` apontam para o Bitbucket (sem acesso, parados em 2024); o código vigente está no GitLab.

- **Cópia no email-service (24/11/2026)**: template `exp-email-holerite-v1` (prd `2b0b0504-203a-4da4-a42a-3993ea8cf547`, dev `11d16281-e06a-4272-88ab-e8440a96579a`), tirado de um `.eml` real de 11/07/2024, já que o HTML não está no Jira (PRD-80587, a demanda original, só tem print) nem no Confluence. Assunto original: "A folha de pagamento da sua empresa está pronta". Como foi feito: [[migrar-template-do-mandrill]].

Desenho do fluxo atual e da proposta de migrar para o email-service: [[fluxo-holerite-email]].

Relacionado: [[notificacao-individual-guias-x-agrupamento]], [[dependencias-experts-functions]].
