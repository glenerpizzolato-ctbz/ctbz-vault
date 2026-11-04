---
name: cloud-run-gen2-container-threat-detection
description: "Deploy no Cloud Run falha com INVALID_ARGUMENT 'Container threat detection ... requires the gen2 execution environment': o projeto passou a exigir gen2 e o serviço ainda está em gen1"
metadata:
  type: reference
tags:
  - infra
  - cloud-run
  - deploy
---

# Cloud Run: Container Threat Detection exige gen2

Sintoma no job `cloudrun-deploy-*` (component `ctbz/devops/recursos/pipeline/ci-cd`):

```
ERROR: (gcloud.run.deploy) INVALID_ARGUMENT: Container threat detection is enabled in <projeto> requires the gen2 execution environment. This Service is using gen1 execution environment, and modifying it would result in a new Revision being created.
```

Causa: o Security Command Center ligou o Container Threat Detection no projeto GCP (visto em `contabilizei-experts-dev` em 2026-10-30), e com ele o Cloud Run recusa qualquer revisão nova em `gen1`. Não é problema do código do MR, nem intermitente: retry não resolve.

Correção: trocar `EXECUTION_ENVIRONMENT: gen1` para `gen2` na config do serviço no repositório `pipeline` (`~/repositories/pipeline/custom/ctbz/<dominio>/.../<servico>.<env>.yml`; o default do `custom/ctbz.yml` já é `gen2`). O gen2 exige no mínimo 512Mi de memória e CPU fracionada (< 1) é só do gen1, então serviços com `CPU: 0.2`/`MEMORY: 128Mi` precisam subir também para `CPU: 1` e `MEMORY: 512Mi` (ou mais).

Conferir o ambiente atual do serviço: `gcloud run services describe <servico> --project <projeto> --region us-central1 --format='value(spec.template.metadata.annotations)'` (anotação `run.googleapis.com/execution-environment`).

Mínimos confirmados na doc do Cloud Run em 2026-10-30: "The second generation execution environment requires at least 512 MiB of memory" e, para CPU < 1, "You must use the first generation execution environment".

Casos: [[_html-to-pdf-indice|html-to-pdf]] (dev, 2026-10-30, job 17621904604; corrigido em dev e prd no pipeline!3282).

Depois do merge no `pipeline`, não dar retry no job que falhou: a config do `custom/` entra quando a pipeline é criada, então o retry provavelmente repetiria o gen1 (não testado). Criar uma pipeline nova na tag (`glab ci run -R <repo> -b <tag>`). No html-to-pdf, a pipeline nova da tag `0.0.4` (#3010578280) subiu a revisão `html-to-pdf-00005-rfb` em gen2.
