---
name: mcp-escopos-e-ram
description: Desabilitar um MCP pelo /mcp vale só para o projeto atual; cada sessão sobe o próprio servidor (o sonarqube-mcp é um container Docker com JVM de 400-700 MB)
metadata:
  type: reference
---

# Escopos de MCP e consumo de RAM

- Os MCPs de escopo **user** ficam em `mcpServers` na raiz de `~/.claude.json` e valem para qualquer pasta. Os de escopo **local** ficam em `projects["<pasta>"].mcpServers`, e o `.mcp.json` do repo é o escopo **project**.
- Desabilitar pelo `/mcp` só grava `projects["<pasta>"].disabledMcpServers`, ou seja, vale só para aquela pasta. Para tirar de tudo: `claude mcp remove <nome> -s user`.
- Cada sessão do Claude sobe a própria instância do servidor. O `sonarqube` (`sonar run mcp` → `docker run --rm sonarsource/sonarqube-mcp`) é uma JVM de 400-700 MB por sessão. Com 4 sessões abertas, isso passa de 2,5 GB.
- Mudar a configuração não afeta sessões já abertas: o servidor só sai quando a sessão é reiniciada ou desligada pelo `/mcp`. Para liberar a RAM na hora, use `docker ps --filter ancestor=sonarsource/sonarqube-mcp` e depois `docker stop <id>`, um por vez. Com vários ids no mesmo comando, o daemon devolveu `page not found`.
- Em 2026-11-18, o `sonarqube` foi removido do escopo user. Quem depende dele é o prompt de auto-resolve da pipeline do BahCode (`dotfiles/.config/bahcode/prompts/mrs/auto-reviewer/pipeline/auto-resolve.md`, que usa as ferramentas `mcp__sonarqube__*`). Sem o MCP, falhas de quality gate voltam com `done false`.
