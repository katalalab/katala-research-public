# Contributing to Katala Research

## Setup

Requires Python ≥ 3.11 and [uv](https://github.com/astral-sh/uv).

```bash
git clone <repo-url> katala-research && cd katala-research
uv sync --locked --extra dev
cp examples/research-prefs.example.yaml ~/.agents/research-prefs.yaml
# Edit ~/.agents/research-prefs.yaml — set llm-default to a valid Anthropic model.
```

## Optional dependencies

```bash
uv sync --extra embed   # sentence-transformers (local embedding)
uv sync --extra scrape  # scrapling + pypdf (web scraping + PDF extraction)
```

## Canonical test command

```bash
scripts/verify.sh
```

Expected: 154 passing. `scripts/verify.sh` requires `uv` and runs
`uv run --locked --extra dev pytest -q` so local and CI verification use the
same lockfile-backed dependency set.

## Env vars

Copy `.env.example` to `.env` and fill in keys you need. The only key
required for live runs is `ANTHROPIC_API_KEY`. Stub mode (`--stub`) works
with no keys set.

## Code style

- Match existing naming and formatting conventions.
- Comments explain WHY only — not what the code does.
- No speculative error handling or fallback for library-internal errors.
- Do not mix bug fixes with refactors in the same commit.

## llm-default model id

`llm-default` in `src/katala_research/config.py` and
`examples/research-prefs.example.yaml` must be a currently-valid Anthropic
model id. Update it when the model used in development changes. The comment
in both files marks the field as subject to this update.
