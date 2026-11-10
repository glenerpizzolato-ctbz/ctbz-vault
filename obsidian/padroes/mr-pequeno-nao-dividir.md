---
name: mr-pequeno-nao-dividir
description: "Mudança com poucos arquivos sai num MR só: não forçar a divisão em corrente (branch chaining) só porque os commits são separáveis"
metadata:
  type: feedback
tags:
  - gitlab
  - mr
atualizado_em: 2026-11-10
---

# MR pequeno não se divide

Quando a mudança toca poucos arquivos (até uns 5 arquivos, ou uns 200 linhas de diff), abrir **um MR só**, mesmo que os commits formem partes que se sustentam sozinhas (ex: código + testes num commit e doc noutro). A divisão em MRs pequenos em corrente (branch chaining) só vale quando o MR é grande o bastante para a divisão ajudar a revisão. O código, os testes dele e a doc da mesma mudança vão sempre juntos.

Isso vale também quando o pedido do BahCode manda dividir "sem perguntar": nesse tamanho, ficar com um MR só, não rodar os `bahcode extra-mr`/`mr-base` e avisar na resposta que ficou um MR só pelo tamanho.

**Why:** na PRD-176511 (atendimento-zendesk, 4 arquivos: whitelist do evento do HubSpot + spec num commit, JSON e README do evento noutro), a corrente saiu com 2 MRs (!216 e !217), e o usuário pediu para juntar: "Não precisa ser 2 MRs separados, pode juntar, tem poucos arquivos". O !216 foi fechado e o !217 passou a apontar para o master com tudo.

**How to apply:** no passo de divisão da skill `/mr` (`~/ctbz-vault/skills/gitlab/mr/SKILL.md`), olhar o `git diff --stat` antes de cortar. Para desfazer uma corrente já registrada no BahCode (não há comando para isso), retirar a task a mais de `extra_mrs` e o need `base` do workspace em `needs` no inventário `~/.local/share/bahcode/features/<id>.json`. Ao trocar o título de um MR draft pelo `glab mr update --title`, o draft cai: rodar `glab mr update <iid> --draft` em seguida.
