---
name: rotina-deploy-separada
description: "Fechar o card da feature quando o desenvolvimento e a validação acabam e abrir uma Rotina só para o deploy em produção, para o card não ocupar cycle time esperando o deploy"
metadata:
  type: reference
tags:
  - jira
  - cycle-time
  - deploy
atualizado_em: 2026-10-29
---

# Rotina separada para o deploy (cycle time)

O time é medido por cycle time, e o card não deve ficar parado em `Ready for Release` esperando uma janela de deploy, uma dependência externa ou a publicação na Ultimate. Quando a feature está desenvolvida e validada, mas o deploy em produção ainda vai demorar:

1. Criar um card do tipo **Rotina** no projeto PRD, só para o deploy, no **mesmo épico** da feature, com Quarter, Assigned Squad (`Engenharia Canais`, 68720), Story Points 1 e responsável eu.
2. Título `[<tema>] Subir em produção <o que sobe>`; na descrição, dizer que o card da feature foi fechado por conta do cycle time, linkar o card original e listar os **passos** do deploy (MR, jobs da pipeline na ordem, casos de uso da Ultimate, configs/segredos a conferir) e a **validação em prd**.
   - **Épico:** sempre o mesmo da feature, nunca o de CTS.
   - **Status:** a rotina tem que ficar em **`To-do`**, e não em `Backlog`. O card nasce em `Backlog`, então logo depois de criar é preciso aplicar a transição `Detailed` (id `51`, `Backlog` → `To-do`).
3. Fechar o card da feature com a transição `Released` (→ `Concluído`).
4. No vault: nota da feature como `pronto` e da rotina como `backlog` (tipo `rotina`, atuação `Rotina`), com `relacionados` apontando uma para a outra; depois `prds.py rebuild`.
5. Quando o deploy for executado, concluir a rotina: de `To-do` não existe `Released`; aplicar `Started` (id `61`, → `Building`) e depois `Finished` (id `121`, → `Concluído`), uma transição por vez (ver [[jira-transicoes-passo-a-passo]]). No vault, marcar a rotina como `pronto` com `data_pronto` e rodar `prds.py rebuild`.

## Exemplos

- PRD-170026 (feature, fora do vault) / [[PRD-170272]] — opt-out de notificações de impostos; deploy aguardando a migração do atendimento-zendesk para o GitLab.
- [[PRD-173035]] / [[PRD-174558]] — menu da Super Ouvidoria na Ultimate; deploy é o `upgrade bots` e a publicação dos casos de uso.
