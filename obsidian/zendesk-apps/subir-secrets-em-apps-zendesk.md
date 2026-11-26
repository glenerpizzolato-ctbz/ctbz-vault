---
name: subir-secrets-em-apps-zendesk
description: "Receita: como subir secrets (e parâmetros comuns) num app Zendesk do atendimento - parâmetro no manifest, ${VAR} no template do zcli, variável na UI do GitLab por ambiente, deploy que reescreve a instalação; uso no código com {{setting.x}}, execução local e rotação"
metadata:
  type: reference
tags:
  - zendesk-apps
  - secrets
  - zcli
  - gitlab-ci
criado_em: 2026-11-26
---

# Subir secrets em apps Zendesk

Vale para todos os `zendeskapp-*` do grupo `ctbz/atendimento/geral`, que fazem deploy pelo componente `ci-cd` com `zcli apps:update`. O fluxo e os riscos do modelo atual estão em [[zendesk-apps-segredo-jwt]].

## Como funciona

```
Variável do projeto no GitLab (por ambiente)
  -> deploy: config:${ENV} troca ${VAR} em environments/zcli.apps.config.<env>.json
  -> dist/zcli.apps.config.json
  -> zcli apps:update dist: sobe o pacote e faz PUT na instalação com TODOS os parâmetros
  -> configuração da instalação no Zendesk (secure: valor fica no Zendesk, não vai ao navegador)
```

- **A fonte da verdade é a variável do GitLab.** O `zcli apps:update` reescreve as configurações da instalação a cada deploy (`updateProductInstallation` do `@zendesk/zcli-apps`). Mudar o valor à mão no Admin Center > Apps só vale até o próximo deploy.
- Parâmetro do manifest que não está no `zcli.apps.config.json` o zcli tenta perguntar no terminal; no CI ele fica vazio. Todo parâmetro precisa estar no template.
- `ZENDESK_SUBDOMAIN` (não é segredo) fica versionado no repo `pipeline` (`custom/ctbz/atendimento/geral/<app>.<env>.yml`). `ZENDESK_OAUTH_TOKEN` (credencial do zcli) e os segredos do app ficam só na UI do GitLab.

## Passo a passo: novo secret

1. **Manifest** (`src/manifest.json`): declarar o parâmetro com `"secure": true`.
   ```json
   { "name": "minhaChaveApi", "type": "text", "required": true, "secure": true }
   ```
2. **Templates do zcli** (`environments/zcli.apps.config.dev.json` e `.prod.json`/`.prd.json`): `"minhaChaveApi": "${MINHA_CHAVE_API}"`. Valor que não é segredo e é igual para todos (URL, `jwtIss`) pode ficar fixo no template.
3. **Variável no GitLab**, uma por ambiente, no projeto do app (Settings > CI/CD > Variables), com:
   - **Environment scope** `dev` e `prd` (os nomes dos ambientes da pipeline), com valores **diferentes** por ambiente;
   - **Masked** (e, se der, **Hidden**, que só pode ser marcado na criação): o valor some do log. Exige pelo menos 8 caracteres e sem espaço;
   - **Protected**: só roda em branch/tag protegida (o deploy de prd sai da `master`).
   Pela CLI: `glab variable set MINHA_CHAVE_API --scope prd --masked --protected` (o valor vem do stdin ou de `--value`; não deixar no histórico do shell).
4. **`.env.example`** do app: acrescentar a variável com um valor de exemplo, para a execução local.
5. **Deploy**: rodar a pipeline (o job de deploy aplica a variável na instalação). Para conferir sem expor o valor, olhar no Admin Center > Apps > o app > configurações que o campo está preenchido.

Parâmetro **não secreto** (ex: id de grupo `PERMISSION_GP_*`) segue os mesmos passos com `"secure": false`, e a variável não precisa de mask. Lembrar que parâmetro não secreto chega ao JavaScript (`client.metadata().settings`) e qualquer agente consegue ler: segredo nunca vai com `secure: false`.

## Usar o secret no código

O valor de um parâmetro `secure` não existe no navegador. Ele só pode ser usado dentro de `client.request` com `secure: true`, por placeholder que o proxy do Zendesk resolve no servidor:

```js
client.request({
  url: `${settings.baseUrl}/api/...`,
  type: 'GET',
  secure: true,
  headers: { 'x-api-key': '{{setting.minhaChaveApi}}' },
});
```

Para o JWT dos apps (`jwtSecretKey`), o proxy também assina o token: `jwt: { algorithm: 'HS256', secret_key: '{{setting.jwtSecretKey}}', claims: {...} }` e `Authorization: Bearer {{jwt.token}}` (padrão do `auth-rest-client` dos apps; o Kong valida com o mesmo segredo, vindo do Secret Manager do `atendimento-api-gateway`).

## Rodar local

- `.env` (gitignored, modelo no `.env.example`) + `config:dev` gera o `dist/zcli.apps.config.json` para o `zcli apps:server dist`.
- Com `ENV=localhost`, os apps não usam o proxy para assinar o JWT: leem o token do `localStorage` (`jwt-token-zendesk`) e mandam `secure: false`. O `JWT_SECRET_KEY` do `.env` pode ser qualquer valor nesse modo.
- Nunca commitar o `.env` nem o `dist/`.

## Atualizar ou rotacionar

1. Trocar o valor da variável no GitLab (por ambiente).
2. Rodar o deploy do app no ambiente (dev pela pipeline do MR com deploy manual, prd pela `master`).
3. Se o segredo é compartilhado com outro sistema (caso do `JWT_SECRET_KEY`, igual ao `ZENDESKAPP_JWT_SECRET` do gateway), trocar os dois lados juntos: novo valor no Secret Manager do gateway, redeploy do gateway e de **todos** os apps que usam o segredo. Para não derrubar ninguém no meio, o Kong pode aceitar dois consumers JWT (o antigo e o novo) durante a troca.

## Armadilhas

- **Não imprimir o config no deploy.** Os deploys antigos fazem `cat dist/zcli.apps.config.json`, que joga os parâmetros seguros no log (com a variável sem mask, em claro). O `zendeskapp-warnings-and-messages` já não faz isso.
- **Um segredo por ambiente.** Hoje o `JWT_SECRET_KEY` é o mesmo em dev e prd em todos os apps (ver [[zendesk-apps-segredo-jwt]]); app novo deve nascer com valores separados.
- Variável com environment scope errado (ex: `production` em vez de `prd`) não chega ao job: o `config:<env>` falha por variável sem valor (no gerador do warnings-and-messages) ou grava vazio (no `envsub` dos apps antigos, sem erro).
- Os apps não usam Vault nem Secret Manager para os próprios segredos; o vault-roleset da pipeline é só para credenciais GCP (token do Artifact Registry, chave de SA).
