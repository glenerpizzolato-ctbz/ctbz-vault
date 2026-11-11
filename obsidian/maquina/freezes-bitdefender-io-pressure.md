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

O Vitals (extensão do GNOME) não mostra PSI. Ele tem só `Read rate`/`Write rate` em Storage, que nesse caso ficam baixos e não denunciam o problema.
