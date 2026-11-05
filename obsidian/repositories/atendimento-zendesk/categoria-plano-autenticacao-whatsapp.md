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

## Como o statusBot é calculado

O `statusBot` não é persistido: é recalculado a cada chamada em `autenticar-empresa.usecase.ts`.

1. Telefone na lista de bloqueados → `BLOQUEADO`.
2. `statusAutenticacao` (`identificar-status-autenticacao.usecase.ts`) começa em `SEM_AUTORIZACAO` e vira `AUTENTICADO` se a `area` do body estiver em `fluxosHabilitados`. Empresa `inativo` → `EMPRESA_INATIVA`, fluxo eventual → `EVENTUAL` e onboarding → `ONBOARDING` sobrescrevem nessa ordem.
3. `AUTENTICADO` + 2FA `VERIFICADO` → `AUTENTICADO_VERIFICADO`; 2FA só é `NAO_VERIFICADO` quando a busca é por CNPJ e o telefone não está vinculado à empresa.

Empresa com `status` `inativo` (comparação case-insensitive em `empresaLogada.status`) volta `statusBot: EMPRESA_INATIVA` em qualquer área **exceto `OUVIDORIA`** (veja abaixo), com ou sem vínculo do telefone: o `identificarStatusBotUseCase` só olha o 2FA quando o status é `AUTENTICADO`; nos demais casos ele repassa o `statusAutenticacao`. As únicas exceções são o telefone bloqueado (`BLOQUEADO`, checado antes da busca) e a empresa estar no fluxo eventual ou de onboarding, que sobrescrevem para `EVENTUAL`/`ONBOARDING`.

Fluxos habilitados (`buscar-fluxos-whatsapp-empresa-possui-acesso.usecase.ts`):

- `CRM`: status `ativo`/`rascunho` e plano `AVANCADO`, `PREMIUM`, `EXPERT` ou `MULTIBENEFICIOS` (`BASICO` só com autopilot ou ramo `COMERCIO`). **Plano Expert desliga o `CRM`**, então cliente Expert chamado com `area: "CRM"` sempre volta `SEM_AUTORIZACAO`. Isso foi mantido de propósito, porque o `CRM` é usado por outros fluxos.
- `OUVIDORIA`: desde 2026-11-05 (PRD-175399, branch `fix/PRD-174256-ouvidoria-inativa`, MR !189) tem **use case próprio**, o `AutenticarEmpresaOuvidoriaUseCase`, que o controller chama quando `area = OUVIDORIA`. A duplicação de código foi aceita para manter as áreas independentes. O código compartilhado (`AutenticarEmpresaUseCase`, `identificarStatusAutenticacaoUseCase`, `verificarEmpresaPossuiAcessoWhatsAppUseCase`, `buscarFluxosWhatsAppEmpresaPossuiAcessoUseCase`) voltou ao que era antes da OUVIDORIA, e o `Fluxo.OUVIDORIA` não aparece mais nos `fluxosHabilitados`. O acesso fica em `verificar-empresa-possui-acesso-ouvidoria.usecase.ts`, com regra própria (não delega para a do WhatsApp) e exposto no `ResultadoBuscaEmpresaDTO.possuiAcessoOuvidoria`: exige CNPJ, aceita status `ativo`/`rascunho`/`inativo` e repete a regra de plano do `CRM`, com o Expert incluso. Resultado: empresa inativa autentica como ativa (com telefone vinculado `AUTENTICADO_VERIFICADO`, sem vínculo `AUTENTICADO_NAO_VERIFICADO`, nunca `EMPRESA_INATIVA`); plano sem acesso e outros status (ex: `cancelado`) voltam `SEM_AUTORIZACAO`; `BLOQUEADO`, `ONBOARDING` e `EVENTUAL` continuam valendo. Armadilha: como o `dto.ts` importa esse arquivo (import circular), a lista de planos com `CategoriaPlano` precisa ficar dentro da função; numa constante de módulo, o enum ainda está `undefined` e a suíte quebra com `Cannot read properties of undefined (reading 'AVANCADO')`. Só a rota `POST /` aceita essa área; `POST /perguntas` não aceita. Isso é intencional: o fluxo de ouvidoria do bot não faz 2FA (telefone não vinculado é tratado como não autenticado). Se um dia a ouvidoria passar a usar 2FA, o `perguntas` precisa aceitar a área e reautenticar pelo use case da Ouvidoria. A área também não consulta `habilitadoOuvidoria` (módulo `clientes-habilitados-ouvidoria`); a elegibilidade fica na rota separada `bots/core/verificar-cliente-elegivel-ouvidoria` (não confirmado se o bot a chama antes).
- `BANK`: CNPJ, `categoriaPlano` preenchida e status `ativo`/`rascunho`.
- `EXPERT`: plano normalizado contém "EXPERT" (sem checar status).
- `ATIVACAO`: nenhuma empresa/CNPJ encontrado.

## O que é o quantidadeEmpresas (busca sem CNPJ)

Vem do `meta.count` da `GET .../dados-cliente/basico-padrao` da plataforma-crm-web (`BuscarDadosClienteBasicoPadraoWhatsAppBotFacade.filtrarEmpresa`), que busca as empresas pelo telefone da empresa ou do responsável. **Não é só empresa ativa:**

- 1 empresa no telefone: `1`, qualquer que seja o status (pode ser inativa).
- Mais de uma, com alguma `ativo`/`rascunho`: o número de ativas/rascunho, e a `data` é a "melhor" delas (ordenação de `EmpresaAtivaOuRascunhoBasicoPadraoDTO`).
- Mais de uma, todas inativas: o total de empresas, com a `data` da primeira.

Confirmado no código da plataforma-crm-web (`BuscarDadosClienteBasicoPadraoWhatsAppBotFacade.filtrarEmpresa`) e em teste em dev (2026-11-05): telefone com 1 empresa ativa e 1 inativa volta `count = 1`, e a inativa não aparece. Na área `OUVIDORIA` sem CNPJ, o `quantidadeEmpresas` devolvido ao bot já não é esse: vem do total da `buscar-por-telefone` (veja a seção das flags).

Com CNPJ é sempre `1` (ou `0` se não existir). CNPJ que não tem 14 dígitos nem chega a consultar e volta `0`.

Nas áreas `EXPERT` e `ATIVACAO`, a busca vai ao contabilizei-abertura quando vem CPF no body ou quando a busca pelo telefone volta `0`. Nesse caso, `BuscarEmpresaEmAtivacaoPorCpfUseCase` monta o resultado com `meta: { count: 1 }` fixo e `status: 'Rascunho'`, mesmo que o processo venha vazio. Pelo telefone, sem CPF no processo, a busca lança erro. No atendimento-zendesk, o número é só repassado: `ResultadoBuscaEmpresaDTO` copia o `meta.count` (`|| 0`), e a `empresaLogada` só é preenchida quando ele é `1`. Para saber ativas x inativas de verdade, usar a `buscar-por-telefone` (veja a seção abaixo).

## Flags de vínculo na Ouvidoria (PRD-174256)

Na área `OUVIDORIA`, a resposta traz flags para o bot classificar quem entra no número de Ouvidoria (empresa ativa, inativa, abertura ou sem vínculo) sem bloquear o atendimento. A regra fica no `AutenticarEmpresaOuvidoriaUseCase` (2026-11-05, PRD-175399). Histórico: a primeira versão olhava todas as empresas do telefone; a segunda (PRD-175138) usava só a empresa da busca de autenticação e não trazia flags com mais de uma empresa, o que escondia as inativas; a atual volta a olhar todas as empresas sem CNPJ.

- Com CNPJ: `clienteTemEmpresaAtiva` (`ativo`/`rascunho`) e `clienteTemEmpresaInativa` (`inativo`) da **empresa informada**; CNPJ não encontrado volta as duas `false`. `quantidadeEmpresas` é o da busca por CNPJ (1 ou 0).
- Sem CNPJ: flags e `quantidadeEmpresas` vêm da `POST .../dados-cliente/buscar-por-telefone` da plataforma-crm-web (`DadosClienteBasicoPadraoService.buscarEmpresasPorTelefone`, telefone em E.164, cache de 5 min). `quantidadeEmpresas` = `empresasQualquerStatus.quantidades.total`; `clienteTemEmpresaAtiva` = `empresasAtivasOuRascunho.total > 0`; `clienteTemEmpresaInativa` = `empresasInativas.total > 0`, inclusive com mais de uma empresa. A autenticação (`statusBot`, `empresaLogada`) continua pela `basico-padrao`, que escolhe a melhor empresa ativa; se a `buscar-por-telefone` falhar, o erro sobe.
- Sem CNPJ e nenhuma empresa: só `clienteTemProcessoAbertura`, via `VerificarProcessoAberturaUseCase` (`GET /integracao/twilio/processo/telefone/:tel` do contabilizei-abertura, telefone em E.164, processos com `statusJira` diferente de `FINALIZADO`). Falha vira `false`; cache de 5 min guardado como `{ possuiProcesso }`, porque o cache trata `false` como ausente.
- `BLOQUEADO` e as demais áreas não trazem flags.

Como o `quantidadeEmpresas` = 1 pode esconder empresas inativas (veja a seção acima), as flags sem CNPJ refletem só a empresa que a plataforma escolheu. Se um dia precisar de ativas x inativas de todo o telefone, a rota é a `POST .../dados-cliente/buscar-por-telefone` da plataforma-crm-web (separa `empresasAtivasOuRascunho` e `empresasInativas` com `quantidades.total`).
