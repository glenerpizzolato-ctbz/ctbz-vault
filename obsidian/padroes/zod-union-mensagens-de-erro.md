---
name: zod-union-mensagens-de-erro
description: "zod v4: z.union de valor único ou lista (string | string[]) devolve 'Invalid input' genérico quando os dois lados falham sem erro de tipo (ex: enum inválido); como recuperar a mensagem específica no error do union"
metadata:
  type: reference
tags:
  - padroes
  - zod
---

# zod v4: mensagens de erro em `z.union` (valor único ou lista)

Num campo `z.union([item, z.array(item)...])`, o zod v4 só repassa a mensagem específica quando **um único lado** do union casa o tipo da entrada. Ex: `companyCode: ['A', '']` dá "Código da empresa é obrigatório", porque o lado `string` falha por tipo e o erro do array sobe.

Quando **os dois lados** falham sem erro de tipo, o resultado é um `invalid_union` com a mensagem genérica "Invalid input". O caso típico é um enum: `'PROMO'` é string (o lado escalar falha por valor, não por tipo), e `['TAX', 'PROMO']` é array (o lado da lista falha no item). Isso pode virar regressão quando um campo que era só `z.enum(...)`, com mensagem própria, passa a aceitar lista.

Correção: no `error` do union, tratar o `invalid_union` pegando o erro do lado que corresponde à forma enviada (`issue.errors[Array.isArray(issue.input) ? 1 : 0]`) e prefixar a posição do item quando o `path` do erro aninhado não for vazio (ex: `purpose[1]: Finalidade inválida...`). Junto com o `issue.input === undefined` para a mensagem de obrigatório.

Implementado no `oneOrMany` de `register-optout.object.ts` do [[_contato-service-indice|contato-service]] (PRD-175849, MR !60), apontado por uma thread do GitLab Duo.
