---
name: prc-email-inbound-spam-atendimento-experts
description: PRC — cliente envia e-mail para atendimento.experts@contabilizei.com.br mas cai no spam (Google) da nossa caixa e nenhum ticket é criado; quem abriu a PRC resgata pelo formulário de resgate do spam (Apps Script) e a PRC fecha na ACR PRD-167733 com mensagem padrão
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

O resgate é **autoatendimento**: quem abriu a PRC usa o formulário de resgate (Apps Script) para tirar o e-mail do spam. Nós só fechamos a PRC atrelada à ACR padrão e respondemos com a mensagem padrão abaixo, marcando quem abriu.

- **Link principal (usar este):** https://sites.google.com/contabilizei.com.br/resgate-spam-experts
- **Fallback (se o principal estiver fora do ar):**
  - Site antigo com o formulário: https://sites.google.com/contabilizei.com.br/resgate-emails-spam
  - Formulário direto (script): https://script.google.com/a/macros/contabilizei.com.br/s/AKfycbzaeSzfRGUefwIYNCu1tGlt9c2QzVk1amhSl6wA9B0s9Y-dLh-ejoj-8fckfRF0nLdx/exec
- **Como funciona (tela "Resgate de e-mails do spam"):** informa-se o **e-mail do cliente** (remetente) e clica-se em **Resgatar e-mail**. O script procura no spam de `atendimento.experts@` a mensagem **mais recente** desse remetente; se achar, tira a conversa do spam e devolve à caixa de entrada (vira ticket no Zendesk) e encaminha uma cópia para o e-mail corporativo de quem executou. Se não houver e-mail do cliente no spam, nada muda. Com mais de uma mensagem do mesmo cliente no spam, rodar de novo para cada uma. A cópia encaminhada pode cair no spam de quem executou. Todas as consultas ficam registradas. Acesso só com conta `@contabilizei.com.br`.

### Passo a passo da PRC

1. Confirmar pelo sintoma/prints que é este caso (envio para `atendimento.experts@`, sem bounce). Se houver NDR `5.7.520 AS(4810)`, é o caso do provedor do cliente, não este.
2. Atribuir a PRC ao Glener (regra de `_prcs-indice`).
3. Comentar a **mensagem padrão** abaixo, com **mention do reporter da PRC** (quem abriu o chamado) e o e-mail remetente do cliente preenchido.
4. Vincular à ACR padrão [PRD-167733](https://contabilizeicontabilidade.atlassian.net/browse/PRD-167733): link `Problem/Incident` no `createJiraIssueLink`, `inwardIssue` = PRD-167733, `outwardIssue` = PRC (a PRC **is caused by** a ACR).
5. Fechar: de `To-do`, `Started` (61, → Em Andamento) e depois `Solved` (121, → Concluído), com os 7 campos obrigatórios (Classificação N3, Devido ou Indevido?, Funcionalidade, Grau do Impacto, Ofensor do Chamado, Resolução do chamado, Tipo de chamado). Os IDs de referência estão em [[PRD-168944 - Cliente não quer receber pesquisa (CSAT e-ou NPS)]]; para este caso, usar Ofensor `email_spam_atendimento` e Resolução "Resolvido diretamente pela plataforma" (`17922`), e registrar aqui os valores de Classificação e Funcionalidade de e-mail na primeira PRC fechada por esse fluxo.

### Mensagem padrão

> @<reporter da PRC>, o e-mail do cliente (`<email do remetente>`) chegou até nós, mas caiu no **spam** da caixa `atendimento.experts@contabilizei.com.br`, por isso não virou ticket. Você mesmo(a) consegue resgatá-lo pelo formulário de resgate de e-mails do spam:
>
> https://sites.google.com/contabilizei.com.br/resgate-spam-experts
>
> (se esse link não abrir, use https://sites.google.com/contabilizei.com.br/resgate-emails-spam)
>
> Como usar:
> 1. Acesse o link com a sua conta `@contabilizei.com.br`.
> 2. Em **E-mail do cliente**, informe o e-mail remetente (`<email do remetente>`) e clique em **Resgatar e-mail**.
> 3. O formulário tira do spam a mensagem mais recente desse remetente e a devolve para a caixa de entrada do `atendimento.experts@` (o ticket é criado no Zendesk), e encaminha uma cópia para o seu e-mail. Se o cliente enviou mais de uma mensagem, execute de novo para cada uma.
> 4. Se a cópia não chegar em alguns minutos, olhe a sua própria pasta de spam. Se o formulário não encontrar nada, a mensagem pode ter passado dos 30 dias que o Google guarda o spam: peça para o cliente reenviar.
>
> Nos próximos casos de cliente que não consegue enviar e-mail para o atendimento, o formulário pode ser usado direto, sem abrir PRC. Estamos encerrando este chamado vinculado à ACR PRD-167733.

### Exceções

- **Formulário não encontrou a mensagem:** passou da janela de 30 dias do spam do Google ou a mensagem ficou nos *Suspended Tickets* do Zendesk (ver variação do PRC-154406 acima). Olhar os suspended tickets; se não estiver lá, orientar o reenvio.
- **Fluxo anterior (antes do formulário):** a PRC era atribuída à Murieli Schrickte, que tem acesso à caixa `atendimento.experts@` e tirava a mensagem do spam manualmente. Fica só como contingência se o formulário estiver fora do ar.
- **Recorrência do mesmo remetente/domínio:** adicionar o remetente ou domínio na **regra anti-spam** do e-mail (whitelist) e, se preciso, no Zendesk.

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
