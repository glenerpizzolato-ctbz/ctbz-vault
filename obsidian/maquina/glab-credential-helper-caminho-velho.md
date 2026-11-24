---
name: glab-credential-helper-caminho-velho
description: Push/fetch no GitLab falha com "/usr/bin/glab: not found" porque o ~/.gitconfig aponta o credential helper para o caminho antigo do glab (hoje em ~/.local/bin); contorna por comando e correção definitiva
metadata:
  type: reference
tags: [maquina, git, glab, gitlab]
---

# Credential helper do GitLab apontando para um glab que não existe

## Sintoma

O push (ou fetch) por HTTPS no GitLab falha, e com ele o auto-resolve de pipeline e threads do BahCode (skills `pipe`, `comentario` e `mr`):

```
/usr/bin/glab auth git-credential get: 1: /usr/bin/glab: not found
fatal: could not read Username for 'https://gitlab.com': No such device or address
```

## Causa

O `~/.gitconfig` (arquivo local, não versionado no dotfiles) tem o helper com o caminho absoluto de quando o glab era instalado pelo apt:

```
[credential "https://gitlab.com"]
	helper =
	helper = !/usr/bin/glab auth git-credential
```

Hoje o glab fica em `~/.local/bin/glab`, então o helper não roda e o git cai no prompt de usuário (que não existe no terminal do agente).

## Contorna (sem mexer na config)

Trocar o helper só no comando, pelo glab do `PATH` (testado em 2026-11-24 com `ls-remote` no experts-api-gateway):

```sh
git -c credential.https://gitlab.com.helper= -c "credential.https://gitlab.com.helper=!$(command -v glab) auth git-credential" push <argumentos>
```

O `helper=` vazio zera a lista vinda do `~/.gitconfig`; o segundo `-c` põe o caminho certo. As skills `gitlab/pipe`, `gitlab/comentario` e `gitlab/mr` têm essa contorna na seção "Push com o glab fora de `/usr/bin`".

## Correção definitiva

```sh
git config --global --replace-all credential.https://gitlab.com.helper '!glab auth git-credential' '/usr/bin/glab'
```

Sem caminho absoluto, o helper segue o glab do `PATH` em qualquer instalação.

> [!NOTE]
> Correção definitiva aplicada nesta máquina em 2026-11-24 (o helper agora é `!glab auth git-credential`). A contorna nas skills fica para outra máquina ou instalação que volte a ter o caminho velho.
