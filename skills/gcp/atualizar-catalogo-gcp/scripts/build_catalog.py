#!/usr/bin/env python3
"""Build the CTBZ GCP service catalog in the Obsidian vault.

Collects Pub/Sub (topics, subscriptions), Cloud Scheduler jobs, Cloud Tasks queues, Cloud Run (services, jobs, functions) and, with --gke, GKE workloads from every project in PROJECTS. Then cross-references every resource name with the source code in ~/repositories to find which repositories cite it, and writes one note per subject into the vault (default: ~/dotfiles/docs/ai/obsidian/ctbz/infra).

Usage:
    python3 build_catalog.py                 # collect + generate (GKE note is kept as is)
    python3 build_catalog.py --gke           # also list GKE workloads (needs VPN for private clusters)
    python3 build_catalog.py --offline       # regenerate notes from the last raw collection, no API calls
    python3 build_catalog.py --projects aida-prd aida-stg   # restrict the collection (other projects are kept from the last run)

Auth: uses `gcloud auth print-access-token` (account with read access). Raw data goes to ~/.cache/gcp-catalog/raw.
"""

import argparse
import concurrent.futures as cf
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from collections import defaultdict

# (project id, domain, environment). Keep in sync with the "Projetos por domínio" table in ~/.claude/CLAUDE.md.
PROJECTS = [
    ("atendimento-canais-dev", "Atendimento / canais", "dev"),
    ("atendimento-canais-prd", "Atendimento / canais", "prod"),
    ("contabilizei-experts-dev", "Experts", "dev"),
    ("contabilizei-experts-prd", "Experts", "prod"),
    ("aida-stg", "AIDA", "dev/stg"),
    ("aida-prd", "AIDA", "prod"),
    ("contabilizei-crm-dev", "CRM", "dev"),
    ("contabilizei-crm", "CRM", "prod"),
    ("contabilizeiapp-dev-02", "App Contabilizei", "dev"),
    ("contabilizeiapp", "App Contabilizei", "prod"),
    ("contabilizei-impostos-teste", "Impostos", "dev"),
    ("contabilizei-impostos", "Impostos", "prod"),
    ("contabilizei-issue", "Issue", "dev/prod"),
    ("contabilizei-abertura", "Abertura", "prod"),
    ("fintech-228118", "Fintech", "prod"),
    ("contabilizei-dev-01", "K8s dev", "dev"),
    ("contabilizei-prod-01", "K8s prod", "prod"),
]

# GKE clusters: (cluster, project, location, env, private)
CLUSTERS = [
    ("contabilizei-private-cluster-dev-01", "contabilizei-dev-01", "us-central1-a", "dev", True),
    ("contabilizei-cluster-dev-01", "contabilizei-dev-01", "us-central1-a", "dev", False),
    ("contabilizei-private-cluster-prod-01", "contabilizei-prod-01", "us-central1", "prod", True),
    ("contabilizei-cluster-prd-01", "contabilizei-prod-01", "us-central1", "prod", False),
]
SYSTEM_NAMESPACES = {"kube-system", "gmp-system", "gke-mcs", "default", "otelcol-agent", "custom-metrics"}

# Fallback when the project does not allow listing locations.
FALLBACK_LOCATIONS = ["us-central1", "us-east1", "southamerica-east1", "europe-west1"]

# Repos citing more names than this ratio are treated as config/infra repos (they cite almost everything) and listed apart.
CONFIG_REPO_RATIO = 0.15

HOME = os.path.expanduser("~")
CACHE = os.path.join(HOME, ".cache", "gcp-catalog", "raw")
TODAY = dt.date.today().isoformat()

TOKEN = None


def token():
    global TOKEN
    if TOKEN is None:
        TOKEN = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip()
    return TOKEN


def api_list(url, key, page_size=500):
    """GET every page of a Google list API. Returns (items, error)."""
    items, page = [], None
    while True:
        full = url + ("&" if "?" in url else "?") + f"pageSize={page_size}" + (f"&pageToken={page}" if page else "")
        req = urllib.request.Request(full, headers={"Authorization": f"Bearer {token()}"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.load(r)
        except urllib.error.HTTPError as e:
            try:
                status = json.load(e).get("error", {}).get("status", str(e.code))
            except Exception:
                status = str(e.code)
            return items, status
        except Exception as e:  # network/timeout
            return items, type(e).__name__
        items += data.get(key, [])
        page = data.get("nextPageToken")
        if not page:
            return items, None


def short(name):
    return name.rsplit("/", 1)[-1] if name else name


def location_of(name):
    m = re.search(r"/locations/([^/]+)/", name or "")
    return m.group(1) if m else ""


# --------------------------------------------------------------------------- collect


def collect_project(project):
    raw = {"project": project, "errors": {}}

    def put(key, url, field):
        items, err = api_list(url, field)
        raw[key] = items
        if err:
            raw["errors"][key] = err

    put("topics", f"https://pubsub.googleapis.com/v1/projects/{project}/topics", "topics")
    put("subscriptions", f"https://pubsub.googleapis.com/v1/projects/{project}/subscriptions", "subscriptions")
    put("run_services", f"https://run.googleapis.com/v2/projects/{project}/locations/-/services", "services")
    put("functions", f"https://cloudfunctions.googleapis.com/v2/projects/{project}/locations/-/functions", "functions")

    # Cloud Run jobs do not accept the "-" location wildcard
    run_locs = sorted({location_of(s["name"]) for s in raw["run_services"]} | set(FALLBACK_LOCATIONS))
    raw["run_jobs"] = []
    with cf.ThreadPoolExecutor(8) as ex:
        for got, _ in ex.map(lambda l: api_list(f"https://run.googleapis.com/v2/projects/{project}/locations/{l}/jobs", "jobs"), run_locs):
            raw["run_jobs"] += got

    for key, base, field in (
        ("scheduler_jobs", "https://cloudscheduler.googleapis.com/v1", "jobs"),
        ("task_queues", "https://cloudtasks.googleapis.com/v2", "queues"),
    ):
        locs, err = api_list(f"{base}/projects/{project}/locations", "locations")
        locs = [l["locationId"] for l in locs] or FALLBACK_LOCATIONS
        items, errors = [], set()
        with cf.ThreadPoolExecutor(16) as ex:
            for got, e in ex.map(lambda l: api_list(f"{base}/projects/{project}/locations/{l}/{field}", field), locs):
                items += got
                if e and e != "INVALID_ARGUMENT":  # INVALID_ARGUMENT = service not offered in that location
                    errors.add(e)
        raw[key] = items
        if errors and not items:
            raw["errors"][key] = ",".join(sorted(errors))
    return raw


def collect_gke():
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, KUBECONFIG=os.path.join(tmp, "kubeconfig"))
        for cluster, project, loc, _, _ in CLUSTERS:
            flag = "--zone" if loc.count("-") == 2 else "--region"
            subprocess.run(["gcloud", "container", "clusters", "get-credentials", cluster, flag, loc, "--project", project], env=env, capture_output=True)
            ctx = f"gke_{project}_{loc}_{cluster}"
            try:
                res = subprocess.run(["kubectl", "--context", ctx, "--request-timeout=60s", "get", "deploy,statefulset,cronjob", "-A", "-o", "json"], env=env, capture_output=True, text=True, timeout=120)
                items = json.loads(res.stdout)["items"] if res.returncode == 0 else None
            except (subprocess.TimeoutExpired, json.JSONDecodeError):
                items = None
            if items is None:
                print(f"  GKE {cluster}: falhou (VPN conectada?)", file=sys.stderr)
                continue
            out[cluster] = [{"kind": i["kind"], "ns": i["metadata"]["namespace"], "name": i["metadata"]["name"]} for i in items]
            print(f"  GKE {cluster}: {len(items)} workloads", file=sys.stderr)
    return out


# --------------------------------------------------------------------------- repos


TOKEN_RE = r"[A-Za-z0-9][A-Za-z0-9._-]{3,}"


def repo_tokens(repo_dir, names):
    """Return the subset of `names` that appear as whole tokens in the repo source."""
    found = set()
    # git grep: only tracked files (no node_modules/build output) and available everywhere git is
    cmd = ["git", "-C", repo_dir, "grep", "-o", "-h", "-I", "-E", TOKEN_RE, "--", ".", ":!*.lock", ":!package-lock.json", ":!*.min.js", ":!*.svg", ":!*.map", ":!*.csv"]
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, errors="ignore") as p:
        for line in p.stdout:
            t = line.strip().strip(".-")
            if t in names:
                found.add(t)
            # names inside paths like projects/x/topics/<name> are already split by the regex (no "/")
    return found


def index_repos(repos_dir, names):
    repos = sorted(d for d in os.listdir(repos_dir) if os.path.isdir(os.path.join(repos_dir, d)) and not d.startswith("."))
    by_repo = {}
    with cf.ThreadPoolExecutor(8) as ex:
        for repo, found in zip(repos, ex.map(lambda r: repo_tokens(os.path.join(repos_dir, r), names), repos)):
            if found:
                by_repo[repo] = found
    limit = max(30, int(len(names) * CONFIG_REPO_RATIO))
    config_repos = {r for r, f in by_repo.items() if len(f) > limit}
    by_name = defaultdict(set)
    for repo, found in by_repo.items():
        for n in found:
            by_name[n].add(repo)
    return by_name, by_repo, config_repos


# --------------------------------------------------------------------------- helpers for notes


def frontmatter(name, description, tags):
    lines = ["---", f"name: {name}", f'description: "{description}"', "metadata:", "  type: reference", "tags:"]
    lines += [f"  - {t}" for t in tags]
    lines += [f"atualizado_em: {TODAY}", "---", ""]
    return lines


def code_list(xs):
    return ", ".join(f"`{x}`" for x in sorted(xs))


def repos_str(name, by_name, config_repos):
    rs = by_name.get(name, set())
    main = sorted(rs - config_repos)
    cfg = sorted(rs & config_repos)
    parts = []
    if main:
        parts.append("repos: " + ", ".join(main))
    if cfg:
        parts.append("config: " + ", ".join(cfg))
    return " · ".join(parts)


def service_from_url(url):
    """Map a push endpoint / http target to a human readable service."""
    m = re.match(r"https?://([^/:]+)(/[^?]*)?", url or "")
    if not m:
        return url
    host, path = m.group(1), m.group(2) or ""
    if host.endswith(".run.app"):
        h = host[: -len(".run.app")]
        h = re.sub(r"-\d{6,}\.[a-z0-9-]+$", "", h)  # <svc>-<projectnumber>.<region>
        h = re.sub(r"-[a-z0-9]{10}-[a-z]{2}\.a$", "", h)  # <svc>-<hash>-uc.a
        return f"Cloud Run `{h}`{path and ' ' + path}"
    if host.endswith(".appspot.com"):
        svc = host.split("-dot-")[0] if "-dot-" in host else "default"
        if ".r.appspot.com" in host or (host.count(".") == 2 and "-dot-" not in host):
            svc = "default"
        if "." in svc and "-dot-" not in host:
            svc = svc.split(".")[0]
        return f"App Engine `{svc}`{path and ' ' + path}"
    if host.endswith("cloudfunctions.net"):
        return f"Function `{path.strip('/')}`"
    return f"`{host}{path}`"


def sub_prefix(sub):
    for sep in (".sub.", "_sub_", ".sub-", "-sub-"):
        if sep in sub:
            return sub.split(sep)[0]
    if "." in sub:
        return sub.split(".")[0]
    return None


# --------------------------------------------------------------------------- notes


def note_pubsub(project, dom, env, raw, by_name, config_repos, schedulers_by_topic):
    topics = {short(t["name"]): t for t in raw.get("topics", [])}
    subs_by_topic = defaultdict(list)
    for s in raw.get("subscriptions", []):
        subs_by_topic[s.get("topic", "")].append(s)
    lines = frontmatter(f"pubsub-{project}", f"Tópicos e subscriptions do Pub/Sub em {project} ({dom}, {env}) com consumidor e repositórios que citam cada um", ["infra", "pubsub"])
    lines += [f"# Pub/Sub: {project}", "", f"{dom}, {env}. Fotografia de {TODAY}. Formato: tópico → subscriptions (tipo e consumidor) · repositórios que citam o nome do tópico/subscription em `~/repositories` (`config:` = repos de configuração que citam quase tudo). Ver [[_infra-indice]] para o significado de cada campo.", ""]
    err = raw["errors"].get("topics") or raw["errors"].get("subscriptions")
    if err:
        lines += [f"> Sem permissão para listar tudo neste projeto ({err}).", ""]
    all_topic_paths = set(subs_by_topic) | {t["name"] for t in raw.get("topics", [])}
    for tpath in sorted(all_topic_paths, key=short):
        tname = short(tpath)
        foreign = not tpath.startswith(f"projects/{project}/")
        if tpath == "_deleted-topic_":
            tname = "(tópico apagado)"
        head = f"- **`{tname}`**" + (f" (tópico de `{tpath.split('/')[1]}`)" if foreign and "/" in tpath else "")
        extra = repos_str(tname, by_name, config_repos)
        if tname in topics and topics[tname].get("labels", {}).get("goog-eventarc") is not None:
            head += " (Eventarc)"
        sched = schedulers_by_topic.get(tpath)
        if sched:
            head += " · publicado por scheduler " + code_list(sched)
        lines.append(head + (f" · {extra}" if extra else ""))
        for s in sorted(subs_by_topic.get(tpath, []), key=lambda x: x["name"]):
            sname = short(s["name"])
            if s.get("pushConfig", {}).get("pushEndpoint"):
                kind = "push → " + service_from_url(s["pushConfig"]["pushEndpoint"])
            elif s.get("bigqueryConfig"):
                kind = "BigQuery → `" + s["bigqueryConfig"].get("table", "") + "`"
            elif s.get("cloudStorageConfig"):
                kind = "Cloud Storage → `" + s["cloudStorageConfig"].get("bucket", "") + "`"
            else:
                kind = "pull"
                prefix = sub_prefix(sname)
                if prefix:
                    kind += f", consumidor provável `{prefix}`"
            if s.get("deadLetterPolicy"):
                kind += f", DLQ `{short(s['deadLetterPolicy'].get('deadLetterTopic', ''))}`"
            if s.get("state") and s["state"] != "ACTIVE":
                kind += f", estado {s['state']}"
            r = repos_str(sname, by_name, config_repos)
            lines.append(f"    - `{sname}` ({kind})" + (f" · {r}" if r else ""))
    return "\n".join(lines).rstrip() + "\n"


def describe_target(job):
    if "pubsubTarget" in job:
        return f"Pub/Sub `{short(job['pubsubTarget'].get('topicName', ''))}`"
    if "httpTarget" in job:
        t = job["httpTarget"]
        return f"{t.get('httpMethod', 'POST')} {service_from_url(t.get('uri', ''))}"
    if "appEngineHttpTarget" in job:
        t = job["appEngineHttpTarget"]
        svc = t.get("appEngineRouting", {}).get("service", "default")
        return f"{t.get('httpMethod', 'POST')} App Engine `{svc}` {t.get('relativeUri', '')}"
    return "?"


def note_schedulers(data, by_name, config_repos):
    lines = frontmatter("schedulers", "Cloud Scheduler: agendamentos por projeto GCP com cron, alvo (Pub/Sub, HTTP, App Engine) e repositórios que citam cada job", ["infra", "scheduler"])
    lines += ["# Cloud Scheduler", "", f"Fotografia de {TODAY}. Formato: job · cron (fuso) · alvo · estado se não estiver ativo · repositórios que citam o nome do job.", ""]
    denied = []
    for project, dom, env in PROJECTS:
        raw = data.get(project)
        if not raw:
            continue
        jobs = raw.get("scheduler_jobs", [])
        if not jobs:
            if raw["errors"].get("scheduler_jobs"):
                denied.append(project)
            continue
        lines += [f"## {project}", "", f"{dom}, {env}.", ""]
        for j in sorted(jobs, key=lambda x: x["name"]):
            name = short(j["name"])
            st = "" if j.get("state") == "ENABLED" else f" · **{j.get('state', '?')}**"
            loc = location_of(j["name"])
            loc = "" if loc == "us-central1" else f" ({loc})"
            r = repos_str(name, by_name, config_repos)
            lines.append(f"- `{name}`{loc} · `{j.get('schedule', '')}` ({j.get('timeZone', 'UTC')}) · {describe_target(j)}{st}" + (f" · {r}" if r else ""))
        lines.append("")
    if denied:
        lines += ["## Sem acesso para listar", "", "Sem permissão para listar Cloud Scheduler em: " + code_list(denied) + ". Nesses domínios, agendamentos também podem ser CronJobs no GKE (ver [[gke-workloads]]).", ""]
    return "\n".join(lines).rstrip() + "\n"


def note_tasks(data, by_name, config_repos):
    lines = frontmatter("cloud-tasks", "Cloud Tasks: filas por projeto GCP com taxa, tentativas e repositórios que citam cada fila", ["infra", "cloud-tasks"])
    lines += ["# Cloud Tasks", "", f"Fotografia de {TODAY}. Formato: fila · taxa máx. por segundo / concorrência · máx. tentativas · estado se não estiver rodando · roteamento App Engine se houver · repositórios que citam o nome da fila. O alvo de cada task é definido por quem cria a task (ver os repositórios).", ""]
    denied = []
    for project, dom, env in PROJECTS:
        raw = data.get(project)
        if not raw:
            continue
        qs = raw.get("task_queues", [])
        if not qs:
            if raw["errors"].get("task_queues"):
                denied.append(project)
            continue
        lines += [f"## {project}", "", f"{dom}, {env}.", ""]
        for q in sorted(qs, key=lambda x: x["name"]):
            name = short(q["name"])
            rl = q.get("rateLimits", {})
            rc = q.get("retryConfig", {})
            parts = [f"`{name}`"]
            loc = location_of(q["name"])
            if loc != "us-central1":
                parts[0] += f" ({loc})"
            parts.append(f"{rl.get('maxDispatchesPerSecond', '?')}/s, {rl.get('maxConcurrentDispatches', '?')} concorrentes")
            attempts = rc.get("maxAttempts", -1)
            parts.append("tentativas ilimitadas" if attempts == -1 else f"{attempts} tentativas")
            if q.get("state", "RUNNING") != "RUNNING":
                parts.append(f"**{q['state']}**")
            route = q.get("appEngineRoutingOverride", {}).get("service")
            if route:
                parts.append(f"App Engine `{route}`")
            r = repos_str(name, by_name, config_repos)
            if r:
                parts.append(r)
            lines.append("- " + " · ".join(parts))
        lines.append("")
    if denied:
        lines += ["## Sem acesso para listar", "", "Sem permissão para listar Cloud Tasks em: " + code_list(denied) + ".", ""]
    return "\n".join(lines).rstrip() + "\n"


def note_cloud_run(data, by_name, config_repos):
    lines = frontmatter("cloud-run-servicos", "Lista de serviços Cloud Run, Cloud Run functions e jobs por projeto GCP, para localizar onde um serviço roda em dev/prod", ["infra", "cloud-run"])
    lines += ["# Cloud Run e functions", "", f"Fotografia de {TODAY}. As Cloud Run functions (gen2) também aparecem como serviço Cloud Run; quando o nome coincide, é o mesmo serviço. Região `us-central1` salvo indicação. Entre parênteses no fim: repositórios que citam o nome.", ""]
    denied = []

    def fmt(items):
        out = []
        for i in sorted(items, key=lambda x: short(x["name"])):
            n = short(i["name"])
            loc = location_of(i["name"])
            s = f"`{n}`" + ("" if loc == "us-central1" else f" ({loc})")
            r = sorted(by_name.get(n, set()) - config_repos)
            if r:
                s += f" ({', '.join(r)})"
            out.append(s)
        return ", ".join(out)

    for project, dom, env in PROJECTS:
        raw = data.get(project)
        if not raw:
            continue
        s, j, f = raw.get("run_services", []), raw.get("run_jobs", []), raw.get("functions", [])
        if not (s or j or f):
            if raw["errors"].get("run_services"):
                denied.append(project)
            continue
        lines += [f"## {project}", "", f"{dom}, {env}.", ""]
        if s:
            lines.append("- **Serviços**: " + fmt(s))
        if f:
            lines.append("- **Functions**: " + fmt(f))
        if j:
            lines.append("- **Jobs**: " + fmt(j))
        lines.append("")
    if denied:
        lines += ["## Sem acesso para listar", "", "Sem permissão para listar Cloud Run/functions em: " + code_list(denied) + ". Serviços desses domínios em geral rodam no GKE (ver [[gke-workloads]]) ou no App Engine.", ""]
    return "\n".join(lines).rstrip() + "\n"


def note_gke(gke):
    kinds = {"Deployment": "", "StatefulSet": " (sts)", "CronJob": " (cron)"}
    lines = frontmatter("gke-workloads", "Lista de workloads (deployments, statefulsets, cronjobs) por cluster GKE e namespace, para localizar onde um serviço roda em dev/prod", ["infra", "gke"])
    lines += ["# Workloads no GKE", "", f"Fotografia de {TODAY} (`kubectl get deploy,statefulset,cronjob -A`), sem namespaces de sistema ({code_list(SYSTEM_NAMESPACES)}). Sem marcação = Deployment; `(sts)` = StatefulSet; `(cron)` = CronJob. Para achar um serviço, buscar o nome nesta nota; se não estiver aqui, pode ser novo: listar de novo no cluster (com VPN nos privados).", ""]
    for cluster, project, loc, env, private in CLUSTERS:
        if cluster not in gke:
            continue
        flag = "zone" if loc.count("-") == 2 else "region"
        vpn = "sim" if private else "provavelmente não (cluster não privado; não testado sem VPN)"
        lines += [f"## {cluster}", "", f"Projeto `{project}`, local `{loc}`, ambiente {env}, VPN necessária: {vpn}. Credenciais: `gcloud container clusters get-credentials {cluster} --{flag} {loc} --project {project}`.", ""]
        by_ns = defaultdict(list)
        for w in gke[cluster]:
            if w["ns"] not in SYSTEM_NAMESPACES:
                by_ns[w["ns"]].append(w["name"] + kinds.get(w["kind"], f" ({w['kind']})"))
        for ns in sorted(by_ns):
            lines.append(f"- **{ns}**: " + code_list(by_ns[ns]))
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def note_by_repo(data, by_repo, config_repos, kinds_of):
    lines = frontmatter("por-repositorio", "Visão reversa do catálogo GCP: para cada repositório em ~/repositories, os tópicos, subscriptions, schedulers, filas e serviços que ele cita", ["infra", "repositorios"])
    lines += ["# Recursos GCP por repositório", "", f"Fotografia de {TODAY}. Para cada repositório local em `~/repositories`, os nomes de recursos GCP que aparecem no código (busca por token exato). Citar não diz se o repo publica ou consome: abrir o código para confirmar. Repositórios de configuração (citam quase tudo) ficam no fim, só com a contagem.", ""]
    for repo in sorted(by_repo):
        if repo in config_repos:
            continue
        groups = defaultdict(set)
        for n in by_repo[repo]:
            for k in kinds_of.get(n, ()):
                groups[k].add(n)
        if not groups:
            continue
        lines += [f"## {repo}", ""]
        for k in ("Tópico", "Subscription", "Scheduler", "Fila Cloud Tasks", "Cloud Run / function"):
            if groups.get(k):
                lines.append(f"- **{k}**: " + code_list(groups[k]))
        lines.append("")
    if config_repos:
        lines += ["## Repositórios de configuração", ""]
        for r in sorted(config_repos):
            lines.append(f"- `{r}`: cita {len(by_repo[r])} nomes")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def note_index(data, gke_present):
    lines = ["---", "name: infra-indice", 'description: "Índice de notas de infraestrutura GCP: onde cada serviço roda (GKE, Cloud Run, functions), Pub/Sub, Scheduler e Cloud Tasks por projeto, com repositórios que citam cada recurso"', "metadata:", "  type: reference", "tags:", "  - infra-indice", "---", ""]
    lines += ["# Infra", "", "Catálogo de onde cada serviço e recurso roda na GCP, para localizar rapidamente um serviço que está fora, um tópico sem consumidor ou um agendamento que não disparou. O mapa de projetos por domínio fica no `CLAUDE.md` global; aqui ficam as listas.", ""]
    lines += [f"As notas são geradas pelo script da skill `atualizar-catalogo-gcp` (`~/.claude/skills/atualizar-catalogo-gcp/`); não editar à mão, rodar a skill de novo. Última geração: {TODAY}.", ""]
    lines += ["Campos: **repos** = repositórios em `~/repositories` cujo código cita o nome exato do recurso (produtor, consumidor ou quem cria); **config** = repos de configuração que citam quase tudo; **consumidor provável** = prefixo do nome da subscription (convenção `<consumidor>.sub.<evento>`); push → serviço que recebe o push.", ""]
    lines += ["## Serviços", ""]
    lines.append("- [[gke-workloads|Workloads no GKE]] — deployments, statefulsets e cronjobs por cluster (dev/prod, privado/público) e namespace")
    lines.append("- [[cloud-run-servicos|Cloud Run e functions]] — serviços Cloud Run, Cloud Run functions e jobs por projeto")
    lines += ["", "## Mensageria e agendamentos", ""]
    lines.append("- [[schedulers|Cloud Scheduler]] — agendamentos por projeto: cron, alvo e repositórios")
    lines.append("- [[cloud-tasks|Cloud Tasks]] — filas por projeto: taxa, tentativas e repositórios")
    for project, dom, env in PROJECTS:
        raw = data.get(project)
        if raw and (raw.get("topics") or raw.get("subscriptions")):
            lines.append(f"- [[pubsub-{project}|Pub/Sub {project}]] — {dom}, {env}: {len(raw.get('topics', []))} tópicos, {len(raw.get('subscriptions', []))} subscriptions")
    lines += ["", "## Visões", ""]
    lines.append("- [[por-repositorio|Recursos GCP por repositório]] — para cada repo, os tópicos, subscriptions, schedulers, filas e serviços que ele cita")
    return "\n".join(lines).rstrip() + "\n"


# --------------------------------------------------------------------------- main


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gke", action="store_true", help="also list GKE workloads (needs VPN)")
    ap.add_argument("--offline", action="store_true", help="do not call APIs, reuse the last raw collection")
    ap.add_argument("--projects", nargs="*", help="collect only these projects")
    ap.add_argument("--repos", default=os.path.join(HOME, "repositories"))
    ap.add_argument("--out", default=os.path.join(HOME, "dotfiles", "docs", "ai", "obsidian", "ctbz", "infra"))
    args = ap.parse_args()
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(args.out, exist_ok=True)

    if not args.offline:
        targets = args.projects or [p for p, _, _ in PROJECTS]
        print(f"Coletando {len(targets)} projetos...", file=sys.stderr)
        with cf.ThreadPoolExecutor(6) as ex:
            for raw in ex.map(collect_project, targets):
                json.dump(raw, open(os.path.join(CACHE, f"{raw['project']}.json"), "w"))
                counts = {k: len(raw.get(k, [])) for k in ("topics", "subscriptions", "scheduler_jobs", "task_queues", "run_services", "functions")}
                print(f"  {raw['project']}: {counts} erros={raw['errors']}", file=sys.stderr)
        if args.gke:
            json.dump(collect_gke(), open(os.path.join(CACHE, "gke.json"), "w"))

    data = {}
    for p, _, _ in PROJECTS:
        f = os.path.join(CACHE, f"{p}.json")
        if os.path.exists(f):
            data[p] = json.load(open(f))
    gke_file = os.path.join(CACHE, "gke.json")
    gke = json.load(open(gke_file)) if os.path.exists(gke_file) else {}

    # names to look for in the repos, and what kind each one is
    kinds_of = defaultdict(set)
    for raw in data.values():
        for t in raw.get("topics", []):
            kinds_of[short(t["name"])].add("Tópico")
        for s in raw.get("subscriptions", []):
            kinds_of[short(s["name"])].add("Subscription")
        for j in raw.get("scheduler_jobs", []):
            kinds_of[short(j["name"])].add("Scheduler")
        for q in raw.get("task_queues", []):
            kinds_of[short(q["name"])].add("Fila Cloud Tasks")
        for x in raw.get("run_services", []) + raw.get("run_jobs", []) + raw.get("functions", []):
            kinds_of[short(x["name"])].add("Cloud Run / function")
    # only distinctive names: generic ones (config, default, functions) would match unrelated code
    names = {n for n in kinds_of if len(n) >= 8 and re.search(r"[-._]", n)}
    print(f"Indexando {len(names)} nomes em {args.repos}...", file=sys.stderr)
    by_name, by_repo, config_repos = index_repos(args.repos, names)
    print(f"  {len(by_repo)} repos citam algum recurso; config: {sorted(config_repos)}", file=sys.stderr)

    schedulers_by_topic = defaultdict(set)
    for raw in data.values():
        for j in raw.get("scheduler_jobs", []):
            if "pubsubTarget" in j:
                schedulers_by_topic[j["pubsubTarget"].get("topicName", "")].add(short(j["name"]))

    written = []

    def write(fname, content):
        open(os.path.join(args.out, fname), "w").write(content)
        written.append(fname)

    # remove stale per-project Pub/Sub notes before regenerating
    for f in os.listdir(args.out):
        if f.startswith("pubsub-") and f.endswith(".md"):
            os.remove(os.path.join(args.out, f))
    for project, dom, env in PROJECTS:
        raw = data.get(project)
        if raw and (raw.get("topics") or raw.get("subscriptions")):
            write(f"pubsub-{project}.md", note_pubsub(project, dom, env, raw, by_name, config_repos, schedulers_by_topic))
    write("schedulers.md", note_schedulers(data, by_name, config_repos))
    write("cloud-tasks.md", note_tasks(data, by_name, config_repos))
    write("cloud-run-servicos.md", note_cloud_run(data, by_name, config_repos))
    if gke:
        write("gke-workloads.md", note_gke(gke))
    write("por-repositorio.md", note_by_repo(data, by_repo, config_repos, kinds_of))
    write("_infra-indice.md", note_index(data, bool(gke)))
    print(f"Notas escritas em {args.out}: {', '.join(written)}", file=sys.stderr)


if __name__ == "__main__":
    main()
