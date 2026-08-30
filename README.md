# Katala Research v0

Anti-filter-bubble deep-research agent. Ranks candidates with a diversity-aware `Score(z)` instead of pure preference-following, and runs them through a `Source → Hydrator → Filter → Scorer → Selector → SideEffect` pipeline.

Docs:
- [docs/OPERATIONS.md](docs/OPERATIONS.md) — operations and incident response
- [docs/godproof.md](docs/godproof.md) — the `kr godproof` proof-frontier mode
- [NOTICE](NOTICE) — third-party attribution

## Why

Pure preference-following turns research into an echo chamber. v0 makes anti-bubble a **structural** property:

- **Gate** rejects candidates that aren't on-brief / can't be translated / can't be adopted
- **Scorer** = `α·Relevance + β·Discovery − γ·Risk` (β = 0.35 default; discovery is not optional)
- **Selector** enforces ≥25% creativity floor, ≤40% per-domain, ≤50% per-paradigm, ≥1 counter-evidence slot
- **Reflection** computes `GapScore` and **must** spawn a far query if coverage is too narrow

## Quickstart

```bash
git clone <repo-url> katala-research && cd katala-research
uv sync --locked --extra dev                              # install reproducible dev deps
scripts/verify.sh                                         # local verification
uv run kr config                                           # show resolved prefs
uv run kr run --stub "test query"                          # smoke test, no external services
uv run kr run "What is the state of MCP servers in 2026?"  # real run (needs ANTHROPIC_API_KEY, SearXNG up)
uv run kr bench --tasks 5                                  # run DRB-5 smoke
uv run kr godproof                                         # local God-proof frontier + full logs
```

## Architecture

```
Source → Hydrator → Filter → Scorer → Selector → SideEffect
  ↑          ↓         ↓        ↓         ↓           ↓
SERP gen   fetch    Gates    Score(z)   diversity  ledger
+ counter  +clean  reject   +ranking   floor+caps  +reflect
```

- **Pipeline shape**: borrowed from the x-algorithm personal-info-feed project
- **Creativity scoring**: own formulation; each axis derived from published diversity/novelty/attribution evaluation work — see [NOTICE](NOTICE) and the docstrings in `src/katala_research/creativity/`
- **Iterative strategy**: distilled from [dzhng/deep-research](https://github.com/dzhng/deep-research) (MIT)

`vendor/deep-research/` and `vendor/searxng-docker/` are referenced by some docs
but are **not** bundled here. Clone them yourself if you want to compare:

```bash
git clone https://github.com/dzhng/deep-research vendor/deep-research
git clone https://github.com/searxng/searxng-docker vendor/searxng-docker
```

## Config

Default config: `examples/research-prefs.example.yaml`.
User config: `~/.agents/research-prefs.yaml` (created on first run if missing).

## Out of scope (v0)

- supervisor / answer / wiki strategies (only iterative)
- web UI
- vector DB / RAG
- preference learning / RL
- multi-tenant / auth
- MCP server wrapper (later)

## Sessions

Each run writes `$KATALA_SESSIONS_DIR/<ts>-<slug>/` (default: `~/.local/share/katala-research/sessions/`):
- `brief.md` — clarified brief
- `plan.md` — research plan
- `learnings.jsonl` — extracted learnings with scores
- `sources.jsonl` — visited URLs with scores
- `scores.jsonl` — full Score(z) breakdown per candidate
- `gates-rejected.jsonl` — candidates rejected by Gate (debug)
- `report.md` — final report with citations
- `prefs-used.yaml` — snapshot of effective prefs
- `transcript.jsonl` — full event log

`kr godproof` is a local-only proof-frontier mode: it records which premises,
counterarguments, and unsatisfied gates stand between the classical arguments for
the existence of God and a formal proof. It does not claim that God is proven.
See [docs/godproof.md](docs/godproof.md) for its ~40 output files.

## License

MIT.

- [Contributing](CONTRIBUTING.md)

- [Changes and releases](CHANGELOG.md)

- [Lifecycle](CHANGELOG.md)

- [Automation](.github/workflows/)

- [Repository hygiene](.gitignore)
