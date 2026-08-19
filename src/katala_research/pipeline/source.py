"""Source stage — generate SERP queries (incl. counter-queries) from the brief.

Mirrors `dzhng/deep-research`'s `generateSerpQueries` but adds the explicit
counter-query branch driven by the Reflection step (creativity/reflect.py).
"""
from __future__ import annotations

import json
from typing import Any

from ..creativity.reflect import derive_counter_query_seed
from ..primitives.llm import LLMBackend
from ..types import Brief, Learning


_SERP_SYS = (
    "You are an expert researcher. Given a brief, propose SERP queries that "
    "would surface high-signal evidence. Prefer specific, distinct queries; avoid duplicates."
)


def generate_serp_queries(
    brief: Brief,
    llm: LLMBackend,
    *,
    n: int = 4,
    prior_learnings: list[Learning] | None = None,
) -> list[str]:
    """Return up to `n` SERP queries derived from the brief (+ prior learnings)."""
    learnings_block = ""
    if prior_learnings:
        learnings_block = "Prior learnings (use these to make NEW queries, not duplicates):\n"
        learnings_block += "\n".join(f"- {l.text}" for l in prior_learnings[-10:])

    prompt = (
        f"Brief:\n{brief.clarified or brief.original_query}\n\n"
        f"Sub-questions:\n" + "\n".join(f"- {q}" for q in brief.sub_questions) + "\n\n"
        + learnings_block + "\n"
        f"Generate up to {n} SERP queries. Return JSON: "
        f'{{"queries": [{{"query": "...", "researchGoal": "..."}}]}}.'
    )
    try:
        resp = llm.generate_json(prompt, system=_SERP_SYS, max_tokens=800)
        queries = [q.get("query", "").strip() for q in resp.get("queries", [])]
    except Exception:
        queries = []
    return [q for q in queries if q][:n]


def generate_counter_queries(
    brief: Brief, llm: LLMBackend, learnings: list[Learning]
) -> list[str]:
    """Generate ≤2 contradictory / perspective-shifting queries."""
    prompt = derive_counter_query_seed(brief, learnings)
    try:
        resp = llm.generate_json(prompt, system=_SERP_SYS, max_tokens=400)
        out: list[str] = []
        for q in resp.get("counter_queries", []):
            if isinstance(q, str) and q.strip():
                out.append(q.strip())
        return out[:2]
    except Exception:
        return []


def generate_follow_ups(
    brief: Brief, learnings: list[Learning], llm: LLMBackend, *, n: int = 3
) -> list[str]:
    """Refine sub-questions based on what we've learned so far."""
    if not learnings:
        return []
    prompt = (
        f"Brief: {brief.clarified or brief.original_query}\n\n"
        f"Learnings so far:\n" + "\n".join(f"- {l.text}" for l in learnings[-15:]) + "\n\n"
        f"What are the {n} most important follow-up questions to research next? "
        f'Return JSON: {{"followUpQuestions": ["q1", ...]}}.'
    )
    try:
        resp: dict[str, Any] = llm.generate_json(prompt, system=_SERP_SYS, max_tokens=400)
        return [q for q in resp.get("followUpQuestions", []) if isinstance(q, str)][:n]
    except Exception:
        return []
