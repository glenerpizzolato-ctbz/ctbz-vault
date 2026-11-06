---
name: optout-empresa-obrigatoria
description: "contato-service: o opt-out é sempre por empresa (companyCode obrigatório desde o PRD-175745); registros legados com company_id nulo e o sinal da Meta"
metadata:
  type: project
tags:
  - contato-service
  - opt-out
---

# Opt-out: empresa obrigatória

- Desde o [[PRD-175745]] (branch `feat/PRD-175745`), o `POST /api/v1/optouts` exige `companyCode`: sem ele devolve 400, com código inexistente devolve 404. Para valer em todas as empresas do titular, o consumidor grava **uma manifestação por empresa**; não existe mais "manifestação global".
- O upsert (`OptoutDAO.upsert`) mira só o índice parcial `contact_optout_company_unique`.
- **Legado:** a coluna `company_id` segue nullable e o índice `contact_optout_global_unique` continua existindo, só por causa dos registros antigos sem empresa. Em prd, em 2026-11-06, eram **12** linhas com `company_id` nulo (8 `AGENT` e 4 `CLIENT_REQUEST`), num total de 27. Na leitura, elas continuam aparecendo no filtro por grupo e contam como sobrepostas a qualquer grupo na regra de canal único de `TAX`. **Decisão (2026-11-06): o banco continua aceitando `company_id` nulo** — sem migration de `NOT NULL` e sem remover o `global_unique`; a obrigatoriedade é só na validação da API, para os registros novos, e o legado fica como está.
- **Sinal da Meta (`META_USER_PREFERENCES`):** os comentários antigos diziam que ele chegava só com o telefone, mas nenhum código do serviço grava opt-out a partir do webhook da Meta (o `webhooks/meta` não chama o registro de opt-out) e não havia nenhuma linha com essa origem em prd. Se esse fluxo for implementado, ele terá de resolver as empresas do titular e gravar uma linha por empresa.
- Contagem do legado (prd, só leitura): `select source, count(*) filter (where company_id is null), count(*) from contact_optout group by source;` em `prd_atendimento_canais_contato_service`. Em dev, o serviço `dev_*` falha na autenticação com o usuário do e-mail (ver `db/bancos-dev.md`).
