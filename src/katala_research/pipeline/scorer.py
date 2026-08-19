"""Scorer stage — thin wrapper around creativity.score.CandidateScorer.

Candidate isolation invariant: every candidate is scored in isolation (no
inter-candidate references). The same Scorer instance carries pre-computed
embeddings of brief / sub-questions / prior learnings; those are batch-invariant.
"""
from __future__ import annotations

from ..config import ResearchPrefs
from ..creativity.score import CandidateScorer
from ..primitives.embed import EmbedBackend
from ..types import Brief, Candidate, Learning


def score_candidates(
    candidates: list[Candidate],
    *,
    brief: Brief,
    learnings: list[Learning],
    prefs: ResearchPrefs,
    embed: EmbedBackend,
) -> list[Candidate]:
    """Score in place; returns the same list for chaining."""
    scorer = CandidateScorer(
        config=prefs.creativity,
        embed=embed,
        brief=brief,
        learnings=learnings,
        preferred_sources=prefs.preferred_sources,
        banned_domains=prefs.banned_domains,
        language=prefs.language,
    )
    for c in candidates:
        c.score = scorer.score(c)
    return candidates
