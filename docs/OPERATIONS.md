# Operations

## Daily arXiv ingest

```bash
uv run --project . python scripts/arxiv_daily_ingest.py
```

Suggested cron (documented in the script's own docstring, formalized here):

```
0 6 * * * KATALA_RESEARCH_ROOT=/path/to/katala-research \
          /usr/local/bin/uv run --project $KATALA_RESEARCH_ROOT \
          python $KATALA_RESEARCH_ROOT/scripts/arxiv_daily_ingest.py
```

Optional flags: `--categories cs.LG q-bio.QM econ.GN`, `--max-per-category 30`,
`--queries "deep research,personalization"`.

Output: `$KATALA_SESSIONS_DIR/inbox/arxiv-YYYYMMDD.jsonl` — one file per day.

## Incident Response

| Symptom | Likely cause | Action |
|---|---|---|
| No `arxiv-YYYYMMDD.jsonl` appears for a given day | Cron didn't fire, or arXiv API was unreachable | Re-run the script manually with the same flags; check for a stack trace before assuming a silent no-op |
| Ingest output is empty or near-empty | `--categories`/`--queries` filters too narrow, or arXiv had a low-volume day for those categories | Verify with a broader `--categories` run before treating it as a bug |
| Downstream research pipeline (Gate → Hydrator → Filter → Scorer → Selector) produces a low-diversity result set | Per `README.md`, the Selector enforces a ≥25% creativity floor, ≤40% per-domain, ≤50% per-paradigm — a violation here is a scoring-layer bug, not an ingest issue | Check `GapScore`/Reflection output first; it should auto-spawn a far query when coverage is too narrow |

## Retention

`$KATALA_SESSIONS_DIR/inbox/*.jsonl` has no declared retention rule — each daily
run adds one file with no prune step. Recommend a max-age policy (e.g. 180 days,
matching the arXiv-recency window most queries care about) once volume becomes a
concern.
