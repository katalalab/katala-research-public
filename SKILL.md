---
name: katala-research
description: Anti-filter-bubble deep-research agent. Use when the user asks for in-depth research, literature review, fact synthesis, or a cited report — especially when they want creative/contrarian sources mixed in, not just preference-confirming ones. Wraps a creativity-aware Scorer (Score = α·Relevance + β·Discovery − γ·Risk) and an x-algorithm-style Selector that enforces a 25% creativity floor + domain/paradigm diversity caps + mandatory counter-evidence.
license: MIT
homepage: https://github.com/Nicolas0315/katala-research
metadata:
  version: 0.1.0
  origin: local
  related_skills:
    - academic-deep-research
    - openalex-search
    - asta-skill
    - defuddle
---

# Katala Research

Anti-filter-bubble deep-research agent for the Katala OS fleet.

## When to invoke

- "リサーチして" / "深掘りして" / "deep research" / "literature review" / "competitive intel"
- Any time the user wants a cited report, not just a single answer
- Especially when they say "新しい発見" / "discovery" / "creative angle" / "contrarian view"

## When NOT to invoke

- Quick fact check → use Anthropic `web_search` directly
- "URL を読んで" → use `defuddle` skill directly
- Academic-only with APA citations → prefer `academic-deep-research` skill
- Lead/company enrichment → use `composio--lead-research-assistant`

## How

```bash
uv sync --locked --extra dev      # reproducible local setup
scripts/verify.sh                 # local verifier
uv run kr run "<query>"           # full research session
uv run kr run --stub "<query>"    # smoke, no external services
uv run kr bench --tasks 5         # DRB-5 + creativity rubric
uv run kr config                  # show resolved prefs
```

## Configuration

User-level: `~/.agents/research-prefs.yaml` (created from `examples/research-prefs.example.yaml` on first run).

Key knobs (all overridable per-session via CLI flags):
- `default-breadth`, `default-depth`
- `creativity.weights.{relevance,discovery,risk}` (α=0.50, β=0.35, γ=0.15 default)
- `creativity.selector.discovery_floor_ratio` (default 0.25)
- `preferred-sources`, `banned-domains`

## Output

`$KATALA_SESSIONS_DIR/<ts>-<slug>/` with brief, plan, learnings, scores, gates-rejected, report.

## References

- [README.md](README.md) — architecture and the Score / Selector formulas
- [NOTICE](NOTICE) — third-party attribution, and the literature the creativity
  axes are derived from
