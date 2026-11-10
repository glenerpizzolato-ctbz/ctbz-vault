---
name: approves-do-dia-via-glab
description: "Como contar os MRs aprovados no dia por uma pessoa no GitLab via glab (events API) e como achar o id GitLab dos colegas do time"
metadata:
  type: reference
---

# Approves do dia via glab

O `rinha-ai-revisors` (ranking de brincadeira com pódio de bichinhos, `node server.mjs` → http://localhost:3000) conta os approves de MR do dia de cada pessoa de `team.json`, a cada 5 min.

- **Fonte**: `glab api "users/<id>/events?action=approved&after=<AAAA-MM-DD>&per_page=100"`. Traz os approves de MR de qualquer usuário (não só o logado), com `target_iid`, `project_id`, `target_title` e `created_at` (UTC). O `after` é exclusivo e em UTC, então pedir a partir de dois dias antes e filtrar pela data local (`America/Sao_Paulo`).
- Aprovar, remover o approve e aprovar de novo gera eventos repetidos: deduplicar por `project_id` + `target_iid`.
- **Achar o id de um colega**: a busca `users?search=<nome>` no gitlab.com traz vários homônimos. Buscar entre os membros do grupo: `glab api "groups/ctbz/members/all?query=<nome>"`.
- Ids do time Eng Canais (2026-11): Henrique Aurelio `29488727` (henrique.aurelio), Rafael Maestro `27871512` (rafael.maestro1), Gabriel Ganassin `27227622` (gabriel.ganassin.ctbz), Igor Alves `27247552` (igor.alves4), Luiz Nascimento `42030357` (luiz.nascimento8, nome no GitLab "Luiz Henrique"), Glener Pizzolato `27870772` (glener.pizzolato), Eugenio Bonadio `33107896` (eugenio.bonadio, nome no GitLab "Geninho").

## Outras fontes usadas pelo ranking

- **Comentários**: `users/<id>/events?action=commented` traz `note.noteable_type` (`MergeRequest`), `note.noteable_iid` e `note.system`. Muitos comentários são respostas no próprio MR, então para medir revisão é preciso buscar o autor do MR (`projects/<id>/merge_requests/<iid>` → `author.username`) e descartar os próprios.
- **Detalhes do MR** (`created_at`, `author`, `web_url`): não mudam, então vale cachear por `project_id!iid` durante a vida do processo.
- Os eventos paginam em 100; para olhar ~15 dias de approves de quem revisa muito, iterar `page` até vir menos de 100.
- **Expor para o time sem tela de aviso**: o localtunnel (`lt`) mostra uma tela anti-phishing pedindo o IP público; o ngrok gratuito também tem aviso. O `cloudflared tunnel --url http://localhost:<porta>` (binário em `~/.local/bin/cloudflared`, sem conta) não tem. A URL `*.trycloudflare.com` some no log; recuperar com `curl -s localhost:20241/quicktunnel`. Ela leva de 10 a 30 s para resolver no DNS depois de criada.
