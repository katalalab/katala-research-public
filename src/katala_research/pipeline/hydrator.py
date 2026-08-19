"""Hydrator stage — turn SearchHits into Candidates with fetched content.

Uses the Read fallback chain (jina → defuddle → stub).
Fetches are sequential in v0 to keep concurrency simple; can parallelize later.
"""
from __future__ import annotations

from ..primitives.read import ReadBackend, read_with_fallback
from ..types import Candidate, SearchHit


def hydrate(
    hits: list[SearchHit], read_chain: list[ReadBackend], *, fetch: bool = True
) -> list[Candidate]:
    """Convert hits to candidates. If fetch=False, leave content empty (snippet-only scoring)."""
    out: list[Candidate] = []
    for h in hits:
        c = Candidate(
            url=h.url,
            title=h.title,
            snippet=h.snippet,
            rank=h.rank,
            backend=h.backend,
        )
        if fetch:
            page = read_with_fallback(read_chain, h.url)
            if page.markdown and not page.error:
                c.content = page.markdown
                if not c.title and page.title:
                    c.title = page.title
        out.append(c)
    return out
