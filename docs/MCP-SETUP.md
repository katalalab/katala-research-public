# MCP setup — playwright-mcp & related

Katala Research v0.1 does not itself ship an MCP server. But several **read /
search** primitives can be exposed to Claude Code / Codex CLI / Cursor as MCP
servers. The most impactful is **microsoft/playwright-mcp** — when the user asks
"go check this in a real browser", Claude can drive it without leaving the chat.

## microsoft/playwright-mcp

### What it gives you

A Playwright instance exposed over MCP, with tools for navigation, click, type,
screenshot, evaluate JS. Use cases:

- Auth-walled / login-required research targets
- JS-heavy SPAs where Jina Reader returns empty
- Verifying live UI claims found in scraped text
- Filling in forms during structured research (rare)

### Install (per-host)

```bash
# Claude Code
claude mcp add playwright npx -- --yes @playwright/mcp@latest

# Codex CLI
codex mcp add playwright npx -- --yes @playwright/mcp@latest

# Cursor / Windsurf: edit ~/.cursor/mcp.json or settings UI
```

Verify:
```bash
claude mcp list | grep playwright
codex mcp list | grep playwright
```

### Evidence to record

Before registering the server, record the following somewhere durable:

- source URL: https://github.com/microsoft/playwright-mcp
- retrieval date: 2026-05-18
- version: latest npm tag (npx pulls fresh each run)
- decision: register locally
- verification command: `claude mcp list | grep playwright`
- risk: ToS / target sites — same as any browser automation. Use only on
  sites you'd manually visit, never to bypass paywalls
- rollback: `claude mcp remove playwright`
- next refresh: 2026-08-18

### Permission posture

Browser automation is permission-sensitive. Default to **opt-in per session** —
do NOT add to global auto-allow. When Katala Research wants to use it, the
agent should ask for confirmation before invoking.

## Other research-adjacent MCPs to consider

| MCP | Use for | Install |
|---|---|---|
| `openaiDeveloperDocs` | Official OpenAI behavior queries | already configured |
| `mcpdoc` | Generic doc-source MCP | already configured |
| `ihor-sokoliuk/mcp-searxng` | SearXNG → MCP wrapper | `claude mcp add searxng npx -- --yes mcp-searxng` |
| `openags/paper-search-mcp` | arXiv + PubMed + bioRxiv + 17 more academic sources | `pip install paper-search-mcp && claude mcp add paper-search ...` |
| `Asta MCP` | Semantic Scholar 200M+ index | HTTPS endpoint with `x-api-key`, see asta-skill |

## Not auto-installing

Per the user's CLAUDE.md "permission-sensitive areas require explicit user
intent" rule, this doc does NOT auto-run the install commands. Confirm the
list, then run them yourself (or paste back if you want me to run them with
your explicit go-ahead).
