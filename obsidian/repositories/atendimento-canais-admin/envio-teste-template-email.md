---
name: envio-teste-template-email
description: "Telas de e-mail do admin: aviso de envio de teste obrigatório após criar template e o atalho ?enviar=<templateId> que abre o envio com o template já escolhido"
metadata:
  type: project
tags:
  - atendimento-canais-admin
  - email-service
---

# Envio de teste de template de e-mail

Feature [[PRD-176949]] (card PRD-176949, MR atendimento-canais-admin!184, 2026-11-12). A branch se chama `feat/PRD-170664` por engano: o PRD-170664 é outro card (remoção de telefone/e-mail do contato).

- A validação de HTML do modal de criação (`email-templates.html.ts`) só barra CSS que os clientes não aplicam (`<style>`, `<link>`, `class`, `@import`). O SMTP da HubSpot e clientes como Outlook/Gmail ainda descartam ou redesenham muita coisa que o preview (iframe) mostra certo, então a única validação confiável é um envio real.
- Por isso, `src/routes/notificacoes/email/-AvisoEnvioTeste.tsx` mostra um aviso fixo (tons `--c-warning-*`) no modal de criação, junto do botão Criar, e no detalhe do template logo após criar (`TemplateDetalheModal` com `recemCriado`, que a tela de templates liga só para o id que o próprio operador acabou de criar, em estado local, não na URL).
- No detalhe, o aviso tem o atalho para `/notificacoes/email/envios?enviar=<templateId>`: o parâmetro `enviar` abre o modal de envio (`EnvioCriarModal`, prop `templateInicial`) com o template já preenchido. Ele não é filtro (fica fora de `CAMPOS_DE_FILTRO`) e é removido da URL ao fechar o modal, mantendo filtros e página.
- O modal de envio é remontado por `key={enviar}`, porque o rascunho só lê `templateInicial` no mount.

Armadilha: rodar `npx vitest` de dentro de uma subpasta ignora a config do projeto e quebra quase todos os testes; sempre rodar da raiz (`npx vitest run src/routes/...`).
