"""End-to-end smoke: run the orchestrator with stub backends and verify artifacts."""
from __future__ import annotations

import json
from pathlib import Path

from katala_research.config import load_prefs
from katala_research.orchestrator import run_research


def test_e2e_stub_run_produces_all_artifacts(tmp_path: Path):
    prefs = load_prefs()
    summary = run_research(
        "What is the state of anti-filter-bubble research?",
        prefs=prefs,
        sessions_root=tmp_path,
        stub=True,
    )

    session_dir = Path(summary["session_dir"])
    # All standard artifacts present.
    expected = [
        "brief.md", "plan.md",
        "learnings.jsonl", "sources.jsonl", "scores.jsonl",
        "gates-rejected.jsonl", "report.md",
        "prefs-used.yaml", "transcript.jsonl",
    ]
    for name in expected:
        assert (session_dir / name).exists(), f"missing {name}"

    # Report should be non-empty.
    report = (session_dir / "report.md").read_text(encoding="utf-8")
    assert report.strip()

    # At least some sources logged.
    sources_text = (session_dir / "sources.jsonl").read_text(encoding="utf-8")
    lines = [l for l in sources_text.splitlines() if l.strip()]
    assert len(lines) >= 1, "stub run should produce at least one source"

    # At least some learnings extracted (the report depends on these).
    learnings_text = (session_dir / "learnings.jsonl").read_text(encoding="utf-8")
    lrn = [l for l in learnings_text.splitlines() if l.strip()]
    assert len(lrn) >= 1, "stub run should produce at least one learning"


def test_anti_bubble_evidence_in_session(tmp_path: Path):
    """The stub corpus is diverse; the selector should produce multi-domain sources."""
    prefs = load_prefs()
    summary = run_research(
        "Compare deep-research agents and filter-bubble mitigation",
        prefs=prefs,
        sessions_root=tmp_path,
        stub=True,
    )
    session_dir = Path(summary["session_dir"])
    sources_text = (session_dir / "sources.jsonl").read_text(encoding="utf-8")
    domains = set()
    for line in sources_text.splitlines():
        line = line.strip()
        if not line:
            continue
        entry = json.loads(line)
        if entry.get("domain"):
            domains.add(entry["domain"])
    # Stub corpus is diverse enough that we should see ≥2 distinct domains.
    assert len(domains) >= 2, f"only saw {domains} — anti-bubble selector may be broken"


def test_transcript_records_key_events(tmp_path: Path):
    prefs = load_prefs()
    summary = run_research(
        "smoke",
        prefs=prefs,
        sessions_root=tmp_path,
        stub=True,
    )
    transcript = (Path(summary["session_dir"]) / "transcript.jsonl").read_text(encoding="utf-8")
    event_types = set()
    for line in transcript.splitlines():
        line = line.strip()
        if not line:
            continue
        event_types.add(json.loads(line).get("type"))
    for required in ("session_start", "brief", "plan", "session_end"):
        assert required in event_types, f"transcript missing event: {required}"
