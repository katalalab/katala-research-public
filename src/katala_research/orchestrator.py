"""Orchestrator — top-level composition of primitives + pipeline + strategy.

`run_research(query, prefs, ...)` is the entry called from CLI / skill / tests.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from .config import ResearchPrefs, load_prefs
from .primitives.embed import build_embed
from .primitives.llm import LLMBackend, build_llm
from .primitives.read import build_read_chain
from .primitives.search import build_academic_chain, build_search_chain
from .session.ledger import SessionLedger, new_session_dir
from .strategies.iterative import run_iterative
from .types import Brief, Learning


DEFAULT_SESSIONS_ROOT = Path.home() / "work" / "research" / "sessions"


def _build_brief(query: str, llm: LLMBackend) -> Brief:
    """v0: no interactive clarification; we ask the LLM to expand the brief once."""
    prompt = (
        f"User research request: {query}\n\n"
        f"Rephrase the brief in one paragraph and list 3-5 sub-questions that "
        f"a thorough researcher would need to answer to produce a useful report. "
        f'Return JSON: {{"clarified": "...", "sub_questions": ["...", "..."]}}.'
    )
    try:
        resp = llm.generate_json(prompt, max_tokens=600)
        clarified = str(resp.get("clarified", "")).strip()
        sub_qs = [s for s in resp.get("sub_questions", []) if isinstance(s, str) and s.strip()]
    except Exception:
        clarified = query
        sub_qs = [query]
    return Brief(original_query=query, clarified=clarified, sub_questions=sub_qs)


def _synthesize_report(
    brief: Brief, learnings: list[Learning], sources: list, llm: LLMBackend
) -> str:
    """Final synthesis pass — pulls learnings into a Markdown report."""
    if not learnings:
        return _empty_report(brief)
    learnings_block = "\n".join(
        f"- ({l.bucket}) {l.text}  \n  source: {l.source_url}" for l in learnings
    )
    src_block = "\n".join(
        f"- [{c.title or c.domain}]({c.url})" for c in sources
    )
    prompt = (
        f"Brief: {brief.clarified or brief.original_query}\n\n"
        f"Sub-questions:\n" + "\n".join(f"- {q}" for q in brief.sub_questions) + "\n\n"
        f"Learnings (with confidence bucket and source):\n{learnings_block}\n\n"
        f"Write a research report in Markdown. Structure: Executive summary, "
        f"per-sub-question section, Open questions, References. Use inline citations "
        f"like [{{title}}]({{url}}). Be concise but information-dense. "
        f"Mark speculative claims explicitly.\n\n"
        f"After the report, also include the References list:\n{src_block}\n"
    )
    try:
        md = llm.generate_text(prompt, max_tokens=4000)
    except Exception as e:
        md = (
            f"# Research Report (synthesis failed)\n\n"
            f"Error during synthesis: {e}\n\n## Raw learnings\n\n{learnings_block}\n"
        )
    return md


def _empty_report(brief: Brief) -> str:
    return (
        f"# Research Report\n\n"
        f"**Brief**: {brief.clarified or brief.original_query}\n\n"
        f"_No learnings collected. Possible causes: search backend unavailable, "
        f"all candidates rejected by Gates, or the brief was unanswerable. "
        f"Check `gates-rejected.jsonl` and `transcript.jsonl`._\n"
    )


def run_research(
    query: str,
    *,
    prefs: Optional[ResearchPrefs] = None,
    sessions_root: Optional[Path] = None,
    stub: bool = False,
    fetch_content: Optional[bool] = None,
) -> dict:
    """Run one research session and return a summary dict."""
    prefs = prefs or load_prefs()
    sessions_root = sessions_root or DEFAULT_SESSIONS_ROOT

    # Build primitives.
    search_chain = build_search_chain(prefs)
    # Academic sources are skipped in stub mode (they make real HTTP calls
    # and would not return deterministic results for smoke tests).
    academic_sources = [] if stub else build_academic_chain(prefs)
    read_chain = build_read_chain(prefs)
    embed = build_embed(prefer_local_model=not stub)
    llm = build_llm(prefs, stub=stub)

    # Set up session.
    session_dir = new_session_dir(sessions_root, query)
    ledger = SessionLedger(session_dir)
    ledger.write_prefs_used(prefs)
    ledger.log("session_start", {
        "query": query, "stub": stub, "llm_backend": llm.name,
        "search_chain": [b.name for b in search_chain],
        "academic_sources": [s.name for s in academic_sources],
        "read_chain": [b.name for b in read_chain],
        "embed_backend": embed.name,
    })

    # Build brief.
    brief = _build_brief(query, llm)
    ledger.write_brief(brief)
    ledger.log("brief", {"clarified": brief.clarified, "sub_questions": brief.sub_questions})

    # Run iterative strategy.
    # NOTE: in stub mode we still fetch — StubReadBackend returns canned content
    # that the LLM (also stub) needs to extract learnings from. The whole point of
    # the smoke is to exercise the pipeline including SideEffect.
    if fetch_content is None:
        fetch_content = True
    learnings, sources, plan = run_iterative(
        brief, prefs,
        search_chain=search_chain, read_chain=read_chain,
        embed=embed, llm=llm, ledger=ledger,
        fetch_content=fetch_content,
        academic_sources=academic_sources,
    )

    # Synthesize report.
    report_md = _synthesize_report(brief, learnings, sources, llm)
    ledger.write_report(report_md)
    ledger.log("session_end", {
        "n_learnings": len(learnings),
        "n_sources": len(sources),
    })

    summary = ledger.finalize()
    summary.update({
        "query": query,
        "n_learnings": len(learnings),
        "n_sources": len(sources),
        "stub": stub,
    })
    return summary
