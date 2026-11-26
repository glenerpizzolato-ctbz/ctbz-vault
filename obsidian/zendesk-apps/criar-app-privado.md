---
name: criar-app-privado
description: "Como criar (instalar pela primeira vez) um app privado no Zendesk: upload do .zip no Admin Center ou zcli apps:create; por que o botão de upload pode não aparecer; o que configurar depois (parâmetros, restrição por grupo, ZENDESK_APP_ID no GitLab)"
metadata:
  type: reference
tags:
  - zendesk-apps
  - zcli
criado_em: 2026-11-26
---

# Criar um app privado no Zendesk

A pipeline só faz `zcli apps:update` (exige `app_id` de um app que já existe). A **primeira** instalação é manual, uma vez por instância (dev `contabilizei1637606740`, prd `contabilizei`).

## Gerar o pacote

```bash
pnpm build && pnpm config:dev     # ou config:prd
pnpm exec zcli apps:package dist  # gera dist/tmp/app-<data>.zip
```

O `apps:package` grava o .zip **antes** de validar pela API; sem login o comando termina com erro de autorização, mas o arquivo fica em `dist/tmp/`. O zip inclui o `zcli.apps.config.json` (com os valores do `.env`): tirar antes de subir (`zip -d <arquivo>.zip zcli.apps.config.json`); o Zendesk não usa esse arquivo.

## Caminho 1: upload pela tela

Admin Center > **Apps e integrações** > **Apps** > **Aplicativos do Zendesk Support** (em inglês: Apps and integrations > Apps > Zendesk Support apps) > botão **Fazer upload de aplicativo privado** (Upload private app), no canto superior direito da página. Escolher o .zip, dar o nome, preencher os parâmetros e instalar.

O botão **não fica** em Marketplace, em "Apps de canal" nem em "Integrações". Se não aparecer na página certa:

- **Papel**: subir app privado exige papel de **Administrador** no Support. Papel customizado (mesmo com "gerenciar apps") e acesso só ao Admin Center de outro produto não mostram o botão.
- **Instância**: conferir se o acesso de admin é na instância certa (dev é `contabilizei1637606740.zendesk.com`).
- **Plano**: apps privados exigem Support/Suite Growth ou superior. As duas instâncias já têm apps privados (whatsapp-ativo, concierge etc.), então o plano não é o problema.

## Caminho 2: zcli apps:create

Com um usuário Administrador:

```bash
pnpm exec zcli login -i                      # subdomínio, e-mail e senha/token de API do admin
pnpm build && pnpm config:dev
pnpm exec zcli apps:create dist              # cria e instala, usando os parâmetros do zcli.apps.config.json
```

O comando devolve o `app_id`.

## Depois de criar

1. Anotar o `app_id` (saída do zcli, ou o `id` do app em `https://<subdomínio>.zendesk.com/api/v2/apps/owned.json`, aberto no navegador com a sessão de admin; a URL do app no Admin Center mostra o id da instalação, não o app_id) e cadastrar `ZENDESK_APP_ID` no GitLab do projeto, por ambiente. A partir daí a pipeline atualiza o app sozinha (e reescreve os parâmetros, ver [[subir-secrets-em-apps-zendesk]]).
2. Na instalação: aba **Configurações** > restringir o app por grupo (os grupos de Publicador e Leitor, no caso do Avisos e Mensagens).
3. Testar com o app instalado; para desenvolver por cima, `?zcli_apps=true` carrega a versão local.
