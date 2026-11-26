---
name: zendesk-apps-indice
description: "Índice de notas sobre apps Zendesk (ZAF) do atendimento: como configurar, subir secrets e parâmetros, deploy com zcli e particularidades comuns a todos os zendeskapp-*"
metadata:
  type: reference
tags:
  - zendesk-apps-indice
---

# Apps Zendesk

Notas que valem para todos os apps Zendesk (`zendeskapp-*`, ZAF 2.0, deploy com zcli pelo componente de CI do grupo). O que é específico de um app fica na pasta dele em [[_repositories-indice|repositories]].

- [[subir-secrets-em-apps-zendesk]] — como cadastrar e atualizar secrets e parâmetros de um app (manifest, template do zcli, variável do GitLab, deploy), usar no código, rodar local e rotacionar
- [[sdk-zaf-versao-fixa-sri]] — o `<script>` do SDK do ZAF vira hotspot no Sonar (Web:S5725): usar a URL com versão fixa (2.0.37) + integrity + crossorigin
- [[criar-app-privado]] — primeira instalação de um app privado (upload do .zip no Admin Center ou `zcli apps:create`), por que o botão de upload some e o que configurar depois (`ZENDESK_APP_ID`, restrição por grupo)
- [[autenticacao-kong-jwt]] — os apps chegam ao atendimento-zendesk por dois Kongs (antigo `atendimento-crm`, novo `api.contabilizei.com.br`/kong-config, padrão para app novo), com JWT do consumer de apps; o que é a "Chave do JWT", como testar e como plugar um app novo com consumer próprio
