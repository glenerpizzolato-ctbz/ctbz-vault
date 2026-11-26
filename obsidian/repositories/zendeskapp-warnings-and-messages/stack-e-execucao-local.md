---
name: zendeskapp-warnings-and-messages-stack-e-execucao-local
description: "zendeskapp-warnings-and-messages: stack (Node 26, pnpm 11, React 19, Vite 8, TS 7, Biome, Vitest, Sentinela), os dois modos de rodar local (fora do Zendesk com client ZAF falso e dentro com zcli) e as armadilhas do scaffold"
metadata:
  type: reference
tags:
  - zendeskapp-warnings-and-messages
  - zendesk-app
repositorio: zendeskapp-warnings-and-messages
criado_em: 2026-11-26
---

# Stack e execução local

O repositório nasceu como `zendeskapp-warnings-and-menssages` (erro de grafia) e foi renomeado em 2026-11-26 para `zendeskapp-warnings-and-messages` (caminho no GitLab, config de CI no repo `pipeline` pelo !3586, chave do Sonar, `package.json`). O GitLab redireciona o caminho antigo. As pastas locais (checkout e `.wt`) foram movidas com a skill `move-repo-folder` (`bahcode.py move-repo`), que manteve o terminal do BahCode e a sessão do Claude (`claude --resume` no mesmo painel); depois do move, `pnpm install --offline` refaz os atalhos do `node_modules/.bin`.

Scaffold feito em 2026-11-26 (branch `feat/PRD-179389`, sub-task PRD-179409), a partir do `zendeskapp-whatsapp-ativo`, mas trocando webpack/Babel/Jest/ESLint/Prettier por **Vite 8 + Vitest 5 + Biome 2**, com Node 26, pnpm 11, React 19 e TypeScript 7 (só `tsc --noEmit`). O Vite foi escolhido no lugar do webpack porque é o que o scaffold oficial do Zendesk usa hoje e divide a config com o Vitest.

## Rodar

- **Fora do Zendesk** (`pnpm dev`, http://localhost:5173/iframe.html): sem as query params `origin`/`app_guid` o `ZAFClient.init()` do SDK devolve `false`, e o app cai num client ZAF falso (`src/lib/zaf/mock-client.ts`, só em `import.meta.env.DEV`). Papel por `VITE_MOCK_ROLE` (publicador/leitor/nenhum); chamadas vão para `/backend/*`, que o proxy do Vite manda para `BACKEND_URL` (padrão `http://localhost:8080`, o atendimento-zendesk local). Serve enquanto não temos admin no Zendesk.
- **Dentro do Zendesk de dev** (`pnpm dev:zendesk`): build de dev, `dist/zcli.apps.config.json` gerado do `.env` (`tooling/zcli-config.ts`, substitui o `envsub`) e `vite build --watch` + `zcli apps:server dist` (porta 4567). Abrir o Zendesk com `?zcli_apps=true` e recarregar a cada mudança. Pede `zcli login` (subdomínio `contabilizei1637606740`).
- JWT local: com `env` `localhost` ou `mock`, o `ApiClient` manda o token do `localStorage` (`jwt-token-zendesk`), como o whatsapp-ativo.

## Segredos

Como o `jwtSecretKey` e o `ZENDESK_OAUTH_TOKEN` chegam na instalação e no Kong, e os riscos do modelo atual: [[zendesk-apps-segredo-jwt]]; passo a passo em [[subir-secrets-em-apps-zendesk]].

## Papéis

Parâmetros `permissionGpPublicador` e `permissionGpLeitor` (ids de grupos, vários por vírgula). Publicador vence se o usuário tiver os dois. Sem papel, `client.invoke('hide')` tira o ícone (o iframe do nav_bar carrega junto com o Zendesk). Os grupos reais ainda estão em aberto no card.

## Armadilhas

- `pnpm install` dá 401 no `@contabilizei-private/sentinela-foundations` sem token: usar o npmrc temporário com `gcloud auth print-access-token` (ver [[contato-service/install-local|install-local do contato-service]]).
- pnpm 11 bloqueia build scripts: o `pnpm-workspace.yaml` libera `esbuild` e nega `keytar` e `yarn`. O `keytar` (nativo) não compila no `node:26-alpine` (musl) do CI, e o zcli 2.x nem usa o do projeto: o `zcli login` instala o próprio keytar na pasta de plugins dele; no CI o zcli autentica pelas variáveis `ZENDESK_SUBDOMAIN` + `ZENDESK_OAUTH_TOKEN`. O zcli 2.5 não precisa mais do `packageExtensions` de `globby` que o whatsapp-ativo usa.
- `zcli apps:validate` exige login (ou `ZENDESK_SUBDOMAIN` + OAuth): não roda no build local sem credencial.
- O sentinela-foundations exporta `./styles/css` sem tipos: declarar o módulo (`src/types/sentinela.d.ts`).
- Biome 2.6 formata Markdown (alinha as tabelas): o `biome.jsonc` exclui `**/*.md` e `public/`.
- `erasableSyntaxOnly` no tsconfig proíbe parameter properties no construtor (usar campos `#privados`).

## CI

Configuração no repo `pipeline` (MR https://gitlab.com/ctbz/devops/recursos/pipeline/-/merge_requests/3582, sub-task PRD-179455). No componente `ci-cd`, os jobs custom **não instalam dependências sozinhos** (a função `download_dependencies` só roda se for chamada no `*_BEFORE_SCRIPT`). Por isso o build chama `download_dependencies`, que tem o token do `npm-access-token` para o `@contabilizei-private/*`, e o lint e o test reaproveitam o `node_modules` do cache `dependencies`. O deploy não instala nada do app: `node tooling/zcli-config.ts ${ENV}` só usa o Node e o zcli vem do npm público (`npm i -g @zendesk/zcli`). O `test-vitest` lê `coverage/junit-coverage.xml` e `coverage/cobertura-coverage.xml`.

MR do scaffold: https://gitlab.com/ctbz/atendimento/geral/zendeskapp-warnings-and-messages/-/merge_requests/1 (draft).

## Pendente

- Variáveis na UI do GitLab do app: `ZENDESK_OAUTH_TOKEN`, `JWT_SECRET_KEY`, `ZENDESK_APP_ID`, `PERMISSION_GP_PUBLICADOR`, `PERMISSION_GP_LEITOR`.
- `ZENDESK_APP_ID` de dev/prd depois do `zcli apps:create` (precisa de admin).
