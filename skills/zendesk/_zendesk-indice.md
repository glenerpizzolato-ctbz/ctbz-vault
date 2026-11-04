# Zendesk

Skills que leem ou escrevem no Zendesk da CTBZ (`contabilizei.zendesk.com`) pela API REST, com as credenciais da coleção Bruno `~/repositories/experts-bruno/zendesk-api`. Uma linha por skill, com os assuntos que ela cobre.

- [fechar-tickets-teste-zendesk](fechar-tickets-teste-zendesk/SKILL.md) — lista e fecha (`closed`) os tickets abertos em prd do usuário de teste do Glener (end-user `21878313229212`), que os testes dos bots de WhatsApp deixam nas filas
- [mapear-erros-ultimate](mapear-erros-ultimate/SKILL.md) — mapeia as conversas de WhatsApp que caíram em erro nos bots da Ultimate (Technical Error / Action Failed) num período, cruzando o `ultimateai-webhook` com o Sunshine; CSV por bot com cenário, versão da mensagem de erro e identificação do cliente (telefone, CNPJ, ticket, sunshineUserId, BSUID)
