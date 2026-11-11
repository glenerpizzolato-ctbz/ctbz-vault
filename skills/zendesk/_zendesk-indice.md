# Zendesk

Skills que leem ou escrevem no Zendesk da CTBZ (`contabilizei.zendesk.com`) pela API REST, com as credenciais da coleção Bruno `~/repositories/experts-bruno/zendesk-api`. Uma linha por skill, com os assuntos que ela cobre.

- [buscar-gatilho-zendesk](buscar-gatilho-zendesk/SKILL.md) — detalha um gatilho (trigger) por id, link do admin ou nome: condições e ações com ids de grupo, usuário, campo, formulário e webhook traduzidos; só leitura, sandbox por padrão e prod só com aprovação
- [buscar-grupo-zendesk](buscar-grupo-zendesk/SKILL.md) — descobre o nome (e membros) de um grupo do Zendesk de prd pelo id, ou o id pelo nome, só leitura
- [fechar-tickets-teste-zendesk](fechar-tickets-teste-zendesk/SKILL.md) — lista e fecha (`closed`) os tickets abertos em prd do usuário de teste do Glener (end-user `21878313229212`), que os testes dos bots de WhatsApp deixam nas filas
- [mapear-erros-ultimate](mapear-erros-ultimate/SKILL.md) — mapeia as conversas de WhatsApp que caíram em erro nos bots da Ultimate (Technical Error / Action Failed) num período, cruzando o `ultimateai-webhook` com o Sunshine; CSV por bot com cenário, versão da mensagem de erro e identificação do cliente (telefone, CNPJ, ticket, sunshineUserId, BSUID)
