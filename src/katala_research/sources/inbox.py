"""InboxSource — read pre-ingested Candidates from $KATALA_SESSIONS_DIR/inbox/.

Pattern: cron jobs (e.g., arxiv_daily_ingest.py) write JSONL files into the inbox;
the orchestrator's Source stage picks them up so they don't have to be fetched
live each time. This keeps research sessions fast even when broad surveying.

JSONL line format (one SearchHit-equivalent per line):
  {"url": "...", "title": "...", "snippet": "...", "meta": {...}, "ts": "..."}
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from ..types import CandidateMeta, SearchHit


DEFAULT_INBOX = Path.home() / "work" / "research" / "sessions" / "inbox"


class InboxSource:
    """Read recently-ingested candidates from the local inbox.

    Not a true "search" — returns whatever was pre-ingested. The orchestrator
    can score / select them like any other Source's hits.
    """

    name = "inbox"
    peer_review_default = None  # depends on each entry
    domain_tags = ["cs", "q-bio", "q-fin", "econ", "stat", "med", "social", "web"]

    def __init__(self, inbox_dir: Optional[Path] = None, max_age_days: int = 7):
        self.inbox_dir = Path(inbox_dir) if inbox_dir else DEFAULT_INBOX
        self.max_age_days = max_age_days

    def search(self, query: str, *, limit: int = 10) -> list[SearchHit]:
        """Returns up to `limit` entries from recent inbox files.

        v0.1: returns inbox entries unfiltered. v0.2 could rerank by query similarity.
        """
        if not self.inbox_dir.exists():
            return []
        cutoff = datetime.now() - timedelta(days=self.max_age_days)
        candidates: list[SearchHit] = []
        for path in sorted(self.inbox_dir.glob("*.jsonl"), reverse=True):
            try:
                mtime = datetime.fromtimestamp(path.stat().st_mtime)
            except OSError:
                continue
            if mtime < cutoff:
                continue
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                hit = self._entry_to_hit(entry, rank=len(candidates))
                if hit:
                    candidates.append(hit)
                if len(candidates) >= limit:
                    return candidates
        return candidates

    def _entry_to_hit(self, entry: dict, *, rank: int) -> Optional[SearchHit]:
        url = entry.get("url")
        if not url:
            return None
        meta_raw = entry.get("meta") or {}
        try:
            meta = CandidateMeta.model_validate(meta_raw)
        except Exception:
            meta = CandidateMeta()
        return SearchHit(
            url=url,
            title=entry.get("title", ""),
            snippet=entry.get("snippet", ""),
            rank=rank,
            backend=self.name,
            meta=meta,
        )
