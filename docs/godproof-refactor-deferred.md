# godproof.py — Data Extraction Deferred

`src/katala_research/godproof.py` is ~1.1 MB / 23 407 lines. The bulk is 69
top-level data variables (SOURCES, PREMISES, ARGUMENTS, COUNTERARGUMENTS,
WISDOM_CORPUS, and ~60 audit/model/ledger dicts) plus 245 builder functions
that reference them by module-level name.

## Why the refactor was deferred

1. **Entanglement**: every builder function references the global data
   constants by name (`METAPHYSICAL_POSSIBILITY_BRIDGE`, `SOURCES`, etc.).
   Moving data to JSON/YAML requires either keeping module-level aliases or
   rewriting all 245 callsites — both are non-trivial.

2. **Dataclass constructors**: `SOURCES` is a list of `Source(id=..., ...)` calls,
   not plain dicts. Extracting to JSON works but `Source.as_dict()` must be
   replaced by a factory loader, touching both the data file and every consumer.

3. **Test coverage is high but narrow**: `test_godproof` has 100+ tests that
   check the *output* JSON artifacts. They do not catch regressions in the
   intermediate data constants, so a silent data-round-trip bug could pass
   all tests while corrupting the philosophical argument graph.

4. **Risk/reward**: the file is never shipped to end-users (it is a
   development-time proof kernel). Splitting it saves no runtime overhead
   because Python already compiles it to bytecode.

## Recommended future approach

If the file continues to grow past ~2 MB:

1. Extract each top-level data dict/list to `src/katala_research/godproof_data/*.json`.
2. Add a thin `_load_data(name)` loader at module top.
3. Replace each `CONSTANT = {...}` with `CONSTANT = _load_data("constant")`.
4. Where SOURCES uses dataclass constructors, keep them — just load the raw
   list from JSON and instantiate inside a `_load_sources()` helper.
5. Run `uv run pytest tests/test_godproof.py -v` as the acceptance gate.

Do not attempt this refactor under time pressure or without a full test run
as the baseline.
