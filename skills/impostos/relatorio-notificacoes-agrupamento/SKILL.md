---
name: relatorio-notificacoes-agrupamento
description: Gera o relatório das notificações do agrupamento de guias em PRODUÇÃO (rodada do dia 15, crons de 15 a 19) - por segmento (Experts Simples, Experts LP, BP LP) e canal (e-mail, WhatsApp), quantos deveriam receber, quantos receberam, o que está em trânsito (WhatsApp na fila do horário comercial), o que falta enviar e quando roda a próxima cron, falhas por motivo, erros do WhatsApp ativo e o resultado do agrupamento, comparado com a competência anterior. Só leitura (banco do agrupamento + mensagem_ativa do atendimento-zendesk). Entrega um resumo de texto para o chat, um artefato para compartilhar com o time e um PDF. Use quando o usuário pedir o relatório/status/acompanhamento das notificações do agrupamento ou do dia 15, perguntar se as notificações das guias saíram, o que falta enviar, ou quiser algo para mandar ao time.
argument-hint: "[competencia AAAAMM | data AAAA-MM-DD] [publico exp|bp] [regime simples|lp] [canal email|wpp] [plano] [pdf] [publicar]"
---

# Relatório das notificações do agrupamento de guias

Como o fluxo funciona, as crons e as armadilhas ficam no vault CTBZ: `~/ctbz-vault/obsidian/repositories/microsservico-agrupamento-guias/relatorio-notificacoes-dia-15.md` (este relatório: métricas, regras, histórico de execuções) e `notificacao-agrupamento-experts-bp-lp.md` (o fluxo). Ler o primeiro antes de rodar e registrar cada execução no histórico dele.

```sh
# função, não variável: o zsh não quebra "$R" em palavras
R() { python3 -I "$HOME/ctbz-vault/skills/impostos/relatorio-notificacoes-agrupamento/scripts/relatorio.py" "$@"; }
```

## Filtros

Todos opcionais e combináveis; listas separadas por vírgula. Sem filtro, sai tudo (3 segmentos × 2 canais).

| Filtro | Valores | Efeito |
| --- | --- | --- |
| `--publico` | `exp`, `bp` | Experts e/ou BP |
| `--regime` | `simples`, `lp` | Simples e/ou Lucro Presumido (BP Simples não tem notificação: dá erro se for o único segmento pedido) |
| `--canal` | `email`, `wpp` | E-mail e/ou WhatsApp (sem WhatsApp, o banco do atendimento-zendesk nem é consultado) |
| `--plano` | `BASICO`, `AVANCADO`, `PREMIUM`, `MULTIBENEFICIOS`, `EXPERT_ESSENCIAL`, `EXPERT_PRO` | Só os grupos desses planos; os segmentos seguem o público do plano |
| `--competencia AAAAMM` ou `--data AAAA-MM-DD` | — | Competência direta, ou o dia da rodada (o dia 15), que vira a competência do mês anterior. Não usar os dois |

Competência passada mostra o estado **atual** dela (resultado final), não uma foto daquela data. Com filtro, a pasta de saída ganha um sufixo (ex: `…_bp-lp-wpp`) e o relatório mostra o filtro no topo.

Exemplos (traduzir o pedido do usuário para os filtros):

```sh
R gerar --pdf                                                      # tudo, competência atual
R gerar --publico bp --regime lp --canal wpp                       # "só o WhatsApp do BP LP"
R gerar --data 2026-10-15 --publico exp --regime simples --canal email   # "e-mail do Experts Simples da rodada de 15/10"
R gerar --plano EXPERT_PRO --canal email,wpp --competencia 202609  # "plano Pro, competência 09/2026"
```

## Regras

- **Prod é só leitura.** O script só faz `SELECT` pelos serviços `prd_*` (abertos em `default_transaction_read_only`). Nunca disparar rota, cron ou reenvio por conta própria: se faltar envio, o relatório diz o que falta e quando a próxima cron roda; o disparo manual é decisão do usuário.
- **Sem dado de contato nas saídas.** O script nunca grava e-mail nem telefone; só id do agrupamento, CNPJ, segmento, plano e status. Não acrescentar contatos ao artefato.
- O artefato nasce privado. Compartilhar com o time é decisão do usuário (ele traz CNPJs de clientes).

## Passos

1. Proxies de prd: `sql_atendimento_prd` (porta 5443, banco do agrupamento) e `sql_crm_prd` (5444, atendimento-zendesk). Conferir com `ss -ltn | grep -E ':5443|:5444'`; se não estiverem de pé, subir só os que faltam (`zsh -ic '_sql_proxy_start_alias sql_atendimento_prd'`) e derrubá-los no fim, sem derrubar os que já estavam de pé. Logs/status não precisam de VPN.
2. `R gerar --pdf`, com os filtros que o usuário pedir (ver "Filtros"; competência padrão = mês anterior). Leva ~40 s. Grava em `~/Downloads/relatorios/notificacoes-agrupamento/<competencia>/<AAAA-MM-DD_HHMM>/`: `resumo.md`, `relatorio.html`, `relatorio.pdf`, `dados.json`, `pendentes.csv` (elegíveis ainda sem notificação) e `problemas.csv` (falhas e contato incompleto).
3. Mostrar ao usuário o `resumo.md` (veredito por segmento × canal e alertas) e explicar os alertas que pedem ação, usando a seção "Como ler" da nota do vault.
4. **Compartilhar**:
   - **Artefato** (link privado do claude.ai, o mais fácil de repassar): publicar o `relatorio.html` gerado como página (`icon: "chart"`), mesmo que o `quickstart` sugira o tipo *Data*: esse tipo monta o painel a partir de consultas de conectores rodando no navegador de quem abre, e nossos números vêm do Postgres pelos proxies locais (testado em 2026-11-16). Dentro da mesma competência (dias 15 a 19), atualizar **o mesmo artefato**: pegar a URL no histórico da nota do vault e publicar com `url`, para o time ter um link só por competência. O artefato nasce privado: lembrar o usuário de compartilhar pelo menu Share.
   - **PDF** (`relatorio.pdf`) para anexar no chat ou no e-mail.
   - **Texto** (`resumo.md`) para colar no chat do time. Achar o canal em `~/ctbz-vault/obsidian/comunicacao/_comunicacao-indice.md` (se não houver, perguntar e registrar) e só enviar depois da confirmação do usuário.
5. Registrar a execução no "Histórico de execuções" da nota do vault (data/hora, competência, vereditos, alertas relevantes, URL do artefato). Se apareceu um problema novo (ex: muitos `SEM_ATIVO`, erro novo do ativo), investigar com o playbook de PRC `PRD-174011` e anotar o que achou.

## Quando rodar

Crons de prd (America/Sao_Paulo, dias 15 a 19): e-mail Exp SN 3h/12h, BP LP 4h/13h, Exp LP 5h/14h; WhatsApp Exp SN e Exp LP 9h/15h, BP LP 10h. O WhatsApp só sai em dia útil das 9h às 19h (`debounceToBusinessHour`), então:

- **Dia 15 útil**: rodar ~10h30 (primeira foto, depois das três rodadas da manhã) e ~16h (depois da rodada das 15h).
- **Dia 15 em fim de semana ou feriado**: o e-mail sai no dia, o WhatsApp fica `PROCESSANDO` até o próximo dia útil às 9h. Rodar no dia 15 depois das 10h (foto do e-mail) e no dia útil seguinte ~11h e ~16h (o ativo esvazia aos poucos).
- **Fechamento**: dia 19 depois das 16h (última rodada às 15h). Daí em diante, elegível sem notificação só sai com disparo manual.

## Migração para o agrupamento-guias-service

Hoje quem notifica em prod é o `microsservico-agrupamento-guias` (autor `microsservico-agrupamento-guias`). Quando o `agrupamento-guias-service` assumir, ajustar o script (ver a seção "Migração" da nota do vault): `--autor agrupamento-guias-service`, ler o status das tabelas `notifications_email`/`notifications_wpp` do banco próprio dele no lugar de `controle_notificacao` (mapeando `SUCCESS`/`PENDING`/`FAILED`/`BLOCKED_OPTOUT`/`INCOMPLETE_DATA`) e manter `grupo_guia` do microsservico como universo (o agrupamento continua lá).
