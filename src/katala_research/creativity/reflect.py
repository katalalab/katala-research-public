"""Reflection step — GapScore + mandatory counter-query when coverage is too narrow.

This is the explicit anti-echo-chamber check that fires once per iteration.
"""
from __future__ import annotations

from ..config import CreativityReflection
from ..primitives.embed import EmbedBackend, cosine
from ..types import Brief, Learning


def gap_score(brief: Brief, learnings: list[Learning], embed: EmbedBackend) -> float:
    """1 − mean_q [ max_l cos(emb(q), emb(l)) ].

    Interpretation:
      0.0 → every sub-question has a learning that closely matches it (well covered)
      1.0 → no learning is near any sub-question (totally uncovered)
    """
    if not brief.sub_questions or not learnings:
        return 1.0
    q_vecs = embed.encode_batch(brief.sub_questions)
    l_vecs = embed.encode_batch([l.text for l in learnings])
    if not l_vecs:
        return 1.0
    accum = 0.0
    for q in q_vecs:
        best = 0.0
        for l in l_vecs:
            c = cosine(q, l)
            if c > best:
                best = c
        accum += best
    mean_max = accum / len(q_vecs)
    return max(0.0, min(1.0, 1.0 - mean_max))


def needs_counter_query(
    gap: float, config: CreativityReflection
) -> bool:
    """If the gap exceeds threshold, the loop must spawn a far query next iteration."""
    return gap > config.gap_threshold


def derive_counter_query_seed(brief: Brief, learnings: list[Learning]) -> str:
    """Build a prompt seed for the LLM to generate a counter-query.

    Strategy: list the dominant claims of current learnings and ask for what would
    contradict them. The actual LLM call lives in pipeline/source.py — this just
    assembles the input.
    """
    claims = "\n".join(f"- {l.text}" for l in learnings[:5]) if learnings else "(no learnings yet)"
    return (
        f"Original brief: {brief.clarified or brief.original_query}\n\n"
        f"Current strongest learnings:\n{claims}\n\n"
        f"Generate up to 2 SERP queries that would surface CONTRADICTORY or "
        f"perspective-shifting evidence — sources that an analyst trying to falsify "
        f"the current view would consult. Return JSON: {{\"counter_queries\": [\"q1\", \"q2\"]}}"
    )
