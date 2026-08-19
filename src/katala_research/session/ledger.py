"""Session ledger — JSONL append-only event log + per-artifact files.

Layout under <session_dir>/:
  brief.md
  plan.md
  learnings.jsonl       # one Learning per line
  sources.jsonl         # one Candidate (lightweight) per line
  scores.jsonl          # full ScoreBreakdown per scored candidate
  gates-rejected.jsonl  # candidates dropped by Gate (debug)
  report.md             # final synthesis
  prefs-used.yaml       # snapshot of effective prefs
  transcript.jsonl      # generic event log {ts, type, payload}
"""
from __future__ import annotations

import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from ..config import ResearchPrefs
from ..types import Brief, Candidate, Learning, ResearchPlan


def _slugify(text: str, *, max_len: int = 40) -> str:
    """Light slug — alphanumerics+hyphen, lowercase. Keeps non-ASCII as-is for JP queries."""
    s = re.sub(r"\s+", "-", text.strip())
    s = re.sub(r"[^\w\-]", "", s, flags=re.UNICODE)
    return s.lower()[:max_len] or "query"


def new_session_dir(root: Path, query: str) -> Path:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    slug = _slugify(query)
    d = root / f"{ts}-{slug}"
    d.mkdir(parents=True, exist_ok=True)
    return d


class SessionLedger:
    """Append-only event recorder for one research session."""

    def __init__(self, session_dir: Path):
        self.dir = session_dir
        self.dir.mkdir(parents=True, exist_ok=True)
        self._t0 = time.time()
        self._transcript = self.dir / "transcript.jsonl"
        self._scores = self.dir / "scores.jsonl"
        self._learnings = self.dir / "learnings.jsonl"
        self._sources = self.dir / "sources.jsonl"
        self._gates_rejected = self.dir / "gates-rejected.jsonl"
        # Touch files so empty sessions still show structure.
        for f in (self._transcript, self._scores, self._learnings,
                  self._sources, self._gates_rejected):
            f.touch(exist_ok=True)

    def _append(self, path: Path, payload: dict[str, Any]) -> None:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def log(self, event_type: str, payload: dict[str, Any] | None = None) -> None:
        self._append(self._transcript, {
            "ts": time.time(),
            "elapsed": round(time.time() - self._t0, 3),
            "type": event_type,
            "payload": payload or {},
        })

    def log_score(self, candidate: Candidate) -> None:
        self._append(self._scores, {
            "url": candidate.url,
            "domain": candidate.domain,
            "title": candidate.title,
            "rank": candidate.rank,
            "backend": candidate.backend,
            "score": candidate.score.model_dump(),
        })

    def log_learning(self, learning: Learning) -> None:
        self._append(self._learnings, learning.model_dump())

    def log_source(self, candidate: Candidate) -> None:
        self._append(self._sources, {
            "url": candidate.url,
            "domain": candidate.domain,
            "title": candidate.title,
            "rank": candidate.rank,
            "backend": candidate.backend,
            "total_score": candidate.score.total,
            "bucket_hint": (
                "Strong evidence" if candidate.score.total >= 0.55
                else "Worth checking" if candidate.score.total >= 0.30
                else "Speculative"
            ),
        })

    def log_gate_rejection(self, candidate: Candidate) -> None:
        self._append(self._gates_rejected, {
            "url": candidate.url,
            "domain": candidate.domain,
            "title": candidate.title,
            "failures": candidate.score.gate_failures,
            "score": candidate.score.model_dump(),
        })

    def write_brief(self, brief: Brief) -> None:
        (self.dir / "brief.md").write_text(
            f"# Brief\n\n"
            f"**Original query**: {brief.original_query}\n\n"
            f"**Clarified**: {brief.clarified or '(no clarification step)'}\n\n"
            f"## Sub-questions\n\n"
            + ("\n".join(f"- {q}" for q in brief.sub_questions) or "(none)") + "\n",
            encoding="utf-8",
        )

    def write_plan(self, plan: ResearchPlan) -> None:
        (self.dir / "plan.md").write_text(
            f"# Research plan\n\n"
            f"**Breadth**: {plan.breadth}\n"
            f"**Depth**: {plan.depth}\n\n"
            f"## SERP queries\n\n"
            + ("\n".join(f"- {q}" for q in plan.serp_queries) or "(none)") + "\n\n"
            f"## Counter queries\n\n"
            + ("\n".join(f"- {q}" for q in plan.counter_queries) or "(none — will derive at reflection)") + "\n",
            encoding="utf-8",
        )

    def write_report(self, markdown: str) -> Path:
        out = self.dir / "report.md"
        out.write_text(markdown, encoding="utf-8")
        return out

    def write_prefs_used(self, prefs: ResearchPrefs) -> None:
        # by_alias=True so the YAML matches the example file's key style.
        data = prefs.model_dump(by_alias=True)
        (self.dir / "prefs-used.yaml").write_text(
            yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )

    def finalize(self) -> dict[str, Any]:
        """Return a small summary dict (useful for CLI output)."""
        elapsed = time.time() - self._t0
        return {
            "session_dir": str(self.dir),
            "elapsed_seconds": round(elapsed, 2),
            "report_path": str(self.dir / "report.md"),
        }
