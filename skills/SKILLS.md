# Skills de IA — CTBZ

Roteador das skills do ambiente corporativo CTBZ (Contabilizei), versionadas no `~/ctbz-vault` junto com o vault corporativo (`~/ctbz-vault/obsidian/`). As skills pessoais e as regras gerais (formato, `argument-hint`, symlinks) ficam no dotfiles, em `~/dotfiles/docs/ai/skills/SKILLS.md`.

Mesmo sistema de índices do vault: uma pasta por domínio, cada uma com seu índice `_<dominio>-indice.md` listando as skills dela. Aqui fica só uma linha por domínio, nunca skills individuais.

O `~/dotfiles/installers/setup.sh --symlinks` também varre `~/ctbz-vault/skills/` (quando o repositório existe) e cria um symlink plano por skill em `~/.claude/skills/` e `~/.agents/skills/`. O nome da pasta da skill precisa ser único entre todos os domínios, inclusive os do dotfiles. Editar sempre aqui, nunca pelos symlinks.

Ao criar uma skill nova:

1. Colocar em `<dominio>/<skill>/SKILL.md`, criando a pasta do domínio se nenhuma existente for um bom encaixe.
2. Adicionar uma linha no índice do domínio. Se ele for novo, criar o índice e adicionar uma linha aqui.
3. Rodar `~/dotfiles/installers/setup.sh --symlinks` (ou criar o symlink à mão) para a skill aparecer nos harnesses.

## Domínios

- [Empresas](empresas/_empresas-indice.md) — massa de teste por plano, busca de empresas por telefone e autenticação no bot de WhatsApp
- [GCP](gcp/_gcp-indice.md) — catálogo de infraestrutura GCP no vault
- [GitLab](gitlab/_gitlab-indice.md) — abrir MR, tratar comentários de revisão e corrigir pipeline
- [Jira](jira/_jira-indice.md) — sincronização das PRDs do vault com o Jira
- [Zendesk](zendesk/_zendesk-indice.md) — fechar tickets de teste e mapear conversas afetadas por erros da Ultimate
