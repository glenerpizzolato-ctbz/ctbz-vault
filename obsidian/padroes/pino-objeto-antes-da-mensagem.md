---
name: pino-objeto-antes-da-mensagem
description: "No pino (e no @contabilizei-private/pino-logger), logger.x('mensagem', {campos}) descarta os campos; o certo é logger.x({campos}, 'mensagem')"
metadata:
  type: reference
tags:
  - padroes
  - logs
  - nodejs
---

# Pino: objeto antes da mensagem

O pino espera `logger.info(objeto, mensagem, ...args)`. No formato invertido, `logger.info('mensagem', { campos })`, o objeto vira argumento de interpolação do `%s`/`%o` e, sem placeholder na mensagem, é **descartado sem aviso**: o log sai só com `msg`.

```js
l.info('antigo', { emailId: '1' }) // {"msg":"antigo"}
l.info({ emailId: '1' }, 'novo')   // {"emailId":"1","msg":"novo"}
l.error({ err }, 'falhou - %s', detalhe) // campos + interpolação
```

- Vale para o logger do zezu-core/`@contabilizei-private/pino-logger` e para o `ctx.logger` dos workers do `@contabilizei-private/event-workers`, que são pino.
- O teste unitário não pega: o mock aceita qualquer ordem, e o spec costuma conferir a forma errada. Só aparece no Cloud Logging, com o `jsonPayload` sem os campos.
- Erro vai em `err` (`{ err: error }`), que é a chave do serializer padrão do pino (mensagem e stack); `{ error }` grava o objeto cru.
- Para achar em um repo: `git grep -nP "logger\.(info|warn|error|debug)\(\s*'[^']*',\s*\{" -- 'src/*.ts'` (e a variação com a mensagem na linha seguinte).

- Conferir também o `AGENTS.md`/`CLAUDE.md` do repositório: no email-service, a seção Logging Standards ensinava a forma errada, e o agente de código repetia o erro em código novo (corrigido no MR !81).

Caso real: email-service, nov/2026, 15 chamadas (PRD-178406, MR !81); ver [[alertas-de-envio]].
