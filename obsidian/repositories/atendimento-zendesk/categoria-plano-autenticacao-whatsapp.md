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

Fluxos habilitados (`buscar-fluxos-whatsapp-empresa-possui-acesso.usecase.ts`):

- `CRM`: status `ativo`/`rascunho` e plano `AVANCADO`, `PREMIUM`, `EXPERT` ou `MULTIBENEFICIOS` (`BASICO` só com autopilot ou ramo `COMERCIO`). **Plano Expert desliga o `CRM`**, então cliente Expert chamado com `area: "CRM"` sempre volta `SEM_AUTORIZACAO`. Isso foi mantido de propósito, porque o `CRM` é usado por outros fluxos.
- `OUVIDORIA` (adicionado em 2026-10, branch `feat/expert-autenticacao-ouvidoria`): área nova para o bot autenticar cliente Expert. A regra fica em `verificar-empresa-possui-acesso-ouvidoria.usecase.ts`, que exige CNPJ e repete as regras do `CRM` (delega para `verificarEmpresaPossuiAcessoWhatsAppUseCase`), mas não é desligada pelo plano Expert. Expert com status fora de `ativo`/`rascunho` volta `SEM_AUTORIZACAO` ou `EMPRESA_INATIVA`. Na busca por CNPJ com telefone não vinculado, o retorno é `AUTENTICADO_NAO_VERIFICADO`, via 2FA. Só a rota `POST /` aceita essa área; `POST /perguntas` não aceita. Isso é intencional: o fluxo de ouvidoria do bot não faz 2FA (telefone não vinculado é tratado como não autenticado), então o `perguntas` não precisa aceitar `OUVIDORIA`. Se um dia a ouvidoria passar a usar 2FA, o `perguntas` precisa aceitar a área, porque `perguntas/resultados/:id` reautentica com a área salva no sorteio (`processarAcertos`) e mandar `CRM` faria um Expert cair em `SEM_AUTORIZACAO`. A área também não consulta `habilitadoOuvidoria` (módulo `clientes-habilitados-ouvidoria`); a elegibilidade fica na rota separada `bots/core/verificar-cliente-elegivel-ouvidoria` (não confirmado se o bot a chama antes).
- `BANK`: CNPJ, `categoriaPlano` preenchida e status `ativo`/`rascunho`.
- `EXPERT`: plano normalizado contém "EXPERT" (sem checar status).
- `ATIVACAO`: nenhuma empresa/CNPJ encontrado.

## Flags de vínculo na Ouvidoria (PRD-174256)

Na área `OUVIDORIA`, a resposta traz `clienteTemEmpresaAtiva`, `clienteTemEmpresaInativa` e `clienteTemProcessoAbertura`, para o bot classificar quem entra no número de Ouvidoria (empresa ativa, inativa, abertura ou sem vínculo) sem bloquear o atendimento. A regra fica em `services/identificar-vinculos-cliente.usecase.ts` (branch `feat/PRD-174256`, 2026-11).

- Vêm em todos os retornos (autenticado, `NAO_AUTENTICADO` e `BLOQUEADO`) e olham **todas as empresas do telefone**, mesmo quando o bot manda CNPJ. Nas demais áreas as flags não aparecem e nenhuma chamada extra é feita.
- Empresas: `POST auth/atendimento/v2/bots/whatsapp/dados-cliente/buscar-por-telefone` da plataforma-crm-web (`DadosClienteBasicoPadraoService.buscarEmpresasPorTelefone`), que já separa `empresasAtivasOuRascunho` e `empresasInativas` (com `quantidades.total`). **Armadilha:** a autenticação em si usa outra rota, a `GET .../dados-cliente/basico-padrao`, cujo `empresasEncontradasNaConsultaPorTelefone` não traz o status de cada empresa.
- Abertura: `GET /integracao/twilio/processo/telefone/:tel` do contabilizei-abertura (`buscarProcessosPorTelefone`), contando os processos com `statusJira` diferente de `FINALIZADO` (`WhatsAppProcessoUtil.filtrarProcessosPermitidos`). O telefone vai em E.164 nas duas consultas.
- As duas consultas rodam em paralelo com a autenticação. Uma consulta que falha vira `false` e não vai para o cache (5 min), então a autenticação nunca quebra por causa do monitoramento.
