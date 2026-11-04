---
name: prc-email-inbound-bloqueio-spam-provedor-cliente
description: PRC — cliente envia/responde e-mail e a CTBZ não recebe porque o provedor do cliente (geralmente Microsoft) barra como spam na saída (NDR 5.7.520 AS(4810)); problema externo, orientar contornos
metadata:
  type: reference
tags:
  - prc
canal:
  - email
dominio:
  - atendimento
sistemas:
  - zendesk
  - microsoft-365
acr:
  - "[[PRD-168171]]"
qtd_ocorrencias: 0
---

# Cliente não consegue enviar email — bloqueio de spam no provedor do cliente

> [!info] Diferença para o caso parecido
> Aqui a mensagem é barrada **no provedor do cliente** e nunca chega até nós.
> Se o cliente tem evidência de que o e-mail **foi enviado** para
> `atendimento.experts@contabilizei.com.br` e não recebeu bounce, veja
> [[PRD-167733 - Cliente não consegue enviar email - cai no spam do atendimento.experts]].

## Sintoma

- O cliente envia ou responde um e-mail (geralmente para os endereços
  `@contabilizei.zendesk.com`) e nenhum ticket é criado ou atualizado no Zendesk.
- Costuma ser domínio Microsoft (`@hotmail.com` / `@outlook.com` / Exchange
  Online), e o cliente **recebe um bounce (NDR)**:
  ```
  550 5.7.520 Message blocked because it contains content identified as spam. AS(4810)
  ```
  Variante do Exchange:
  ```
  Remote server returned '554 5.7.0 < #5.7.520 smtp;550 5.7.520 Message blocked because it contains content identified as spam. AS(4810)>'
  ```

## Causa

- É o filtro **anti-spam de saída da Microsoft** (`AS(4810)`). O bloqueio é
  **pelo conteúdo da mensagem**, não pelo IP nem pela conta do remetente.
- A mensagem é barrada **antes de sair** do provedor do cliente e **não chega à
  Contabilizei**. Não é problema do nosso produto.
- Gatilhos mais comuns:
  1. Anexo PDF junto com formatação Rich Text/HTML (o mais frequente). Nome de
     arquivo com caracteres especiais também pesa.
  2. Corpo com muitos links, imagens, negrito, assinatura longa (site,
     telefones, redes sociais, disclaimer).
  3. Encaminhamento automático bloqueado pela política de spam de saída do M365.
  4. Falso positivo da Microsoft, o que explica casos **intermitentes**.

## O que fazer

Não temos ação técnica definitiva do nosso lado. **Orientar o cliente** a
tentar, nesta ordem:

1. Reenviar em **texto simples** (sem Rich Text).
2. Renomear o anexo para algo simples (`relatorio.pdf`) e, se possível, compactar em `.zip`.
3. Tirar temporariamente a assinatura completa e os links.
4. Trocar de cliente de e-mail: Outlook Web ↔ app (o roteamento é diferente).
5. Mandar o arquivo por link (OneDrive) em vez de anexo.
6. Conta corporativa: o administrador deve revisar a política de spam de saída
   no Microsoft Defender. Se o falso positivo se repetir em lote, o cliente deve
   abrir chamado no suporte Microsoft.

> [!tip] Evidência na triagem
> Pedir a data/hora exata do envio, o endereço remetente e o NDR completo
> (de preferência o `.eml` com headers).

## ACR para vincular

[PRD-168171](https://contabilizeicontabilidade.atlassian.net/browse/PRD-168171)
— [ACR] Falha sistêmica na recepção de e-mails enviados pelos clientes à
Contabilizei (Zendesk inbound). Concluída sem problema no produto e sem
tratativa associada.
