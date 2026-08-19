"""Report rubric — LLM-as-judge over 8 dimensions × 0-5.

Used by the bench harness to score finished reports beyond DRB's RACE/FACT.

The eight axes are this repository's own formulation of what a *good anti-bubble
research report* looks like. Each axis is stated below with the public evaluation
concept it is derived from, so the rubric can be audited and argued with:

core (higher is better)
  subtopic_recall        how many of the brief's sub-questions get a substantive,
                         sourced answer — subtopic recall / S-recall
                         (Zhai, Cooper & Lafferty, SIGIR 2003)
  viewpoint_spread       how many genuinely different positions, schools, or
                         stakeholder perspectives the report represents, including
                         at least one that cuts against the brief's premise —
                         intent/viewpoint diversity (Clarke et al., SIGIR 2008,
                         alpha-nDCG; Vrijenhoek et al., 2021, RADio)
  cross_source_synthesis claims the report assembles from two or more sources that
                         no single cited source states on its own — combinational
                         creativity (Boden, "The Creative Mind", 2004)
  evidence_grounding     share of load-bearing claims carrying a citation that
                         actually supports them — attributable-to-identified-sources
                         (Rashkin et al., Computational Linguistics 2023)
  decision_utility       whether a reader can decide or act differently after
                         reading — situational relevance / utility
                         (Saracevic, "Relevance: A Review of the Literature", 2007)

cost (lower is better)
  redundancy             restates what the brief already asserts, or repeats itself
                         across sections — novelty & redundancy detection
                         (Zhang, Callan & Minka, SIGIR 2002)
  source_concentration   share of the evidence drawn from one domain, author, or
                         school — intra-list diversity / topic diversification
                         (Ziegler et al., WWW 2005)
  reading_overhead       length, jargon, and structure out of proportion to the
                         payload — Grice's maxim of quantity (Grice, "Logic and
                         Conversation", 1975)

Five core axes and three cost axes, each 0-5, keeps the composite arithmetic
below on the same scale as the candidate-level Score(z) in `score.py`.
"""
from __future__ import annotations

from pydantic import BaseModel

from ..primitives.llm import LLMBackend


RUBRIC_DIMENSIONS = [
    ("subtopic_recall", "下位問いの網羅 (sub-questions answered with sources)", "core"),
    ("viewpoint_spread", "立場の広がり (distinct positions, incl. one against the premise)", "core"),
    ("cross_source_synthesis", "出典間の統合 (claims no single cited source states alone)", "core"),
    ("evidence_grounding", "主張の裏付け (load-bearing claims cite sources that support them)", "core"),
    ("decision_utility", "意思決定への効き (reader can decide or act differently)", "core"),
    ("redundancy", "既知の反復 (repeats the brief or itself — LOWER is better)", "cost"),
    ("source_concentration", "出典の偏り (evidence leans on one domain or school — LOWER is better)", "cost"),
    ("reading_overhead", "読解コスト (length and jargon exceed the payload — LOWER is better)", "cost"),
]


class RubricScore(BaseModel):
    dimension: str
    description: str
    kind: str  # "core" or "cost"
    score: int  # 0-5
    rationale: str = ""


class RubricResult(BaseModel):
    scores: list[RubricScore]
    total_core: float = 0.0
    total_cost: float = 0.0
    composite: float = 0.0  # weighted: core - cost
    verdict: str = "保留"  # 採用 | 保留 | 不採用
    gate_passed: bool = True


def score_report(report_md: str, brief_text: str, llm: LLMBackend) -> RubricResult:
    """Score a finished research report against the 8-dimension rubric."""
    scores: list[RubricScore] = []
    for key, desc, kind in RUBRIC_DIMENSIONS:
        prompt = _make_judge_prompt(key, desc, kind, report_md, brief_text)
        try:
            resp = llm.generate_json(prompt, max_tokens=400)
            raw = resp.get("score", 0)
            score = int(raw) if isinstance(raw, (int, float, str)) and str(raw).strip() != "" else 0
            rationale = str(resp.get("rationale", ""))[:300]
        except Exception as e:
            score = 0
            rationale = f"judge error: {e}"
        score = max(0, min(5, score))
        scores.append(RubricScore(
            dimension=key, description=desc, kind=kind,
            score=score, rationale=rationale,
        ))

    core = sum(s.score for s in scores if s.kind == "core")
    cost = sum(s.score for s in scores if s.kind == "cost")
    # Normalize: 5 core dims × max 5 = 25 max; 3 cost dims × max 5 = 15 max
    core_norm = core / 25.0
    cost_norm = cost / 15.0
    composite = core_norm - 0.6 * cost_norm  # cost is less heavily weighted than core

    # Verdict
    verdict = "保留"
    if composite >= 0.55 and core >= 18:
        verdict = "採用"
    elif composite < 0.20 or core < 10:
        verdict = "不採用"

    return RubricResult(
        scores=scores,
        total_core=core_norm,
        total_cost=cost_norm,
        composite=composite,
        verdict=verdict,
        gate_passed=True,  # Reports don't enforce gates the way candidates do.
    )


def _make_judge_prompt(key: str, desc: str, kind: str, report: str, brief: str) -> str:
    direction = "HIGHER is better" if kind == "core" else "LOWER is better"
    return (
        f"You are an objective rubric judge scoring a research report on ONE dimension.\n\n"
        f"Dimension: {key} ({desc}). {direction}.\n\n"
        f"Brief the report was supposed to address:\n{brief[:1000]}\n\n"
        f"Report (truncated):\n{report[:6000]}\n\n"
        f"Score this dimension on 0-5 (integer only). 0 = absent, 5 = excellent.\n"
        f'Return JSON: {{"score": <int>, "rationale": "<one short sentence>"}}.'
    )
