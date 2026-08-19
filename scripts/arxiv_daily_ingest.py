#!/usr/bin/env python3
"""Daily arXiv ingester — drops a JSONL into $KATALA_SESSIONS_DIR/inbox/.

Cron suggestion (every morning at 6am):
  0 6 * * * KATALA_RESEARCH_ROOT=/path/to/katala-research \
            /usr/local/bin/uv run --project $KATALA_RESEARCH_ROOT \
            python $KATALA_RESEARCH_ROOT/scripts/arxiv_daily_ingest.py

Optional CLI flags:
  --categories cs.LG q-bio.QM econ.GN     restrict
  --max-per-category 30                   limit per category
  --queries "deep research,personalization"   bias queries

Output: $KATALA_SESSIONS_DIR/inbox/arxiv-YYYYMMDD.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Make src/ importable when run directly.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from katala_research.sources.arxiv import ArxivSource  # noqa: E402
from katala_research.sources.inbox import DEFAULT_INBOX  # noqa: E402


DEFAULT_CATEGORIES = ["cs.LG", "cs.IR", "cs.CL", "stat.ML", "q-bio.QM",
                      "q-fin.GN", "econ.GN", "econ.EM"]
DEFAULT_QUERIES = [
    "deep research agent",
    "retrieval augmented generation",
    "filter bubble diversity",
    "personalization recommendation",
    "scientific literature analysis",
]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--categories", nargs="*", default=DEFAULT_CATEGORIES)
    p.add_argument("--queries", nargs="*", default=DEFAULT_QUERIES)
    p.add_argument("--max-per-query", type=int, default=10)
    p.add_argument("--inbox", type=Path, default=DEFAULT_INBOX)
    args = p.parse_args()

    args.inbox.mkdir(parents=True, exist_ok=True)
    out_file = args.inbox / f"arxiv-{datetime.now():%Y%m%d}.jsonl"

    source = ArxivSource(categories=[f"{c}" for c in args.categories])
    seen_urls: set[str] = set()
    n_written = 0
    with open(out_file, "a", encoding="utf-8") as f:
        for q in args.queries:
            hits = source.search(q, limit=args.max_per_query)
            for h in hits:
                if h.url in seen_urls:
                    continue
                seen_urls.add(h.url)
                f.write(json.dumps({
                    "url": h.url,
                    "title": h.title,
                    "snippet": h.snippet,
                    "meta": h.meta.model_dump(),
                    "ts": datetime.now().isoformat(),
                    "ingest_query": q,
                }, ensure_ascii=False) + "\n")
                n_written += 1

    print(f"[arxiv-ingest] wrote {n_written} entries to {out_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
