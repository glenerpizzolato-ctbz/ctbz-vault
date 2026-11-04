# Empresas

Skills que consultam dados das empresas clientes da Contabilizei (plano, status, regime etc.), principalmente para levantar massa de teste. Uma linha por skill, com os assuntos que ela cobre.

- [buscar-empresas-por-plano](buscar-empresas-por-plano/SKILL.md) — lista N empresas de prd (padrão 10) por plano (`BASICO`, `AVANCADO`, `EXPERT`...) pelo BigQuery `saude_empresa.empresa`, com filtros de status, UF e regime; em dev, orienta a tela do admin e a API do monolito
- [buscar-empresas-por-telefone](buscar-empresas-por-telefone/SKILL.md) — lista os CNPJs e planos vinculados a um telefone (ativas/rascunho, inativas) pela rota `buscar-por-telefone` da plataforma-crm-web, via API gateway do atendimento com a chave obtida na hora pela `zendeskbot-config` (como a Ultimate); dono do script `bots_api.py`
- [autenticar-empresa-whatsapp](autenticar-empresa-whatsapp/SKILL.md) — telefone + CNPJ/CPF no bot de WhatsApp: dados da empresa logada (`buscar-por-telefone-e-cnpj` da plataforma-crm-web) e decisão do bot (`statusBot`, `categoriaPlano`, fluxos por área) pela `autenticacao/basico-padrao` do atendimento-zendesk
