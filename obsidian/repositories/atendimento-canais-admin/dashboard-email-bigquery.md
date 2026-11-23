---
name: dashboard-email-bigquery
description: "Dashboard de e-mail (Notificações → Email → Dashboard) do atendimento-canais-admin: envios do email-service por dia, template, aplicação e status, lidos do trusted do CDC no BigQuery"
metadata:
  type: reference
tags:
  - atendimento-canais-admin
  - email-service
  - bigquery
  - dashboard
---

# Dashboard de e-mail (BigQuery)

Tela `/notificacoes/email/dashboard`, criada em 23/11/2026 na feature "Uso por template de e-mail". Mostra KPIs (envios, enviados, falhas, pendentes, bloqueados por opt-out), o gráfico de envios por dia empilhado por aplicação, status ou template (`?serie=`) e a tabela por template, com link para o detalhe na tela de Templates.

- **Fonte**: `email_replications` + `email_templates` do trusted do CDC (ver [[dados-no-bigquery]]), dado D-1; o cabeçalho mostra "dados até" com o `max(created_at)` da tabela.
- **Código**: domínio `src/server/domains/email-dashboard/` (filters, source, domain, service), rota `GET /api/notificacoes/email-dashboard`, telas em `src/routes/notificacoes/email/-EmailDashboard*.tsx`.
- **Uma consulta por janela**: a grade dia × template × aplicação × status é buscada só com o filtro de data, e os filtros de template/aplicação são aplicados em memória. Trocar filtro não vai ao BigQuery (cache por statement de 1 h). 30 dias são ~25 linhas.
- **Proteções**: `maximumBytesBilled` de 100 MB por consulta (opção nova do client `src/server/clients/bigquery`), só colunas sem PII selecionadas, janela máxima de 180 dias.
- **Acesso**: usa a key `notificacoes.email.envios` (mesmos envios, agregados), na rota de API e no `beforeLoad`.
- **Armadilha (Recharts)**: as séries são ligadas por chave de índice (`s0`, `s1`…), não pelo valor, porque `application` pode ser um e-mail (envio manual) e o Recharts lê `dataKey` com ponto como caminho no objeto.
- **Armadilha (rota nova)**: o `src/routeTree.gen.ts` só é regenerado pelo `npm run build` (plugin do Vite); rodar o build antes do `npm run typecheck` quando criar rota.
