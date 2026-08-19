"""Abstract base for academic Sources.

A Source is a `SearchBackend`-shaped adapter that also emits provenance metadata
(peer_reviewed, venue, doi, domain_tag, ...). Sources can be used as drop-in
replacements for `SearchBackend` in the search chain, OR called directly to
populate the inbox.
"""
from __future__ import annotations

from typing import Optional, Protocol

from ..types import CandidateMeta, SearchHit


class SourceResult(SearchHit):
    """A SearchHit guaranteed to carry meta from an academic Source.

    Currently a marker class — exists for type clarity when mixing
    `SearchBackend` results with `AcademicSource` results.
    """
    pass


class AcademicSource(Protocol):
    """Common interface for arXiv / OpenAlex / OpenReview / Semantic Scholar."""

    name: str
    peer_review_default: Optional[bool]
    domain_tags: list[str]

    def search(self, query: str, *, limit: int = 10) -> list[SearchHit]: ...


# Domain detection helpers — used by Sources to populate meta.domain_tag.
_DOMAIN_KEYWORDS = {
    "cs": ["cs.", "machine learning", "neural network", "transformer", "llm",
           "deep learning", "computer science", "algorithm", "software", "ai"],
    "q-bio": ["biology", "genetics", "protein", "neural", "neuroscience",
              "bioinformatics", "molecular", "cell", "drug"],
    "q-fin": ["finance", "trading", "portfolio", "asset", "market", "economic",
              "risk", "derivatives", "pricing"],
    "econ": ["economics", "policy", "labor", "growth", "inflation", "monetary",
             "fiscal", "trade", "development"],
    "stat": ["statistics", "regression", "bayesian", "inference", "estimation",
             "hypothesis", "probability"],
    "med": ["medicine", "clinical", "patient", "disease", "therapy", "trial",
            "diagnosis", "pubmed"],
    "social": ["sociology", "psychology", "political", "behavior", "survey",
               "education", "society"],
}


def detect_domain_tag(text: str) -> Optional[str]:
    """Cheap keyword classifier. Returns the first matching tag or None."""
    if not text:
        return None
    lowered = text.lower()
    best_tag = None
    best_score = 0
    for tag, kws in _DOMAIN_KEYWORDS.items():
        score = sum(1 for k in kws if k in lowered)
        if score > best_score:
            best_score = score
            best_tag = tag
    return best_tag if best_score > 0 else None


def make_meta(
    *,
    peer_reviewed: Optional[bool],
    source_type: str,
    venue: Optional[str] = None,
    venue_rank: Optional[str] = None,
    doi: Optional[str] = None,
    publication_date: Optional[str] = None,
    domain_tag: Optional[str] = None,
    citation_count: Optional[int] = None,
    review_comments: Optional[list[str]] = None,
) -> CandidateMeta:
    """Helper constructor — keeps Source impls terse."""
    return CandidateMeta(
        peer_reviewed=peer_reviewed,
        source_type=source_type,
        venue=venue,
        venue_rank=venue_rank,
        doi=doi,
        publication_date=publication_date,
        domain_tag=domain_tag,
        citation_count=citation_count,
        review_comments=review_comments or [],
    )
