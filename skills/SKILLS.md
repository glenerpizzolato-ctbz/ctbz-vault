# Skills de IA

Roteador das skills versionadas no dotfiles, organizadas por domínio no mesmo sistema de índices do vault: uma pasta por domínio, cada uma com seu índice `_<dominio>-indice.md` listando as skills dela. Um domínio pode agrupar sub-domínios (ex: `ctbz/jira/`), e aí o índice dele só roteia para os índices dos sub-domínios. Aqui fica só uma linha por domínio, nunca skills individuais.

As skills seguem o formato aberto de Agent Skills (`<skill>/SKILL.md` com front-matter `name` e `description`, mais `scripts/` opcionais), que não depende de harness. Por isso ficam em `docs/ai/skills/` e não numa pasta de um agente específico.

Os harnesses só descobrem skills num nível de pasta (`<pasta-de-skills>/<nome>/SKILL.md`), então o `./installers/setup.sh --symlinks` cria um symlink plano por skill (`<dominio>/[<sub-dominio>/]<skill>/` → `<skill>`, em qualquer profundidade) em cada pasta de skills:

- `~/.claude/skills/`: Claude Code (o OpenCode também lê essa pasta).
- `~/.agents/skills/`: pasta compartilhada para outros harnesses.

Para apontar outro harness, incluir a pasta dele em `skills_targets` de `installers/modules/symlinks.sh`. O nome da pasta da skill precisa ser único entre todos os domínios. Editar sempre aqui, nunca pelos symlinks.

Os parâmetros de uma skill ficam no `argument-hint` do front-matter (o campo do Claude Code), sempre entre aspas: `<nome>` é obrigatório, `[nome]` é opcional e `nome: a|b|c` restringe às opções (ex: `argument-hint: "<telefone> [area: CRM|BANK|EXPERT|ATIVACAO] [ambiente: prd|dev]"`). A aba Skills do BahCode monta o formulário a partir dele e chama a skill como `/<skill> nome=valor …`, só com o que foi preenchido; skill sem parâmetro fica sem o campo.

Ao criar uma skill nova:

1. Colocar em `<dominio>/<skill>/SKILL.md`, ou `<dominio>/<sub-dominio>/<skill>/SKILL.md` quando o domínio agrupa sub-domínios (ex: skills do ambiente corporativo vão em `ctbz/<sub-dominio>/`). Criar a pasta do domínio/sub-domínio se nenhuma existente for um bom encaixe.
2. Adicionar uma linha no índice do domínio ou sub-domínio. Se ele for novo, criar o índice e adicionar uma linha no índice de cima (aqui, ou no `_<dominio>-indice.md` do domínio pai).
3. Rodar `./installers/setup.sh --symlinks` (ou criar o symlink à mão) para a skill aparecer nos harnesses.

## Domínios

- [BahCode](bahcode/_bahcode-indice.md) — operar o BahCode por fora da interface: worktrees e conjuntos de terminais das features
- [CTBZ](ctbz/_ctbz-indice.md) — ambiente corporativo da Contabilizei: empresas (massa de teste por plano, busca por telefone e autenticação no bot de WhatsApp), GCP (catálogo de infraestrutura), GitLab (abrir MR, tratar comentários e corrigir pipeline), Jira (sincronização das PRDs do vault) e Zendesk (tickets de teste e conversas afetadas por erros da Ultimate)
