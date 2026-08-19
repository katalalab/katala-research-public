"""Tests for the creativity scoring layer."""
from __future__ import annotations

from katala_research.config import CreativityConfig, CreativityGates
from katala_research.creativity.gates import check_gates
from katala_research.creativity.reflect import gap_score, needs_counter_query
from katala_research.creativity.score import CandidateScorer
from katala_research.primitives.embed import DummyEmbed, cosine
from katala_research.types import Brief, Candidate, Learning, ScoreBreakdown


def _make_brief() -> Brief:
    return Brief(
        original_query="anti-bubble research agents",
        clarified="Survey anti-filter-bubble techniques in deep-research agents.",
        sub_questions=[
            "What is a filter bubble?",
            "How is diversity measured?",
            "What benchmarks exist?",
        ],
    )


def test_score_in_unit_range():
    embed = DummyEmbed()
    brief = _make_brief()
    scorer = CandidateScorer(
        config=CreativityConfig(),
        embed=embed,
        brief=brief,
        learnings=[],
        preferred_sources=["arxiv.org"],
        banned_domains=["spam.com"],
    )
    c = Candidate(
        url="https://arxiv.org/abs/2503.0001",
        title="Diversity in retrieval",
        snippet="Diversity-aware selection improves novelty without hurting relevance.",
    )
    s = scorer.score(c)
    assert 0.0 <= s.relevance <= 1.0
    assert 0.0 <= s.discovery <= 1.0
    assert 0.0 <= s.risk <= 1.0
    assert -1.0 <= s.total <= 1.0
    assert s.why_ranked
    assert s.why_not_higher


def test_candidate_isolation():
    """Same candidate scored twice yields identical score (no inter-candidate leak)."""
    embed = DummyEmbed()
    brief = _make_brief()
    scorer = CandidateScorer(
        config=CreativityConfig(),
        embed=embed,
        brief=brief,
        learnings=[],
        preferred_sources=[],
        banned_domains=[],
    )
    c1 = Candidate(url="https://example.com/a", snippet="Diversity and novelty in research.")
    c2 = Candidate(url="https://example.com/a", snippet="Diversity and novelty in research.")
    s1 = scorer.score(c1)
    s2 = scorer.score(c2)
    assert abs(s1.total - s2.total) < 1e-9
    assert abs(s1.discovery - s2.discovery) < 1e-9


def test_banned_domain_drives_risk_up():
    embed = DummyEmbed()
    brief = _make_brief()
    scorer = CandidateScorer(
        config=CreativityConfig(),
        embed=embed,
        brief=brief,
        learnings=[],
        preferred_sources=["arxiv.org"],
        banned_domains=["spam.com"],
    )
    c_good = Candidate(url="https://arxiv.org/abs/1", snippet="diversity")
    c_bad = Candidate(url="https://spam.com/x", snippet="diversity")
    s_good = scorer.score(c_good)
    s_bad = scorer.score(c_bad)
    assert s_bad.source_risk > s_good.source_risk


def test_gate_rejects_off_brief():
    gates = CreativityGates(topical_fit_min=0.5)
    s = ScoreBreakdown(topical_fit=0.2)
    ok, failures = check_gates(s, gates)
    assert not ok
    assert any("topical_fit" in f for f in failures)
    assert s.gate_passed is False


def test_gate_accepts_compliant():
    gates = CreativityGates()  # defaults
    s = ScoreBreakdown(topical_fit=0.6, content_gap=0.2, source_risk=0.2, reading_cost=0.4)
    ok, failures = check_gates(s, gates)
    assert ok
    assert failures == []


def test_gap_score_high_when_no_learnings():
    embed = DummyEmbed()
    brief = _make_brief()
    assert gap_score(brief, [], embed) == 1.0


def test_gap_score_lower_when_learnings_match_subq():
    embed = DummyEmbed()
    brief = _make_brief()
    # Provide learnings that overlap textually with sub-questions.
    learnings = [
        Learning(text="filter bubble definition diversity measurement benchmark", source_url="x"),
        Learning(text="diversity intra-list metric calibrated relevance", source_url="x"),
    ]
    g_with = gap_score(brief, learnings, embed)
    g_without = gap_score(brief, [], embed)
    assert g_with < g_without  # learnings reduce the gap


def test_needs_counter_query_threshold():
    from katala_research.config import CreativityReflection
    cfg = CreativityReflection(gap_threshold=0.40)
    assert needs_counter_query(0.50, cfg) is True
    assert needs_counter_query(0.30, cfg) is False


def test_rubric_dimensions_split_five_core_three_cost():
    from katala_research.creativity.rubric import RUBRIC_DIMENSIONS
    kinds = [k for _, _, k in RUBRIC_DIMENSIONS]
    assert len(RUBRIC_DIMENSIONS) == 8
    assert kinds.count("core") == 5
    assert kinds.count("cost") == 3
    keys = [k for k, _, _ in RUBRIC_DIMENSIONS]
    assert len(set(keys)) == 8


def test_rubric_normalization_and_verdict():
    """Core/cost normalization uses the 25/15 maxima and composite = core - 0.6*cost."""
    from katala_research.creativity.rubric import RUBRIC_DIMENSIONS, score_report

    class _FixedLLM:
        name = model = "fixed"

        def __init__(self, value: int):
            self.value = value

        def generate_text(self, prompt, *, system="", max_tokens=2048):
            return ""

        def generate_json(self, prompt, *, system="", max_tokens=2048):
            return {"score": self.value, "rationale": "fixed"}

    best = score_report("report", "brief", _FixedLLM(5))
    assert [s.dimension for s in best.scores] == [k for k, _, _ in RUBRIC_DIMENSIONS]
    assert best.total_core == 1.0
    assert best.total_cost == 1.0
    assert abs(best.composite - 0.4) < 1e-9
    assert best.verdict == "保留"  # perfect core, but max cost drags the composite down

    worst = score_report("report", "brief", _FixedLLM(0))
    assert worst.total_core == 0.0 and worst.composite == 0.0
    assert worst.verdict == "不採用"


def test_rubric_clamps_out_of_range_judge_scores():
    from katala_research.creativity.rubric import score_report

    class _WildLLM:
        name = model = "wild"

        def generate_text(self, prompt, *, system="", max_tokens=2048):
            return ""

        def generate_json(self, prompt, *, system="", max_tokens=2048):
            return {"score": 99, "rationale": "out of range"}

    res = score_report("report", "brief", _WildLLM())
    assert all(0 <= s.score <= 5 for s in res.scores)
