"""Iterative strategy — dzhng-style breadth×depth loop on our x-algorithm pipeline.

Differences from the original `dzhng/deep-research`:
- Pipeline shape is Source/Hydrator/Filter/Scorer/Selector/SideEffect (not flat).
- Scorer uses the anti-bubble Score(z), not a raw provider score.
- Selector enforces creativity floor + caps + counter-evidence.
- Reflection step checks GapScore and triggers counter-queries when warranted.
"""
from __future__ import annotations

import math

from ..config import ResearchPrefs
from ..creativity.reflect import gap_score, needs_counter_query
from ..pipeline.filter import apply_creativity_gates, prefilter_by_banned_domains
from ..pipeline.hydrator import hydrate
from ..pipeline.scorer import score_candidates
from ..pipeline.selector import select
from ..pipeline.side_effect import extract_learnings
from ..pipeline.source import (
    generate_counter_queries,
    generate_follow_ups,
    generate_serp_queries,
)
from ..primitives.embed import EmbedBackend
from ..primitives.llm import LLMBackend
from ..primitives.read import ReadBackend
from ..primitives.search import SearchBackend, search_and_merge, search_with_fallback
from ..session.ledger import SessionLedger
from ..types import Brief, Candidate, Learning, ResearchPlan


def _count_by_backend(hits: list) -> dict[str, int]:
    out: dict[str, int] = {}
    for h in hits:
        b = getattr(h, "backend", "unknown") or "unknown"
        out[b] = out.get(b, 0) + 1
    return out


def run_iterative(
    brief: Brief,
    prefs: ResearchPrefs,
    *,
    search_chain: list[SearchBackend],
    read_chain: list[ReadBackend],
    embed: EmbedBackend,
    llm: LLMBackend,
    ledger: SessionLedger,
    fetch_content: bool = True,
    academic_sources: list | None = None,
) -> tuple[list[Learning], list[Candidate], ResearchPlan]:
    """Run the breadth×depth iterative loop. Returns (learnings, sources, plan)."""

    learnings: list[Learning] = []
    sources: list[Candidate] = []
    seen_urls: set[str] = set()

    breadth = prefs.default_breadth
    depth = prefs.default_depth

    # 1) Plan — initial SERP queries.
    serp_queries = generate_serp_queries(brief, llm, n=breadth)
    plan = ResearchPlan(
        brief=brief, serp_queries=serp_queries, depth=depth, breadth=breadth
    )
    ledger.write_plan(plan)
    ledger.log("plan", {"queries": serp_queries, "breadth": breadth, "depth": depth})

    queries_this_level: list[str] = list(serp_queries)
    counter_queries_this_level: list[str] = []

    # 2) Outer loop over depth levels.
    for level in range(depth + 1):
        ledger.log("level_start", {
            "level": level, "breadth": breadth,
            "n_queries": len(queries_this_level),
            "n_counter": len(counter_queries_this_level),
        })

        # 3) Per-query inner pipeline.
        all_queries = queries_this_level + counter_queries_this_level
        if not all_queries:
            ledger.log("no_queries", {"level": level})
            break

        new_learnings_this_level: list[Learning] = []
        new_follow_ups: list[str] = []

        for q in all_queries:
            ledger.log("query_start", {"query": q})
            web_hits = []
            academic_hits = []
            try:
                web_hits = search_with_fallback(search_chain, q, limit=max(3, breadth))
            except RuntimeError as e:
                ledger.log("search_error", {"query": q, "error": str(e)})
            if academic_sources:
                academic_hits = search_and_merge(
                    academic_sources, q, per_source_limit=max(3, breadth)
                )
                if academic_hits:
                    ledger.log("academic_hits", {
                        "query": q, "n": len(academic_hits),
                        "by_source": _count_by_backend(academic_hits),
                    })
            # Merge & dedupe (academic first — usually higher quality).
            hits = academic_hits + [
                h for h in web_hits
                if not any(h.url == ah.url for ah in academic_hits)
            ]
            if not hits:
                continue

            # Hydrator
            candidates = hydrate(hits, read_chain, fetch=fetch_content)
            # Skip already-seen URLs to keep candidate isolation clean.
            candidates = [c for c in candidates if c.url and c.url not in seen_urls]
            for c in candidates:
                seen_urls.add(c.url)

            # Filter (banned-domain prefilter)
            kept, banned_rejected = prefilter_by_banned_domains(
                candidates, prefs.banned_domains
            )
            for r in banned_rejected:
                ledger.log_gate_rejection(r)

            # Scorer (candidate isolation)
            kept = score_candidates(
                kept, brief=brief, learnings=learnings, prefs=prefs, embed=embed
            )
            for c in kept:
                ledger.log_score(c)

            # Filter (Gates)
            passed, gate_rejected = apply_creativity_gates(kept, prefs.creativity.gates)
            for r in gate_rejected:
                ledger.log_gate_rejection(r)

            # Selector
            top_k = max(1, math.ceil(breadth * 1.5))
            selected = select(
                passed,
                k=top_k,
                selector_cfg=prefs.creativity.selector,
                preferred_sources=prefs.preferred_sources,
            )
            ledger.log("selected", {
                "query": q, "n_selected": len(selected),
                "urls": [c.url for c in selected],
            })

            # SideEffect: extract learnings, append to sources.
            for c in selected:
                ledger.log_source(c)
                sources.append(c)
                new_for_c = extract_learnings(c, brief, llm)
                for l in new_for_c:
                    ledger.log_learning(l)
                    learnings.append(l)
                    new_learnings_this_level.append(l)

        # 4) Reflection — compute GapScore, decide whether to spawn counter-queries next.
        gap = gap_score(brief, learnings, embed)
        ledger.log("reflection", {"level": level, "gap_score": gap})
        if level < depth:
            # Build next level: follow-ups + (if gap is high) counter-queries.
            new_breadth = max(1, math.ceil(breadth / 2))
            new_follow_ups = generate_follow_ups(brief, new_learnings_this_level, llm, n=new_breadth)
            counter_queries_this_level = []
            if needs_counter_query(gap, prefs.creativity.reflection):
                counter_queries_this_level = generate_counter_queries(brief, llm, learnings)
                ledger.log("counter_queries_triggered", {
                    "gap_score": gap, "queries": counter_queries_this_level,
                })
            queries_this_level = new_follow_ups
            breadth = new_breadth
        else:
            queries_this_level = []
            counter_queries_this_level = []

        ledger.log("level_end", {
            "level": level, "n_new_learnings": len(new_learnings_this_level),
            "total_learnings": len(learnings),
        })

    return learnings, sources, plan
