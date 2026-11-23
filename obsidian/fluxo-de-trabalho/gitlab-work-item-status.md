---
name: gitlab-work-item-status
description: "Mover um work-item do GitLab (ctbz) entre To do / In progress / Done: é o widget STATUS via GraphQL, não label nem glab issue update"
metadata:
  type: reference
tags:
  - gitlab
  - work-items
---

# Status de work-item no GitLab

Os projetos ctbz não têm label de workflow. O estado do work-item ("To do", "In progress", "Done") é o widget `STATUS`, que só se altera por GraphQL (`glab issue update` não alcança).

Ler o gid e o status atual:

```sh
glab api graphql -f query='query { namespace(fullPath: "<grupo>/<projeto>") {
  workItem(iid: "<iid>") { id widgets { ... on WorkItemWidgetStatus { status { id name } } } } } }'
```

Alterar (ex: In progress):

```sh
glab api graphql -f query='mutation { workItemUpdate(input: {
  id: "gid://gitlab/WorkItem/<id>",
  statusWidget: { status: "gid://gitlab/WorkItems::Statuses::SystemDefined::Status/2" }
}) { errors workItem { widgets { ... on WorkItemWidgetStatus { status { name } } } } } }'
```

IDs system-defined: 1=To do, 2=In progress, 3=Done, 4=Won't do, 5=Duplicate.

No BahCode, "passar para building" um work-item ligado a um sub-terminal (skill `link-work-item`) é mover para In progress assim; o Done vem do merge (o app fecha o work-item citado com `Closes`).
