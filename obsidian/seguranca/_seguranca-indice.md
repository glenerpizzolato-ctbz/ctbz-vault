---
name: seguranca-indice
description: "Índice de notas de segurança: CVEs reportadas pelo Wiz, como mapear o serviço afetado para o repositório e o padrão de correção"
metadata:
  type: reference
tags:
  - seguranca-indice
---

# Segurança

- [[cve-2026-111497-node2shell|CVE-2026-111497 (node2shell)]] — correção nos serviços Cloud Run (pin da imagem Node), planilha de acompanhamento e como achar o repositório real de cada serviço
- [[zendesk-apps-segredo-jwt|Segredo do JWT dos apps Zendesk]] — como o segredo chega na instalação (variável do GitLab -> zcli apps:update) e no Kong (Secret Manager); riscos: igual em dev e prd, impresso no log do deploy, variáveis sem mask
