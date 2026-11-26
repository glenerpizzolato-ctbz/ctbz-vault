---
name: sdk-zaf-versao-fixa-sri
description: "O <script> do SDK do ZAF no iframe.html vira security hotspot no Sonar (Web:S5725, sem integrity) e trava o gate em new_security_hotspots_reviewed; correção: URL de versão fixa (2.0.37) com integrity sha384 e crossorigin"
metadata:
  type: reference
tags:
  - zendesk-apps
  - sonar
  - seguranca
criado_em: 2026-11-26
---

# SDK do ZAF com versão fixa e SRI

**Sintoma:** o quality gate do MR cai em `new_security_hotspots_reviewed < 100` com o hotspot `Web:S5725` ("Make sure not using resource integrity feature is safe here") no `<script src="https://static.zdassets.com/zendesk_app_framework_sdk/2.0/zaf_sdk.min.js">` do `iframe.html`. Marcar o hotspot como Safe exige permissão de administrar hotspots no projeto (devs não têm: "Insufficient privileges").

**Por que não dá hash na URL `2.0`:** a Zendesk atualiza esse arquivo sem mudar a URL (em 2026-11 ela servia um build de 2023 que se declara 2.0.37, diferente do arquivo fixo `2.0.37`, de 2022). Um `integrity` fixo quebraria o app na próxima atualização. O pacote npm `zendesk_app_framework_sdk` está parado na 2.0.11 (2022).

**Correção (zendeskapp-warnings-and-messages, 2026-11-26):** usar a URL com versão fixa, que não muda, com SRI. O CDN manda `access-control-allow-origin: *`, então o `crossorigin="anonymous"` funciona.

```html
<script
  src="https://static.zdassets.com/zendesk_app_framework_sdk/2.0.37/zaf_sdk.min.js"
  integrity="sha384-9EPbYTFD7Oxlnn4s2sg+mfMtqdTzc1mWRudXMR1EBd9dsUlyuDab2OvDWf0Jolsy"
  crossorigin="anonymous"
></script>
```

Hash de outra versão: `curl -s https://static.zdassets.com/zendesk_app_framework_sdk/<versão>/zaf_sdk.min.js | openssl dgst -sha384 -binary | openssl base64 -A`. As versões fixas publicadas vão até a 2.0.37 (a 2.0.38+ dá 404).

Conferir antes do push: `sonar analyze --file src/iframe.html` (CLI do SonarQube, ver [[sonar-new-violations-todo-portugues]]).

Os apps antigos (whatsapp-ativo e outros) ainda usam `assets.zendesk.com/apps/sdk/2.0/zaf_sdk.js` sem SRI; o hotspot não aparece neles porque o código não é novo no MR.
