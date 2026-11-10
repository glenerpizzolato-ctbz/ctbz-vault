---
name: metadados-whatsapp-hubspot
description: "Chaves que o MetadadosGuiaFactory manda em metadados do WhatsApp (evento whatsapp_ativo do HubSpot): grupo, guias e parcelas, formatos e quando cada uma fica ausente"
metadata:
  type: reference
tags:
  - microsservico-agrupamento-guias
  - hubspot
  - whatsapp
repositorio: microsservico-agrupamento-guias
atualizado_em: 2026-11-10
---

# Metadados do WhatsApp (evento `whatsapp_ativo` do HubSpot)

O `MetadadosGuiaFactory.from(grupoGuia)` (`integrations/`) monta o `Map<String, String>` que vai em `metadados` no WhatsApp do agrupamento (Experts e BP LP) e vira property do evento `whatsapp_ativo` no HubSpot. O contrato fica no atendimento-zendesk (`docs/hubspot/README.md` e `evento-whatsapp-ativo.json`): o HubSpot descarta em silêncio chave não declarada no evento, então chave nova exige declarar a property antes (ou junto) do deploy.

Regras (a partir do PRD-176511, branch `feat/PRD-176511`):

- **Grupo**: `id_grupo_guia`, `competencia`, `vencimento` (AAAA-MM-DD em America/Sao_Paulo, o menor entre guias e parcelas), sempre que o grupo tem algum documento.
- **Guias**: `ids_guia`, `quantidade_guias`, `valor_total` (soma do `valorPrincipal`), `tipos_imposto` (nome do enum `Imposto`), só com as guias; ausentes num grupo só de parcelas. O experts-service usa as mesmas chaves na guia avulsa, então o significado não pode mudar.
- **Parcelas**: `ids_parcela` (`idParcela`), `quantidade_parcelas`, `valor_total_parcelas` (soma do `valor`, nulo conta zero), `tipos_parcelamento` (só nomes conhecidos de `TipoParcelamento`; sem nenhum, a chave fica ausente); ausentes quando o grupo não tem parcela.
- Listas cercadas por `;` (`;42;43;`): property de evento só filtra com `contains`, que casaria por substring numa lista com vírgula. Valores com 2 casas, ponto decimal, sem separador de milhar.
- Grupo sem documento algum: mapa vazio.

Antes do PRD-176440 (MR !100), um grupo com parcela quebrava o WhatsApp (`requireNotNull(controleGuia)` → FALHA / ERRO_DESCONHECIDO).

Jira: na sub-task de Desenvolvimento, a transição de To-do para Building se chama `Started` (id 61) e a de Building para Pull Request, `Gerar Pull Request` (id 331).
