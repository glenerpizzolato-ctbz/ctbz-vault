---
name: buscar-empresas-por-plano
description: Lista empresas da Contabilizei por plano (BASICO, AVANCADO, PREMIUM, MULTIBENEFICIOS, EXPERT_ESSENCIAL, EXPERT_PRO), para usar como massa de teste. Em prod, pelo BigQuery (contabilizei-dataflow.saude_empresa.empresa), retornando N empresas aleatórias (padrão 10) com CNPJ, razão social, status, regime, UF e CNAE, com filtros opcionais de status, UF e regime. Em dev, orienta o uso da tela do admin (admin-dev-0N) e da API do monolito. Use quando o usuário pedir uma ou mais empresas/CNPJs de um plano (ex: "me dá uma empresa do plano básico", "lista 5 empresas expert em dev").
argument-hint: "<plano: BASICO|AVANCADO|PREMIUM|MULTIBENEFICIOS|EXPERT|EXPERT_ESSENCIAL|EXPERT_PRO> [quantidade] [status: ATIVO|INATIVO|RASCUNHO|TODOS] [uf] [regime] [ambiente: prd|dev]"
---

# Buscar empresas por plano

Em **prd**, busca empresas por plano na tabela `contabilizei-dataflow.saude_empresa.empresa` do BigQuery, usando o último snapshot de cada empresa. O resultado é uma amostra aleatória, então cada execução traz empresas diferentes.

- **Fonte:** BigQuery, via `bq` CLI, somente leitura. O usuário tem leitura no projeto `contabilizei-dataflow`. Detalhes da tabela em `~/ctbz-vault/obsidian/db/status-empresa-bigquery.md`.
- **Só prod.** Não existe essa tabela para dev: em dev, seguir a seção [Dev](#dev-tela-do-admin-como-apoio).
- **Confirmar em tempo real (prd):** a API do monolito pela coleção `contabilizeiapp` do experts-bruno (`getByCnpj` e `auth/filtrarempresas`, com o plano em `planoPagamentoEmpresa.pagtoPlano.categoriaV2.nome`). Rotas, token e armadilhas em `~/ctbz-vault/obsidian/repositories/plataforma-monolito/rotas-busca-empresa.md`.
- **Snapshot mensal** (`periodo` AAAAMM): o plano/status pode ter mudado depois do último snapshot. Para empresas não inativas, o script só traz as que estão no período mais recente.

## Planos

Valores da coluna `plano`: `BASICO`, `AVANCADO`, `PREMIUM`, `MULTIBENEFICIOS`, `EXPERT_ESSENCIAL`, `EXPERT_PRO` (e `NULL` em `TRIAL`). Passar `EXPERT` traz os dois planos Expert (use `--exato` para não expandir). Para ver os planos e quantidades atuais: `--planos`.

## Passo a passo

1. Identificar o plano pedido e o N (se o usuário não informar, usar o padrão **10**). Mapear nomes informais: "básico" → `BASICO`, "avançado" → `AVANCADO`, "expert" → `EXPERT`, "multibenefícios" → `MULTIBENEFICIOS`.
2. Rodar:

    ```bash
    python3 ~/.claude/skills/buscar-empresas-por-plano/scripts/buscar_empresas.py <PLANO> [-n N] [--status ATIVO|INATIVO|RASCUNHO|TODOS] [--uf SP] [--regime SIMPLES]
    ```

    O status padrão é `ATIVO`. Só mudar se o usuário pedir.
3. Mostrar o resultado em tabela (CNPJ, razão social, plano, status, regime, UF/município). Se vier vazio, sugerir afrouxar os filtros ou rodar `--planos`.

## Dev: tela do admin como apoio

Em dev não há fonte consultável por plano: os dados da plataforma não estão em nenhum banco acessível (`~/ctbz-vault/obsidian/db/bancos-dev.md`), e a listagem da API do monolito (`/rest/empresa/auth/filtrarempresas`) não filtra por plano. Quando o usuário pedir empresas de um plano em dev:

1. **Usar a tela do admin como apoio** (`https://admin-dev-0N.ctbz.com.br`, normalmente `admin-dev-03`): listar as empresas pela tela de empresas (filtros de status, regime, UF etc.) e abrir a empresa (`#/edit-empresa/<cnpj>`) para conferir o plano. A listagem do admin também não filtra por plano (a rota por trás, `view/listaempresa/filtrar`, não tem esse parâmetro), então o plano é conferido empresa a empresa. Pedir ao usuário para fazer isso na tela, ou usar o Chrome (skill `claude-in-chrome`) se ele pedir.
2. **Ou pela API do monolito** (coleção `contabilizeiapp` do experts-bruno), paginando `auth/filtrarempresas?status=ATIVO&limite=<n>&cursor=<offset>` e filtrando do lado do cliente por `planoPagamentoEmpresa.pagtoPlano.categoriaV2.nome` (as empresas vêm em `serializedList`, string JSON). Pré-requisitos em dev:
    - IP liberado em `https://libera-meu-ip.ctbz.com.br/` para o projeto `contabilizeiapp-dev-0N` (sem isso, 403 em HTML).
    - Token gerado no **SSO de teste** com o sistema do ambiente em `sistemasAutorizados` (`["monolito-dev-03", "plataforma"]` para o dev-03; `contabilizeiapp` não existe no SSO de teste), salvo em `sso_token_dev`. Sem isso, 401 com `Token nao possui acesso ao sistema: monolito-dev-0N` no log do App Engine.
    - Mesmo `User-Agent` usado na criação do token (o `navigator.userAgent` do navegador em que o cookie do SSO foi copiado).
    - A listagem de dev quebra com 400 (`No enum constant ...MotivoStatusEmpresa...`) quando a página tem uma empresa com dado inválido: na página que falhar, buscar item a item (`limite=1`) pulando os que dão erro. Empresas Expert são raras em dev (3 a cada ~1.150 ativas), então a varredura é lenta; preferir a tela do admin quando o usuário precisar de poucas empresas.
    - O `cursor` só vai até 1000 (400 `The offset ... must be between 0 and 1000`): a listagem alcança só as ~1.050 primeiras empresas (ordem alfabética) de cada combinação de filtros, então a API não cobre a base inteira de dev.

    Detalhes, causa do 401 e correção em `~/ctbz-vault/obsidian/repositories/plataforma-monolito/rotas-busca-empresa.md`.
3. **Ou CNPJ a CNPJ** pela API de autenticação do bot (`categoriaPlano`), quando já houver candidatos: skill `autenticar-empresa-whatsapp`.

## Armadilhas

- São empresas reais de clientes: usar só para teste/consulta, sem expor dados fora do contexto do trabalho.
- Para testar o bot de WhatsApp com a empresa, o plano no CRM é o que vale. Se o teste depender do plano exato, confirmar pelo `getByCnpj` do monolito ou pela API de autenticação do bot (`categoriaPlano`), já que o BigQuery pode estar até um mês defasado.
- Para o fluxo `CRM` do bot, plano `BASICO` só tem acesso com autopilot ou ramo `COMERCIO`. Essas informações não estão nessa tabela.
