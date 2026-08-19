# GitHub Actions and uv CI Evidence

- Retrieved: 2026-06-29 JST
- Repo: `katala-research` (this repository)
- Local uv: `uv 0.11.23 (Homebrew 2026-06-19 aarch64-apple-darwin)`

## Sources

- `https://github.com/actions/checkout`
- `https://github.com/actions/setup-python`
- `https://docs.astral.sh/uv/guides/integration/github/`
- `https://github.com/astral-sh/setup-uv`

## Decision

- Use `actions/checkout@v7`.
- Use `actions/setup-python@v6` with `python-version-file: ".python-version"`.
- Use `astral-sh/setup-uv@v8` with cache enabled for `pyproject.toml` and `uv.lock`.
- Use `uv sync --locked --extra dev`, then `scripts/verify.sh`.

## Verification Commands

```bash
uv sync --locked --extra dev
scripts/verify.sh
uv run --locked --extra dev pytest tests/test_ci_workflows.py -q
git diff --check
```

## Risk

- CI behavior follows the current major versions of official actions. If a major action release changes behavior, refresh this evidence and rerun `tests/test_ci_workflows.py`.
- `scripts/verify.sh` intentionally excludes live API, scraping, and session-materializing research runs from default verification.

## Rollback

- Remove `.github/workflows/ci.yml`, `.python-version`, `scripts/verify.sh`, `tests/test_ci_workflows.py`, and the docs added with this packet.
- Restore README/CONTRIBUTING/SKILL/CHANGELOG text from git.
