---
name: atendimento-zendesk-indice
description: "Índice de notas do repositório atendimento-zendesk: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - atendimento-zendesk
repositorio: atendimento-zendesk
caminho: ~/repositories/atendimento-zendesk
---

# atendimento-zendesk

Repositório em `~/repositories/atendimento-zendesk`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

- [[categoria-plano-autenticacao-whatsapp]] — valores do enum `categoriaPlano` no endpoint de autenticação basico-padrao do WhatsApp, como o plano do CRM é normalizado como o statusBot e o quantidadeEmpresas são calculados e o histórico da área OUVIDORIA (removida em 2026-11)
- [[contagem-processos-abertura-por-telefone]] — contagem de processos de abertura por telefone do bot (rota da abertura pelo telefone do sócio) e por que dá zero (SOCI Finalizado ou telefone do sócio gravado errado no cadastro)
- [[api-gateway-bots-whatsapp]] (em `apis/`) — como chamar a `autenticacao/basico-padrao` pelo gateway (`/atendimento/zendesk/bots/whatsapp/fluxo/interacao`) com a `x-api-key` da `zendeskbot-config`
- [[deploy-dev-e-prd]] — como subir em dev (merge na `develop`, pipeline manual com `DEPLOY=true`, jobs service-account → migrations → helm) e em prd; a doc oficial é o README do repo
- [[testes-em-worktree]] — como rodar jest/eslint/prettier numa worktree sem `node_modules` (symlink para o checkout principal) e as suítes que já falham no master; cobertura de 100% em branches exigida no job test do MR
- [[uso-de-llm-openai]] — onde o repo usa LLM (OpenAI gpt-4o-mini via LangChain): classificação de tema/subtema, encerramento automático e resumo de atendimento
- [[monitor-mensagens-sistema-indisponivel]] — monitor que loga quando o cliente recebe mensagem de erro do bot: só textos fixos e case-sensitive (pegou só 1 das 5 variantes de 2026-11-03); linhas NotificarAgente* como fonte completa
- [[historico-mrs-atendimento-zendesk|Histórico de MRs]] — MRs abertos e mergeados, registrados pelo BahCode
- [[alerta-grafana-agregador-conversa]] — alerta do Grafana "agregador-conversa-sub • atendimento-zendesk": qual subscription ele mede (não confundir com a do lote), padrão do lote noturno, mensagem em loop sem ack (~600 s) e a troca para idade da mensagem > 45 min em 11/11/2026
- [[teste-evento-hubspot-whatsapp-ativo]] — como validar ponta a ponta o evento whatsapp_ativo do HubSpot: caminho envio → status → worker → hubspot-proxy, containers de log, BigQuery (dataflow, metadados STRING), os 5 assinantes do tópico de status e os tokens dos portais
- [[whatsapp-ativo-fora-do-horario-comercial|WhatsApp ativo fora do horário comercial]] — `debounceToBusinessHour` segura o envio por retentativa até segunda 9h, mas a validade de 24h conta do `criado_em` e a resposta deixa de ser ligada ao ativo (15/08 sábado: 2 respondidas contra ~4 mil)
- [[whatsapp-ativo-telefone-internacional|WhatsApp ativo e telefone internacional]] — validação aceita qualquer DDI, mas o envio à Sunshine usa `formatarTelefoneBrasileiro` (null para não-BR), então internacional não sai
- [[tags-ouvidoria-whatsapp-ultimate]] — de onde vêm as tags de ouvidoria no WhatsApp: `sys_grupo_bot_ouvidoria` do roteamento de tema (Bank "Reclamação/Elogio"), `_ouvidoria_exp` só do Feedback Experts, `sys_direcionado_ouvidoria_exp` de gatilho; como ler o log da Ultimate pela API do dashboard
