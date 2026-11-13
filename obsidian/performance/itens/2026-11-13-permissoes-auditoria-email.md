---
name: 2026-11-13-permissoes-auditoria-email
description: "Permissões por operação e trilha de auditoria persistente na área de e-mail do admin (criar/inativar template e enviar e-mail a clientes)"
metadata:
  type: project
tags:
  - performance
titulo: "Permissões por operação e auditoria na área de e-mail do admin"
data: 2026-11-13
periodo: 2026QD3
categorias: [seguranca]
impacto: medio
fontes: ["[[status-template-email]]", "[[PRD-177215]]"]
---

# Permissões por operação e auditoria na área de e-mail do admin

## Contexto

No soft delete de templates de e-mail (PRD-177215), a área de e-mail do atendimento-canais-admin tinha uma chave só (`notificacoes.email`) que liberava tudo: ler templates, criar, inativar (o que para os envios de todos os serviços) e enviar e-mail a clientes. E nenhuma dessas operações ia para a trilha de auditoria persistente: só uma linha de stdout de 30 dias, sem registro da pessoa no email-service.

## O que fiz

- Separei em cinco permissões (listar templates, criar, ativar/inativar, listar envios, enviar), concedidas por grupo do Keycloak ou e-mail, com guarda nas rotas de API e nos botões da tela (MR !186).
- Passei a gravar na trilha `auditoria` (Firestore, `/admin/auditoria`) quem criou, inativou/reativou e enviou, inclusive as tentativas recusadas, sem dados do cliente (MR !187).

## Resultado

Operações que chegam ao cliente passam a ter quem pode (permissão própria) e quem fez (registro permanente). 100% de cobertura nos arquivos alterados.

## Evidências

- MRs atendimento-canais-admin !185, !186 e !187 (corrente)
- [[status-template-email]]
