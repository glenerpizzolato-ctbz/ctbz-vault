---
name: compartilhar-com-o-time
description: "html-share (https://html-share.ctbz.com.br/): serviço interno para compartilhar com o time páginas HTML e Markdown (artefatos do Claude, relatórios) e deixá-las salvas; é o que o usuário quer dizer com \"compartilhar com o time\""
metadata:
  type: reference
tags:
  - artefatos
  - comunicacao
---

# Compartilhar com o time (html-share)

**"Compartilhar com o time"** um artefato, HTML ou `.md` significa subir no **html-share**: https://html-share.ctbz.com.br/. É o jeito de o time abrir a página e de ela ficar salva, sem depender do link privado do `claude.ai/artifact` (que só abre para quem recebeu acesso).

## Como funciona

- Serviço interno, atrás do login Google da Contabilizei (a raiz redireciona para o SSO). Não há API conhecida: o **upload é feito pelo usuário no navegador**. O Claude gera o arquivo e entrega o caminho; não sobe sozinho.
- Aceita `.html` e `.md`.

## Como gerar o arquivo a partir de um artefato do Claude

O HTML publicado como artefato não tem `<!doctype>`, `<html>`, `<head>` nem `<body>`: a plataforma injeta esse esqueleto na publicação. Para o html-share, gerar a versão completa:

1. Partir do HTML-fonte guardado em `artefatos/arquivos/<slug>.html`.
2. Envolver em `<!doctype html><html lang="pt-BR"><head>…</head><body>…</body></html>`: no `<head>`, `meta charset="utf-8"`, `meta viewport` (`width=device-width, initial-scale=1, viewport-fit=cover`), o reset do artefato (`:root{color-scheme:light;padding-top/bottom: env(safe-area-inset-*)}`, `body{margin:0}`, `img{max-width:100%}`, `[hidden]{display:none!important}`) e tudo o que vem antes do conteúdo (`<title>`, `<meta>`, `<link>` de fontes, `<style>`); no `<body>`, o resto.
3. Salvar em `~/Downloads/<slug>.html` para o upload e conferir que o arquivo parseia.
4. Depois do upload, pedir o link ao usuário e registrar em `html_share` no front-matter da nota do artefato.

Fontes do Google e scripts de CDN continuam carregando normalmente fora do claude.ai.

## Compartilhados

- [[mapa-whatsapp-ativo|Mapa do WhatsApp Ativo]] — gerado em `~/Downloads/mapa-whatsapp-ativo.html` em 19/11/2026; link do html-share pendente
