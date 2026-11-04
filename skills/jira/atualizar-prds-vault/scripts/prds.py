#!/usr/bin/env python3
"""Keep the PRD notes of the Obsidian vault (~/ctbz-vault/obsidian/PRDs) in sync with Jira.

Subcommands:
    backlog                 print the keys of vault items still in `backlog` (to be re-checked in Jira)
    apply <jira.json>       update item notes from a Jira export (see SKILL.md for the format) and print a report
    rebuild                 regenerate the views (_por-epico, _por-periodo, _por-dominio), epic notes and the numbers in _prds-indice.md

`apply` never touches the manual classification (tipo, atuacao, dominio, epico, notes) nor the manual situations (arquivado, resolvido-outro-dev, esquecido): it only syncs backlog/pronto, titles and dates, and reports everything else. Run `rebuild` after `apply` (or after creating notes by hand).
"""

import json
import os
import re
import sys
from collections import defaultdict

VAULT = os.path.expanduser("~/ctbz-vault/obsidian/PRDs")
ITEMS = os.path.join(VAULT, "itens")
EPICS = os.path.join(VAULT, "epicos")
JIRA_URL = "https://contabilizeicontabilidade.atlassian.net/browse/"

MANUAL_SITUATIONS = {"arquivado", "resolvido-outro-dev", "esquecido"}
DONE_STATUSES = {"concluído", "concluido", "done", "resolvido", "fechado"}
CANCEL_STATUSES = {"cancelado", "cancelada", "won't do", "descartado", "descartada"}
DATE_KEYS = ["data_inicio", "data_teste", "data_fim", "data_pronto"]
# order used to pick data_referencia (see _por-periodo.md)
REF_ORDER = ["data_pronto", "data_fim", "data_inicio", "data_teste"]


# --------------------------------------------------------------------------- notes I/O


def split_note(text):
    """Return (frontmatter lines, body text)."""
    assert text.startswith("---\n"), "note without front-matter"
    end = text.index("\n---\n", 4)
    return text[4:end].split("\n"), text[end + 5 :]


def fm_get(fm, key):
    for i, line in enumerate(fm):
        if line.startswith(key + ":"):
            value = line[len(key) + 1 :].strip()
            if value == "":  # list
                items = []
                for nxt in fm[i + 1 :]:
                    if nxt.startswith("  - "):
                        items.append(nxt[4:].strip().strip('"'))
                    else:
                        break
                return items
            if len(value) >= 2 and value[0] == value[-1] == '"':
                return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
            return value
    return None


def fm_set(fm, key, value, after=None):
    """Set a scalar key, keeping its position; insert after `after` (or before `jira`) when new. None removes it."""
    idx = next((i for i, l in enumerate(fm) if l.startswith(key + ":")), None)
    if value is None:
        if idx is not None:
            del fm[idx]
        return
    line = f"{key}: {value}"
    if idx is not None:
        fm[idx] = line
        return
    anchor = None
    for a in ([after] if after else []) + ["jira"]:
        anchor = next((i for i, l in enumerate(fm) if l.startswith(a + ":")), None)
        if anchor is not None:
            pos = anchor + 1 if a == after else anchor
            break
    fm.insert(pos if anchor is not None else len(fm), line)


def fm_set_list(fm, key, values):
    idx = next((i for i, l in enumerate(fm) if l.startswith(key + ":")), None)
    block = [f"{key}:"] + [f"  - {v}" for v in values]
    if idx is None:
        anchor = next((i for i, l in enumerate(fm) if l.startswith("jira:")), len(fm))
        fm[anchor:anchor] = block
        return
    end = idx + 1
    while end < len(fm) and fm[end].startswith("  - "):
        end += 1
    fm[idx:end] = block


def write_note(path, fm, body):
    with open(path, "w") as f:
        f.write("---\n" + "\n".join(fm) + "\n---\n" + body)


def load_items():
    items = {}
    for f in sorted(os.listdir(ITEMS)):
        if not f.endswith(".md"):
            continue
        path = os.path.join(ITEMS, f)
        fm, body = split_note(open(path).read())
        items[f[:-3]] = {"path": path, "fm": fm, "body": body}
    return items


def quoted(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


# --------------------------------------------------------------------------- dates / periods


def period_of(date):
    y, m = int(date[:4]), int(date[5:7])
    return f"{y}QD{1 if m <= 4 else 2 if m <= 8 else 3}", f'"{y}{m:02d}"'


def recompute_reference(fm, created=None):
    dates = {k: fm_get(fm, k) for k in REF_ORDER}
    ref = next((dates[k] for k in REF_ORDER if dates[k]), None)
    if ref:
        fm_set(fm, "data_referencia_origem", None)
    else:
        ref = created or fm_get(fm, "data_referencia")
    if not ref:
        return
    fm_set(fm, "data_referencia", ref, after="data_pronto")
    periodo, mes = period_of(ref)
    fm_set(fm, "periodo", periodo)
    fm_set(fm, "mes", mes)


# --------------------------------------------------------------------------- backlog


def cmd_backlog():
    keys = [k for k, it in load_items().items() if fm_get(it["fm"], "situacao") == "backlog"]
    print(", ".join(keys))


# --------------------------------------------------------------------------- apply


def cmd_apply(jira_file):
    issues = json.load(open(jira_file))
    items = load_items()
    report = defaultdict(list)
    for issue in issues:
        key = issue["key"]
        it = items.get(key)
        if not it:
            report["novos"].append(f"{key} — {issue.get('summary', '')} ({issue.get('status', '')}, épico {issue.get('parent') or '-'})")
            continue
        fm, body = it["fm"], it["body"]
        before = list(fm)
        changes = []

        # situation
        status = (issue.get("status") or "").lower()
        done = issue.get("statusCategory") == "done" or status in DONE_STATUSES
        current = fm_get(fm, "situacao")
        if status in CANCEL_STATUSES:
            if current not in MANUAL_SITUATIONS:
                report["cancelados"].append(f"{key}: Jira `{issue['status']}`, vault `{current}` (sugestão: arquivado)")
        elif current in MANUAL_SITUATIONS:
            # a manual situation is kept; only worth a look when Jira still has the card open
            if not done:
                report["manuais"].append(f"{key}: vault `{current}` (manual, mantido), Jira `{issue['status']}`")
        else:
            target = "pronto" if done else "backlog"
            if current != target:
                fm_set(fm, "situacao", target)
                changes.append(f"situacao {current} → {target}")

        # title
        summary = (issue.get("summary") or "").strip()
        if summary and fm_get(fm, "titulo") != summary:
            old = fm_get(fm, "titulo")
            fm_set(fm, "titulo", quoted(summary))
            fm_set(fm, "description", quoted(summary))
            body = re.sub(rf"^# {re.escape(key)} — .*$", lambda _: f"# {key} — {summary}", body, count=1, flags=re.M)
            changes.append(f"título «{old}» → «{summary}»")

        # dates: only fill/replace with what Jira has, never erase manual ones
        dates = issue.get("dates", {})
        for k in ("data_inicio", "data_fim", "data_pronto"):
            v = dates.get(k)
            if v and fm_get(fm, k) != v:
                changes.append(f"{k} {fm_get(fm, k) or '-'} → {v}")
                prev = DATE_KEYS[: DATE_KEYS.index(k)]
                after = next((p for p in reversed(prev) if fm_get(fm, p)), "mes")
                fm_set(fm, k, v, after=after)
        old_ref = (fm_get(fm, "data_referencia"), fm_get(fm, "periodo"))
        recompute_reference(fm, (issue.get("created") or "")[:10] or None)
        new_ref = (fm_get(fm, "data_referencia"), fm_get(fm, "periodo"))
        if new_ref != old_ref:
            changes.append(f"referência {old_ref[0]} ({old_ref[1]}) → {new_ref[0]} ({new_ref[1]})")

        # epic divergence is reported, not applied (the epic note may need to be created)
        parent = issue.get("parent")
        epic = (fm_get(fm, "epico") or "").strip("[]")
        if parent and parent != epic:
            report["epico"].append(f"{key}: vault `{epic}`, Jira `{parent}`")

        if fm != before or body != it["body"]:
            # keep the summary bullets of the note body in sync with the front-matter
            sit, tipo = fm_get(fm, "situacao"), fm_get(fm, "tipo")
            body = re.sub(r"^- \*\*Situação:\*\* \S+ ·", f"- **Situação:** {sit} ·", body, count=1, flags=re.M)
            body = re.sub(r"^(- \*\*Período:\*\*) \S+ ·", lambda m: f"{m.group(1)} {fm_get(fm, 'periodo')} ·", body, count=1, flags=re.M)
            write_note(it["path"], fm, body)
            report["atualizados"].append(f"{key}: " + "; ".join(changes))
        else:
            report["sem mudança"].append(key)

    for section in ("atualizados", "novos", "cancelados", "manuais", "epico"):
        if report[section]:
            print(f"## {section} ({len(report[section])})")
            for line in report[section]:
                print(f"- {line}")
            print()
    print(f"sem mudança: {len(report['sem mudança'])}")


# --------------------------------------------------------------------------- rebuild


def vocabulary():
    """Domain descriptions from the Vocabulário section of _prds-indice.md."""
    text = open(os.path.join(VAULT, "_prds-indice.md")).read()
    line = next(l for l in text.split("\n") if l.startswith("- **dominio:**"))
    return dict(re.findall(r"`([a-z-]+)` \((.*?)\)(?=; `|$)", line.strip()))


def item_line(key, it):
    return f"- [[{key}]] — {it['titulo']} · {it['situacao']} · {it['periodo']}"


def sort_items(keys, items):
    return sorted(keys, key=lambda k: (items[k]["data_referencia"] or "", int(re.sub(r"\D", "", k) or 0)), reverse=True)


def replace_section(text, header_re, new_block):
    """Replace from the line matching header_re up to the end of the file."""
    m = re.search(header_re, text, flags=re.M)
    return text[: m.start()] + new_block if m else text.rstrip("\n") + "\n\n" + new_block


def write_view(path, blocks):
    text = open(path).read()  # read before opening for write (that truncates the file)
    with open(path, "w") as f:
        f.write(replace_section(text, r"^## ", "\n".join(blocks)))


def cmd_rebuild():
    raw = load_items()
    items = {}
    for k, it in raw.items():
        fm = it["fm"]
        items[k] = {
            "titulo": fm_get(fm, "titulo"),
            "situacao": fm_get(fm, "situacao"),
            "periodo": fm_get(fm, "periodo"),
            "data_referencia": fm_get(fm, "data_referencia"),
            "dominio": fm_get(fm, "dominio") or [],
            "epico": (fm_get(fm, "epico") or "").strip("[]"),
        }

    # epics
    by_epic = defaultdict(list)
    for k, it in items.items():
        by_epic[it["epico"]].append(k)
    epic_titles = {}
    epic_notes = len([f for f in os.listdir(EPICS) if f.endswith(".md")])
    for f in sorted(os.listdir(EPICS)):
        key = f[:-3]
        path = os.path.join(EPICS, f)
        fm, body = split_note(open(path).read())
        epic_titles[key] = fm_get(fm, "titulo")
        keys = sort_items(by_epic.get(key, []), items)
        if not keys:  # grouping card with no items of its own: leave the note as written
            continue
        doms = sorted({d for k in keys for d in items[k]["dominio"]})
        pers = sorted({items[k]["periodo"] for k in keys if items[k]["periodo"]})
        fm_set_list(fm, "dominio", doms)
        fm_set_list(fm, "periodos", pers)
        fm_set(fm, "qtd_demandas", str(len(keys)))
        body = re.sub(r"^- \*\*Domínios:\*\* .*$", lambda _: "- **Domínios:** " + ", ".join(doms), body, count=1, flags=re.M)
        body = re.sub(r"^- \*\*Períodos:\*\* .*$", lambda _: "- **Períodos:** " + ", ".join(pers), body, count=1, flags=re.M)
        block = f"## Demandas ({len(keys)})\n\n" + "\n".join(item_line(k, items[k]) for k in keys) + "\n"
        m = re.search(r"^## Demandas \(\d+\)\n", body, flags=re.M)
        if m:
            nxt = re.search(r"^## ", body[m.end() :], flags=re.M)
            body = body[: m.start()] + block + (("\n" + body[m.end() + nxt.start() :]) if nxt else "")
        else:
            body = body.rstrip("\n") + "\n\n" + block
        write_note(path, fm, body)
    missing = sorted(e for e in by_epic if e and e not in epic_titles and e not in items)

    # _por-epico: epics ordered by their most recent item
    # an item can be its own epic (card without parent): use its own title
    for e in by_epic:
        if e and e not in epic_titles and e in items:
            epic_titles[e] = items[e]["titulo"]
    epics_sorted = sorted((e for e in by_epic if e in epic_titles), key=lambda e: max(items[k]["data_referencia"] or "" for k in by_epic[e]), reverse=True)
    blocks = []
    for e in epics_sorted:
        keys = sort_items(by_epic[e], items)
        blocks.append(f"## [[{e}]] — {epic_titles[e]} ({len(keys)})\n\n" + "\n".join(item_line(k, items[k]) for k in keys) + "\n")
    write_view(os.path.join(VAULT, "_por-epico.md"), blocks)

    # _por-periodo
    by_period = defaultdict(list)
    for k, it in items.items():
        by_period[it["periodo"]].append(k)
    blocks = []
    for p in sorted(by_period, reverse=True):
        keys = sort_items(by_period[p], items)
        blocks.append(f"## {p} ({len(keys)})\n\n" + "\n".join(item_line(k, items[k]) for k in keys) + "\n")
    write_view(os.path.join(VAULT, "_por-periodo.md"), blocks)

    # _por-dominio
    vocab = vocabulary()
    by_domain = defaultdict(list)
    for k, it in items.items():
        for d in it["dominio"]:
            by_domain[d].append(k)
    blocks = []
    for d in sorted(by_domain):
        keys = sort_items(by_domain[d], items)
        desc = f" — {vocab[d]}" if d in vocab else ""
        blocks.append(f"## {d}{desc} ({len(keys)})\n\n" + "\n".join(item_line(k, items[k]) for k in keys) + "\n")
    write_view(os.path.join(VAULT, "_por-dominio.md"), blocks)

    # numbers in _prds-indice.md
    counts = defaultdict(int)
    for it in items.values():
        counts[it["situacao"]] += 1
    order = ["pronto", "backlog", "arquivado", "resolvido-outro-dev", "esquecido"]
    sits = ", ".join(f"{s}: {counts[s]}" for s in order + sorted(set(counts) - set(order)) if counts[s])
    path = os.path.join(VAULT, "_prds-indice.md")
    text = open(path).read()
    numbers = f"## Números\n\n- {len(items)} demandas, {epic_notes} épicos\n- {sits}\n"
    m = re.search(r"^## Números\n", text, flags=re.M)
    if m:
        nxt = re.search(r"^## ", text[m.end() :], flags=re.M)
        text = text[: m.start()] + numbers + (("\n" + text[m.end() + nxt.start() :]) if nxt else "")
    else:
        text = text.rstrip("\n") + "\n\n" + numbers
    open(path, "w").write(text)

    print(f"{len(items)} demandas, {epic_notes} épicos; {sits}")
    if missing:
        print("Épicos citados em itens mas sem nota em epicos/: " + ", ".join(missing))


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("backlog", "apply", "rebuild"):
        print(__doc__)
        sys.exit(1)
    {"backlog": lambda: cmd_backlog(), "apply": lambda: cmd_apply(sys.argv[2]), "rebuild": lambda: cmd_rebuild()}[sys.argv[1]]()
