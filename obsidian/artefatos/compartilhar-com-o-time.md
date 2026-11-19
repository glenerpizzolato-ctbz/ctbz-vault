---
name: compartilhar-com-o-time
description: "HTML Share (https://html-share.ctbz.com.br/): serviço interno para publicar .html e .md atrás do SSO da Contabilizei e compartilhar com o time; como publicar pela tela ou pela skill publish-html-share, versões, campos editáveis, assinaturas, permissões e problemas comuns. É o que o usuário quer dizer com \"compartilhar com o time\""
metadata:
  type: reference
tags:
  - artefatos
  - comunicacao
  - html-share
fonte: https://html-share.ctbz.com.br/h/guia-html-share
atualizado_em: 2026-11-19
---

# Compartilhar com o time (HTML Share)

**"Compartilhar com o time"** um artefato, HTML ou `.md` significa publicar no **HTML Share**: https://html-share.ctbz.com.br/. A página fica num link curto `/h/<slug>`, aberto só para quem tem login Contabilizei (SSO), e fica salva com versões. Assim não se depende do link privado do `claude.ai/artifact`.

Resumo do guia oficial (https://html-share.ctbz.com.br/h/guia-html-share, v24, responsável João Felipe (Bini), lido em 19/11/2026). Código em https://gitlab.com/ctbz/vibe-coding/projetos/html-share; a fonte do guia é `docs/guia-html-share.html` no mesmo repositório.

## Como funciona

- Todo HTML publicado fica num bucket do app (projeto GCP `ctbz-vibe-coding`). O HTML Share (Cloud Run atrás de IAP) lê o bucket, lista o que você pode abrir e serve cada arquivo em `/h/<slug>`, sempre atrás do SSO.
- Dois jeitos de publicar, que gravam no mesmo bucket: pela **tela do app** ou pelo **Claude Code** (skill `publish-html-share`).
- **Dono por link**: só quem publicou atualiza, muda quem vê ou exclui. A autoria vem do SSO (tela) ou do `gcloud` (skill).
- Atualizar **não troca a URL**: as versões anteriores continuam acessíveis.

## Publicar pela tela (sem instalar nada)

1. Abrir https://html-share.ctbz.com.br/ logado.
2. Arrastar (ou escolher) um `.html` ou `.md` de **até 5 MB**.
3. Ajustar o título (vem do `<title>` do HTML ou do `# Título` do Markdown), a descrição (opcional) e a **Categoria** (opcional: escolher uma existente ou criar; vira filtro na lista para todos). Em **Quem vê**:
   - **Empresa**: todo mundo; aparece na lista.
   - **Só com link**: abre pelo link, mas some das listas.
   - **Privado**: só as pessoas escolhidas (só aparece quem já entrou no HTML Share).
4. Copiar o link e mandar para o time. No menu `⋯` da linha ficam Acessos, Insights, Comparar, Atualizar, Quem vê, Assinaturas e Excluir (as quatro últimas só para quem publicou).

**Atualizar sem trocar o link**: menu `⋯` do seu HTML → **Atualizar** envia o arquivo novo como próxima versão. Um upload pelo quadro de cima sempre cria um link novo.

**O HTML precisa ser self-contained**: o app serve o arquivo como está. CSS vai em `<style>`; imagens como `data:` URI ou URL absoluta. Arquivos locais referenciados (`style.css`, `img/x.png`) não sobem junto. Fontes e bibliotecas de CDN (Google Fonts, Chart.js) funcionam.

## Publicar pelo Claude Code (skill `publish-html-share`)

A skill publica, devolve o link e atualiza links existentes sem trocar a URL. Os passos 1 e 2 são feitos uma vez só:

1. **Permissão**: a conta precisa de `roles/storage.objectCreator` no projeto `ctbz-vibe-coding`. O pedido é um MR no repositório `ctbz-acessos`, aprovado por SecOps e pelo líder técnico; depois do merge, a pipeline aplica a role. O arquivo do MR é `usuarios/<email>/projetos/ctbz-vibe-coding` com a linha `roles/storage.objectCreator` (se o arquivo já existir com outras roles, acrescentar a linha). Passo a passo em `references/pedido-acesso.md` da skill. Com a skill instalada, dá para pedir ao Claude: "abre o MR no ctbz-acessos pedindo a permissão do HTML Share pra mim". Enquanto o MR não sai, publicar pela tela.
2. **Instalar** (precisa de `gcloud` logado com a conta Contabilizei e Python 3.10+):
   ```
   gcloud auth login
   git clone git@gitlab.com:ctbz/vibe-coding/projetos/html-share.git
   cp -r html-share/.claude/skills/publish-html-share ~/.claude/skills/
   ```
   Para atualizar a skill: `git pull` e copiar de novo.
3. **Pedir ao Claude**, de qualquer repositório:

| Pedido | O que acontece | Resultado |
| --- | --- | --- |
| "publica esse HTML no HTML Share" | publica com slug novo | link novo `/h/<slug>` |
| "gera um HTML sobre X e me dá o link" | escreve o HTML self-contained e publica | link novo |
| "atualiza o link `<slug>` com esse arquivo" | publica com `--update` e uma nota | mesmo link, nova versão |

Sem o Claude, direto no terminal (da pasta do repositório):

```
# link novo
python3 .claude/skills/publish-html-share/scripts/publish_gcs.py relatorio.html --slug meu-relatorio
# atualizar o mesmo link
python3 .claude/skills/publish-html-share/scripts/publish_gcs.py relatorio.html --slug meu-relatorio --update --note "dados de outubro"
# CSS local? inline antes de publicar
python3 .claude/skills/publish-html-share/scripts/inline_html.py entrada.html saida.html
```

## Versões e slug

- Atualizar nunca apaga nem sobrescreve: cada atualização grava um arquivo novo ao lado (`<slug>~<timestamp>.html` + `.json` com autor, nota e título). `/h/<slug>` mostra sempre a **última** versão; `/h/<slug>?v=1` mostra a versão 1 (vale para qualquer N).
- A nota da versão vem do `--note`. O título na lista acompanha a última versão. **Excluir** tira o link do ar com todas as versões; não dá para apagar uma versão só.
- Todo link tem a **barra do HTML Share no canto inferior direito**: quem vê (Empresa, Só com link ou Privado), título, autor, versão, atalhos (copiar link, favoritar, like, quem vê, acessos, comparar versões), quem está vendo agora e os comentários. Numa versão antiga ela fica amarela, com atalho "Ver a última"; quando sai versão nova enquanto você lê, aparece o aviso **Nova versão**. O botão `⌄` recolhe a barra.
- Para **imprimir ou apresentar**: link limpo `?limpo=1`, que abre o HTML sem a barra.
- **Que slug usar**: relatório vivo, atualizado de tempos em tempos → slug estável sem data (ex: `fallback-rag`) e `--update` a cada rodada. Foto de um momento → slug com data (ex: `fallback-2026-09-29`), publicado uma vez.
- Publicar num slug que já existe **sem** `--update` é recusado de propósito (código 15).

## Recursos depois de publicar

- **Marcações**: checkboxes, rádios, selects e campos de texto do próprio HTML ficam salvos e são iguais para todos (vale a última mudança), com histórico de quem mudou (botão 🕘 Marcações da barra). Ver "Campos editáveis".
- **Comentários**: selecionar um trecho e clicar em 💬 Comentar, ou comentar em geral pelo painel. `@` marca alguém (página Menções). Se uma versão nova tirar o trecho, o comentário fica marcado "trecho não encontrado".
- **Ao vivo**: comentários e marcações de outras pessoas aparecem em poucos segundos.
- **Like** (público, entra no ranking), **Favorito** (só seu, com pastas), **Categoria** (definida por quem publicou), **Vendo agora**.
- **Acessos e Insights**: quem abriu, quando e quanto leu (até onde rolou, tempo com a página em uso), e ranking dos HTMLs com taxa de leitura.
- **Pelo Claude (MCP)**: com o conector Vibecoding no Claude, dá para pedir para publicar, atualizar ou ler um HTML, ou contar o que comentaram, quem assinou e como estão as marcações. Versões publicadas por ali aparecem como "pelo Claude (MCP)". Assinar e marcar continuam só no link, com a própria pessoa.
- Links de um HTML para outro HTML do app abrem na aba inteira.

## Markdown

Um `.md` vira página formatada (estilo GitHub: títulos, listas, tabelas, código, citações, imagens, links) e ganha tudo o que um HTML tem.

- `- [ ]` vira caixa de marcar clicável, salva para todos.
- Botões no canto: ⬇ `.md` baixa o original; ☀/🌙 troca o tema.
- Bloco ` ```mermaid ` vira um cartão com o botão **Abrir diagrama**, que desenha no mermaid.live (site externo: evitar diagrama com dado sensível).
- **Notas do Obsidian são compatíveis**: o front matter (`---`) some da página e os `[[links]]` viram texto destacado. Dá para subir nota do vault direto.

## Campos editáveis (marcações)

Servem para checklist do time, acompanhamento de pendências, votação simples ou anotação por item, sem planilha à parte.

- Usar **campos de verdade**: `<input type="checkbox">`, `radio`, `<select>`, `<input type="text">` (e date, number etc.) e `<textarea>`. O símbolo ☐ ou uma `<div>` clicável não salvam nada. Não precisa de script nem de configuração.
- Dar um **`id` estável** a cada campo (ou `name`): a marcação fica presa à chave do campo e sobrevive a versões que reordenam, incluem ou tiram itens. Sem `id`/`name`, vale a posição no HTML.
- O nome no histórico é o `<label>` do campo (senão `aria-label`, `placeholder` ou o começo da linha da tabela).
- O texto é salvo quando a pessoa sai do campo. Se o HTML tem contadores ou filtros próprios, eles reagem às marcações dos outros (o app dispara `input` e `change`).
- Vale a última marcação (para aprovação formal, usar Assinaturas). Campos de senha, de arquivo e ocultos não são salvos; cada texto guarda até 5.000 caracteres. As marcações são do link (valem para todas as versões).

```html
<label><input type="checkbox" id="contrato-assinado"> Contrato assinado</label>
<select id="status-migracao"><option>Não iniciado</option><option>Em andamento</option><option>Concluído</option></select>
<textarea id="obs-migracao" placeholder="Observações"></textarea>
```

## Assinaturas (aprovação)

Para propostas e aprovações: as pessoas escolhidas assinam com o próprio login, e fica registrado quem aprovou, qual versão e quando.

1. Ao publicar, em **Assinatura (opcional)**, marcar ✍ **Pedir assinatura** (ou menu `⋯` → Assinaturas num HTML já publicado).
2. Escolher quem assina. Sem ninguém na lista, qualquer pessoa que abre pode assinar, e o estado "Aprovado" não existe.
3. Opcional: colocar `<div data-html-share-assinaturas></div>` onde o bloco de assinaturas deve aparecer (o marcador sozinho já liga a assinatura, aberta a qualquer pessoa).
4. Quem assina clica em ✍ **Assinar como (nome)** e confirma no painel da barra. **Retirar minha assinatura** desfaz.

- Na barra: `✍ Assinar · 1/3` (amarelo, falta a sua), `✍ 2/3`, `✍ Aprovado` (verde, todos assinaram a última versão).
- **Versão nova pede assinatura nova**: as assinaturas valem para a versão assinada (número + impressão digital do conteúdo).
- Cada assinatura grava IP, navegador e dados do aparelho, além do hash do conteúdo; quem publicou baixa o comprovante (JSON).
- É registro de aprovação interna, não assinatura eletrônica com valor jurídico (ICP-Brasil).
- Acompanhar em **Menções** (Esperando a sua assinatura), **Assinaturas** (abas Falta assinar e Assinados) e no selo da linha em Publicados.

## Permissão e segurança

- `storage.objectCreator` só cria arquivo no bucket (publicar e atualizar): não lê, não lista, não sobrescreve e não apaga (excluir é pela tela). Vale para o projeto `ctbz-vibe-coding` inteiro.
- O app é classificado como **interno**: publicar só conteúdo interno, **nada de dado pessoal ou sensível de cliente**.
- O HTML abre isolado num quadro separado (scripts, gráficos e CDN funcionam, mas não leem a sessão do usuário). Mesmo assim, não publicar HTML de origem não confiável.
- HTML Privado não aparece em lista, ranking nem busca para quem não está na lista.
- A publicação não é pela API do app porque o IAP recusa chamada de API feita com conta de usuário; a skill grava direto no bucket.

## Problemas comuns

| Sintoma | Causa | O que fazer |
| --- | --- | --- |
| Script sai com código 13 | sem permissão no bucket, ou `gcloud` com outra conta | `gcloud config get-value account`; sem a role, pedir no ctbz-acessos |
| Script sai com código 15 | o slug já existe | usar `--update` para atualizar, ou outro `--slug` |
| Script sai com código 14 | o bucket mudou de nome | rodar com `HTML_SHARE_BUCKET=<novo>` e avisar o dono do app |
| Link diz "Documento não encontrado" | arquivo numa pasta que o app não lê | abrir `/api/app/_debug` e conferir bucket e prefixo |
| Página sem estilo ou sem imagens | HTML aponta para arquivos locais | `inline_html.py` para o CSS; imagens como `data:` URI ou URL absoluta |
| Atualizou, mas o link mostra outra coisa | slug do `--update` digitado diferente | publicar de novo no slug certo e excluir o errado pela tela |
| Markdown sem os botões ⬇ `.md` e ☀/🌙 | subido antes de 06/11/2026 ou app em versão antiga | recarregar (Ctrl+Shift+R) e `⋯` → Atualizar com o mesmo `.md` |

## Como o Claude deve compartilhar um artefato

1. **Gerar o arquivo completo**: o HTML publicado como artefato do Claude não tem `<!doctype>`, `<html>`, `<head>` nem `<body>` (a plataforma injeta na publicação). Partir de `artefatos/arquivos/<slug>.html` e envolver em `<!doctype html><html lang="pt-BR"><head>…</head><body>…</body></html>`: no `<head>`, `meta charset="utf-8"`, `meta viewport` (`width=device-width, initial-scale=1, viewport-fit=cover`), o reset do artefato (`:root{color-scheme:light;padding-top/bottom: env(safe-area-inset-*)}`, `body{margin:0}`, `img{max-width:100%}`, `[hidden]{display:none!important}`) e tudo o que vem antes do conteúdo (`<title>`, `<meta>`, `<link>` de fontes, `<style>`); no `<body>`, o resto. Salvar em `~/Downloads/<slug>.html` e conferir que parseia. Conferir também que não há dado pessoal ou sensível de cliente.
2. **Publicar**:
   - Com a skill `publish-html-share` instalada (`~/.claude/skills/publish-html-share`) e a role concedida: confirmar com o usuário o slug e a visibilidade e publicar com `publish_gcs.py` (`--update --note` para nova versão do mesmo link).
   - Sem a skill (situação em 19/11/2026: não instalada, repositório não clonado): entregar o caminho do arquivo para o usuário subir pela tela e, para atualizar, usar `⋯` → Atualizar.
3. **Registrar** o link em `html_share` no front-matter da nota do artefato e na lista abaixo.

## Compartilhados

- [[mapa-whatsapp-ativo|Mapa do WhatsApp Ativo]] — gerado em `~/Downloads/mapa-whatsapp-ativo.html` em 19/11/2026; link do HTML Share pendente
