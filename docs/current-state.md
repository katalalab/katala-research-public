# Katala Research Current State

- Updated: 2026-10-10 JST
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
  - `astral-sh/setup-uv`: `c18668ad3cf93ea998bef934396af7bb5c839dc7` (v10.2.0).
- Pull requests run verification once; push verification targets `main` to avoid
  duplicate checks on feature branches.
- Optional dependency minimums and the lockfile use `sentence-transformers` 5.6.0
  and `pypdf` 6.19.0 to address the currently reported security advisories.
- The optional embedding dependency tree also locks `fsspec` to 2026.6.0;
  the exported dependency set passes `pip-audit` without installing model weights.
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
