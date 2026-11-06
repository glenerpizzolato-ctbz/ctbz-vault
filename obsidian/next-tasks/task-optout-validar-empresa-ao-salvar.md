---
name: task-optout-validar-empresa-ao-salvar
description: "Opt-out: não salvar opt-out de contato sem empresa preenchida"
metadata:
  type: project
tags:
  - next-task
titulo: "Opt-out: não salvar opt-out de contato sem empresa preenchida"
tipo: tarefa
tema: opt-out
dominio:
  - notificacoes
origem: planilha
---

# Opt-out: não salvar opt-out de contato sem empresa preenchida

Validação no admin do atendimento-canais para impedir salvar opt-out de um contato sem empresa vinculada, já que o opt-out passou a ser só por contato ([[PRD-170057]]).

> Texto original na planilha: "optout: Não permitir salvar optout de contato sem ter empresa preenchido"

## Notas

<!-- Detalhes, decisões, PRD criado a partir desta tarefa. -->

- **2026-11-06 — backend não valida (conferido no `contato-service`, `origin/master` e4851b3):** no `POST` de opt-out, `companyCode` é **opcional** de propósito (`register-optout.object.ts`: "Ausente = manifestação válida para todos os grupos do titular"). O `RegisterOptoutUsecase` só valida que o grupo **existe** quando o código vem (senão `NotFoundError`); sem código, grava com `company_id = null`. A tabela `contact_optout` tem `company_id` nullable e um unique parcial só para a linha global (`contact_optout_global_unique`). Nenhum MR aberto ou branch recente mexe nisso.
- Exigir a empresa no backend quebraria o sinal orgânico da Meta (`source = META_USER_PREFERENCES`), que chega só com o telefone. Se a regra for no back, condicionar à origem (ex: obrigatório para `AGENT`/`CLIENT_REQUEST`, vindos do admin); senão, validar só no formulário do `atendimento-canais-admin`.
- **2026-11-06, resolvido no backend pelo [[PRD-175745]]** (branch `feat/PRD-175745` do `contato-service`): o `POST` de opt-out passa a exigir `companyCode` (400 sem ele). Falta avisar o `atendimento-canais-admin`, cujo formulário precisa sempre mandar a empresa. Apagar esta tarefa quando o MR for mergeado. Detalhes em [[optout-empresa-obrigatoria]].
