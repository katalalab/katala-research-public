"""Hard pass/fail Gate on the Score(z) sub-terms.

A candidate that fails ANY gate is rejected outright, regardless of total Score.
This is the "no amount of novelty rescues an off-brief candidate" rule.
"""
from __future__ import annotations

from ..config import CreativityGates
from ..types import ScoreBreakdown


def check_gates(score: ScoreBreakdown, gates: CreativityGates) -> tuple[bool, list[str]]:
    """Return (passed, list_of_failed_gate_names). Empty list ⇔ passed."""
    failed: list[str] = []
    if score.topical_fit < gates.topical_fit_min:
        failed.append(f"topical_fit={score.topical_fit:.2f}<{gates.topical_fit_min}")
    if score.content_gap > gates.content_gap_max:
        failed.append(f"content_gap={score.content_gap:.2f}>{gates.content_gap_max}")
    if score.source_risk > gates.source_risk_max:
        failed.append(f"source_risk={score.source_risk:.2f}>{gates.source_risk_max}")
    if score.reading_cost > gates.reading_cost_max:
        failed.append(f"reading_cost={score.reading_cost:.2f}>{gates.reading_cost_max}")
    score.gate_passed = not failed
    score.gate_failures = failed
    return (not failed), failed
