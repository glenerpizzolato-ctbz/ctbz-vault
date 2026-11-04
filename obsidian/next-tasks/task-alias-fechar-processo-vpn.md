---
name: task-alias-fechar-processo-vpn
description: "Alias para fechar processo aberto da VPN"
metadata:
  type: project
tags:
  - next-task
titulo: "Alias para fechar processo aberto da VPN"
tipo: tarefa
tema: terminal
dominio:
  - dev-tools
origem: conversa
anotado_em: 2026-10-09
---

# Alias para fechar processo aberto da VPN

Criar um alias para encerrar um processo da VPN que ficou aberto/travado. Hoje existe a função `vpn_off` (alias `vpn-off`) em `ctbz/terminal`, que mata o `forticlientsslvpn_cli`; avaliar cobrir também o processo da GUI (`forticlientsslvpn`) e um `pppd` preso.

> Texto original: "Alias fechar processo aberto da vpn"

## Notas

<!-- Detalhes, decisões, PRD criado a partir desta tarefa. -->
