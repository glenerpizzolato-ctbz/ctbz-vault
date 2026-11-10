---
name: regressao-notificacoes-agrupamento
description: Roda (e ensina) os testes de regressão das notificações do microsservico-agrupamento-guias em DEV - e-mail, WhatsApp e diagnósticos dos públicos Experts SN (Simples), Experts LP e BP LP, em todos os planos, mais as buscas de elegibilidade das crons, diagnóstico BP e erros (avulsa, sem documento, dados incompletos, competência, já notificado). Gera a massa sintética, checa que só o contato de teste do usuário será alcançado, dispara as rotas de lote, compara banco e logs com o esperado de cada cenário (OK/BUG/FALHA), documenta as evidências no Jira e limpa. Use quando o usuário pedir para testar, validar ou fazer regressão das notificações do agrupamento de guias, conferir se algo parou de funcionar depois de um MR, ou entender como testar esse fluxo.
argument-hint: "[cenarios: todos|SN|LP|BP|DBP] [canais: email|whatsapp|diagnostico-bp] [jira]"
---

# Regressão das notificações do agrupamento de guias

O playbook (fluxo, crons, regras de elegibilidade, templates, catálogo de cenários, como ler o resultado e armadilhas) fica no vault CTBZ: `~/ctbz-vault/obsidian/repositories/microsservico-agrupamento-guias/notifications-regression-tests.md`. **Ler antes de rodar.** O esperado de cada cenário vive no script `scripts/regressao.py` (`cenarios` imprime); ao mudar uma regra de negócio, atualizar o script e o playbook juntos.

```sh
R="python3 -I $HOME/ctbz-vault/skills/impostos/regressao-notificacoes-agrupamento/scripts/regressao.py"
```

## Regra inviolável: só o contato de teste

Toda notificação vai **só** para `glener.pizzolato@contabilizei.com.br` e o telefone `55996981032` (fixos no script, em `CONTATO_TESTE`). Nunca disparar para outro e-mail ou telefone. As rotas de lote alcançam todo grupo elegível da competência, então:

- sempre rodar `$R checar` antes de disparar e mostrar o resultado;
- o `$R disparar` refaz a checagem e cancela se houver qualquer destino fora do contato de teste; nunca contornar (nem chamar as rotas com curl por fora);
- se aparecer registro alheio elegível, parar e avisar o usuário (ou isolar o registro com o aval dele), nunca seguir.

## Passos

1. Ler o playbook. Conferir com o usuário que o pod de DEV está com a branch a testar.
2. Pré-requisitos: proxy de dev do atendimento de pé (`sql_atendimento_dev`; regras de proxy do CLAUDE.md), `gcloud` autenticado e o token do api-gateway de dev numa variável (`DECK_BRUNO_EXPERTS_TO_MICROSSERVICO_AGRUPAMENTO_GUIAS_DEV` do `docs/bruno/.env` do repo; nunca exibir).
3. `$R limpar --aplicar`, `$R massa --aplicar` e `$R checar`.
4. Anotar o início (`date -u +%FT%TZ`) e disparar: `$R disparar --token-env <VAR> --rotas email`, depois `--rotas whatsapp,diagnostico-bp` (só os canais pedidos). Esperar ~1 min.
5. `$R verificar --desde <início>`: `OK` bate com o esperado, `BUG` é bug conhecido (citado no playbook), `FALHA` é regressão. Para cada `FALHA`, investigar no log do pod (`gcloud logging read … container_name="microsservico-agrupamento-guias"` em `contabilizei-dev-01`) antes de concluir: pode ser massa errada.
6. Evidências: tabela do `verificar`, trechos de log e prints (HTML do template renderizado com as `variables` do `email_replications` de dev, via Chrome headless). Se o usuário pedir, comentar na sub-task de testes do card (upload pelo `uploadAttachmentToJiraIssue` e imagens inline).
7. `$R limpar --aplicar` ao terminar (salvo pedido de manter a massa).
8. Registrar a execução no "Histórico de execuções" do playbook e, se uma regra mudou, atualizar o catálogo e o script.

## Observações

- Em DEV o e-mail não chega (SMTP rejeita com 421); valida-se o `nomeGuia`/template publicado. Para receber de fato, ver "rodar-testes-localmente" no vault (app local, só o envio em prod).
- A massa usa `id_empresa` 99000000000001–99000000000999 e `sistema_origem = 'regressao-notificacoes'`; o `limpar` só apaga essa faixa.
- Prod é só leitura: nunca rodar `massa`, `limpar` ou `disparar` contra prod.
