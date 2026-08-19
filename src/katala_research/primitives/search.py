"""Search primitives — SearXNG, Stub.

Each backend implements the same Protocol. The orchestrator wires a fallback chain
based on `prefs.search_backend_order`.
"""
from __future__ import annotations

import hashlib
from typing import Protocol

import httpx

from ..config import ResearchPrefs
from ..types import SearchHit


class SearchBackend(Protocol):
    name: str

    def search(self, query: str, *, limit: int = 5) -> list[SearchHit]: ...


class SearXNGBackend:
    """JSON API client for a self-hosted SearXNG instance."""

    name = "searxng"

    def __init__(self, url: str, timeout: float = 10.0):
        self.url = url.rstrip("/")
        self.timeout = timeout

    def search(self, query: str, *, limit: int = 5) -> list[SearchHit]:
        params = {"q": query, "format": "json", "safesearch": "1"}
        try:
            resp = httpx.get(f"{self.url}/search", params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except (httpx.HTTPError, ValueError) as e:
            raise RuntimeError(f"SearXNG query failed: {e}") from e

        hits: list[SearchHit] = []
        for i, r in enumerate(data.get("results", [])[:limit]):
            hits.append(
                SearchHit(
                    url=r.get("url", ""),
                    title=r.get("title", ""),
                    snippet=r.get("content", ""),
                    rank=i,
                    backend=self.name,
                )
            )
        return hits


class StubSearchBackend:
    """Deterministic canned results — used by --stub smoke and unit tests."""

    name = "stub"

    # Seed corpus covering diverse domains/perspectives so the creativity selector
    # actually has something to work with.
    _CORPUS: list[tuple[str, str, str]] = [
        ("https://en.wikipedia.org/wiki/Filter_bubble",
         "Filter bubble - Wikipedia",
         "A filter bubble is a state of intellectual isolation caused by personalization algorithms."),
        ("https://arxiv.org/abs/2503.00001",
         "On the Diversity-Relevance Tradeoff in Retrieval",
         "We propose a Maximum-Marginal-Relevance variant that explicitly penalizes paradigm-domain overlap."),
        ("https://openalex.org/works/W123",
         "Anti-bubble information retrieval",
         "Empirical study showing that 25% diversity floor improves user-reported novelty without harming relevance."),
        ("https://github.com/example/anti-bubble",
         "anti-bubble OSS reference impl",
         "Open-source pipeline implementing diversity-aware selection with hard caps."),
        ("https://medium.com/@author/personalization-is-fine",
         "Personalization is fine, actually",
         "A contrarian take: filter bubbles are overblown; users benefit from personalization."),
        ("https://allenai.org/blog/asta",
         "Asta — trustworthy AI for science",
         "Asta blends literature search with iterative reflection to surface non-obvious papers."),
        ("https://blog.langchain.com/open-deep-research/",
         "Open Deep Research (LangChain blog)",
         "Supervisor-based agent that delegates research subtasks with explicit reflection steps."),
        ("https://www.scientificamerican.com/article/echo-chamber",
         "The science of echo chambers",
         "Cognitive science on confirmation bias and how recommender systems amplify it."),
        ("https://news.ycombinator.com/item?id=999",
         "HN: Is RAG enough?",
         "Discussion thread arguing that RAG alone cannot prevent filter bubbles without diversity constraints."),
        ("https://twitter.com/researcher/status/1",
         "Tweet: discovery > personalization",
         "Short thread: best research agents inject contrarian sources as a structural property."),
    ]

    def search(self, query: str, *, limit: int = 5) -> list[SearchHit]:
        # Deterministic pseudo-ranking: hash query against each URL to vary order per query.
        scored: list[tuple[int, tuple[str, str, str]]] = []
        for entry in self._CORPUS:
            h = hashlib.sha1(f"{query}::{entry[0]}".encode()).hexdigest()
            scored.append((int(h[:8], 16), entry))
        scored.sort(key=lambda x: x[0])
        out: list[SearchHit] = []
        for i, (_, (url, title, snippet)) in enumerate(scored[:limit]):
            out.append(
                SearchHit(url=url, title=title, snippet=snippet, rank=i, backend=self.name)
            )
        return out


def build_search_chain(prefs: ResearchPrefs) -> list[SearchBackend]:
    """Build the ordered list of search backends per prefs."""
    chain: list[SearchBackend] = []
    for name in prefs.search_backend_order:
        if name == "searxng":
            chain.append(SearXNGBackend(url=prefs.searxng.url))
        elif name == "stub":
            chain.append(StubSearchBackend())
        # brave / tavily / exa / firecrawl: deferred to v0.1+
    if not chain:
        chain.append(StubSearchBackend())
    return chain


def search_with_fallback(chain: list[SearchBackend], query: str, *, limit: int = 5) -> list[SearchHit]:
    """Try each backend; first success wins. Raises only if all fail."""
    errors: list[str] = []
    for backend in chain:
        try:
            hits = backend.search(query, limit=limit)
            if hits:
                return hits
        except Exception as e:
            errors.append(f"{backend.name}: {e}")
    if errors:
        raise RuntimeError("all search backends failed: " + " | ".join(errors))
    return []


def search_and_merge(sources, query: str, *, per_source_limit: int = 5) -> list[SearchHit]:
    """Call all sources sequentially, merge results, dedupe by URL.

    Used for academic sources (arxiv + openalex + ...) which complement rather
    than substitute each other. Errors from individual sources are swallowed —
    a single failing source must not block the others.
    """
    seen_urls: set[str] = set()
    merged: list[SearchHit] = []
    for src in sources:
        try:
            hits = src.search(query, limit=per_source_limit)
        except Exception:
            continue
        for h in hits:
            if not h.url or h.url in seen_urls:
                continue
            seen_urls.add(h.url)
            merged.append(h)
    return merged


def build_academic_chain(prefs):
    """Build the list of academic Sources per prefs.academic_sources.

    Lazy imports each Source so users who don't enable a Source never pay the
    import cost.
    """
    chain = []
    for name in getattr(prefs, "academic_sources", []) or []:
        if name == "arxiv":
            from ..sources.arxiv import ArxivSource
            chain.append(ArxivSource())
        elif name == "openalex":
            from ..sources.openalex import OpenAlexSource
            chain.append(OpenAlexSource())
        elif name == "openreview":
            from ..sources.openreview import OpenReviewSource
            chain.append(OpenReviewSource())
        elif name == "semantic_scholar":
            from ..sources.semantic_scholar import SemanticScholarSource
            chain.append(SemanticScholarSource())
        elif name == "inbox":
            from ..sources.inbox import InboxSource
            chain.append(InboxSource())
    return chain
