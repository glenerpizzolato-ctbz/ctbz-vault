---
name: validar-email-tomador-nfs
description: "O que faz a rota POST .../bots/whatsapp/fluxos/experts/nfs/tomadores/email/validar do atendimento-zendesk (fluxo de nota fiscal Experts no bot WhatsApp): só checa formato de e-mail por regex frouxa, sem chamada externa"
metadata:
  type: reference
tags:
  - ultimate
  - atendimento-zendesk
  - experts-nfs
---

# Validar e-mail do tomador (fluxo NFS Experts)

Conferido no código do `atendimento-zendesk` em 2026-11-16.

- **URL pelo gateway:** `POST https://{{apigatewayUrl}}/atendimento/zendesk/bots/whatsapp/fluxo/interacao/api/v1/bots/whatsapp/fluxos/experts/nfs/tomadores/email/validar`. O prefixo `/atendimento/zendesk/bots/whatsapp/fluxo/interacao` é do Kong (`strip_path_fluxo_interacao` na coleção Bruno); no serviço a rota é `/api/v1/bots/whatsapp/fluxos/experts/nfs/tomadores/email/validar`.
- **Código:** `experts-fluxo-notafiscal.controller.ts` (`buscarValidadeEmailTomadorSanitizar`) → `ValidarEmailTomadorService.executar` → `EmailUtil.validate` (`src/infra/util/email.util.ts`).
- **Body:** `{ "email": "..." }`. Coleção Bruno: `experts-bruno/atendimento-zendesk/(kong)/[web]/bots/whatsapp/experts/nf-individual/tomadores/novo/validar/email.bru`.
- **Resposta (sempre 200):** `{ "data": { "experts": { "nfs": { "emailTomador": { "motivo": "SUCESSO" | "EMAIL_INVALIDO", "isValido": true | false } } } } }`.

## O que valida, de fato

- Só o **formato**, com a regex `/\S+@\S+\.\S+/`. Não consulta nenhum serviço, não grava nada e não olha a empresa nem o tomador.
- A regex **não é ancorada**: basta o texto **conter** algo como `x@y.z`. Passa `a@b.c`, `meu email é joao@empresa.com.br obrigado` e `a@b.c@d`. Também passa e-mail com espaço em volta ou letras maiúsculas, porque não há trim nem normalização.
- Reprova o que não tem `@` ou não tem ponto depois do `@` (ex: `joao@empresa`), e também body sem `email`: `undefined` vira a string `"undefined"` e dá `EMAIL_INVALIDO`, sem erro 400.
- Não checa domínio (o `EmailUtil.validateDomain`, que só aceita `contabilizei.com(.br)`, não é usado aqui), MX nem e-mail descartável.
- O enum tem `ERRO_INTERNO`, mas a rota nunca o devolve.
- No fluxo, o bot usa a rota para aceitar ou pedir de novo o e-mail do tomador ao emitir nota. Como a regex é frouxa, o e-mail que passa pode chegar com texto extra ou espaços ao experts-nfs.

## De onde vem o `emailAssessorOngoing` que o bot envia (conferido em 2026-11-16)

Lido no bot `[prod] ctbz wpp main` pela API de leitura do dashboard ([[dashboard-read-api]]), com aprovação do Glener na conversa:

- Os replies `Wpp Shared | Id Empresa Count v01` (`6a996986d7cec5465398a561`) e `Wpp Shared | Id Empresa Auth v02` (`6aabea0ed20cdb130e7e8915`) não citam a variável nos nós. Quem a preenche é a integração **`[pltf-crm] GET | consulta CNPJ - Shared`** (`673b8c73da41e7fc95e7a4bf`), chamada no Auth v02, no cenário `Success`: `emailAssessorOngoing <- data.data.empresaLogada.assessor`.
- Outras integrações que também mapeiam a variável: `[pltf-crm] POST | autentica CNPJ - Shared` (`66a015df6c8ff05882b4802e`), `[pltf-crm] POST | autentica CNPJ • Shared Survey`, `Contabilizei - Experts - Identificação - Carteira Agente`, `Contabilizei - Experts - Validar Email - Ongoing` e `Contabilizei - Experts - Validate - Post Feedback`.
- No `plataforma-crm-web`, a rota é `POST auth/atendimento/v2/bots/whatsapp/dados-cliente/buscar-por-telefone-e-cnpj` (`BuscarDadosGeralWhatsAppBotFacade.prepararDadosParaRetorno`). O `empresaLogada.assessor` é `empresa.planoPagamentoEmpresa.assessorPlano`, o assessor do plano da empresa. A entidade fica numa lib, fora do repo.
- Só é preenchido quando a empresa tem acesso Experts (`categoriaPlano` contém `EXPERT`). Fora disso, fica `""` (default do DTO).
- **Exceção:** empresa Experts **em abertura** (`identificarEmpresaAbertura()`), sem assessor no plano e com `idProcesso` → o `assessor` fica `""` e o e-mail vai para `empresaLogada.assessorOnboarding`, que vem de `AberturaFacade.consultarProcessoPorId(...).emailAssessor`, com cache de 3 h. O `assessorOnboarding` **não é mapeado** nessa integração. Para essas empresas, `emailAssessorOngoing` chega vazio e o `/tomadores/email/validar` responde `EMAIL_INVALIDO`.
- A mesma integração também mapeia `statusJira <- empresaLogada.jiraStatus`, `jiraFinalizado <- empresaLogada.jiraFinalizado` e `aberturaEmpresa <- empresaLogada.abertura`, usados no roteamento N1 Ativação ([[roteamento-n1-ativacao-soci]]).
