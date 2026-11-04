---
name: comentario
description: Trata os comentários de revisão pendentes de um Merge Request do GitLab - lê as threads abertas pelo glab, corrige o código quando o comentário procede, commita e dá push, e responde (e resolve) cada thread explicando o que foi feito ou por que não. Use quando o usuário pedir para tratar/responder os comentários do MR, ou quando o BahCode mandar `/comentario !<iid>` (botão "Mandar pro Claude" da aba MR).
argument-hint: "[!iid]"
---

# Tratar os comentários do MR

1. Descobrir o MR: o `!<iid>` dos argumentos (`$ARGUMENTS`) ou o da branch atual (`glab mr list --source-branch $(git branch --show-current)`).
2. Ler as threads: `glab api "projects/:id/merge_requests/<iid>/discussions?per_page=100"`, ficando só com as que têm nota resolvível e não resolvida (`resolvable && !resolved`), e com o arquivo/linha de cada uma (`position.new_path`, `position.new_line`).
3. Para cada thread, ler o código no ponto citado e decidir:
   - **procede**: corrigir;
   - **não procede** ou é dúvida: preparar a resposta com o motivo;
   - **não está claro** ou muda o escopo: perguntar ao usuário antes de mexer.
4. Rodar os testes/lint do que foi mexido, commitar com commit semântico (`fix: …` / `refactor: …`, citando a key do card quando houver) e dar push na branch do MR.
5. Responder cada thread em português, curto, com o que foi feito (citando o commit) ou o porquê de não mudar: `glab api -X POST "projects/:id/merge_requests/<iid>/discussions/<discussion_id>/notes" -f body="…"`. Resolver (`-X PUT …/discussions/<discussion_id> -f resolved=true`) só as que foram corrigidas; as respondidas sem mudança ficam para o revisor resolver.
6. Responder ao usuário com a lista: thread, decisão e commit.
