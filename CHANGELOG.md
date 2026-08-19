# Changelog

## [Unreleased]

### Added
- `.python-version`, `scripts/verify.sh`, GitHub Actions CI, PR template, docs
  index/current-state, and workflow drift tests for reproducible verification.
- `AGENTS.md` with repo-specific verification and live-research boundaries.
- LICENSE file (MIT, matching pyproject.toml declaration).
- CONTRIBUTING.md with uv setup, optional deps, and canonical test command.
- CHANGELOG.md (this file).
- Tests covering the report rubric's shape, normalization, verdict bands, and
  clamping of out-of-range judge scores.
- `docs/godproof-refactor-deferred.md` documenting why godproof.py data
  extraction was deferred and the recommended future approach.
- `.gitignore` `**/bench/results/` rule so nested bench result files are
  ignored regardless of nesting depth.
- Standalone `git init` at repo root; the repo is now a self-contained local
  git repository (no remote).

### Changed
- Creativity scoring re-formulated from published evaluation work (subtopic
  recall, novelty/redundancy detection, intra-list and viewpoint diversity,
  attribution, situational relevance, combinational creativity, Grice's maxim of
  quantity). The report rubric's eight axes and the candidate `Score(z)`
  sub-terms are named and defined after those concepts, and NOTICE lists the
  citations. Score ranges, weights, gate semantics, and composite arithmetic
  are unchanged.
- Deleted stale `.venv` (shebang pointed to a previous checkout path); recreated
  with `uv sync` so `uv run pytest` works without `--no-project`.
- `scripts/arxiv_daily_ingest.py` cron comment: replaced hardcoded absolute
  paths with `$KATALA_RESEARCH_ROOT` env-var references.
- `SKILL.md` homepage field: replaced local absolute path with a portable URL
  placeholder.
- `README.md` quickstart `cd` line and architecture comments: replaced
  hardcoded absolute paths with portable references.
- `src/katala_research/config.py` `llm_default`: updated from non-existent
  `claude-opus-4-7` to `claude-opus-4-5`; added comment that this should be
  updated as models evolve.
- `examples/research-prefs.example.yaml` `llm-default`: same correction plus
  explanatory comment.

### Removed
- `src/katala_research/bench/results/bench-20260518-155606.json` (run
  artifact, regenerable).
- `src/katala_research/bench/results/bench-20260518-155750.json` (run
  artifact, regenerable).

## [0.1.0] — 2026-05

Initial release of the anti-filter-bubble deep-research agent.

- Source → Hydrator → Filter → Scorer → Selector → SideEffect pipeline.
- Creativity scoring (`α·Relevance + β·Discovery − γ·Risk`).
- x-axis diversity selector with 25 % creativity floor, domain/paradigm caps,
  mandatory counter-evidence slot.
- God-proof frontier kernel (`godproof.py`).
- DRB-5 benchmark runner.
- ArXiv daily ingester script.
- 154-test suite covering config, creativity, pipeline, selector, smoke, and
  godproof.
