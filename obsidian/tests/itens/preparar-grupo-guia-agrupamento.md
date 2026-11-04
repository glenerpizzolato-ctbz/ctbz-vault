---
name: preparar-grupo-guia-agrupamento
description: "Como preparar uma controle_guias de teste e gerar um grupo_guia com PDF (SUCESSO_AGRUPAMENTO) no microsserviço-agrupamento-guias em dev, cuidando da competência"
metadata:
  type: reference
tags:
  - tests
  - agrupamento-guias
dominio:
  - impostos
  - notificacoes
repositorios:
  - microsservico-agrupamento-guias
  - plataforma-faturamento-worker
  - dotfiles
ambiente: dev
atualizado_em: 2026-10-09
---

# Preparar grupo_guia para teste (agrupamento de guias)

Passo a passo para ter um `grupo_guia` em `SUCESSO_AGRUPAMENTO`, com o PDF agrupado no Storage, no `microsservico-agrupamento-guias` em dev. É pré-requisito para testar as notificações de grupo de guia (e-mail/WhatsApp), que só olham grupos agrupados.

## Massa de teste usada

| campo | valor |
|---|---|
| `controle_guias.id` | `2121317` |
| `id_empresa` | `5775972832378880` |
| `id_guia` | `5757820599271424` |
| `cnpj` | `12996446000105` |
| `imposto` | `SIMPLES` |
| `status` | `REGISTRADO` |

## Competência (o ponto que mais quebra)

- O serviço só agrupa a **competência anterior ao mês corrente**. Em outubro/2026 a competência é `202609`. Qualquer outra competência volta com erro de competência e não cria nada (`AgrupamentoGuiasServiceImpl.isCompetenciaAtual`).
- O `grupo_guia.periodo_apuracao` é gravado com essa competência, e é único por `id_empresa` + `periodo_apuracao`.
- As guias entram no grupo por `id_empresa` + `periodo_apuracao`, então **`controle_guias.periodo_apuracao` tem que ser igual à competência do grupo**. Guia com outra competência simplesmente não entra, e o grupo fica `AGRUPAMENTO_SEM_GUIA`.
- O `GET /agrupamento-guias/reprocessa-erros` também só olha a competência anterior.
- Na virada do mês a massa fica velha: atualizar o `periodo_apuracao` da `controle_guias` para a nova competência antes de testar de novo.
- Exceção: quando a competência é novembro, as guias `INSS_SIMPLES_13` e `INSS_PRESUMIDO_13` de dezembro do mesmo ano também entram no grupo.

## Requisitos da controle_guias

- `periodo_apuracao` = competência anterior ao mês corrente (ver acima).
- `status` diferente de `CANCELADA`. Para gerar PDF, o status precisa estar em `PDF_GERADO` (`REGISTRADO`, `PENDENTE`, `VENCIDA`, `PARCELADA`, `REGISTRADO_PARCELADO`, `PAGAMENTO_AGENDADO`, `VERIFICANDO_PAGAMENTO`). Status `AVULSA` (`EMISSAO_PENDENTE`, `EMISSAO_FUTURA`, `EMISSAO_FUTURA_GERADA`) agrupa sem PDF; `FALHA_UPLOAD`/`ERRO_PROCESSAR_GUIA` deixa o grupo em `GUIAS_COM_ERRO`.
- `imposto` precisa estar em `ImpostoPermiteAgrupamento` (Simples, INSS, IRRF, PIS, COFINS, IRPJ, CSLL, DARF unificado, FGTS a partir de 202403 etc.).
- **`id_arquivo` e `bucket_name` preenchidos com um PDF que exista no Storage.** `id_arquivo` é o nome do objeto (o caminho dentro do bucket), não a URL. A coluna é `NOT NULL`, então string vazia passa no banco mas quebra na geração do PDF.

Ajuste usado (o PDF não precisa ser do mesmo CNPJ, o serviço não valida):

```sql
UPDATE controle_guias
SET periodo_apuracao = 202609, -- competência anterior ao mês corrente
    id_arquivo  = '02825314000159/2021/01/COFINS_2021_01_1613061669.pdf',
    bucket_name = 'contabilizei-guias-dev2'
WHERE id = 2121317;
```

Para tirar o caminho de uma URL do console (`.../storage/browser/_details/<bucket>/<objeto>;tab=...&project=<projeto>`): o primeiro segmento depois de `_details/` é o bucket, o resto até o `;` é o `id_arquivo`, e o `project=` é o projeto GCP.

## Storage: projeto x bucket

No `application-dev.yml`/`application-local.yml`:

```yaml
storage:
  project-id: contabilizeiapp-dev-02     # projeto GCP, só vai para o client (AppConfig.initStorage)
  bucket-guias: contabilizei-guias-dev2  # onde o PDF agrupado é gravado
```

- A leitura do PDF de cada guia usa o `bucket_name` da própria `controle_guias`, não o `bucket-guias`.
- O PDF agrupado vai para `bucket-guias` em `<cnpj>/<ano>/<mes>/IMPOSTO-GUIAS-<AAAAMM>-<timestamp>.pdf`, com senha = 5 primeiros dígitos do CNPJ.
- Rodando local com ADC (`gcloud auth application-default login`), a conta precisa ler o bucket da guia e escrever no `bucket-guias`. Minha conta não tem `storage.objects.list` no `contabilizei-guias-teste`, por isso uso o `contabilizei-guias-dev2`.

## Disparar o agrupamento

Entrada real: `plataforma-faturamento-worker`, rota `POST worker/agrupamento-guia/envia-empresa-ms-agrupamento-guia/{idEmpresa}` (`AgrupamentoGuiaJersey.java`) → `AgrupamentoGuiasFacade.enviaMsAgrupamentoGuia()` (só cliente Expert) → tópico `agrupar-guias-empresa` (projeto `contabilizei-impostos-teste`) → subscription `ms-agrupamento-guias.sub.agrupar-guias` (projeto `atendimento-canais-dev`) → `AgrupamentoGuiasConsumer` → `AgrupamentoGuiasService.agrupar()`.

Opções para testar:

1. Publicar direto no tópico pelo script do dotfiles (pula a checagem de Expert do faturamento-worker); o payload já calcula a competência anterior e envia `regimeTributario`/`planoPagamentoEmpresa`:
   ```bash
   cd ~/dotfiles && node src/google/publish-topic.google.js topic=agrupar-guias-empresa
   ```
2. Chamar a rota do faturamento-worker acima (fluxo real; o DTO de lá não manda `regimeTributario`/`planoPagamentoEmpresa`).
3. `POST /agrupamento-guias` no próprio microsserviço, com o mesmo payload do `AgrupamentoGuiasDTO` (chama o service direto, sem Pub/Sub).

## Quando o grupo já existe

`GrupoGuiaServiceImpl.agruparPorEmpresa()`:

- Grupo em `ERRO_SISTEMA`, `ERRO_GERACAO_PDF_AGRUPAMENTO` ou `AGRUPAMENTO_SEM_GUIA`: reprocessa (apaga os `item_grupo_guia`, reseta `path`/`status` e agrupa de novo).
- Qualquer outro status: `AgrupamentoJaExisteException` e nada muda.

Para refazer um grupo que já está em outro status, voltar para um status reprocessável e chamar o reprocessamento:

```sql
UPDATE grupo_guia SET status = 'ERRO_SISTEMA'
WHERE id_empresa = 5775972832378880 AND periodo_apuracao = 202609;
```

```
GET /agrupamento-guias/reprocessa-erros
```

## Status do grupo_guia e o que significam

| status | causa | o que fazer |
|---|---|---|
| `AGRUPAMENTO_SEM_GUIA` | nenhuma guia elegível na competência (geralmente `periodo_apuracao` da guia errado, imposto não agrupável ou guia cancelada) | corrigir a guia e reprocessar |
| `GUIAS_COM_ERRO` | alguma guia em `FALHA_UPLOAD`/`ERRO_PROCESSAR_GUIA` | corrigir o status da guia |
| `GUIAS_AGUARDANDO_GERACAO` | alguma guia ainda sem PDF (status fora de `PDF_GERADO`/`AVULSA`) | ajustar o status da guia |
| `ERRO_GERACAO_PDF_AGRUPAMENTO` | exceção ao montar o PDF: `id_arquivo`/`bucket_name` vazio, sem acesso ao bucket, objeto inexistente, CNPJ inválido | ver o log `[ERRO_AGRUPAMENTO_GUIAS][CRIAR_PDF_AGRUPAMENTO] Motivo:`; corrigir e reprocessar |
| `SUCESSO_AGRUPAMENTO_SEM_ARQUIVO_GUIA_AVULSA` | todas as guias são avulsas | esperado, não gera PDF |
| `SUCESSO_AGRUPAMENTO` | PDF gerado, `path` preenchido | pronto para testar notificações |

A exceção da geração do PDF é engolida em `EfetivaStatusAgrupamentoServiceImpl.buildPathGrupoGuias()`; o motivo só aparece no log.

## Conferência

```sql
SELECT id, id_empresa, cnpj, periodo_apuracao, status, path, regime_tributario, plano_pagamento_empresa
FROM grupo_guia
WHERE id_empresa = 5775972832378880
ORDER BY id DESC;

SELECT i.grupo_guia_id, c.id, c.periodo_apuracao, c.imposto, c.status, c.bucket_name, c.id_arquivo
FROM item_grupo_guia i
JOIN controle_guias c ON c.id = i.controle_guia_id
WHERE c.id_empresa = 5775972832378880
ORDER BY i.grupo_guia_id DESC;
```
