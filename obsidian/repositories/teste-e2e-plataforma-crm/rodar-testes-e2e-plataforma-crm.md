---
name: rodar-testes-e2e-plataforma-crm
description: Como instalar e rodar os E2E (Cypress) do teste-e2e-plataforma-crm localmente em stg/dev03 e como eles rodam na pipeline de outros repositórios (template e2e-plataforma-crm, tags, Currents)
metadata:
  type: reference
tags:
  - teste-e2e-plataforma-crm
  - e2e
  - cypress
repositorio: teste-e2e-plataforma-crm
atualizado_em: 2026-11-26
---

# Rodar os E2E da Plataforma CRM

## Estrutura

- Specs em `cypress/e2e/autoatendimento/*.cy.js` (`chat-history`, `customer-service`, `faq`, `invoice`, `self-service`), comandos em `cypress/support/autoatendimento/{actions,elements,services}.js` e `cypress/support/helpers/*` (iframe, `data-factory` com `generateInvoice` e `closeUserZendeskTickets`).
- Massa: usuários de teste em `cypress/fixtures/data/data-user.json` (`general`, `crm`, `history`, `checkStatus`), dados em `data-crm.json`. Os textos esperados do bot ficam em `cypress/fixtures/messages/{user,system}-*.json` e são comparados **na ordem e por igualdade exata**: qualquer mudança de texto no widget quebra o teste.
- Ambientes: `cypress/environments/stg.config.js` (`https://app-stg.ctbz.com.br`) e `dev03.config.js` (`https://app-dev3.ctbz.com.br`), os dois com o Zendesk sandbox `contabilizei1637606740` e o pagamentos de teste.
- Filtro por tags com `@cypress/grep` (`grepFilterSpecs` e `grepOmitFiltered` ligados): só o que tem a tag pedida roda; um `it` sem tag fica de fora sem aviso.

## Instalar (local)

O binário do Cypress 12.17.4 está versionado em `binaries/cypress/12.17.4/linux-x64/` (~180 MB, deixa o clone lento: o `glab repo clone` pareceu travar, mas só estava baixando).

```sh
cd ~/repositories/teste-e2e-plataforma-crm
CYPRESS_INSTALL_BINARY="$PWD/binaries/cypress/12.17.4/linux-x64/cypress-linux-x64-12.17.4.zip" HUSKY=0 yarn install --frozen-lockfile
npx cypress verify
```

## Rodar (local)

```sh
yarn cypress run --browser chrome --config-file ./cypress/environments/stg.config.js --spec cypress/e2e/autoatendimento/customer-service.cy.js
yarn cypress run --browser chrome --config-file ./cypress/environments/stg.config.js --env grepTags="@regression+@autoatendimento"   # o mesmo conjunto da pipeline
yarn open:stg   # modo interativo
```

- **Precisa da VPN.** Sem ela, `app-stg.ctbz.com.br` responde **403 Forbidden** na borda (página "Error Details" com "Your IP") e o teste falha no login com `Expected to find element: input[id="user"]`.
- `--config retries=0` (nem `--config '{"retries":{"runMode":0}}'`) desliga as retentativas: o `retries.runMode: 4` vem aninhado do `cypress.config.js`; cada falha roda 5 vezes (~45 s de timeout por tentativa). O que funciona é `{ retries: 0 }` no próprio `describe`/`it`, ou `yarn open:stg`.
- Mesmo com VPN, o stg às vezes responde **403** no meio da execução (no `cy.visit` ou nas rotas `/api/plataforma/atendimento/...`), principalmente depois de várias tentativas seguidas; o `curl` volta 200 logo depois. Rodar de novo antes de concluir que é bug.
- O Zendesk Messaging segue o idioma do navegador: no Chrome headless (local e pipeline) os rótulos vêm em inglês (`Messaging window`, `Close`, `Type a message`). Seletores do Zendesk precisam aceitar pt e en.
- Para investigar um seletor que sumiu, criar uma spec temporária (ex: `zz-debug.cy.js`, com `{ retries: 0 }`) que repete os passos e grava com `cy.writeFile` os `iframe`/`button` do `contentDocument` em `cypress/downloads/`; apagar depois. Rodar uma spec apaga `cypress/downloads/example.txt` (versionado): restaurar com `git checkout -- cypress/downloads/example.txt`.
- Os temas/subtemas do widget em stg vêm do banco `atendimento-zendesk` de dev (`bots_temas`, `id_tema_antecessor` = tema pai, `ativo`); consultar lá (serviço `dev_crm_atendimento_zendesk`, proxy `sql_crm_dev`) quando o fluxo do widget não bater com as fixtures.
- Commits: o hook do repo (commitlint) exige primeira linha com no máximo 80 caracteres e tipos `fix`, `docs`, `refactor`, `test`, `build`.
- Relatórios e screenshots em `cypress/reports/` (`yarn report:create:linux` monta o HTML).

## Na pipeline

- Template `~/repositories/pipeline/templates/e2e-plataforma-crm/template.yml`, job `e2e-plataforma-crm-feat-autoatendimento`, stage `post-staging`, imagem `teste-e2e-plataforma-crm:latest` (gerada pela pipeline deste repo, com `yarn install` no build). Roda `yarn run:cloud:stg` com `CYPRESS_grepTags: "@regression+@autoatendimento"`, ou seja, **só os `it` com `@regression`** (o `@autoatendimento` vem do `describe`).
- Habilitado por `E2E_ENABLED`, `E2E_PLATAFORMA_CRM` e `E2E_PLATAFORMA_CRM_FEAT_AUTOATENDIMENTO` no `pipeline/custom/...` do repo que faz deploy (ex.: `plataforma-web`, `contabilizei-front`; o `contabilizei-pagamentos` desliga). O próprio `contabilizei-crm-widget-window` não roda esse job.
- As execuções vão para o Currents (projeto `DXFHsV`); o link "Run URL" aparece no log do job. Para ver o último resultado sem Currents: `glab api "projects/ctbz%2Fengajamento-experiencia%2Farquitetura%2Fplataforma-web/jobs?per_page=100"`, filtrar `name == e2e-plataforma-crm-feat-autoatendimento` e ler o `trace`.
- Em 26/11/2026 (job 18408389282 do `plataforma-web`) os 7 testes com `@regression` passaram; `customer-service.cy.js` e `faq.cy.js` rodaram com 0 testes. Em 18/11 o "Deve gerar um novo atendimento (ticket)" falhou nas 5 tentativas (a 1ª mensagem do bot veio fora de ordem) e passou depois: é intermitente.

Métrica e cobertura do squad Canais: [[e2e-criticos-canais]].
