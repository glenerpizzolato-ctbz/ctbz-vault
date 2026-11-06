---
name: comunicacao-indice
description: "Onde enviar mensagens por assunto (espaços do Google Chat etc.) e como enviar; consultar sempre que o usuário pedir para enviar/avisar algo sobre um assunto"
metadata:
  type: reference
tags:
  - comunicacao-indice
---

# Comunicação

Para onde vai cada mensagem, por assunto. Quando o usuário pedir para "enviar", "avisar" ou "mandar mensagem" sobre um assunto, procurar o canal aqui. Se o assunto não estiver na tabela, perguntar o canal e registrá-lo aqui.

## Canais por assunto

| Assunto | Canal | Link |
| --- | --- | --- |
| PRCs (chamados): andamento, triagem, repasses, pedidos ao time | Espaço "PRCs \| Eng. Canais" (Google Chat) | https://mail.google.com/mail/u/0/#chat/space/AAQAfFlovh4 |
| Alertas de prod do Cloud Monitoring (Pub/Sub, memória do Cloud Run, % de erro) e as investigações automáticas: responder na thread do alerta | Espaço "Engenharia Canais \| Alertas" (Google Chat) | https://chat.google.com/room/AAAA22umHGg |

## Como enviar

- **Google Chat:** não há integração direta (MCP). O envio é feito pelo navegador com a extensão Claude in Chrome, e a mensagem sai com o nome do usuário. Abrir o link do espaço numa aba nova, clicar na caixa de mensagem (o Chat fica num iframe, então o `find` não acha a caixa: usar coordenada do screenshot), digitar, conferir no screenshot, `Enter` e fechar a aba. Sempre mostrar o texto ao usuário e enviar só depois da confirmação dele.
- **Links e menções no Google Chat (via Claude in Chrome):**
  - Link no texto: digitar o texto (ex: `PRC-153105`), selecionar com `shift+Left` (repetido), `ctrl+k`, digitar a URL e clicar em **Apply**. O `Enter` não fecha a caixa do link de forma confiável e tira o foco do editor: depois de cada link, clicar no fim do texto e dar `ctrl+End` antes de continuar digitando.
  - Menção: digitar `@` sozinho (com a ação `type`, não `shift+2`, que sai como `2` no layout do teclado), esperar ~2s, digitar as primeiras letras uma a uma (`M`, `u`) e clicar na pessoa na lista. Se o texto for digitado de uma vez, a lista de sugestões não abre.
  - Editar mensagem já enviada: passar o mouse sobre ela e clicar no lápis; `ctrl+a` substitui o texto; salvar em **Update**. Menção adicionada na edição vira chip normal.
  - Links de PRC: `https://contabilizeicontabilidade.atlassian.net/browse/<PRC>`.
- **Extensão desconectada** ("Browser extension is not connected" / `list_connected_browsers` vazio, mesmo com a extensão ativa): o usuário roda `/chrome` no Claude Code para reconectar.
- **Google Chat via API, em nome do usuário (pendente):** não há MCP do Google Chat. Para enviar com o nome do usuário pela API, é preciso um OAuth client em projeto GCP **corporativo** (tela de consentimento `Internal`, escopo `chat.messages.create`) e o app do Chat configurado no projeto. A Chat API já está ativa em `atendimento-canais-dev`. O usuário não tem permissão para criar o client (só papéis de uso nos projetos de experts/atendimento), então isso depende do time de infra. Webhook do espaço também funciona, mas posta como bot.
- **Estilo:** mensagens curtas, em português, com as chaves dos PRCs em link e, quando houver, quem ficou responsável e qual o próximo passo.
