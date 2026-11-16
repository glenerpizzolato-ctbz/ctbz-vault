---
name: rollout-ia-ativacao
description: "De onde vêm flagRolloutIAAtivExp e flagRolloutAtivacaoInboundBP no bot wpp main da Ultimate: calculadas na integração [zd-fns] GET | config env - Shared pelo segundo do relógio (rollout aleatório). Experts ~42% vai para a IA de Ativação; BP 100%"
metadata:
  type: reference
tags:
  - ultimate
  - ativacao
  - aida
  - rollout
---

# Rollout da IA de Ativação (Experts e BP)

Conferido em 2026-11-16 no bot `[prod] ctbz wpp main` (`66c6220557465548f3ff0d6e`), pela API de leitura do dashboard ([[dashboard-read-api]]).

As duas variáveis são preenchidas no cenário `Success` da integração **`[zd-fns] GET | config env - Shared`** (`668c345bc2932ebcec62a717`), a mesma que carrega a config do bot (cloud function `zendeskbot-config`). Elas **não vêm da resposta da API**: são expressões JSONata sobre a hora atual.

| Variável | Expressão | Efeito |
| --- | --- | --- |
| `flagRolloutIAAtivExp` | `$number($substring($now(),17,2)) <= 24` | `true` quando o **segundo** do relógio está entre 00 e 24, ou seja, 25 de 60 (~42%) das conversas Experts em abertura vão para a IA (**AIDA [Ativação] [WhatsApp] [Experts]**, `31714889423900`, "Contador Inteligente") |
| `flagRolloutAtivacaoInboundBP` | `$number($substring($now(),17,2)) <= 60` | sempre `true` (segundos vão de 00 a 59): **100%** das conversas BP em abertura vão para a IA (**AIDA [Ativação] [WhatsApp] [BP]**, `29248769628572`) |

- `$substring($now(),17,2)` pega o "SS" de `AAAA-MM-DDTHH:MM:SS.sssZ`. O sorteio é por conversa, no instante em que a integração de config roda.
- **Impacto nos testes do roteamento N1 ([[testes-roteamento-n1-ativacao]]):**
  - Experts: só cai no fluxo dos drops (sem IA) se a config rodar entre os segundos 25 e 59. No piloto 2, a conversa começou às 19:18:15 (segundo 15), então foi para a IA. Para testar, mandar a primeira mensagem perto do segundo 25 a 30 (a config roda logo depois) ou repetir até cair fora da IA.
  - BP: com o rollout em 100%, processo BP em abertura sempre vai para a IA. Não dá para testar os drops com processo BP sem mudar a expressão.
- Para mudar o percentual, editar a expressão na integração (por exemplo `<= 24` vira `<= -1` para desligar). É mudança em prd, combinar com o time dono.
