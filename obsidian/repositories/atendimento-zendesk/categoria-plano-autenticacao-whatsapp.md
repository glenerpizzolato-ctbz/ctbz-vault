---
name: categoria-plano-autenticacao-whatsapp
description: "Valores do enum CategoriaPlano retornado em categoriaPlano pelo endpoint /api/v1/bots/whatsapp/autenticacao/basico-padrao e como o valor do CRM é normalizado"
metadata:
  type: reference
tags:
  - atendimento-zendesk
  - whatsapp
  - autenticacao
---

# CategoriaPlano na autenticação do WhatsApp (basico-padrao)

O campo `categoriaPlano` da resposta de `/api/v1/bots/whatsapp/autenticacao/basico-padrao` (controller `whatsapp-autenticacao-basico-padrao.controller.ts`) é o enum `CategoriaPlano`, definido em `src/domain/bots/whatsapp/whatsapp-autenticacao/dto.ts`:

- `NAO_IDENTIFICADO` (default, inclusive quando nenhuma empresa é encontrada)
- `AVANCADO`
- `BASICO`
- `EXPERT`
- `PREMIUM`
- `MULTIBENEFICIOS`

O valor vem do `categoriaPlano` (ou `plano`) devolvido pela plataforma-crm-web e é classificado em `services/identificar-categoria-plano.usecase.ts`: remove acentos e tudo que não é letra/espaço, passa para maiúsculas e compara por igualdade com `AVANCADO`, `BASICO`, `PREMIUM` e `MULTIBENEFICIOS`. `EXPERT` é por `includes` (qualquer plano que contenha "EXPERT" vira `EXPERT`). Qualquer outro valor cai em `NAO_IDENTIFICADO`.

## categoriaPlano na plataforma-crm-web (buscar-por-telefone-e-cnpj e demais rotas do bot)

Na plataforma-crm-web, o `empresaLogada.categoriaPlano` da `POST .../dados-cliente/buscar-por-telefone-e-cnpj` (e das outras rotas do bot) não é o enum acima: é o valor cru de `Empresa.identificarCategoriaPlano()` (`domain/plataforma/extension/EmpresaExtension.kt`).

1. Se o `PagtoPlano` tem `categoriaV2`, devolve o `nome` dessa entidade (`CategoriaPlano` do Datastore, no contabilizei-back-core). É um cadastro, não um enum, então pode vir qualquer nome que exista lá.
2. Senão, devolve o enum `PagtoPlanoCategoria` do contabilizei-back-core: `BASICO`, `AVANCADO`, `PREMIUM`, `EXPERT_ESSENCIAL`, `EXPERT_PRO`, `MULTIBENEFICIOS`.
3. Empresa sem categoria no plano volta `BASICO` (default).
4. Se o CNPJ não é encontrado no telefone, o DTO volta sem empresa, com `categoriaPlano: ""`.

O atendimento-zendesk normaliza esse valor para o seu enum (`EXPERT_ESSENCIAL`/`EXPERT_PRO` viram `EXPERT`).

## Como o statusBot é calculado

O `statusBot` não é persistido: é recalculado a cada chamada em `autenticar-empresa.usecase.ts`.

1. Telefone na lista de bloqueados → `BLOQUEADO`.
2. `statusAutenticacao` (`identificar-status-autenticacao.usecase.ts`) começa em `SEM_AUTORIZACAO` e vira `AUTENTICADO` se a `area` do body estiver em `fluxosHabilitados`. Empresa `inativo` → `EMPRESA_INATIVA`, fluxo eventual → `EVENTUAL` e onboarding → `ONBOARDING` sobrescrevem nessa ordem.
3. `AUTENTICADO` + 2FA `VERIFICADO` → `AUTENTICADO_VERIFICADO`; 2FA só é `NAO_VERIFICADO` quando a busca é por CNPJ e o telefone não está vinculado à empresa.

Empresa com `status` `inativo` (comparação case-insensitive em `empresaLogada.status`) volta `statusBot: EMPRESA_INATIVA` em qualquer área, com ou sem vínculo do telefone: o `identificarStatusBotUseCase` só olha o 2FA quando o status é `AUTENTICADO`; nos demais casos ele repassa o `statusAutenticacao`. As únicas exceções são o telefone bloqueado (`BLOQUEADO`, checado antes da busca) e a empresa estar no fluxo eventual ou de onboarding, que sobrescrevem para `EVENTUAL`/`ONBOARDING`.

Fluxos habilitados (`buscar-fluxos-whatsapp-empresa-possui-acesso.usecase.ts`):

- `CRM`: status `ativo`/`rascunho` e plano `AVANCADO`, `PREMIUM`, `EXPERT` ou `MULTIBENEFICIOS` (`BASICO` só com autopilot ou ramo `COMERCIO`). **Plano Expert desliga o `CRM`**, então cliente Expert chamado com `area: "CRM"` sempre volta `SEM_AUTORIZACAO`. Isso foi mantido de propósito, porque o `CRM` é usado por outros fluxos.
- `OUVIDORIA`: **removida em 2026-11-05** (MR !189, branch `fix/PRD-174256-ouvidoria-inativa`). Ela existiu entre 2026-10 e 2026-11, para o bot de Ouvidoria autenticar cliente Expert e receber as flags `clienteTemEmpresaAtiva`/`clienteTemEmpresaInativa`/`clienteTemProcessoAbertura` (PRD-174256), e chegou a ter use case próprio aceitando empresa inativa. Saiu porque o bot de Ouvidoria passou a usar outras APIs, diretas e prontas. O `POST /` voltou a aceitar só `ATIVACAO`, `BANK`, `CRM` e `EXPERT`, e o código ficou idêntico ao de antes do merge de `feat/expert-autenticacao-ouvidoria`. O `BotsTipoFluxo.OUVIDORIA` (tickets, grupos, horário de atendimento) é outro enum e continua.
- `BANK`: CNPJ, `categoriaPlano` preenchida e status `ativo`/`rascunho`.
- `EXPERT`: plano normalizado contém "EXPERT" (sem checar status).
- `ATIVACAO`: nenhuma empresa/CNPJ encontrado.

## O que é o quantidadeEmpresas (busca sem CNPJ)

Vem do `meta.count` da `GET .../dados-cliente/basico-padrao` da plataforma-crm-web (`BuscarDadosClienteBasicoPadraoWhatsAppBotFacade.filtrarEmpresa`), que busca as empresas pelo telefone da empresa ou do responsável. **Não é só empresa ativa:**

- 1 empresa no telefone: `1`, qualquer que seja o status (pode ser inativa).
- Mais de uma, com alguma `ativo`/`rascunho`: o número de ativas/rascunho, e a `data` é a "melhor" delas (ordenação de `EmpresaAtivaOuRascunhoBasicoPadraoDTO`).
- Mais de uma, todas inativas: o total de empresas, com a `data` da primeira.

Confirmado no código da plataforma-crm-web (`BuscarDadosClienteBasicoPadraoWhatsAppBotFacade.filtrarEmpresa`) e em teste em dev (2026-11-05): telefone com 1 empresa ativa e 1 inativa volta `count = 1`, e a inativa não aparece.

Com CNPJ é sempre `1` (ou `0` se não existir). CNPJ que não tem 14 dígitos nem chega a consultar e volta `0`.

Nas áreas `EXPERT` e `ATIVACAO`, a busca vai ao contabilizei-abertura quando vem CPF no body ou quando a busca pelo telefone volta `0`. Nesse caso, `BuscarEmpresaEmAtivacaoPorCpfUseCase` monta o resultado com `meta: { count: 1 }` fixo e `status: 'Rascunho'`, mesmo que o processo venha vazio. Pelo telefone, sem CPF no processo, a busca lança erro. No atendimento-zendesk, o número é só repassado: `ResultadoBuscaEmpresaDTO` copia o `meta.count` (`|| 0`), e a `empresaLogada` só é preenchida quando ele é `1`. Para saber ativas x inativas de verdade, usar a `buscar-por-telefone` (veja a seção abaixo).

## Flags de vínculo na Ouvidoria (PRD-174256, removidas)

As flags da Ouvidoria saíram junto com a área `OUVIDORIA` em 2026-11-05 (veja acima). Se um dia for preciso saber as empresas ativas x inativas de um telefone, a rota é a `POST .../dados-cliente/buscar-por-telefone` da plataforma-crm-web, que separa `empresasAtivasOuRascunho`, `empresasInativas` e `empresasQualquerStatus` (com `quantidades.total` e os CNPJs). A busca de autenticação (`basico-padrao`) esconde as inativas quando o telefone tem alguma ativa.

Como o `quantidadeEmpresas` = 1 pode esconder empresas inativas (veja a seção acima), as flags sem CNPJ refletem só a empresa que a plataforma escolheu. Se um dia precisar de ativas x inativas de todo o telefone, a rota é a `POST .../dados-cliente/buscar-por-telefone` da plataforma-crm-web (separa `empresasAtivasOuRascunho` e `empresasInativas` com `quantidades.total`).
