"""SideEffect stage — extract learnings from selected candidates, append to ledger.

The "side effect" name comes from x-algorithm's pipeline ontology: this is where
state-mutating IO happens (ledger writes, learning storage). Keep it isolated.
"""
from __future__ import annotations

from typing import Any

from ..primitives.llm import LLMBackend
from ..types import Brief, Candidate, Learning


_EXTRACT_SYS = (
    "You are an expert researcher extracting concise, information-dense learnings "
    "from web content. Each learning must be a standalone fact / claim with entities, "
    "numbers, dates where present."
)


def extract_learnings(
    candidate: Candidate,
    brief: Brief,
    llm: LLMBackend,
    *,
    max_learnings: int = 3,
) -> list[Learning]:
    """LLM-extract learnings from a single candidate's content."""
    if not candidate.content:
        return []
    # Trim very long pages.
    content = candidate.content[:20_000]
    prompt = (
        f"Brief: {brief.clarified or brief.original_query}\n\n"
        f"Source URL: {candidate.url}\n"
        f"Source title: {candidate.title}\n\n"
        f"Content (truncated):\n{content}\n\n"
        f"Extract up to {max_learnings} concise learnings relevant to the brief. "
        f"Include any specific entities, numbers, dates, names. "
        f'Return JSON: {{"learnings": ["...", "..."], "followUpQuestions": ["...", "..."]}}.'
    )
    try:
        resp: dict[str, Any] = llm.generate_json(prompt, system=_EXTRACT_SYS, max_tokens=800)
    except Exception:
        return []

    out: list[Learning] = []
    for text in resp.get("learnings", []):
        if not isinstance(text, str) or not text.strip():
            continue
        out.append(Learning(
            text=text.strip(),
            source_url=candidate.url,
            source_title=candidate.title,
            confidence=_bucket_to_confidence(candidate.score.total),
            bucket=_bucket_label(candidate.score.total, candidate.score.discovery),
            why_ranked=candidate.score.why_ranked,
            why_not_higher=candidate.score.why_not_higher,
        ))
    return out


def _bucket_to_confidence(total: float) -> float:
    return max(0.0, min(1.0, total + 0.5))  # shift [-0.5..0.5] → [0..1]


def _bucket_label(total: float, discovery: float) -> str:
    if total >= 0.55:
        return "Strong evidence"
    if total >= 0.30 or discovery >= 0.40:
        return "Worth checking"
    return "Speculative"
