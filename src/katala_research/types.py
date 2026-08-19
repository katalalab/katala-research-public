"""Shared data types across primitives, pipeline, creativity, strategies."""
from __future__ import annotations

from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field


def _extract_domain(url: str) -> str:
    try:
        netloc = urlparse(url).netloc
        return netloc[4:] if netloc.startswith("www.") else netloc
    except Exception:
        return ""


class CandidateMeta(BaseModel):
    """Provenance metadata attached to a Candidate by Source-level enrichment.

    All fields default to None ("unknown"). Web-search results typically leave
    most fields empty; Academic Sources (Arxiv, OpenAlex, Semantic Scholar,
    OpenReview) fill them in.
    """

    peer_reviewed: Optional[bool] = None     # None = unknown — neutral
    venue: Optional[str] = None              # "NeurIPS 2025", "Nature", "arXiv:cs.LG"
    venue_rank: Optional[str] = None         # "A*", "A", "B" — DBLP/CORE if known
    doi: Optional[str] = None
    publication_date: Optional[str] = None   # ISO date string
    domain_tag: Optional[str] = None         # "cs"|"q-bio"|"q-fin"|"econ"|"stat"|"med"|"social"|"web"
    source_type: str = "web"                 # "web"|"preprint"|"peer-reviewed"|"review"
    citation_count: Optional[int] = None
    review_comments: list[str] = Field(default_factory=list)  # OpenReview review excerpts


class SearchHit(BaseModel):
    """A single SERP result from any search backend."""

    url: str
    title: str = ""
    snippet: str = ""
    rank: int = 0
    backend: str = ""
    meta: CandidateMeta = Field(default_factory=CandidateMeta)

    @property
    def domain(self) -> str:
        return _extract_domain(self.url)


class FetchedPage(BaseModel):
    """Result of fetching+cleaning a URL."""

    url: str
    title: str = ""
    markdown: str = ""
    error: Optional[str] = None
    backend: str = ""


class ScoreBreakdown(BaseModel):
    """Full Score(z) breakdown, retained for audit / why_ranked / why_not_higher."""

    relevance: float = 0.0
    discovery: float = 0.0
    risk: float = 0.0
    # Discovery sub-terms
    source_distance: float = 0.0
    semantic_novelty: float = 0.0
    topical_fit: float = 0.0
    subtopic_coverage: float = 0.0
    redundancy: float = 0.0
    depth_fit: float = 0.0
    # Risk sub-terms
    content_gap: float = 0.0
    source_risk: float = 0.0
    reading_cost: float = 0.0
    # Final composite
    total: float = 0.0
    # Reasons
    why_ranked: str = ""
    why_not_higher: str = ""
    gate_passed: bool = True
    gate_failures: list[str] = Field(default_factory=list)


class Candidate(BaseModel):
    """A research candidate: hit + (optional) hydrated content + scores."""

    url: str
    title: str = ""
    snippet: str = ""
    rank: int = 0
    backend: str = ""
    content: Optional[str] = None  # markdown, after Hydrator
    score: ScoreBreakdown = Field(default_factory=ScoreBreakdown)
    meta: CandidateMeta = Field(default_factory=CandidateMeta)

    @property
    def domain(self) -> str:
        return _extract_domain(self.url)

    @property
    def text_for_embed(self) -> str:
        """Best available text for embedding."""
        if self.content:
            # Trim long content to keep embeddings fast.
            return self.content[:4000]
        return f"{self.title}\n\n{self.snippet}".strip()


class Learning(BaseModel):
    """An extracted fact/claim from a fetched page."""

    text: str
    source_url: str
    source_title: str = ""
    confidence: float = 0.5
    bucket: str = "Worth checking"  # Strong evidence | Worth checking | Speculative
    # Provenance breadcrumbs (borrowed from personal-info-feed)
    why_ranked: str = ""
    why_not_higher: str = ""
    # v0.1: propagate source provenance
    source_peer_reviewed: Optional[bool] = None
    source_venue: Optional[str] = None
    source_domain_tag: Optional[str] = None


class Brief(BaseModel):
    """User's clarified research brief."""

    original_query: str
    clarified: str = ""
    sub_questions: list[str] = Field(default_factory=list)

    @property
    def text_for_embed(self) -> str:
        parts = [self.original_query, self.clarified]
        parts.extend(self.sub_questions)
        return "\n".join(p for p in parts if p).strip()


class ResearchPlan(BaseModel):
    brief: Brief
    serp_queries: list[str] = Field(default_factory=list)
    counter_queries: list[str] = Field(default_factory=list)
    depth: int = 2
    breadth: int = 4
