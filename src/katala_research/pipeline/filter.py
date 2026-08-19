"""Filter stage — banned-domain prefilter + Gate enforcement post-scoring.

The hard banned-domain check runs BEFORE scoring (cheap reject).
The Gate runs AFTER scoring (requires ScoreBreakdown).
"""
from __future__ import annotations

from ..config import CreativityGates, ResearchPrefs
from ..creativity.gates import check_gates
from ..types import Candidate


def prefilter_by_banned_domains(
    candidates: list[Candidate], banned: list[str]
) -> tuple[list[Candidate], list[Candidate]]:
    """Split candidates into (kept, rejected) based on banned-domain suffix match."""
    kept: list[Candidate] = []
    rejected: list[Candidate] = []
    banned_lower = [b.lower() for b in banned]
    for c in candidates:
        d = (c.domain or "").lower()
        is_banned = any(d.endswith(b) for b in banned_lower)
        if is_banned:
            c.score.gate_failures.append(f"banned-domain:{c.domain}")
            c.score.gate_passed = False
            rejected.append(c)
        else:
            kept.append(c)
    return kept, rejected


def apply_creativity_gates(
    candidates: list[Candidate], gates: CreativityGates
) -> tuple[list[Candidate], list[Candidate]]:
    """Split candidates into (passed, failed) by the Score(z) Gate.

    Mutates candidate.score with gate_passed / gate_failures.
    """
    passed: list[Candidate] = []
    failed: list[Candidate] = []
    for c in candidates:
        ok, _ = check_gates(c.score, gates)
        (passed if ok else failed).append(c)
    return passed, failed
