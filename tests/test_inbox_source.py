"""InboxSource reads pre-ingested JSONL entries."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from katala_research.sources.inbox import InboxSource


def test_reads_recent_jsonl_entries(tmp_path: Path):
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    entries = [
        {"url": "https://arxiv.org/abs/2503.00001", "title": "Paper A",
         "snippet": "snippet a",
         "meta": {"peer_reviewed": False, "venue": "arXiv:cs.LG",
                  "domain_tag": "cs", "source_type": "preprint"}},
        {"url": "https://arxiv.org/abs/2503.00002", "title": "Paper B",
         "snippet": "snippet b",
         "meta": {"peer_reviewed": False, "venue": "arXiv:q-bio.QM",
                  "domain_tag": "q-bio", "source_type": "preprint"}},
    ]
    f = inbox / f"arxiv-{datetime.now():%Y%m%d}.jsonl"
    f.write_text("\n".join(json.dumps(e) for e in entries), encoding="utf-8")

    source = InboxSource(inbox_dir=inbox)
    hits = source.search("anything", limit=5)
    assert len(hits) == 2
    assert all(h.backend == "inbox" for h in hits)
    assert hits[0].meta.peer_reviewed is False
    assert hits[0].meta.venue == "arXiv:cs.LG"
    assert hits[0].meta.domain_tag == "cs"


def test_returns_empty_when_inbox_missing(tmp_path: Path):
    source = InboxSource(inbox_dir=tmp_path / "nonexistent")
    assert source.search("anything") == []


def test_respects_max_age(tmp_path: Path):
    """Old files (older than max_age_days) should be ignored."""
    inbox = tmp_path / "inbox"
    inbox.mkdir()
    f = inbox / "arxiv-20200101.jsonl"
    f.write_text(json.dumps({"url": "https://x.com/1", "title": "old"}) + "\n",
                 encoding="utf-8")
    # Backdate it.
    import os
    old_ts = 1577836800  # 2020-01-01
    os.utime(f, (old_ts, old_ts))

    source = InboxSource(inbox_dir=inbox, max_age_days=7)
    assert source.search("anything") == []
