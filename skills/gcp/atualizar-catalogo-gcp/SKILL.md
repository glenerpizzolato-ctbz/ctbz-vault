---
name: atualizar-catalogo-gcp
description: Atualiza o catálogo de infraestrutura GCP da CTBZ no vault Obsidian CTBZ (`~/ctbz-vault/obsidian/infra/`) — Pub/Sub (tópicos e subscriptions com consumidor), Cloud Scheduler, Cloud Tasks, Cloud Run/functions e workloads do GKE, cruzando cada recurso com os repositórios em ~/repositories que o citam. Use quando o usuário pedir para atualizar/re-sincronizar o catálogo, quando um tópico, subscription, agendamento, fila ou serviço não aparecer no catálogo, ou quando um projeto GCP novo precisar entrar nele.
argument-hint: "[modo: sem-gke|com-gke|offline] [projetos]"
---

# Atualizar o catálogo GCP

O catálogo fica em `~/ctbz-vault/obsidian/infra/` (índice `_infra-indice.md`) e é inteiramente gerado pelo script `scripts/build_catalog.py` desta skill. Nunca editar as notas geradas à mão: qualquer ajuste de formato ou de dado vai para o script, e o catálogo é gerado de novo.

## O que o script faz

1. Para cada projeto em `PROJECTS` (no topo do script), lista via API (token de `gcloud auth print-access-token`): tópicos e subscriptions do Pub/Sub, jobs do Cloud Scheduler e filas do Cloud Tasks (em todas as localizações), serviços/jobs do Cloud Run e Cloud Run functions. Com `--gke`, lista também deployments, statefulsets e cronjobs dos clusters em `CLUSTERS`.
2. Guarda o bruto em `~/.cache/gcp-catalog/raw/` (permite regenerar as notas com `--offline`, sem chamar as APIs).
3. Procura cada nome de recurso (só nomes distintivos: 8+ caracteres com `-`, `.` ou `_`) como token exato no código versionado de cada repositório em `~/repositories` (`git grep`), para indicar quais repos citam cada recurso.
4. Escreve as notas: `pubsub-<projeto>.md` (uma por projeto), `schedulers.md`, `cloud-tasks.md`, `cloud-run-servicos.md`, `gke-workloads.md` (só com `--gke`), `por-repositorio.md` (visão reversa) e `_infra-indice.md`.

Como o consumidor é inferido: subscription push → serviço do endpoint (Cloud Run, App Engine ou host); BigQuery/Cloud Storage → destino; pull → prefixo do nome da subscription (convenção `<consumidor>.sub.<evento>`) mais os repos que citam o nome da subscription. Scheduler mostra cron, fuso e alvo (tópico, HTTP ou App Engine).

## Passo a passo

1. **Atualizar os repositórios locais (opcional, mas melhora o cruzamento):** o cruzamento usa o código que está em `~/repositories`. Se o usuário quiser o mapeamento de repos atualizado, perguntar se pode rodar `git pull` nos repos (não fazer por conta própria, pode haver trabalho local). Repos que não estão clonados não aparecem como citantes.
2. **GKE precisa de VPN:** os clusters privados só respondem com a VPN conectada. Se for atualizar o GKE, pedir para o usuário conectar (ex: `! vpn`) e aguardar a confirmação antes de rodar com `--gke`; não conectar por conta própria. Sem `--gke`, a nota `gke-workloads.md` existente é mantida.
3. **Rodar o script:**

    ```bash
    python3 ~/.claude/skills/atualizar-catalogo-gcp/scripts/build_catalog.py          # tudo, menos GKE
    python3 ~/.claude/skills/atualizar-catalogo-gcp/scripts/build_catalog.py --gke    # inclui GKE (VPN)
    python3 ~/.claude/skills/atualizar-catalogo-gcp/scripts/build_catalog.py --projects aida-prd aida-stg   # só alguns projetos (os demais vêm do último bruto)
    python3 ~/.claude/skills/atualizar-catalogo-gcp/scripts/build_catalog.py --offline   # só regenera as notas
    ```

    Leva ~1–2 min. O resumo no stderr mostra, por projeto, as contagens e os erros (`PERMISSION_DENIED` = a conta não tem acesso para listar aquele recurso; `INVALID_ARGUMENT` em localizações = serviço não disponível ali, é normal).
4. **Conferir o resultado:** `git -C ~/ctbz-vault diff --stat obsidian/infra` e uma olhada no diff para ver o que entrou/saiu (tópicos novos, schedulers removidos etc.). Contar ao usuário as principais mudanças e os projetos sem permissão.
5. **Commit:** só com autorização do usuário, um commit semântico, ex: `docs(obsidian): refresh GCP service catalog`. Se o script também mudou, commitar o script separado (`feat(claude): ...` / `fix(claude): ...`).

## Quando mexer no script

- **Projeto GCP novo:** adicionar em `PROJECTS` (`id`, domínio, ambiente) e também na tabela "Projetos por domínio" do `~/dotfiles/.config/claude/CLAUDE.md`.
- **Cluster novo:** adicionar em `CLUSTERS` e atualizar a seção Kubernetes do `CLAUDE.md`.
- **Namespace de sistema poluindo a lista do GKE:** adicionar em `SYSTEM_NAMESPACES`.
- **Repositório de configuração citando quase tudo:** o script já separa automaticamente os repos que citam mais de `CONFIG_REPO_RATIO` dos nomes (aparecem como `config:`); ajustar a razão se precisar.
- **Localização nova** (ex: recursos em outra região quando a listagem de localizações é negada): incluir em `FALLBACK_LOCATIONS`.

O script vive em `~/ctbz-vault/skills/gcp/atualizar-catalogo-gcp/` (versionado no ctbz-vault) e chega em `~/.claude/skills/` por symlink (`~/dotfiles/installers/setup.sh --symlinks`). Editar sempre a versão do repositório.
