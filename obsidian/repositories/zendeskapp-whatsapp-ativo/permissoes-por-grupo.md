---
name: zendeskapp-whatsapp-ativo-permissoes-por-grupo
description: "Como o zendeskapp-whatsapp-ativo libera atendimentos/projetos de template (ex: ATIVACAO_MIGRACAO, CSA, FINANCEIRO, FLOW) por grupo do Zendesk, via settings permissionGp* do app"
metadata:
  type: reference
tags:
  - zendeskapp-whatsapp-ativo
  - permissoes
---

# Permissões por grupo do Zendesk

Cada permissão é um setting do app (`src/manifest.json`, `permissionGp*`, tipo texto) cujo valor é o **id de um grupo do Zendesk**. O front compara `authClient._currentUser.groups[].id` com o id do setting (`id == settings.permissionGpX`). O valor vem de `environments/zcli.apps.config.<dev|prod>.json` (`${PERMISSION_GP_...}`) no deploy e pode ser visto/alterado nas configurações do app instalado no Zendesk (Admin Center > Apps). Não está nas variáveis de CI do projeto (lá só há `ZENDESK_SUBDOMAIN`).

## ATIVACAO_MIGRACAO

Tem grupo próprio: `permissionGpAtivacaoMigracao` (`PERMISSION_GP_ATIVACAO_MIGRACAO`).

- **Criação de template** (`WhatsappTemplates/components/ModalAddTemplate.tsx` + `InputsModal.tsx`): a opção "ATIVAÇÃO E MIGRAÇÃO" do dropdown Projeto só aparece se o agente estiver no grupo. Mesmo padrão de `CSA`, `FINANCEIRO` e `FLOW`; os demais projetos (CORE, EXPERTS, BANK…) aparecem para todos.
- **Seleção de atendimento** (`components/whatsapp-ativo/atendimento-select/atendimento.service.ts`): sem o grupo, `ATIVACAO_MIGRACAO` é removido da lista.
- **WhatsApp individual** (`WhatsappIndividual.tsx`, `filter-mode.ts`): sem o grupo, o filtro específico de ativação/migração nunca é aplicado.

Se o agente "não vê" a opção, conferir se ele está no grupo cujo id está em `permissionGpAtivacaoMigracao` (skill `buscar-grupo-zendesk` traduz id ↔ nome e lista membros). Lembrar que o Zendesk pode precisar de reload do app após mudar grupo do agente.

`permissionGpTemplateCreation` é outra coisa: libera recursos extras do editor de template (header, botões etc.), não o projeto.
