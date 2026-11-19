#!/usr/bin/env python3
"""Levanta as dependências de um repositório de ~/repositories e grava a nota dependencias-<repo>.md no vault CTBZ.

A nota tem duas partes. A de cima (Consome / Consumido por) é a confirmada, mantida à mão pelos agentes conforme o trabalho
no repositório confirma cada dependência no código. A de baixo, entre os marcadores `deps:auto`, é o levantamento
automático deste script: candidatos achados por nome no código, nos manifestos, no catálogo infra/ e no grafo manual, que
o script reescreve a cada execução sem tocar no resto da nota.

Uso:
    deps.py <repo> [<repo>...]          # grava (cria a nota e a linha no índice do repo, se faltarem)
    deps.py <repo> --print              # só mostra o levantamento, sem gravar
    deps.py --all                       # todos os repos que já têm pasta no vault e clone em ~/repositories
    deps.py --refresh                   # ignora o cache da varredura (~/.cache/repo-deps)

O cruzamento entre repositórios varre uma vez cada repo de ~/repositories (git grep pelos nomes dos outros) e guarda o
resultado em ~/.cache/repo-deps/<repo>.json, pela HEAD e pelo conjunto de nomes; repos sem mudança não são relidos.
"""

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
REPOS = HOME / "repositories"
VAULT = HOME / "ctbz-vault" / "obsidian"
CACHE = HOME / ".cache" / "repo-deps"

BEGIN = "<!-- deps:auto:inicio (gerado por mapear-dependencias; não editar à mão) -->"
END = "<!-- deps:auto:fim -->"

# pastas de ~/repositories que não são repositórios de verdade ou são cópias de outro
SKIP_DIRS = re.compile(r"(\.wt$|-wt-|^bahcode-sandbox|^ctbz_|^glener10$|^x$|^obsidian$|^rinha-|^poc-|^rbac-poc$)")
# nomes sem hífen que são palavras comuns (gerariam ruído como token)
STOP_NAMES = {"pipeline", "migrations", "environments", "arquitetura", "atalhos", "flow", "team-kb", "local-dev", "dev-tools", "js-libraries"}
# arquivos que citam nomes sem ser dependência (lockfiles, changelog, docs geradas)
PATHSPEC = [
    ".",
    ":(exclude,glob)**/*lock*",
    ":(exclude,glob)**/CHANGELOG*",
    ":(exclude,glob)**/*.min.js",
    ":(exclude,glob)**/*.svg",
    ":(exclude,glob)**/*.snap",
    ":(exclude,glob)**/dist/**",
    ":(exclude,glob).planning/**",
]
SCAN_VERSION = "2"
KEEP = 12
# exemplos de documentação e teste vêm depois dos de código
DOCISH = re.compile(r"(^|/)(docs?|\.planning|adr)/|(^|/)(README|AGENTS|CLAUDE|CHANGELOG)[^/]*$|\.(md|mdx|excalidraw|drawio|txt|properties)$", re.I)
TESTISH = re.compile(r"(^|/)(tests?|__tests__|spec)/|[._-](test|spec)\.[a-z]+$", re.I)


def rank(ex):
    """Os exemplos na ordem de interesse: código, depois teste, depois documentação."""
    def score(e):
        f = e.rsplit(":", 1)[0]
        return 2 if DOCISH.search(f) else 1 if TESTISH.search(f) else 0
    return sorted(ex, key=score)[:EXAMPLES]
# repos que citam muitos outros sem depender deles (gateway, configmaps, roles, CI, diagramas, coleções, levantamentos):
# as citações deles vão numa linha à parte; além da lista, vale a razão (fração dos nomes citados)
CONFIG_REPOS = {
    "pipeline", "kong-config", "gateway-kong", "k8s-configmap", "environments", "vault-roleset", "tf-cloudrun", "local-dev",
    "dev-tools", "atalhos", "cnpj-alfanumerico", "experts-drawio", "experts-excalidraw", "experts-erd", "experts-bruno",
    "ide-bahcode", "arquitetura", "team-knowledge-base", "team-kb",
}
CONFIG_RATIO = 0.3
EXAMPLES = 3

# SDKs e bibliotecas de serviços de terceiros, pelo nome no manifesto
THIRD_SDKS = [
    (r"^openai$", "OpenAI"),
    (r"^(@anthropic-ai/.*|anthropic)$", "Anthropic (Claude)"),
    (r"^(@google/genai|google-genai|google-generativeai|@google-cloud/vertexai|google-cloud-aiplatform|vertexai)$", "Google Gemini / Vertex AI"),
    (r"^litellm$", "LiteLLM (gateway de LLMs)"),
    (r"^(@sendgrid/.*|sendgrid)$", "SendGrid"),
    (r"^twilio$", "Twilio"),
    (r"^(@sentry/.*|sentry-sdk)$", "Sentry"),
    (r"^(dd-trace|datadog|ddtrace)$", "Datadog"),
    (r"^newrelic$", "New Relic"),
    (r"^(node-zendesk|zendesk|zenpy)$", "Zendesk"),
    (r"^@slack/.*$", "Slack"),
    (r"^(firebase-admin|firebase)$", "Firebase"),
    (r"^stripe$", "Stripe"),
    (r"^@hubspot/.*$", "HubSpot"),
    (r"^(aws-sdk|@aws-sdk/.*|boto3)$", "AWS"),
    (r"^(jira-client|jira|jira\.js)$", "Jira"),
    (r"^(@gitbeaker/.*|python-gitlab)$", "GitLab API"),
    (r"^(@octokit/.*|PyGithub)$", "GitHub API"),
    (r"^(mixpanel|mixpanel-browser)$", "Mixpanel"),
    (r"^(@segment/.*|analytics-node)$", "Segment"),
    (r"^(intercom-client)$", "Intercom"),
    (r"^(googleapis|google-api-python-client)$", "Google Workspace APIs"),
]
# hosts de terceiros no código
THIRD_HOSTS = [
    (r"[a-z0-9-]+\.zendesk\.com", "Zendesk"),
    (r"graph\.facebook\.com", "Meta (WhatsApp Cloud API / Graph)"),
    (r"ultimate\.ai", "Ultimate (bots)"),
    (r"[a-z0-9-]+\.atlassian\.net", "Jira / Confluence"),
    (r"hooks\.slack\.com|slack\.com/api", "Slack"),
    (r"chat\.googleapis\.com", "Google Chat"),
    (r"api\.openai\.com", "OpenAI"),
    (r"api\.anthropic\.com", "Anthropic (Claude)"),
    (r"generativelanguage\.googleapis\.com|aiplatform\.googleapis\.com", "Google Gemini / Vertex AI"),
    (r"api\.sendgrid\.com", "SendGrid"),
    (r"api\.twilio\.com", "Twilio"),
    (r"sentry\.io", "Sentry"),
    (r"datadoghq\.com", "Datadog"),
    (r"gitlab\.com/api", "GitLab API"),
    (r"api\.github\.com", "GitHub API"),
    (r"api\.iugu\.com", "Iugu"),
    (r"api\.pagar\.me", "Pagar.me"),
    (r"brasilapi\.com\.br|receitaws\.com\.br|viacep\.com\.br", "APIs públicas (CNPJ/CEP)"),
    (r"serpro\.gov\.br", "Serpro"),
    (r"api\.hubapi\.com", "HubSpot"),
    (r"bitrix24", "Bitrix24"),
    (r"api\.mixpanel\.com", "Mixpanel"),
    (r"api\.intercom\.io", "Intercom"),
    (r"(sheets|drive|gmail|calendar)\.googleapis\.com", "Google Workspace APIs"),
]
# bibliotecas que dizem qual banco/armazenamento/mensageria o repo usa
DATA_SDKS = [
    (r"^(prisma|@prisma/client)$", "Postgres (Prisma)"),
    (r"^typeorm$", "SQL (TypeORM)"),
    (r"^(pg|postgres|psycopg2?|psycopg2-binary|asyncpg|pgx|lib/pq)$", "Postgres"),
    (r"^(knex|sequelize|kysely|drizzle-orm)$", "SQL (query builder/ORM)"),
    (r"^(sqlalchemy|SQLAlchemy|sqlmodel)$", "SQL (SQLAlchemy)"),
    (r"^(mongoose|mongodb|pymongo)$", "MongoDB"),
    (r"^(redis|ioredis|@redis/.*)$", "Redis"),
    (r"^(@google-cloud/bigquery|google-cloud-bigquery)$", "BigQuery"),
    (r"^(@google-cloud/firestore|google-cloud-firestore)$", "Firestore"),
    (r"^(@google-cloud/storage|google-cloud-storage)$", "Cloud Storage"),
    (r"^(@google-cloud/pubsub|google-cloud-pubsub)$", "Pub/Sub"),
    (r"^(@google-cloud/tasks|google-cloud-tasks)$", "Cloud Tasks"),
    (r"^(@google-cloud/secret-manager|google-cloud-secret-manager)$", "Secret Manager"),
    (r"^(@google-cloud/datastore|google-cloud-datastore)$", "Datastore"),
]
INTERNAL_SCOPE = re.compile(r"^@(contabilizei|ctbz)[\w-]*/")


def git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    return r.stdout if r.returncode in (0, 1) else ""


def all_repos():
    out = []
    for d in sorted(REPOS.iterdir()):
        if d.is_dir() and (d / ".git").exists() and not SKIP_DIRS.search(d.name):
            out.append(d.name)
    return out


def token_names(repos):
    """Os nomes que valem como token de busca: com hífen, ou longos e fora da lista de palavras comuns."""
    return [n for n in repos if n not in STOP_NAMES and ("-" in n or "_" in n or len(n) >= 8)]


def scan(repo, names, refresh):
    """Onde o repo cita os outros nomes: {nome: {"n": linhas, "ex": ["arquivo:linha"]}}, com cache pela HEAD."""
    head = git(REPOS / repo, "rev-parse", "HEAD").strip()
    key = hashlib.sha1((SCAN_VERSION + head + "\0" + "\0".join(names)).encode()).hexdigest()
    cf = CACHE / f"{repo}.json"
    if not refresh and cf.exists():
        try:
            c = json.loads(cf.read_text())
            if c.get("key") == key:
                return c["hits"]
        except (ValueError, KeyError):
            pass
    others = [n for n in names if n != repo]
    hits = {}
    if others:
        args = ["grep", "-n", "-I", "-w", "-F"]
        for n in others:
            args += ["-e", n]
        out = git(REPOS / repo, *args, "--", *PATHSPEC)
        pats = {n: re.compile(r"(?<![\w-])" + re.escape(n) + r"(?![\w])") for n in others}
        for line in out.splitlines():
            parts = line.split(":", 2)
            if len(parts) < 3:
                continue
            f, ln, text = parts
            if len(text) > 2000:
                text = text[:2000]
            for n, p in pats.items():
                if n in text and p.search(text):
                    h = hits.setdefault(n, {"n": 0, "ex": []})
                    h["n"] += 1
                    if len(h["ex"]) < KEEP and not any(e.startswith(f + ":") for e in h["ex"]):
                        h["ex"].append(f"{f}:{ln}")
    CACHE.mkdir(parents=True, exist_ok=True)
    cf.write_text(json.dumps({"key": key, "hits": hits}))
    return hits


def manifests(repo):
    """Dependências declaradas nos manifestos (package.json, pyproject/requirements, go.mod, pom): [(nome, arquivo)]."""
    files = git(REPOS / repo, "ls-files", "--", "*package.json", "*pyproject.toml", "*requirements*.txt", "*go.mod", "*pom.xml", "*build.gradle*").split()
    deps = []
    for f in files:
        if "node_modules/" in f:
            continue
        p = REPOS / repo / f
        try:
            text = p.read_text(errors="replace")
        except OSError:
            continue
        name = os.path.basename(f)
        if name == "package.json":
            try:
                j = json.loads(text)
            except ValueError:
                continue
            for sec in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
                for d in (j.get(sec) or {}):
                    deps.append((d, f))
        elif name == "pyproject.toml" or name.startswith("requirements"):
            for m in re.finditer(r'^\s*"?([A-Za-z0-9_.\-]+)(?:\[[^\]]*\])?\s*(?:[<>=!~;@ ]|"|$)', text, re.M):
                d = m.group(1)
                if d.lower() not in {"python", "name", "version", "description", "requires-python", "readme", "dependencies", "authors"}:
                    deps.append((d, f))
            for m in re.finditer(r"gitlab\.com[/:]ctbz/[\w./-]+?/([\w.-]+?)(?:\.git)?(?=[@#\s\"']|$)", text):
                deps.append(("gitlab:" + m.group(1), f))
        elif name == "go.mod":
            for m in re.finditer(r"^\s*(?:require\s+)?([\w.\-]+\.[a-z]+/[\w./\-]+)\s+v", text, re.M):
                deps.append((m.group(1), f))
        else:
            for m in re.finditer(r"<groupId>([^<]+)</groupId>\s*<artifactId>([^<]+)</artifactId>", text):
                deps.append((f"{m.group(1)}:{m.group(2)}", f))
            for m in re.finditer(r"['\"]([\w.\-]+):([\w.\-]+):[^'\"]+['\"]", text):
                deps.append((f"{m.group(1)}:{m.group(2)}", f))
    return deps


def package_owner(repos):
    """O repo que publica cada pacote (o `name` do package.json, o module do go.mod): {pacote: repo}."""
    own = {}
    for r in repos:
        for f in git(REPOS / r, "ls-files", "--", "package.json", "*/package.json", "go.mod").split():
            if "node_modules/" in f:
                continue
            try:
                text = (REPOS / r / f).read_text(errors="replace")
            except OSError:
                continue
            if f.endswith("package.json"):
                try:
                    n = json.loads(text).get("name")
                except ValueError:
                    continue
                if n and INTERNAL_SCOPE.match(n):
                    own.setdefault(n, r)
            else:
                m = re.search(r"^module\s+(\S+)", text, re.M)
                if m:
                    own.setdefault(m.group(1), r)
    return own


def grep_o(repo, patterns):
    """Ocorrências (arquivo, trecho) dos padrões no código versionado, sem diferenciar maiúsculas."""
    args = ["grep", "-n", "-I", "-o", "-i", "-E"]
    for p in patterns:
        args += ["-e", p]
    out = git(REPOS / repo, *args, "--", *PATHSPEC)
    res = []
    for line in out.splitlines():
        parts = line.split(":", 2)
        if len(parts) == 3:
            res.append((f"{parts[0]}:{parts[1]}", parts[2]))
    return res


def ci_includes(repo):
    """Os projetos de template do CI que o .gitlab-ci.yml inclui."""
    p = REPOS / repo / ".gitlab-ci.yml"
    if not p.exists():
        return []
    text = p.read_text(errors="replace")
    return sorted(set(re.findall(r"project:\s*['\"]?([\w./-]+)", text)))


def infra_section(repo):
    """As linhas do repo na visão por-repositorio do catálogo GCP."""
    p = VAULT / "infra" / "por-repositorio.md"
    if not p.exists():
        return [], ""
    text = p.read_text()
    m = re.search(r"^atualizado_em:\s*(\S+)", text, re.M)
    when = m.group(1) if m else ""
    m = re.search(rf"^## {re.escape(repo)}\s*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not m:
        return [], when
    return [l for l in m.group(1).splitlines() if l.startswith("- ")], when


def graph_edges():
    """As arestas A → B do grafo manual (infra/grafo-chamadas-canais.md, seção em texto)."""
    p = VAULT / "infra" / "grafo-chamadas-canais.md"
    if not p.exists():
        return []
    edges = []
    for line in p.read_text().splitlines():
        if not line.startswith("- `") or "→" not in line:
            continue
        hops = line[2:].split("→")
        for a, b in zip(hops, hops[1:]):
            src = re.findall(r"`([^`]+)`", a)
            dst = re.findall(r"`([^`]+)`", b)
            if src:
                for d in dst:
                    note = re.search(r"`" + re.escape(d) + r"`\s*\(([^)]*)\)", b)
                    edges.append((src[-1], d, note.group(1) if note else ""))
    return edges


def build(repo, repos, names, matrix, owners, edges):
    """O Markdown do bloco automático."""
    today = dt.date.today().isoformat()
    head = git(REPOS / repo, "rev-parse", "--short", "HEAD").strip()
    branch = git(REPOS / repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
    n_names = max(len(names) - 1, 1)
    config = {r for r in repos if r in CONFIG_REPOS or len(matrix.get(r, {})) / n_names > CONFIG_RATIO}
    L = [BEGIN, "", f"## Levantamento automático", ""]
    L.append(f"Gerado em {today} sobre `{branch}` @ `{head}` pela skill `mapear-dependencias`. São **candidatos**: o nome aparece no código, mas citar não prova o uso nem o sentido. Ao confirmar um no código, levar para Consome / Consumido por (acima), com o contrato e o arquivo.")
    L.append("")

    # 1. outros repositórios que este cita
    mine = matrix.get(repo, {})
    L.append("### Repositórios que este cita")
    L.append("")
    rows = sorted(((n, h) for n, h in mine.items() if n not in config), key=lambda x: -x[1]["n"])
    if rows:
        for n, h in rows:
            L.append(f"- `{n}` ({h['n']}×): " + ", ".join(f"`{e}`" for e in rank(h["ex"])))
    else:
        L.append("_Nenhum._")
    cfg_here = sorted(n for n in mine if n in config)
    if cfg_here:
        L.append(f"- Configuração, CI e documentação citadas: " + ", ".join(f"`{n}`" for n in cfg_here))
    L.append("")

    # 2. quem cita este
    L.append("### Repositórios que citam este")
    L.append("")
    rev = []
    for r in repos:
        if r == repo or r in config:
            continue
        h = matrix.get(r, {}).get(repo)
        if h:
            rev.append((r, h))
    rev.sort(key=lambda x: -x[1]["n"])
    if rev:
        for r, h in rev:
            L.append(f"- `{r}` ({h['n']}×): " + ", ".join(f"`{e}`" for e in rank(h["ex"])))
    else:
        L.append("_Nenhum._" if repo in names else f"_O nome `{repo}` é comum demais para busca por token; procurar pelo host, rota ou tópico._")
    cfg_rev = sorted(r for r in config if r != repo and repo in matrix.get(r, {}))
    if cfg_rev:
        L.append("- Configuração, CI e documentação que citam este (gateway, configmaps, roles, diagramas, coleções): " + ", ".join(f"`{r}`" for r in cfg_rev))
    L.append("")

    # 3. grafo manual
    g_out = [(b, n) for a, b, n in edges if a == repo]
    g_in = [(a, n) for a, b, n in edges if b == repo]
    if g_out or g_in:
        L.append("### No grafo manual ([[grafo-chamadas-canais]])")
        L.append("")
        if g_out:
            L.append("- Consome: " + ", ".join(f"`{b}`" + (f" ({n})" if n else "") for b, n in g_out))
        if g_in:
            L.append("- Consumido por: " + ", ".join(f"`{a}`" + (f" ({n})" if n else "") for a, n in g_in))
        L.append("")

    # 4. manifestos: libs internas, dados, terceiros
    deps = manifests(repo)
    internal, data, third = {}, {}, {}
    for d, f in deps:
        if INTERNAL_SCOPE.match(d) or d.startswith("gitlab:") or "gitlab.com/ctbz" in d or d.startswith("br.com.contabilizei"):
            internal.setdefault(d, f)
        for pat, label in DATA_SDKS:
            if re.match(pat, d):
                data.setdefault(label, set()).add(d)
        for pat, label in THIRD_SDKS:
            if re.match(pat, d):
                third.setdefault(label, set()).add(f"`{d}`")
    L.append("### Libs internas")
    L.append("")
    if internal:
        for d, f in sorted(internal.items()):
            name = d.removeprefix("gitlab:")
            src = owners.get(d) or next((owners[k] for k in owners if d.startswith(k + "/")), None) or (name if name in repos else None)
            L.append(f"- `{d}` (`{f}`)" + (f" — publicada por `{src}`" if src and src != repo else ""))
    else:
        L.append("_Nenhuma._")
    L.append("")

    # 5. infra GCP (catálogo) e CI
    infra, when = infra_section(repo)
    L.append(f"### Infra GCP (catálogo [[por-repositorio]]" + (f", de {when}" if when else "") + ")")
    L.append("")
    L.extend(infra or ["_Nenhum recurso do catálogo citado._"])
    ci = ci_includes(repo)
    if ci:
        L.append("- **Templates de CI** (`.gitlab-ci.yml`): " + ", ".join(f"`{c}`" for c in ci))
    L.append("")

    # 6. bancos e dados
    bq = sorted({t.lower() for _, t in grep_o(repo, [r"contabilizei-(data|dataflow)[.:`][a-z0-9_]+(\.[a-z0-9_]+)?"])})
    L.append("### Bancos e dados")
    L.append("")
    if data or bq:
        for label, ds in sorted(data.items()):
            L.append(f"- {label}: " + ", ".join(f"`{d}`" for d in sorted(ds)))
        if bq:
            L.append("- Tabelas/datasets do BigQuery citados: " + ", ".join(f"`{t}`" for t in bq[:15]) + (" …" if len(bq) > 15 else ""))
    else:
        L.append("_Nenhum driver ou dataset achado._")
    L.append("")

    # 7. terceiros
    for ref, t in grep_o(repo, [p for p, _ in THIRD_HOSTS]):
        for pat, label in THIRD_HOSTS:
            if re.fullmatch(pat, t, re.I):
                host = t.lower()
                seen = third.setdefault(label, set())
                if not any(x.startswith(f"`{host}` em") for x in seen) and sum(" em `" in x for x in seen) < EXAMPLES:
                    seen.add(f"`{host}` em `{ref}`")
                break
    L.append("### Terceiros")
    L.append("")
    if third:
        for label, ev in sorted(third.items()):
            L.append(f"- {label}: " + ", ".join(sorted(ev)[:EXAMPLES + 2]))
    else:
        L.append("_Nenhum SDK ou host de terceiro achado._")
    L.append("")
    L.append(END)
    return "\n".join(L)


TEMPLATE = """---
name: dependencias-{repo}
description: "Dependências do {repo}: o que ele consome (outros repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome, com o contrato e onde fica no código"
metadata:
  type: reference
tags:
  - dependencias
  - {repo}
repositorio: {repo}
---

# Dependências do {repo}

O que o `{repo}` consome e quem o consome (padrão em [[dependencias-entre-repositorios]]). As seções **Consome** e **Consumido por** são as confirmadas no código, uma linha por contrato; o **Levantamento automático**, no fim, traz os candidatos achados pela skill `mapear-dependencias`, a conferir.

## Consome

### Repositórios internos

_Nada confirmado ainda._

### Libs internas

_Nada confirmado ainda._

### Infra GCP

_Nada confirmado ainda._

### Bancos e dados

_Nada confirmado ainda._

### Terceiros

_Nada confirmado ainda._

## Consumido por

Quem consome os contratos deste repositório; a revisão de MRs confere se o diff quebra algum deles.

_Nada confirmado ainda._

"""

INDEX_LINE = "- [[dependencias-{repo}|Dependências]] — o que consome (repositórios, libs internas, infra GCP, bancos, terceiros) e quem o consome"

INDEX_TEMPLATE = """---
name: {repo}-indice
description: "Índice de notas do repositório {repo}: como rodar localmente, como testar, fluxos e particularidades"
metadata:
  type: reference
tags:
  - repositories-indice
  - {repo}
repositorio: {repo}
caminho: ~/repositories/{repo}
---

# {repo}

Repositório em `~/repositories/{repo}`. Notas sobre ele (como rodar localmente, como testar, como funciona cada fluxo, particularidades), uma linha por nota.

_Nenhuma nota ainda._
"""


def write(repo, block):
    folder = VAULT / "repositories" / repo
    idx = folder / f"_{repo}-indice.md"
    created_index = False
    if not idx.exists():
        folder.mkdir(parents=True, exist_ok=True)
        idx.write_text(INDEX_TEMPLATE.format(repo=repo))
        created_index = True
        top = VAULT / "repositories" / "_repositories-indice.md"
        text = top.read_text()
        line = f"- [[_{repo}-indice|{repo}]]"
        if line not in text:
            lines = text.rstrip("\n").splitlines()
            items = [i for i, l in enumerate(lines) if l.startswith("- [[_")]
            pos = next((i for i in items if lines[i].lower() > line.lower()), (items[-1] + 1) if items else len(lines))
            lines.insert(pos, line)
            top.write_text("\n".join(lines) + "\n")
    note = folder / f"dependencias-{repo}.md"
    text = note.read_text() if note.exists() else TEMPLATE.format(repo=repo)
    if BEGIN.split(" (")[0] in text and END in text:
        start = text.index(BEGIN.split(" (")[0])
        end = text.index(END) + len(END)
        text = text[:start] + block + text[end:]
    else:
        text = text.rstrip("\n") + "\n\n" + block + "\n"
    if not text.endswith("\n"):
        text += "\n"
    note.write_text(text)
    # a linha no índice do repo
    it = idx.read_text()
    if f"[[dependencias-{repo}" not in it:
        it = it.replace("_Nenhuma nota ainda._\n", "").rstrip("\n")
        # depois de um parágrafo (índice sem notas), uma linha em branco antes da lista
        sep = "\n" if it.splitlines()[-1].startswith("- ") else "\n\n"
        it = it + sep + INDEX_LINE.format(repo=repo) + "\n"
        idx.write_text(it)
    return note, created_index


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repos", nargs="*")
    ap.add_argument("--all", action="store_true", help="todos os repos com pasta no vault e clone local")
    ap.add_argument("--print", action="store_true", help="só mostra o levantamento, sem gravar")
    ap.add_argument("--refresh", action="store_true", help="ignora o cache da varredura")
    a = ap.parse_args()
    repos = all_repos()
    targets = list(a.repos)
    if a.all:
        vault_repos = {p.name for p in (VAULT / "repositories").iterdir() if p.is_dir()}
        targets = [r for r in repos if r in vault_repos]
    if not targets:
        ap.error("informe o repositório (ou --all)")
    for t in targets:
        if not (REPOS / t / ".git").exists():
            sys.exit(f"{t}: não está clonado em ~/repositories")
    names = token_names(repos)
    matrix = {}
    for i, r in enumerate(repos, 1):
        if sys.stderr.isatty():
            print(f"\rvarrendo {i}/{len(repos)} {r[:40]:<40}", end="", file=sys.stderr)
        matrix[r] = scan(r, names, a.refresh)
    print("", file=sys.stderr)
    owners = package_owner(repos)
    edges = graph_edges()
    for t in targets:
        block = build(t, repos, names, matrix, owners, edges)
        if a.print:
            print(block)
            continue
        note, created = write(t, block)
        print(f"{t}: {note.relative_to(VAULT)}" + (" (índice do repo criado)" if created else ""))


if __name__ == "__main__":
    main()
