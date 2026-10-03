# Katala Research Current State

- Updated: 2026-10-03 UTC
- Repo: `katala-research` (this repository)
- Purpose: Anti-filter-bubble deep-research agent with creativity-aware scoring.

## Reproducibility

- Repo task contract: `AGENTS.md`.
- Python runtime: `.python-version` pins `3.11`, matching `pyproject.toml` `requires-python >=3.11`.
- Dependency lock: `uv.lock`.
- Install: `uv sync --locked --extra dev`.
- Verify: `scripts/verify.sh`.

## CI

- GitHub Actions entrypoint: `.github/workflows/ci.yml`.
- CI pins actions to immutable commit SHAs:
  - `actions/checkout`: `3d3c42e5aac5ba805825da76410c181273ba90b1` (v7.0.1).
  - `actions/setup-python`: `5fda3b95a4ea91299a34e894583c3862153e4b97` (v7.0.0).
  - `astral-sh/setup-uv`: `11f9893b081a58869d3b5fccaea48c9e9e46f990` (v8.3.2).
- CI resolves Python from `.python-version`, dependencies from `uv.lock`, then runs `scripts/verify.sh`.
- Workflow drift is covered by `tests/test_ci_workflows.py`.

## Operational Boundary

- `scripts/verify.sh` runs the local pytest suite only.
- Live API research, scraping, and session-materializing smoke flows are outside default verification.
- Stub/live research runs can create session output under `$KATALA_SESSIONS_DIR` or `~/.local/share/katala-research/sessions/`; run them only when explicitly required.

## Historical Local Verification (2026-06-29 JST)

- `uv sync --locked --extra dev`: passed on 2026-06-29 JST.
- `uv run --locked --extra dev pytest -q`: `154 passed`.
- `uv run --locked kr run --stub "test query"`: passed; created a local session artifact outside this repo.
