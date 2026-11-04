---
name: html-to-pdf-smoke-test-dev
description: "Como testar o html-to-pdf no Cloud Run de dev com uma requisição autenticada, e por que o status 200 sozinho não prova que funcionou"
metadata:
  type: reference
tags:
  - html-to-pdf
---

# Smoke test do html-to-pdf em dev

O serviço tem uma rota só: `POST /`, que recebe o HTML no body e devolve `application/pdf` (`main.go`). Em dev ele roda no Cloud Run `html-to-pdf` do projeto `contabilizei-experts-dev` (URL `https://html-to-pdf-uzyfdfmsca-uc.a.run.app`). O serviço não aceita chamada sem autenticação: requisição sem token volta 403 no Cloud Run, sem chegar ao container.

```bash
T=$(gcloud auth print-identity-token)
curl -s -o smoke.pdf -w 'status=%{http_code} bytes=%{size_download}\n' -X POST -H "Authorization: Bearer $T" -H 'Content-Type: text/html' --data '<html><body><h1>Smoke test</h1></body></html>' https://html-to-pdf-uzyfdfmsca-uc.a.run.app/
file smoke.pdf   # esperado: PDF document, version 1.4, 1 page(s)
```

**Armadilha:** o handler ignora os erros (de `ReadAll`, `GeneratePDF` e `ReadFile`) e sempre responde 200, mesmo quando o `wkhtmltopdf` falha. Para validar, conferir que o body começa com `%PDF` e tem tamanho maior que zero, não só o status.

Em dev o serviço quase não recebe tráfego real: em outubro de 2026, os logs de 30 dias só tinham 403 de scanners (`/.env`, `/swagger`, `/mcp` etc.). Então, depois de um deploy, a validação é o smoke test acima, não o tráfego. Em 2026-10-30, a revisão `html-to-pdf-00005-rfb` (gen2) respondeu 200 com um PDF válido de 13.595 bytes em ~1,9 s.
