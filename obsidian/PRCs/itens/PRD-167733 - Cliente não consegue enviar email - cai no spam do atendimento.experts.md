---
name: prc-email-inbound-spam-atendimento-experts
description: PRC — cliente envia e-mail para atendimento.experts@contabilizei.com.br mas cai no spam (Google) da nossa caixa e nenhum ticket é criado; resolver com whitelist / regra anti-spam
metadata:
  type: reference
tags:
  - prc
canal:
  - email
dominio:
  - atendimento
sistemas:
  - google-workspace
  - zendesk
acr:
  - "[[PRD-167733]]"
ocorrencias:
  - PRC-148705
  - PRC-152490
  - PRC-152605
  - PRC-153076
  - PRC-153105
  - PRC-154406
qtd_ocorrencias: 6
ultima_ocorrencia: 2026-11-05
---

# Cliente não consegue enviar email — cai no spam do atendimento.experts

> [!info] Diferença para o caso parecido
> Aqui o cliente **de fato envia** e a mensagem chega até nós, mas cai no
> **nosso** spam. Se o cliente recebeu bounce `5.7.520 AS(4810)`, o bloqueio é
> no provedor dele. Veja
> [[PRD-168171 - Cliente não consegue enviar email - bloqueio de spam no provedor do cliente]].

## Sintoma

- O cliente envia para `atendimento.experts@contabilizei.com.br` e nenhum
  ticket é criado. **Não há bounce.**
- Às vezes outros endereços do mesmo cliente funcionam normalmente.
- **Quando há evidência de que o cliente enviou para esse e-mail, geralmente é
  este o problema.**

## Causa

- A mensagem cai no **spam do Google** da conta `atendimento.experts`, e por
  isso não vira ticket no Zendesk.
- Pode estar ligada à reputação ou à segurança (SPF/DKIM/DMARC) do domínio do
  remetente. Exemplo: o domínio `pm.me` (ProtonMail) foi retido em "Tickets
  Suspensos" / rejeitado de forma silenciosa.

## Como confirmar

> [!tip] Triagem pelos prints da PRC
> Se o print do cliente mostra o e-mail **na caixa de enviados**, endereçado a `atendimento.experts@` (às vezes aparece só como "Support" ou "Equipe Contabilizei Experts"), **sem NDR**, e o remetente é Gmail ou Google Workspace (a interface do Gmail mostra "enviado por <domínio>"), é este caso, não o do provedor do cliente. Anexos `.zip`/PDF aparecem com frequência nesses casos. Lote de out/2026: PRC-152490 (722.network, `.zip`), PRC-152605 (smartflowsistemas.com.br, PDF, recorrente), PRC-153076, PRC-153105 (gmail.com).

> [!tip] Variações vistas no PRC-154406 (CC Iglesias, nov/2026)
> O remetente pode enviar por um serviço como a Brevo (SPF/DKIM/DMARC ok, aceito pelo Google com 250) e a resposta a um ticket pode ir direto para `support+id…@contabilizei.zendesk.com` em vez de `atendimento.experts@`. Nesse caso a mensagem pode ficar nos *Suspended Tickets* do Zendesk, não no spam do Google: olhar os dois.

- Verificar a caixa de spam de `atendimento.experts@` na janela do envio.
- Verificar os *suspended tickets* e a *blocklist* do Zendesk.

## O que fazer

- **Quem resolve:** atribuir a PRC à Murieli Schrickte, que tem acesso à caixa `atendimento.experts@` e recupera a mensagem do spam. Comentar na PRC que é caixa de spam, com remetente, assunto e data do e-mail.
- **Janela de 30 dias:** o spam do Google guarda a mensagem por 30 dias. No comentário, marcar a Murieli (mention) dizendo se está dentro de 30 dias: se estiver, pedir para remover do spam; se passou de 30 dias, pedir para repassar para a área dedicada.

- Adicionar o remetente ou domínio do cliente na **regra anti-spam** do e-mail
  (whitelist) e, se preciso, no Zendesk.

> [!warning] Ponto em aberto
> Já houve uma resolução anterior em
> [PRD-151889](https://contabilizeicontabilidade.atlassian.net/browse/PRD-151889),
> mas novos casos continuam aparecendo. Ainda não se sabe se e-mails alterados
> do cliente são considerados no script.

> [!question] Ponto em aberto: outros endereços
> A PRC-152367 (INSPIRABOX) tem o mesmo sintoma, mas o envio foi para `suporte@contabilizei.com.br` (remetente leandroleonardi.com.br, 14/09 e 21/09/2026), não para `atendimento.experts@`. Ainda não se sabe se `suporte@` gera ticket no Zendesk e se passa pelo mesmo filtro anti-spam.

## ACR para vincular

[PRD-167733](https://contabilizeicontabilidade.atlassian.net/browse/PRD-167733)
— Análise de Bloqueio e Whitelisting dos e-mails no Canal de Atendimento

- PRC de exemplo: [PRC-148705](https://contabilizeicontabilidade.atlassian.net/browse/PRC-148705)
