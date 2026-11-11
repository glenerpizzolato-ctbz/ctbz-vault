---
name: freezes-bitdefender-io-pressure
description: Freezes na máquina com disco ocioso mas pressão de I/O alta; suspeita principal é o Bitdefender (bdsecd, módulo ctc); como diagnosticar com PSI
metadata:
  type: reference
---

# Freezes com pressão de I/O alta (Bitdefender)

Em 2026-11-11 a máquina (Ubuntu 24.04, NVMe ADATA 512GB com LUKS + LVM, 20 núcleos, 31GB RAM) estava travando ("freezes macabros"), e um colega do time relatou o mesmo.

## O que o diagnóstico mostrou

- `/proc/pressure/io` com `some ≈ 42%` e `full ≈ 36%` de forma constante: em mais de um terço do tempo todos os processos ativos estavam parados esperando I/O. `top` mostrava 15–17% de `wa`.
- O disco em si estava ocioso: na amostra de 10s do `/proc/diskstats`, ~2 MB/s, latência < 1ms e util ~0%. Então a espera não vinha do throughput do NVMe.
- CPU e memória sem pressão (PSI cpu/memory ~0), swap 2.6G/8G usado, sem OOM nem `hung task` no journal.
- O Bitdefender (`bdsecd`, serviço `bdsec-daemon`) era o maior consumidor: o módulo `ctc` com ~5h de CPU em 6,5h de vida e picos de 150–240%, e ~6GB de RSS somando os módulos. Os módulos `ctc` e `antimalware` tinham reiniciado ~1h depois do boot, num update (`update.jso.temp`). Ele intercepta abertura de arquivo via fanotify (módulo `fanotify`, `pkgSlots=32`), o que pode segurar processos esperando sem que o disco trabalhe.

Conclusão provável: os travamentos vêm do Bitdefender (scan on-access/EDR), e não do hardware. Por ser o agente corporativo, isso também explicaria o mesmo problema na máquina de um colega. A correção (exclusões de pastas como `~/repositories`, `node_modules`, `.git`, `~/.cache`, ou ajuste da política do `ctc`) é com o time de TI/segurança, que administra a política.

## Como diagnosticar de novo

```bash
cat /proc/pressure/io            # some/full avg10 altos = processos esperando I/O
top -b -n 3 -d 2 | grep -E "bdsecd|^%Cpu"   # wa% e CPU do Bitdefender
ps -o pid,etime,time,pcpu,rss,cmd -p $(pgrep -d, bdsecd)
```

Se o PSI de io estiver alto e o disco ocioso no `/proc/diskstats`, a espera é artificial (fanotify/agente), não do disco.

## Por que Read/Write rate (Vitals) não denunciam o Bitdefender

`Read rate`/`Write rate` medem o volume de dados que **chega ao disco**. Com o Bitdefender, a espera acontece **antes** do disco:

1. O programa (git, node, Chrome) pede para abrir um arquivo.
2. O kernel avisa o Bitdefender via fanotify e o processo fica parado até ele liberar.
3. Com o `ctc` em 150–240% de CPU, a liberação demora; só depois a leitura vai para o disco, e aí é rápida.

O Linux conta essa espera como "esperando I/O" (`wa` no `top`, PSI de io), mesmo com o disco parado. É como uma fila enorme num caixa lento: Read/Write rate medem o que passa pelo caixa, e o PSI mede o tamanho da fila.

## Diagnóstico diferencial durante um freeze

| Freeze com... | Causa provável |
|---|---|
| Read/Write rate **altos** (dezenas/centenas de MB/s) | carga real de disco: `docker pull`, build, swap, `git clone` grande |
| Read/Write rate **baixos** e PSI io alto | processos presos no fanotify: Bitdefender |

Limitações do Vitals:

- Ele roda dentro do `gnome-shell` e atualiza a cada 5s (`update-time`); num freeze forte trava junto ou mostra o valor antigo. O valor logo depois de destravar é mais confiável.
- Não mostra PSI, que é o que de fato denuncia a fila. Chaves dos sensores de disco, se quiser na barra: `_storage_read_rate_` e `_storage_write_rate_` (em `hot-sensors`, via `dconf write /org/gnome/shell/extensions/vitals/hot-sensors`; a extensão só relê ao ser reiniciada com `gnome-extensions disable/enable Vitals@CoreCoding.com`).

Para registrar evidência de cada freeze (horário, PSI de io e CPU do Bitdefender) e olhar depois que destravar:

```bash
while true; do echo "$(date +%T) $(head -1 /proc/pressure/io) $(top -b -n1 | awk '/bdsecd/{s+=$9} END{print "bdsecd="s"%"}')"; sleep 2; done | tee ~/freeze-io.log
```

Em `/proc/pressure/io`, `avg10` acima de ~20 durante o travamento confirma a fila de I/O.
