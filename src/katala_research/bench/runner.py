"""Bench harness — runs DRB-5 tasks + scores reports with creativity rubric.

This is a smoke benchmark, not a publication-grade evaluation. It validates that:
  • the orchestrator runs end-to-end
  • the anti-bubble selector actually fires (creativity floor met)
  • the rubric judge produces sane scores
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Optional

from ..config import load_prefs
from ..creativity.rubric import score_report
from ..orchestrator import DEFAULT_SESSIONS_ROOT, run_research
from ..primitives.llm import build_llm

BENCH_DIR = Path(__file__).resolve().parent
DEFAULT_TASKS = BENCH_DIR / "tasks" / "drb-subset-5.json"
RESULTS_DIR = BENCH_DIR / "results"


def _check_anti_bubble(session_dir: Path, floor_ratio: float) -> dict:
    """Verify the Selector's creativity floor actually fired in this session.

    Reads sources.jsonl. A run is "anti-bubble compliant" if:
      • At least floor_ratio of sources have total_score ≥ 0.30 AND domain not in preferred-set (proxy).
    The proxy is loose but catches obvious bubbling.
    """
    src_file = session_dir / "sources.jsonl"
    if not src_file.exists():
        return {"compliant": False, "reason": "sources.jsonl missing"}
    sources: list[dict] = []
    with open(src_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                sources.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    if not sources:
        return {"compliant": False, "reason": "no sources"}

    domain_counter: dict[str, int] = {}
    for s in sources:
        d = s.get("domain", "unknown")
        domain_counter[d] = domain_counter.get(d, 0) + 1
    # Top domain share
    top_share = max(domain_counter.values()) / len(sources)
    distinct_domains = len(domain_counter)
    compliant = distinct_domains >= max(2, math.ceil(len(sources) * floor_ratio))
    return {
        "compliant": compliant,
        "n_sources": len(sources),
        "distinct_domains": distinct_domains,
        "top_domain_share": round(top_share, 3),
        "floor_ratio": floor_ratio,
    }


def run_bench(
    *,
    n_tasks: int = 5,
    stub: bool = False,
    sessions_root: Optional[Path] = None,
    tasks_path: Optional[Path] = None,
) -> dict:
    """Run the bench. Returns a summary dict and writes per-task + aggregate JSON."""
    tasks_file = tasks_path or DEFAULT_TASKS
    with open(tasks_file, "r", encoding="utf-8") as f:
        bench_data = json.load(f)
    tasks = bench_data.get("tasks", [])[:n_tasks]

    sessions_root = sessions_root or DEFAULT_SESSIONS_ROOT / "bench"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    prefs = load_prefs()
    rubric_llm = build_llm(prefs, stub=stub)
    floor_ratio = prefs.creativity.selector.discovery_floor_ratio

    per_task: list[dict] = []
    for t in tasks:
        run_summary = run_research(
            t["query"],
            prefs=prefs,
            sessions_root=sessions_root,
            stub=stub,
        )
        session_dir = Path(run_summary["session_dir"])

        # Anti-bubble compliance.
        bubble = _check_anti_bubble(session_dir, floor_ratio=floor_ratio)

        # Creativity rubric.
        report_path = session_dir / "report.md"
        report_md = report_path.read_text(encoding="utf-8") if report_path.exists() else ""
        rubric = score_report(report_md, t["query"], rubric_llm)

        per_task.append({
            "id": t["id"],
            "lang": t["lang"],
            "domain": t["domain"],
            "query": t["query"],
            "session_dir": str(session_dir),
            "n_learnings": run_summary["n_learnings"],
            "n_sources": run_summary["n_sources"],
            "anti_bubble": bubble,
            "rubric": rubric.model_dump(),
        })

    # Aggregate.
    n = len(per_task)
    agg = {
        "n_tasks": n,
        "stub": stub,
        "compliant_count": sum(1 for r in per_task if r["anti_bubble"].get("compliant")),
        "mean_core": (sum(r["rubric"]["total_core"] for r in per_task) / n) if n else 0.0,
        "mean_cost": (sum(r["rubric"]["total_cost"] for r in per_task) / n) if n else 0.0,
        "mean_composite": (sum(r["rubric"]["composite"] for r in per_task) / n) if n else 0.0,
        "verdicts": {v: sum(1 for r in per_task if r["rubric"]["verdict"] == v)
                     for v in ("採用", "保留", "不採用")},
        "per_task": per_task,
    }

    # Persist.
    from datetime import datetime
    out = RESULTS_DIR / f"bench-{datetime.now():%Y%m%d-%H%M%S}.json"
    out.write_text(json.dumps(agg, ensure_ascii=False, indent=2), encoding="utf-8")
    agg["results_file"] = str(out)
    return agg
