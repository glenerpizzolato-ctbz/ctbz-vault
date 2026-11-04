---
name: hdmi-nvidia-driver-kernel
description: Notebook Dell (Intel + RTX 3050) não reconhece HDMI quando o kernel atualiza e o módulo NVIDIA não acompanha; como diagnosticar e corrigir
metadata:
  type: reference
---

# HDMI não reconhecido (driver NVIDIA ausente no kernel novo)

No notebook (Intel Raptor Lake + NVIDIA RTX 3050 Laptop, Ubuntu 24.04 HWE, `prime-select on-demand`), a saída HDMI é ligada à GPU NVIDIA. Sem o driver `nvidia` carregado, a porta nem aparece em `/sys/class/drm/` (só `card1-eDP-1` e `card1-DP-1` da Intel), e o monitor não é detectado.

Causa encontrada em 2026-10-28: o kernel subiu para `6.17.0-22-generic`, mas o meta-pacote `linux-modules-nvidia-570-open-generic-hwe-24.04` ficou parado no 6.14, então não havia módulo NVIDIA para o kernel em uso (`nouveau` está em blacklist, então a GPU fica sem driver).

## Diagnóstico

```bash
ls /sys/class/drm/                 # sem card*-HDMI-* => GPU NVIDIA sem driver
lsmod | grep nvidia                # sem o módulo nvidia
nvidia-smi                         # "couldn't communicate with the NVIDIA driver"
find /lib/modules/$(uname -r) -name 'nvidia*.ko*'   # sem nvidia.ko para o kernel atual
```

## Correção

```bash
sudo apt update
sudo apt install linux-modules-nvidia-570-open-$(uname -r) linux-modules-nvidia-570-open-generic-hwe-24.04
sudo reboot
```

Atualizar o meta-pacote `-generic-hwe-24.04` junto evita que o problema volte no próximo kernel. Alternativa: `sudo ubuntu-drivers install` para escolher o driver recomendado.

## Armadilha: "unmet dependencies" / "held packages" no 570 (2026-10-28)

A correção acima falhou com `nvidia-driver-570-open : Depends: nvidia-kernel-common-570 (<= 570.172.08-1) but 570.211.01... is to be installed` e `pkgProblemResolver::Resolve generated breaks, this may be caused by held packages`. Causas:

- `nvidia-driver-570-open` e `linux-modules-nvidia-570-open-generic-hwe-24.04` estavam em `hold` (`apt-mark showhold`; `linux-generic-hwe-24.04` também), travados no 570.172 / kernel 6.14, enquanto o módulo do 6.17 exige o `nvidia-kernel-common-570` 570.211.
- No noble-updates o 570.211 virou transição para o 580 (instalar o 570 puxa `nvidia-driver-580-open`), e o meta-pacote `-generic-hwe-24.04` novo já aponta para o kernel 7.0 e o 580.
- O módulo pré-compilado `linux-modules-nvidia-580-open-6.17.0-22-generic` foi gerado para o 580.142, mas o repositório tem o 580.178, então também não instala. Saída: DKMS.

Correção que resolve na simulação (`apt-get -s ... --allow-change-held-packages`):

```bash
sudo apt-mark unhold nvidia-driver-570-open linux-modules-nvidia-570-open-generic-hwe-24.04
sudo apt install nvidia-driver-580-open nvidia-dkms-580-open linux-headers-$(uname -r) \
  nvidia-driver-570-open- linux-modules-nvidia-570-open-generic-hwe-24.04- linux-modules-nvidia-570-open-6.14.0-33-generic-
sudo reboot
```

Secure Boot está ligado e a chave `/var/lib/shim-signed/mok/MOK.der` não estava registrada: o install pede uma senha de MOK e, no reboot, a tela azul do MOK Manager pede "Enroll MOK" > Continue > Yes > a mesma senha. Sem esse passo o módulo assinado pelo DKMS não carrega (`Required key not available`). Para refazer manualmente: `sudo mokutil --import /var/lib/shim-signed/mok/MOK.der`. Com DKMS, o módulo é recompilado a cada kernel novo.

## Resultado da troca 570 → 580 (confirmado em 2026-10-28)

Depois de registrar a chave MOK, o 580 ficou funcionando: `nvidia-smi` mostra `Driver Version: 580.178.04` (CUDA 13.0), `/proc/driver/nvidia/version` mostra o *Open Kernel Module* 580.178.04, o `modinfo nvidia` aponta para `/lib/modules/6.17.0-22-generic/updates/dkms/nvidia.ko.zst` (DKMS), `lspci -k` mostra `Kernel driver in use: nvidia` na RTX 3050 e `card2-HDMI-A-1` aparece como `connected`. O `prime-select` continua `on-demand` (a Intel renderiza o desktop e a NVIDIA cuida do HDMI e do offload, provider `NVIDIA-G0` no `xrandr --listproviders`).

### Intel (`i915`) x NVIDIA: as duas ficam em uso

O notebook tem duas placas e cada uma usa o próprio driver, sem conflito: a Intel integrada usa o `i915` e a RTX 3050 usa o `nvidia`. Ver `i915` em uso não quer dizer que o driver da NVIDIA não esteja ativo.

| Modo (`prime-select`) | Intel (`i915`) | NVIDIA (`nvidia`) |
| --- | --- | --- |
| `on-demand` (atual) | Desenha o desktop e a tela do notebook (eDP) | Liga o HDMI e roda o que for mandado para ela (jogos, CUDA, `__NV_PRIME_RENDER_OFFLOAD=1`) |
| `nvidia` | Fica praticamente parada | Desenha tudo, inclusive a tela do notebook |

Para trocar: `sudo prime-select nvidia` + reboot (para voltar: `sudo prime-select on-demand` + reboot). A parte negativa de deixar só a NVIDIA é a bateria: a placa dedicada fica sempre ligada e gasta bem mais energia, por isso o `on-demand` é o padrão.

Sobras do 570 que podem ser removidas: `nvidia-utils-570`, `nvidia-kernel-common-570` e `nvidia-kernel-source-570-open` (ainda instalados), além dos pacotes em estado `rc` (`sudo apt purge '~c'` limpa as configs residuais).

Para conferir rapidamente qual driver está em uso:

```bash
nvidia-smi | head -4
cat /proc/driver/nvidia/version
modinfo nvidia | grep -E '^(version|filename)'
dkms status
prime-select query
```

## Travadas na tela depois da troca para o 580 (investigado em 2026-10-30)

Sintoma: travadinhas de vez em quando, com CPU, memória e GPU NVIDIA aparentemente ociosas. O que foi encontrado:

- Os dois monitores externos não estavam no HDMI (NVIDIA), e sim no hub USB-C/DP MST da Intel (`DP-1-1` a 180 Hz e `DP-1-2` a 144 Hz), com a tela do notebook (`eDP-1`) a 120 Hz. `HDMI-1-0` aparecia `disconnected`, e o `nvidia-smi` mostrava só o Xorg com 4 MiB: a NVIDIA não desenhava nada.
- Sessão em **X11** (`XDG_SESSION_TYPE=x11`), embora o Wayland esteja disponível (`ubuntu-wayland.desktop`, `WaylandEnable` comentado no gdm). No X11 o GNOME sincroniza todos os monitores por um único relógio, então taxas diferentes (120/144/180) causam engasgos.
- `/proc/pressure/io` com `full` ~30% e load average ~7, mas o NVMe parado: quem ficava em estado `D` eram os workers `kworker/...+i915_flip` (49 de 50 amostras), isto é, o pipeline de exibição da Intel esperando page flip, não disco.

Testes sugeridos, nesta ordem: igualar os monitores externos a 60 Hz (ou todos na mesma taxa) e ver se as travadas somem; entrar na sessão "Ubuntu" em Wayland pela engrenagem do login; ligar um dos monitores direto no HDMI (NVIDIA) para tirar o MST do caminho. Conferir o efeito com:

```bash
for i in $(seq 50); do ps -eo stat,comm | awk '$1~/^D/ && $2~/i915_flip/' | wc -l; sleep 0.1; done | grep -vc '^0'
cat /proc/pressure/io
```
