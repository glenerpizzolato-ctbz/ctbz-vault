---
name: contato-service-vincular-contato-empresa
description: "Como vincular um contato (person) a uma empresa no contato-service: POST /api/v1/contacts é idempotente e reaproveita a person pelo telefone/e-mail; o PATCH não mexe em empresa"
metadata:
  type: reference
tags:
  - contato-service
---

# Vincular contato a empresa (contato-service)

Não existe rota dedicada de "vincular". O vínculo (`membership`) é feito pelo `POST /api/v1/contacts` (Bruno: `docs/bruno/contacts/create-contact.bru`), que funciona como um upsert:

1. Procura persons existentes pelos `phones[].phoneNumber` e `emails[].address` informados. Se acharem mais de uma person diferente → 409 (ambíguo).
2. Se achar uma person, reaproveita (adiciona só os telefones/e-mails novos; o `person` do body é exigido pelo schema, mas não sobrescreve nome). Se não achar, cria a person.
3. `companyDAO.upsertByCode`: cria a empresa pelo `company.code` se não existir (`companyCreated: true` na resposta).
4. Cria o `membership` (person × company) com o `membership.role` se ainda não existir; se já existir, devolve o existente (o role não é atualizado).

Para linkar um contato existente a outra empresa, basta mandar o POST com um telefone ou e-mail que ele já tem e a nova `company`.

- `company.type`: `EMPRESA`, `PROCESSO`, `LEAD`.
- `membership.role`: `PARTNER`, `REPRESENTATIVE`.
- `PATCH /api/v1/contacts/:id` só altera person/phones/emails; não aceita `company`. Não há rota para remover um vínculo.
- `base_url`: dev `https://api-dev.contabilizei.com.br/contato-service`, prd `https://api.contabilizei.com.br/contato-service`, local `http://localhost:3000`.
- A branch padrão real é `master` (o `origin/HEAD -> main` do clone está desatualizado; `main` é antigo).

## Rota dedicada (MR !53, ainda não mergeado)

O MR !53 (`feat/zendesk-company-user-sync` → `master`, "centraliza empresa ↔ pessoa e sincroniza com o Zendesk") traz a rota própria para linkar uma person existente pelo id:

- `PUT /api/v1/companies/:code/memberships/:personId` com body `{ "role": "PARTNER" | "REPRESENTATIVE" }` (Bruno: `docs/bruno/companies/upsert-membership.bru`). 201 se criou o vínculo, 200 se já existia (e aí troca o papel), 404 se a empresa ou a person não existem.
- A empresa precisa existir antes: `PUT /api/v1/companies/:code` (`upsert-company.bru`); `GET /api/v1/companies/:code` consulta.
- Sincroniza com o Zendesk de forma assíncrona e aditiva (garante o usuário e a organization_membership; nunca remove).

Enquanto não for mergeado, o caminho em `master` é o POST /api/v1/contacts acima.

Objetivo do MR: o modelo N:N (uma person em várias empresas via `membership`) já existe em `master`. O MR faz do contato-service o dono da relação empresa ↔ pessoa e a propaga para o Zendesk (empresa → organization com `external_id` = CNPJ, person → user, membership → organization_membership), por outbox + Pub/Sub (`contato-service.topic.zendesk-sync`), via `zendesk-proxy`, sem nunca sobrescrever ou remover nada (ambíguos viram `CONFLICT` no `GET /companies/:code`). Também promove `PROCESSO` (code = IdProcessoAbertura) para `EMPRESA` no mesmo registro quando sai o CNPJ (`PUT /companies/:cnpj` com `aberturaId`). Fica desligado por padrão (`ZENDESK_SYNC_ENABLED=false`); o `plataforma-back-worker` segue escrevendo no Zendesk e no futuro passa a chamar essas APIs.

> [!NOTE]
> A pipeline de MR do contato-service faz deploy em dev (`helm-deploy-gke-dev`) a partir de `refs/merge-requests/<iid>/head`. Então rotas de um MR aberto podem estar no ar em dev, até outro MR ou a `master` deployar por cima. Para saber o que está em dev, ver o último job `helm-deploy-gke-dev` com sucesso: `glab api "projects/:id/jobs?scope=success&per_page=100"`. Em 2026-11-06 o último deploy de dev era o do MR !53 (2026-11-04).
