---
name: 2026-11-24-skill-validar-drop-ativacao
description: "Skill validar-drop-ativacao: explica com evidências por que um ticket de WhatsApp de Ativação caiu num grupo do Zendesk (drop por status do SOCI, rollout da IA, retorno de ativo, empresa ativa), sem chamar a API de prd do Zendesk"
metadata:
  type: project
tags:
  - performance
titulo: "Diagnóstico automatizado do drop de tickets de Ativação (skill validar-drop-ativacao)"
data: 2026-11-24
periodo: 2026QD3
categorias: [ia, qualidade]
impacto: medio
fontes: ["[[roteamento-n1-ativacao-soci]]", "[[trilha-chamadas-bot-load-balancer]]", "[[2026-11-16-testes-e2e-roteamento-n1-ativacao]]"]
---

# Diagnóstico automatizado do drop de tickets de Ativação (skill validar-drop-ativacao)

## Contexto

Entender por que um cliente em ativação caiu num grupo do Zendesk (e não em outro) exigia juntar à mão o ticket, o status do SOCI na hora, a contagem de processos pelo telefone do sócio, o rollout da IA, o retorno de ativo e o log da Ultimate. Além disso, a IA não deve chamar a API de prd do Zendesk/Sunshine.

## O que fiz

- Criei a skill `validar-drop-ativacao` (`~/ctbz-vault/skills/ativacao/`), que recebe o id/link do ticket e uma pergunta opcional e gera o relatório com veredito, checklist e links (ticket, log da Ultimate, SOCI, processo no admin da Abertura, trilha no Cloud Logging).
- Achei duas fontes que dispensam a API do Zendesk: a tabela `tickets` do `prd_crm_atendimento_zendesk` (tags, telefone, conversa do Sunshine, transcrição) e os logs do load balancer de `api.contabilizei.com.br`, que mostram cada GET que o bot fez na conversa (ativo, contagem, dados do processo).
- Codifiquei a árvore do bot (ativo → empresa ativa onboarding/ongoing → contagem → rollout da IA → drops da Entrega 03) num mapa editável (`roteamento.json`).

## Resultado

- Validado em 5 tickets reais de 24/11/2026. Dois achados que corrigiram o entendimento do roteamento: cliente BP também passa pelos drops depois que a AIDA transfere; e tag de ativo não garante o fluxo do ativo (a trilha mostra se houve contagem de processo).
- Caso `DIVERGENTE` achado no teste: ticket 30426058 com SOCI em Em Stand-by (ELSE esperado) caiu em Cadastro depois da IA (provável transferência pela etapa do SOCI).

- A skill passou a tratar os retornos de mensagem ativa: lê o ativo e o histórico de status no banco, reconhece o retorno de CSAT, o FUP de transbordo e os demais ativos, extrai da transcrição o caminho no bot e as transferências, e explica por que não houve IA. Exemplo: o ticket 30420639 voltou de uma pesquisa CSAT sem CNPJ, foi reidentificado e ficou fora do rollout da IA pelo sorteio (segundo :33).

## Evidências

- Skill: `~/ctbz-vault/skills/ativacao/validar-drop-ativacao/SKILL.md`
- Notas: [[trilha-chamadas-bot-load-balancer]], [[roteamento-n1-ativacao-soci]]
