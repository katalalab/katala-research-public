# Katala Research Docs

Start here:

- `../README.md` - product overview and local usage
- `../AGENTS.md` - repo-specific agent rules and live-research boundary
- `../SKILL.md` - agent skill contract
- `current-state.md` - repository health, CI, reproducibility, and boundaries
- `MCP-SETUP.md` - optional MCP setup notes
- `godproof-refactor-deferred.md` - deferred refactor rationale

Verification:

- Runtime pin: `.python-version` (`3.11`)
- Dependency lock: `uv.lock`
- Local verifier: `scripts/verify.sh`
- CI verifier: `.github/workflows/ci.yml`

Boundaries:

- Default verification does not run live API research, scraping, or session-materializing smoke flows.
- Live research requires explicit operator intent and configured external credentials.
