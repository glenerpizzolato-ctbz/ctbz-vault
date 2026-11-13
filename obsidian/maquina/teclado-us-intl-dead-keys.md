---
name: teclado-us-intl-dead-keys
description: "Teclado US (ex: CK103 Motorspeed) no Ubuntu/GNOME com acentos iguais ao US-International do Windows: layout us+intl, .XCompose para o ç e as armadilhas (us+altgr-intl, .Xmodmap)"
metadata:
  type: reference
tags:
  - maquina
  - teclado
  - linux
---

# Teclado US com acentos como no Windows (Ubuntu/GNOME)

Teclado físico US ANSI (ex: **CK103 Motorspeed**, sem a tecla `ç`) usado no Ubuntu com GNOME (Wayland + IBus), para os acentos funcionarem como no layout **US-International do Windows**.

## Comportamento esperado

- `'` + `e` = `é`, `` ` `` + `a` = `à`, `~` + `a` = `ã`, `^` + `e` = `ê`, `"` + `u` = `ü` (teclas mortas, sem AltGr).
- `'` + `c` = `ç` (e `'` + `C` = `Ç`).
- `'` + espaço = `'`, e também <kbd>AltGr</kbd> + `'` = `'`.

## Configuração

1. Layout **English (US, intl., with dead keys)** = `us+intl`, mantendo o `br` como segunda opção (troca com <kbd>Super</kbd>+<kbd>Espaço</kbd>):

   ```bash
   gsettings set org.gnome.desktop.input-sources sources "[('xkb', 'us+intl'), ('xkb', 'br')]"
   ```

2. `~/.XCompose` para o `ç`, porque no Linux `'` + `c` dá `ć` por padrão. O IBus lê esse arquivo também no Wayland:

   ```
   include "%L"
   <dead_acute> <c> : "ç" ccedilla
   <dead_acute> <C> : "Ç" Ccedilla
   ```

3. `ibus restart` e reabrir os apps (ou logout/login) para o `ç` valer.

O arquivo fica versionado no dotfiles (`~/dotfiles/.config/.XCompose`) e o `~/dotfiles/installers/setup.sh --symlinks` aplica os dois passos; o checklist está em `~/dotfiles/installers/setup.md` (seção Native Linux Desktop Environment).

## Armadilhas

- **`us+altgr-intl`** (English, intl., with AltGr dead keys) é o oposto do desejado: o `'` sai direto e o acento só funciona com <kbd>AltGr</kbd> + `'` + letra.
- **`us+alt-intl`** é outra variante (antiga), não usar.
- Um `~/.Xmodmap` com `keycode 48 = apostrophe quotedbl` (contorno antigo) mata a tecla morta do `'` se for carregado. No GNOME Wayland ele não é aplicado automaticamente; conferir com `xmodmap -pke | grep -E "keycode +48 "`, que deve mostrar `dead_acute`.
- Sem o `.XCompose`, `'` + `c` gera `ć` em vez de `ç`.
