---
name: _por-dominio-tests
description: "Índice dos roteiros de teste agrupados por domínio; um roteiro pode estar em mais de um"
metadata:
  type: reference
tags:
  - tests-indice
---

# Testes por domínio

Um roteiro pode aparecer em mais de um domínio.

## atendimento — canais, WhatsApp, Zendesk

- [[fechar-tickets-teste-zendesk]] — fechar os tickets que os testes dos bots deixam abertos no Zendesk (skill `fechar-tickets-teste-zendesk`) · prd
- [[clientes-inativos-cnpjs-teste]] — CNPJs inativos por motivo (baixa, inadimplência, cancelamento) e preparo do teste do fluxo de inativos no WhatsApp · dev, prd
- [[destravar-atendimento-ultimate]] — conversa de WhatsApp presa numa sessão antiga do bot (`Sem assistência`): inatividade, pass/release control e delete da conversa no Sunshine · prd

## impostos — guias de imposto, agrupamento de guias, diagnóstico

- [[preparar-grupo-guia-agrupamento]] — preparar `controle_guias` e gerar `grupo_guia` com PDF; competência, Storage e status · dev

## notificacoes — WhatsApp ativo, templates, e-mails

- [[preparar-grupo-guia-agrupamento]] — pré-requisito das notificações de grupo de guia (grupo em `SUCESSO_AGRUPAMENTO`) · dev

## ultimate — bots da Ultimate

- [[clientes-inativos-cnpjs-teste]] — massa de teste do fluxo de clientes inativos (intents Id Empresa/Id Ativação e Cliente Inativo) · dev, prd
- [[destravar-atendimento-ultimate]] — destravar sessão presa da Ultimate para testar a versão nova do fluxo · prd
