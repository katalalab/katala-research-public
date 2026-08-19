"""SemanticScholarSource — citation graph + venue + DOI.

Direct call to Semantic Scholar Graph API. SEMANTIC_SCHOLAR_API_KEY raises the
rate limit. peer_reviewed inferred from venue + externalIds.DOI.
"""
from __future__ import annotations

from typing import Optional

import httpx

from ..config import resolve_env
from ..types import SearchHit
from .base import detect_domain_tag, make_meta


S2_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"


class SemanticScholarSource:
    name = "semantic_scholar"
    peer_review_default = None  # decided per-result
    domain_tags = ["cs", "q-bio", "q-fin", "econ", "stat", "med", "social"]

    def __init__(self, timeout: float = 20.0):
        self.timeout = timeout
        self.api_key = resolve_env("SEMANTIC_SCHOLAR_API_KEY")

    def search(self, query: str, *, limit: int = 10) -> list[SearchHit]:
        fields = "title,abstract,venue,publicationVenue,externalIds,year,citationCount,publicationTypes,openAccessPdf,url,fieldsOfStudy"
        params = {"query": query, "limit": min(limit, 25), "fields": fields}
        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        try:
            resp = httpx.get(S2_SEARCH, params=params, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
        except (httpx.HTTPError, ValueError):
            return []

        hits: list[SearchHit] = []
        for i, p in enumerate(data.get("data", [])[:limit]):
            hits.append(self._parse_paper(p, rank=i))
        return hits

    def _parse_paper(self, p: dict, *, rank: int) -> SearchHit:
        title = p.get("title") or ""
        abstract = p.get("abstract") or ""
        venue = p.get("venue") or (p.get("publicationVenue") or {}).get("name") or ""
        external = p.get("externalIds") or {}
        doi = external.get("DOI") or external.get("doi")
        year = p.get("year")
        pub_date = f"{year}-01-01" if year else None
        cite_count = p.get("citationCount")
        url = p.get("openAccessPdf", {}).get("url") if p.get("openAccessPdf") else p.get("url")
        if not url and doi:
            url = f"https://doi.org/{doi}"
        if not url:
            url = f"https://www.semanticscholar.org/paper/{p.get('paperId', '')}"

        pub_types = p.get("publicationTypes") or []
        pt_lower = [str(t).lower() for t in pub_types if t]
        venue_low = venue.lower() if isinstance(venue, str) else ""

        peer_reviewed: Optional[bool]
        if any("preprint" in t for t in pt_lower) or "arxiv" in venue_low or "biorxiv" in venue_low or "ssrn" in venue_low:
            peer_reviewed = False
        elif venue and any(t in pt_lower for t in ("journalarticle", "conference", "review", "book")):
            peer_reviewed = True
        elif venue and not any("preprint" in t for t in pt_lower):
            # Has a real venue, not flagged preprint — treat as peer-reviewed by default.
            peer_reviewed = True
        else:
            peer_reviewed = None

        fos = p.get("fieldsOfStudy") or []
        fos_text = " ".join(str(f) for f in fos)
        domain_tag = detect_domain_tag(f"{title} {abstract} {fos_text} {venue}")

        meta = make_meta(
            peer_reviewed=peer_reviewed,
            source_type=(
                "peer-reviewed" if peer_reviewed else
                "preprint" if peer_reviewed is False else
                "web"
            ),
            venue=venue or None,
            doi=doi,
            publication_date=pub_date,
            domain_tag=domain_tag,
            citation_count=cite_count,
        )
        return SearchHit(
            url=url,
            title=title,
            snippet=abstract[:500] if abstract else "",
            rank=rank,
            backend=self.name,
            meta=meta,
        )
