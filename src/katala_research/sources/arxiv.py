"""ArxivSource — preprint coverage across cs / q-bio / q-fin / econ / stat.

Uses the arXiv API (Atom XML). No API key required. Default categories cover
the 4 user-prioritized domains (ML/CS / 学際 / 生命科学 / 経済社会).
"""
from __future__ import annotations

import re
import time
from typing import Optional
from xml.etree import ElementTree as ET

import httpx

from ..config import resolve_env
from ..types import SearchHit
from .base import detect_domain_tag, make_meta


# arXiv requests HTTPS now (HTTP still redirects but with overhead).
ARXIV_API = "https://export.arxiv.org/api/query"
ATOM_NS = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"

DEFAULT_CATEGORIES = [
    "cs.*",
    "q-bio.*",
    "q-fin.*",
    "econ.*",
    "stat.*",
]

# arXiv category prefix → our domain_tag.
_CATEGORY_TO_DOMAIN = {
    "cs": "cs",
    "q-bio": "q-bio",
    "q-fin": "q-fin",
    "econ": "econ",
    "stat": "stat",
    "math": "stat",   # treat math as stats-adjacent for our purposes
    "physics": "cs",  # rough fallback
    "eess": "cs",
}


class ArxivSource:
    """Search arXiv preprints. peer_reviewed=False by default (preprint server)."""

    name = "arxiv"
    peer_review_default = False
    domain_tags = ["cs", "q-bio", "q-fin", "econ", "stat"]

    # arXiv asks for ≥3 seconds between API calls. Class-level last-call timestamp
    # so multiple instances cooperate.
    _last_call_ts: float = 0.0
    _polite_delay: float = 3.5

    def __init__(self, categories: Optional[list[str]] = None, timeout: float = 20.0):
        self.categories = categories or DEFAULT_CATEGORIES
        self.timeout = timeout

    def search(self, query: str, *, limit: int = 10) -> list[SearchHit]:
        # Compose category filter: cat:cs.* OR cat:q-bio.* OR ...
        cat_clause = " OR ".join(f"cat:{c}" for c in self.categories)
        search_query = f"({cat_clause}) AND all:{_arxiv_escape(query)}"
        params = {
            "search_query": search_query,
            "start": 0,
            "max_results": min(limit, 25),
            "sortBy": "relevance",
            "sortOrder": "descending",
        }
        # arXiv asks for a descriptive User-Agent with a contact email — same
        # politeness norm as OpenAlex.
        mailto = resolve_env("OPENALEX_MAILTO") or resolve_env("CROSSREF_MAILTO")
        headers = {
            "User-Agent": f"katala-research/0.1 (mailto:{mailto or 'unknown'})",
        }
        # Respect the 3-second-per-call rule, even across instances.
        elapsed = time.time() - ArxivSource._last_call_ts
        if elapsed < self._polite_delay:
            time.sleep(self._polite_delay - elapsed)
        ArxivSource._last_call_ts = time.time()

        try:
            resp = httpx.get(ARXIV_API, params=params, headers=headers, timeout=self.timeout)
            # 429 = rate exceeded. Sleep and retry once.
            if resp.status_code == 429:
                retry_after = float(resp.headers.get("retry-after", "10"))
                time.sleep(min(retry_after, 30.0))
                ArxivSource._last_call_ts = time.time()
                resp = httpx.get(ARXIV_API, params=params, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
        except httpx.HTTPError:
            return []
        try:
            root = ET.fromstring(resp.text)
        except ET.ParseError:
            return []

        hits: list[SearchHit] = []
        for i, entry in enumerate(root.findall(f"{ATOM_NS}entry")):
            hit = self._parse_entry(entry, rank=i)
            if hit:
                hits.append(hit)
        return hits

    def _parse_entry(self, entry: ET.Element, *, rank: int) -> Optional[SearchHit]:
        url_el = entry.find(f"{ATOM_NS}id")
        title_el = entry.find(f"{ATOM_NS}title")
        summary_el = entry.find(f"{ATOM_NS}summary")
        published_el = entry.find(f"{ATOM_NS}published")
        primary_cat_el = entry.find(f"{ARXIV_NS}primary_category")
        doi_el = entry.find(f"{ARXIV_NS}doi")

        if url_el is None or title_el is None:
            return None
        url = (url_el.text or "").strip()
        title = re.sub(r"\s+", " ", (title_el.text or "").strip())
        snippet = re.sub(r"\s+", " ", (summary_el.text or "").strip()) if summary_el is not None else ""
        published = (published_el.text or "")[:10] if published_el is not None else None
        primary_cat = primary_cat_el.attrib.get("term", "") if primary_cat_el is not None else ""
        doi = (doi_el.text or "").strip() if doi_el is not None else None
        cat_prefix = primary_cat.split(".")[0] if "." in primary_cat else primary_cat
        domain_tag = _CATEGORY_TO_DOMAIN.get(cat_prefix) or detect_domain_tag(title + " " + snippet)
        venue = f"arXiv:{primary_cat}" if primary_cat else "arXiv"

        meta = make_meta(
            peer_reviewed=False,
            source_type="preprint",
            venue=venue,
            doi=doi,
            publication_date=published,
            domain_tag=domain_tag,
        )
        return SearchHit(
            url=url,
            title=title,
            snippet=snippet[:500],
            rank=rank,
            backend=self.name,
            meta=meta,
        )


def _arxiv_escape(query: str) -> str:
    """arXiv accepts simple Boolean queries — keep characters that confuse the
    server out. (Lucene-style; over-conservative is fine.)"""
    cleaned = re.sub(r"[^\w\s\-]", " ", query)
    return cleaned.strip() or query.strip()
