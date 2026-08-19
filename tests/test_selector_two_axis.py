"""Selector must enforce paradigm_cap on BOTH preferred-sources AND peer-review axes."""
from __future__ import annotations

from katala_research.config import CreativitySelector
from katala_research.pipeline.selector import select
from katala_research.types import Candidate, CandidateMeta, ScoreBreakdown


def _mk(url: str, total: float, peer_reviewed: bool | None = None,
        discovery: float = 0.1, semantic_novelty: float = 0.5) -> Candidate:
    return Candidate(
        url=url, title=url,
        score=ScoreBreakdown(
            total=total, discovery=discovery, semantic_novelty=semantic_novelty,
            topical_fit=0.6, content_gap=0.2, source_risk=0.2, reading_cost=0.3,
            gate_passed=True,
        ),
        meta=CandidateMeta(peer_reviewed=peer_reviewed),
    )


def test_peer_review_axis_cap_enforced():
    """Selecting 4 with paradigm_cap=0.50 means ≤2 peer-reviewed AND ≤2 preprint."""
    cfg = CreativitySelector(
        domain_cap_ratio=1.0,
        paradigm_cap_ratio=0.50,
        discovery_floor_ratio=0.0,
        discovery_threshold=1.1,
        must_include_counter=False,
    )
    cands = [
        _mk("https://a.com/1", 0.95, peer_reviewed=True),
        _mk("https://b.com/1", 0.92, peer_reviewed=True),
        _mk("https://c.com/1", 0.90, peer_reviewed=True),  # would be 3rd peer-reviewed → blocked
        _mk("https://d.com/1", 0.88, peer_reviewed=False),
        _mk("https://e.com/1", 0.85, peer_reviewed=False),
        _mk("https://f.com/1", 0.60, peer_reviewed=None),
    ]
    selected = select(cands, k=4, selector_cfg=cfg, preferred_sources=[])
    pr_true = sum(1 for c in selected if c.meta.peer_reviewed is True)
    pr_false = sum(1 for c in selected if c.meta.peer_reviewed is False)
    assert pr_true <= 2, f"peer-reviewed cap violated: {pr_true}>2"
    assert pr_false <= 2, f"preprint cap violated: {pr_false}>2"


def test_two_axis_cap_combines_with_preferred_cap():
    """Both axes apply simultaneously."""
    cfg = CreativitySelector(
        domain_cap_ratio=1.0,
        paradigm_cap_ratio=0.50,
        discovery_floor_ratio=0.0,
        discovery_threshold=1.1,
        must_include_counter=False,
    )
    preferred = ["arxiv.org", "openalex.org"]
    cands = [
        # preferred + peer-reviewed
        _mk("https://arxiv.org/abs/1", 0.95, peer_reviewed=True),
        _mk("https://openalex.org/W1", 0.93, peer_reviewed=True),
        # would-be 3rd from preferred
        _mk("https://arxiv.org/abs/2", 0.91, peer_reviewed=True),
        # outside preferred, preprint
        _mk("https://outside1.com/x", 0.50, peer_reviewed=False),
        _mk("https://outside2.com/y", 0.45, peer_reviewed=False),
        # outside, unknown
        _mk("https://blog.example.com/x", 0.40, peer_reviewed=None),
    ]
    selected = select(cands, k=4, selector_cfg=cfg, preferred_sources=preferred)
    n_preferred = sum(
        1 for c in selected if any(c.domain.endswith(p) for p in preferred)
    )
    pr_true = sum(1 for c in selected if c.meta.peer_reviewed is True)
    assert n_preferred <= 2
    assert pr_true <= 2


def test_unknown_peer_review_does_not_count_toward_cap():
    """meta.peer_reviewed=None is "uncapped" — neither axis counts it."""
    cfg = CreativitySelector(
        domain_cap_ratio=1.0,
        paradigm_cap_ratio=0.50,
        discovery_floor_ratio=0.0,
        discovery_threshold=1.1,
        must_include_counter=False,
    )
    cands = [
        _mk("https://a.com/1", 0.95, peer_reviewed=None),
        _mk("https://b.com/1", 0.92, peer_reviewed=None),
        _mk("https://c.com/1", 0.90, peer_reviewed=None),  # OK even with cap
        _mk("https://d.com/1", 0.88, peer_reviewed=None),
    ]
    selected = select(cands, k=4, selector_cfg=cfg, preferred_sources=[])
    # All 4 should fit — None is uncapped.
    assert len(selected) == 4
