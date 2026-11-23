---
name: credenciais-separadas-infra-e-usuario
description: "Credencial de infraestrutura (identity token do GCP para o Cloud Run privado ou apikey do Kong) e credencial de usuário (JWT da aplicação) nunca compartilham variável nem header, na aplicação e na coleção Bruno"
metadata:
  type: reference
tags:
  - padroes
  - autenticacao
  - bruno
  - cloud-run
  - kong
atualizado_em: 2026-11-23
---

# Credenciais: infraestrutura e usuário

A credencial de **infraestrutura** (quem pode invocar o serviço: identity token do GCP no Cloud Run privado ou `apikey` do Kong) e a credencial de **usuário** (quem está logado: JWT da aplicação) são coisas diferentes, com variáveis, headers e ciclos de vida próprios. Nunca uma vale pela outra.

| | Infraestrutura | Usuário |
| --- | --- | --- |
| O que é | Identity token do GCP (`eyJ...`) ou `apikey` do Kong | JWT da aplicação (sessão do login) |
| Quem valida | Cloud Run IAM ou Kong, na borda | A própria aplicação |
| Onde viaja | `X-Serverless-Authorization: Bearer <token>` ou `apikey: <key>` | `Authorization: Bearer <jwt>` |
| Variável no Bruno | `gcp_token` (secret) ou `apikey` | `jwt_token` (secret) |
| Validade | ~1 h, gerado a cada uso | definida pela aplicação (access/refresh) |

## Na aplicação

- `Authorization: Bearer <jwt>` é reservado ao token do usuário.
- Nunca aceitar o identity token do GCP, o `apikey` do Kong ou um header do proxy como sessão: qualquer portador de credencial de serviço viraria usuário.

## Na coleção Bruno

- `gcp_token` em header de **coleção** (`X-Serverless-Authorization: Bearer {{gcp_token}}`), para valer em todas as requisições, inclusive as com `auth: none`. No ambiente `local`, fica vazio.
- `jwt_token` na auth herdada (`auth: inherit`, header `Authorization`).
- Gerar o identity token com `gcloud auth print-identity-token`. O `print-access-token` (`ya29...`) é recusado pelo Cloud Run com 401.
- Quando o `base_url` aponta para o **Kong**, usar `apikey` e não mandar `X-Serverless-Authorization`: um valor vazio ou velho nesse header tem precedência no Cloud Run e derruba a chamada (o Kong já injeta o token).
- Segredos ficam no `docs/bruno/.env` (gitignored), referenciados por `{{process.env.NOME}}`.

## Anti-padrões

| Anti-padrão | Efeito |
| --- | --- |
| Identity token do GCP em `jwt_token` | IAM passa, a aplicação devolve 401 |
| JWT do usuário em `gcp_token` | Cloud Run rejeita antes de chegar na aplicação |
| Uma variável `token` para os dois papéis | Impossível expirar ou trocar um sem quebrar o outro |
| `X-Serverless-Authorization` em chamada pelo Kong | Token velho/vazio tem precedência e o Cloud Run rejeita |
