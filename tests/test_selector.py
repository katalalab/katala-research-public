"""Tests for the diversity-aware Selector — the anti-bubble heart of v0."""
from __future__ import annotations

from katala_research.config import CreativitySelector
from katala_research.pipeline.selector import select
from katala_research.types import Candidate, ScoreBreakdown


def _mk(url: str, total: float, discovery: float, semantic_novelty: float = 0.5) -> Candidate:
    return Candidate(
        url=url,
        title=url,
        score=ScoreBreakdown(
            total=total, discovery=discovery, semantic_novelty=semantic_novelty,
            topical_fit=0.6, content_gap=0.2, source_risk=0.2, reading_cost=0.3,
            gate_passed=True,
        ),
    )


def test_domain_cap_limits_dominance():
    cfg = CreativitySelector(
        domain_cap_ratio=0.40,  # ≤ 40% from any domain
        paradigm_cap_ratio=1.0,
        discovery_floor_ratio=0.0,
        discovery_threshold=1.1,  # disable floor
        must_include_counter=False,
    )
    cands = [
        _mk("https://hot.com/a", 0.9, 0.1),
        _mk("https://hot.com/b", 0.85, 0.1),
        _mk("https://hot.com/c", 0.8, 0.1),
        _mk("https://hot.com/d", 0.75, 0.1),
        _mk("https://other.com/a", 0.7, 0.4),
        _mk("https://third.com/a", 0.6, 0.4),
    ]
    selected = select(cands, k=5, selector_cfg=cfg, preferred_sources=[])
    hot_count = sum(1 for c in selected if "hot.com" in c.url)
    # 40% of 5 = 2; cap is ceil(5 * 0.40) = 2.
    assert hot_count <= 2


def test_creativity_floor_swaps_in_discovery():
    cfg = CreativitySelector(
        domain_cap_ratio=1.0,
        paradigm_cap_ratio=1.0,
        discovery_floor_ratio=0.50,   # require 50% discovery (aggressive)
        discovery_threshold=0.50,
        must_include_counter=False,
    )
    # Top-scored candidates have low discovery; a few mid-scored have high discovery.
    cands = [
        _mk("https://a.com/1", 0.95, 0.10),
        _mk("https://b.com/1", 0.92, 0.15),
        _mk("https://c.com/1", 0.90, 0.20),
        _mk("https://d.com/1", 0.70, 0.80),  # high discovery
        _mk("https://e.com/1", 0.65, 0.75),  # high discovery
        _mk("https://f.com/1", 0.60, 0.10),
    ]
    selected = select(cands, k=4, selector_cfg=cfg, preferred_sources=[])
    high_disc = sum(1 for c in selected if c.score.discovery >= 0.50)
    # Floor of 50% of 4 = 2.
    assert high_disc >= 2


def test_paradigm_cap_blocks_preferred_set_dominance():
    cfg = CreativitySelector(
        domain_cap_ratio=1.0,
        paradigm_cap_ratio=0.50,   # ≤ 50% from preferred-set
        discovery_floor_ratio=0.0,
        discovery_threshold=1.1,
        must_include_counter=False,
    )
    preferred = ["arxiv.org", "openalex.org"]
    cands = [
        _mk("https://arxiv.org/abs/1", 0.95, 0.1),
        _mk("https://arxiv.org/abs/2", 0.93, 0.1),
        _mk("https://openalex.org/W1", 0.91, 0.1),
        _mk("https://openalex.org/W2", 0.89, 0.1),
        _mk("https://outside1.com/x", 0.50, 0.4),
        _mk("https://outside2.com/x", 0.45, 0.4),
    ]
    selected = select(cands, k=4, selector_cfg=cfg, preferred_sources=preferred)
    preferred_count = sum(
        1 for c in selected if any(c.domain.endswith(p) for p in preferred)
    )
    # Cap of 50% of 4 = 2.
    assert preferred_count <= 2


def test_counter_evidence_included_when_required():
    cfg = CreativitySelector(
        domain_cap_ratio=1.0,
        paradigm_cap_ratio=1.0,
        discovery_floor_ratio=0.0,
        discovery_threshold=1.1,
        must_include_counter=True,
    )
    cands = [
        _mk("https://a.com/1", 0.95, 0.1, semantic_novelty=0.2),
        _mk("https://b.com/1", 0.92, 0.1, semantic_novelty=0.3),
        _mk("https://c.com/1", 0.90, 0.1, semantic_novelty=0.4),
        _mk("https://counter.com/x", 0.60, 0.5, semantic_novelty=0.8),  # high semantic_novelty
    ]
    selected = select(cands, k=3, selector_cfg=cfg, preferred_sources=[])
    has_counter = any(c.score.semantic_novelty >= 0.55 for c in selected)
    assert has_counter
