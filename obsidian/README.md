# Vault Obsidian — Memórias de IA

Vault do Obsidian usado para persistir localmente, dentro deste repositório, o conhecimento acumulado nas sessões de agentes de IA (Claude Code, OpenCode etc.) sobre o ambiente CTBZ e o uso pessoal deste dotfiles.

## Como abrir

1. Instale o Obsidian (já incluso em `./installers/setup.sh --ai`):
    ```bash
    sudo snap install obsidian --classic
    ```
2. Abra o Obsidian → "Open folder as vault" → selecione `<raiz do repo>/docs/ai/obsidian`.

## Estrutura

Dois ambientes na raiz, cada um com pastas livres por assunto (sem taxonomia fixa). Dentro de cada ambiente, o `MEMORY.md` é o roteador.

### `ctbz/` — ambiente corporativo CTBZ

- `PRCs/` — Playbooks de PRCs, uma nota por problema em `itens/`, classificados por canal, domínio e sistemas (`_prcs-indice.md`, `PRCs.base`).
- `PRDs/` — Demandas (PRDs) que criei: uma nota por PRD em `itens/`, épicos em `epicos/` e visões por épico, período e domínio (`_prds-indice.md`, `PRDs.base`).
- `next-tasks/` — Próximas tarefas e ideias que ainda não viraram PRD, uma nota por tarefa (`_next-tasks-indice.md`).
- `retros/` — Retrospectivas do time: uma nota por retro (`retro-AAAA-MM-DD.md`) e a pauta da próxima (`retro-proxima.md`).
- `apis/` — Como obter tokens (SSO dev/prd), liberar IP e chamar APIs internas pelo Bruno/curl; só passo a passo, nunca valores (`_apis-indice.md`).
- `tests/` — Roteiros de teste (preparar massa, disparar fluxos, conferir resultado), com visões por domínio e por repositório (`_tests-indice.md`).
- `padroes/` — Convenções que valem para qualquer serviço do time (`_padroes-indice.md`).
- `infra/` — Catálogo GCP do CTBZ: onde cada serviço roda (GKE, Cloud Run/functions), Pub/Sub com consumidores, Scheduler, Cloud Tasks e repositórios que citam cada recurso (`_infra-indice.md`).
- `db/` — Bancos Cloud SQL Postgres por ambiente (dev/prd): instância, porta do proxy, database e como consultar via `psql service=...` (`_db-indice.md`).
- `repositories/` — Uma pasta por repositório com seu índice: como rodar localmente, como testar, fluxos e particularidades (`_repositories-indice.md`).
- `claude-code/` — Uso do próprio Claude Code: onde ficam as sessões, resume global (`cr`) e configurações (`_claude-code-indice.md`).

### `pessoal/` — fora do contexto CTBZ

- `infra/` — Catálogo GCP do projeto pessoal (Cloud Run, Pub/Sub, Scheduler e Cloud Tasks, com repositórios que citam cada recurso) e guias de deploy (Cloud Run, Terraform, GitHub Actions) (`_infra-indice.md`).
- `db/` — Bancos pessoais: locais (Postgres em Docker) e de produção (Supabase/Neon), como conectar via psql e regra de só leitura em prod (`_db-indice.md`).
- `padroes/` — Convenções e receitas que valem para qualquer serviço pessoal (`_padroes-indice.md`).
- `repositories/` — Uma pasta por repositório com seu índice: como rodar localmente, como testar, fluxos e particularidades (`_repositories-indice.md`).

## Como as notas se relacionam

- **Conteúdo genérico fica uma vez só.** Ideia que vale para qualquer serviço vai em `padroes/` (convenção/receita), `infra/` ou `db/`. O que é específico do repositório vai em `repositories/<repo>/`.
- **Nota de repositório não repete o genérico:** ela linka a nota genérica e só acrescenta o que é daquele repositório.
- **Padrão ↔ implementação:** a nota de `padroes/` é o hub e tem uma seção `## Implementações` com os repositórios que o implementam (situação `implementado` ou `planejado`). A nota do repositório aponta de volta para o padrão.
- **Frontmatter carrega a relação**, além do link no texto: no padrão, `implementacoes` (lista de repositórios) e `planejado_em` (lista de repositórios que ainda vão implementar); na nota do repositório, `padroes` (lista de slugs de padrões aplicados). Isso permite consultas e futuras visões em Base sem depender de prosa.
- **Nomes únicos:** cada assunto tem uma nota canônica; se outro repositório precisa da mesma ideia, linke a nota genérica em vez de duplicar. Quando o nome se repetir (ex.: conteúdo espelhado em `ctbz/` e `pessoal/`), use link com caminho desde a raiz do vault: `[[pessoal/infra/schedulers|schedulers]]`.
- **Índices em dois níveis:** o `MEMORY.md` do ambiente é só um roteador (uma linha por sub-pasta, apontando para o índice dela); cada sub-pasta tem seu `_<pasta>-indice.md`, que lista as notas ou roteia para sub-pastas e visões.
- **Front-matter padrão** de cada nota: `name`, `description`, `metadata.type`; campos de relação e `atualizado_em` quando fizer sentido.

## Aviso de segurança

Não salvar segredos, tokens ou credenciais aqui. Este vault entra no versionamento do repositório de dotfiles.
