# Katala Research Agent Rules

Rules for coding agents working in this repository.

- Use `uv sync --locked --extra dev` for reproducible setup.
- Verify behavior with `scripts/verify.sh` before opening or updating a PR.
- Keep default verification offline and deterministic; do not add network-dependent tests to `scripts/verify.sh`.
- Do not run live API research, scraping, external retrieval, or session-materializing smoke flows unless the task explicitly asks for research execution.
- Keep API keys, `.env*`, user research preferences, raw session logs, downloaded source content, and generated research sessions out of commits.
- Preserve `SKILL.md` as the local workflow entrypoint for Katala Research domain behavior.
