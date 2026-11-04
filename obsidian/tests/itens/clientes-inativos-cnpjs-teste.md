---
name: clientes-inativos-cnpjs-teste
description: "CNPJs de empresas inativas (baixa, inadimplência, cancelamento) para testar o fluxo de clientes inativos no WhatsApp/Ultimate em dev e prd, levantados dos cards do épico PRD-153607, e como preparar o teste"
metadata:
  type: reference
tags:
  - tests
  - clientes-inativos
dominio:
  - atendimento
  - ultimate
repositorios:
  - ultimate-ia
  - plataforma-crm-web
  - bots-api
ambiente: dev, prd
atualizado_em: 2026-10-26
---

# Clientes inativos: CNPJs de teste (baixa, inadimplência, cancelamento)

Massa de teste do fluxo que recebe clientes inativos no WhatsApp (Ultimate + Zendesk), entregue pelo épico [[PRD-153607]]. Os CNPJs foram tirados das descrições e dos comentários dos cards de teste do épico e conferidos em 2026-10-26.

## CNPJs por cenário

O motivo de prd foi conferido no BigQuery (`contabilizei-dataflow.saude_empresa.empresa`, último snapshot por CNPJ, tabela com período máximo `202609`). Em dev, a API do bot respondeu 503 em 2026-10-26 e não deu para revalidar: fica a evidência do teste feito no card.

| Cenário | CNPJ | Razão social | Inativa desde | Prd (BQ) | Usado em teste | Card |
|---|---|---|---|---|---|---|
| Baixa | `28983783000190` | 1984 COMERCIO DE PRODUTOS ARTISTICOS LTDA - ME | 2019-03-22 | INATIVO / BAIXA (último snapshot 202608) | dev (Zendesk sandbox, 2026-07) | [PRD-159983](https://contabilizeicontabilidade.atlassian.net/browse/PRD-159983) |
| Baixa | `44310168000179` | 2MARQUES TECNOLOGIA DA INFORMACAO LTDA | 2026-05-26 | INATIVO / BAIXA | prd (2026-05) | [PRD-154005](https://contabilizeicontabilidade.atlassian.net/browse/PRD-154005) |
| Inadimplência | `27296605000128` | ALENCASTRO & ALBUQUERQUE PRODUCAO MUSICAL LTDA - ME | 2018-06-04 | INATIVO / INADIMPLENCIA | dev (admin-dev-03, 2026-07) | [PRD-159983](https://contabilizeicontabilidade.atlassian.net/browse/PRD-159983), [PRD-159773](https://contabilizeicontabilidade.atlassian.net/browse/PRD-159773) |
| Inadimplência | `55495245000129` | 10LOK LOCADORA DE VEICULOS LTDA | 2025-03-01 | INATIVO / INADIMPLENCIA | prd (2026-05) | [PRD-154006](https://contabilizeicontabilidade.atlassian.net/browse/PRD-154006) |
| Cancelamento | `28209303000138` | 300 SOFTWARES SOLUCOES EM TI LTDA | 2026-05-23 | INATIVO / CANCELAMENTO | dev (2026-07) | [PRD-159983](https://contabilizeicontabilidade.atlassian.net/browse/PRD-159983) |
| Cancelamento | `07570742000100` | 1500 AGENCIA DE VIAGENS LTDA | 2020-07-13 | INATIVO / CANCELAMENTO | dev (alternativa, 2026-07) | [PRD-159983](https://contabilizeicontabilidade.atlassian.net/browse/PRD-159983) |
| Cancelamento | `58146704000157` | AMOR MARCA MARKETING DESIGN E CRIATIVIDADE LTDA | 2025-11-25 | INATIVO / CANCELAMENTO (último snapshot 202608) | prd (2026-05) | [PRD-153930](https://contabilizeicontabilidade.atlassian.net/browse/PRD-153930) |
| Cancelamento | `30399517000166` | FELIPE DA CRUZ SANTOS SILVA | 2026-05-23 | INATIVO / CANCELAMENTO | prd (2026-09, teste sem feature-flag) | [PRD-167694](https://contabilizeicontabilidade.atlassian.net/browse/PRD-167694) |

Sugestão por ambiente:

- **Dev:** baixa `28983783000190`, inadimplência `27296605000128`, cancelamento `28209303000138` (ou `07570742000100`). Foram os usados na homologação de dev (Zendesk sandbox `contabilizei1637606740`).
- **Prd:** baixa `44310168000179`, inadimplência `55495245000129`, cancelamento `58146704000157` ou `30399517000166`. Os CNPJs de dev também estão inativos em prd com o mesmo motivo, então servem nos dois ambientes.

Não usar `12996446000105`: aparece em [PRD-153874](https://contabilizeicontabilidade.atlassian.net/browse/PRD-153874) só como "CNPJ de outra pessoa", para provar que o bot barra um CNPJ não vinculado ao telefone.

## Como preparar o teste

1. **Telefone do testador só na empresa do cenário:** editar a empresa no admin (dev: `https://admin-dev-03.ctbz.com.br/#/edit-empresa/<cnpj>`) e colocar o próprio telefone nela. Tirar o telefone das empresas ativas de teste, senão o bot autentica pela empresa ativa.
2. **Achar outra empresa inativa, se precisar:** filtrar no admin por status/motivo. Para impersonar uma empresa de prd, há o endpoint de impersonate do `bots-api` (tutorial em [PRD-153623](https://contabilizeicontabilidade.atlassian.net/browse/PRD-153623)).
3. **Feature-flag:** até 2026-09-17 o CNPJ precisava estar na flag `sys_rollout_cliente_inativo` do `bots-api`. A flag foi removida em [[PRD-167692]], e hoje toda empresa inativa entra no fluxo novo.
4. **Horário de atendimento:** desde [PRD-166516](https://contabilizeicontabilidade.atlassian.net/browse/PRD-166516), o fluxo de inativos só atende de segunda a sexta, das 9h às 18h (schedule_flow próprio no `bots-api`/`experts-admin`). Fora desse horário, o bot bloqueia e avisa o horário.
5. **Depois dos testes:** fechar os tickets abertos com a skill `fechar-tickets-teste-zendesk` ([[fechar-tickets-teste-zendesk]]).

## O que conferir (cenários dos cards)

- **Segurança:** um telefone com 2+ empresas inativas não avança com um CNPJ que não seja dele. Uma empresa inativa sem motivo vai direto para o OTP.
- **Cada motivo:** o menu cai depois de 2 erros, o escalonamento manda a mensagem certa para o grupo certo e as tags ficam certas no ticket. Os menus de cada motivo estão nos comentários de [PRD-159983](https://contabilizeicontabilidade.atlassian.net/browse/PRD-159983). Exemplos: inadimplência tem "Colocar em dia", "Pedir um documento", "Cancelar plano" e "Outro assunto"; baixa tem "Reativar meu CNPJ", "Documentos finais" e "Outro assunto".
- **Desidratar a Ouvidoria ([[PRD-173036]]):** nos três motivos, "Outro assunto" passa a transbordar para Cobrança D60 (inadimplência) ou para Contábil Cancelamento (cancelado/baixado). O nó novo "Fazer reclamação" vai para a Ouvidoria, com as tags `metric_inat_*_outro_reclamacao`.
- **Zendesk:** o grupo `[Autoatendimento] Clientes inativos` tem ID `29093144928284` em dev e `29092124673692` em prd ([PRD-153624](https://contabilizeicontabilidade.atlassian.net/browse/PRD-153624)).

## Como revalidar o status de um CNPJ

- **Prd (BigQuery):** `SELECT cnpj, periodo, status, motivo_status, data_inativacao FROM \`contabilizei-dataflow.saude_empresa.empresa\` WHERE cnpj = '<cnpj>' QUALIFY ROW_NUMBER() OVER (PARTITION BY cnpj ORDER BY periodo DESC) = 1`. É um snapshot mensal: uma inativação recente pode ainda não aparecer.
- **Dev/prd (API do bot):** `GET {{bots_base_url}}/atendimento/zendesk/bots/whatsapp/plataforma/atendimento/v2/bots/whatsapp/dados-cliente/experts/cnpj/<cnpj>` com header `x-api-key`. Está na coleção Bruno do `plataforma-crm-web`, em `docs/bruno/bots/autentica empresa by cnpj.bru`. Em 2026-10-26, dev respondeu 503 e prd respondeu 401 com o `apiGatewayTokenPrd` do `.env`.
