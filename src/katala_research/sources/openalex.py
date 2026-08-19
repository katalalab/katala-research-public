"""OpenAlexSource — cross-domain peer-reviewed primary backbone.

Uses the OpenAlex /works endpoint. Free, no API key. If OPENALEX_MAILTO is set,
queries enter the polite pool (10 req/s + priority).

peer_reviewed is inferred:
  • type == "article" AND host_venue is not None → True
  • type == "preprint" OR venue is "Preprint Server" → False
  • else None (unknown)
"""
from __future__ import annotations

from typing import Optional

import httpx

from ..config import resolve_env
from ..types import SearchHit
from .base import detect_domain_tag, make_meta


OPENALEX_API = "https://api.openalex.org/works"


class OpenAlexSource:
    name = "openalex"
    peer_review_default = None  # decided per-result
    domain_tags = ["cs", "q-bio", "q-fin", "econ", "stat", "med", "social"]

    def __init__(self, timeout: float = 20.0):
        self.timeout = timeout
        self.mailto = resolve_env("OPENALEX_MAILTO")

    def search(self, query: str, *, limit: int = 10) -> list[SearchHit]:
        params: dict = {
            "search": query,
            "per-page": min(limit, 25),
            "select": (
                "id,doi,title,abstract_inverted_index,publication_date,"
                "type,primary_location,cited_by_count,concepts"
            ),
        }
        if self.mailto:
            params["mailto"] = self.mailto
        try:
            resp = httpx.get(OPENALEX_API, params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except (httpx.HTTPError, ValueError):
            return []

        hits: list[SearchHit] = []
        for i, w in enumerate(data.get("results", [])):
            hits.append(self._parse_work(w, rank=i))
        return hits

    def _parse_work(self, w: dict, *, rank: int) -> SearchHit:
        title = w.get("title") or ""
        abstract = _recover_abstract(w.get("abstract_inverted_index"))
        doi = w.get("doi")
        if doi and doi.startswith("https://doi.org/"):
            doi = doi[len("https://doi.org/"):]

        # OpenAlex deprecated `host_venue` (2024-04). Use primary_location.source instead.
        primary_loc = w.get("primary_location") or {}
        source = primary_loc.get("source") or {}
        venue_name = source.get("display_name")
        source_type = (source.get("type") or "").lower()  # "journal"|"ebook platform"|"repository"|"conference"
        landing_url = primary_loc.get("landing_page_url") or w.get("id") or ""

        wtype = (w.get("type") or "").lower()
        peer_reviewed: Optional[bool]
        vname_low = (venue_name or "").lower()
        # Repositories (arxiv, biorxiv, ssrn, etc.) and explicit preprint types → not peer-reviewed.
        if (
            source_type == "repository"
            or "arxiv" in vname_low or "biorxiv" in vname_low or "medrxiv" in vname_low or "ssrn" in vname_low
            or wtype in {"preprint", "posted-content"}
        ):
            peer_reviewed = False
        # Journal / conference with a real venue → peer-reviewed.
        elif venue_name and source_type in {"journal", "conference"}:
            peer_reviewed = True
        elif venue_name and wtype in {"article", "review", "book-chapter", "conference-paper", "journal-article"}:
            peer_reviewed = True
        else:
            peer_reviewed = None

        concepts = w.get("concepts") or []
        concept_text = " ".join(c.get("display_name", "") for c in concepts[:5])
        domain_tag = detect_domain_tag(f"{title} {abstract} {concept_text}")

        meta = make_meta(
            peer_reviewed=peer_reviewed,
            source_type="peer-reviewed" if peer_reviewed else ("preprint" if peer_reviewed is False else "web"),
            venue=venue_name,
            doi=doi,
            publication_date=w.get("publication_date"),
            domain_tag=domain_tag,
            citation_count=w.get("cited_by_count"),
        )
        return SearchHit(
            url=landing_url,
            title=title,
            snippet=abstract[:500],
            rank=rank,
            backend=self.name,
            meta=meta,
        )


def _recover_abstract(inverted: Optional[dict]) -> str:
    """OpenAlex stores abstracts as {word: [positions]}. Reverse to plain text."""
    if not inverted:
        return ""
    positions: list[tuple[int, str]] = []
    for word, idxs in inverted.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort(key=lambda x: x[0])
    return " ".join(w for _, w in positions)
