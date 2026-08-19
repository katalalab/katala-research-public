"""Peer-review metadata must flow Candidate → Score → Selector → ledger."""
from __future__ import annotations

from katala_research.config import CreativityConfig
from katala_research.creativity.score import CandidateScorer
from katala_research.primitives.embed import DummyEmbed
from katala_research.types import Brief, Candidate, CandidateMeta


def _brief() -> Brief:
    return Brief(
        original_query="diversity in retrieval",
        clarified="Survey diversity-aware retrieval.",
        sub_questions=["what is diversity-aware retrieval?"],
    )


def test_peer_reviewed_lowers_r_counter():
    embed = DummyEmbed()
    cfg = CreativityConfig()
    scorer = CandidateScorer(
        config=cfg, embed=embed, brief=_brief(), learnings=[],
        preferred_sources=[], banned_domains=[],
    )
    snippet = "Diversity-aware retrieval surfaces non-redundant evidence."

    pr_true = Candidate(url="https://x.com/a", snippet=snippet,
                        meta=CandidateMeta(peer_reviewed=True))
    pr_false = Candidate(url="https://x.com/b", snippet=snippet,
                         meta=CandidateMeta(peer_reviewed=False))
    pr_none = Candidate(url="https://x.com/c", snippet=snippet,
                        meta=CandidateMeta(peer_reviewed=None))

    s_t = scorer.score(pr_true)
    s_f = scorer.score(pr_false)
    s_n = scorer.score(pr_none)

    # Peer-reviewed should have the lowest source_risk; preprint the highest.
    assert s_t.source_risk < s_n.source_risk < s_f.source_risk, (
        f"expected t<n<f, got {s_t.source_risk:.3f}/{s_n.source_risk:.3f}/{s_f.source_risk:.3f}"
    )
    # Risk feeds into total; peer-reviewed should outscore preprint, all else equal.
    assert s_t.total >= s_f.total


def test_unknown_peer_review_is_neutral():
    """Candidate without meta.peer_reviewed should behave exactly like before v0.1."""
    embed = DummyEmbed()
    cfg = CreativityConfig()
    scorer = CandidateScorer(
        config=cfg, embed=embed, brief=_brief(), learnings=[],
        preferred_sources=[], banned_domains=[],
    )
    snippet = "Same text both times."
    a = Candidate(url="https://example.com/a", snippet=snippet)
    b = Candidate(url="https://example.com/b", snippet=snippet,
                  meta=CandidateMeta(peer_reviewed=None))
    sa = scorer.score(a)
    sb = scorer.score(b)
    assert abs(sa.source_risk - sb.source_risk) < 1e-9
    assert abs(sa.total - sb.total) < 1e-9
