"""Candidate-level Score(z) — the anti-bubble ranking score.

Score(z) = alpha*Relevance(z) + beta*Discovery(z) - gamma*Risk(z)

    Relevance(z) = topical_fit
    Discovery(z) = topical_fit * novelty * marginal_coverage * depth_fit
        novelty            = sqrt(source_distance * semantic_novelty)
        marginal_coverage  = max(0, subtopic_coverage - redundancy)
    Risk(z)      = mean(content_gap, source_risk, reading_cost)

Each sub-term is a normalized [0, 1] reading of a public evaluation concept:

  topical_fit         topical relevance to the brief (Saracevic, "Relevance: A
                      Review of the Literature", 2007)
  source_distance     distance from the sources the user habitually reads —
                      viewpoint/source diversity (Vrijenhoek et al., 2021, RADio)
  semantic_novelty    1 - similarity to what has already been learned this run —
                      novelty detection (Zhang, Callan & Minka, SIGIR 2002)
  subtopic_coverage   similarity to the brief's sub-questions — subtopic recall
                      (Zhai, Cooper & Lafferty, SIGIR 2003)
  redundancy          similarity to existing learnings, same source as above
  depth_fit           reading depth vs. the depth the brief asked for — Grice's
                      maxim of quantity (Grice, "Logic and Conversation", 1975)
  source_risk         provenance-based credibility: banned/untrusted domain,
                      non-peer-reviewed venue
  reading_cost        cost of consuming the candidate at its length, same source
                      as depth_fit
  content_gap         how little usable text was actually retrieved — a plumbing
                      signal, not a literature-derived axis

Novelty is a geometric mean because the two channels are independent: a familiar
source saying something new and a new source repeating a known claim should both
score mid, and a candidate that is neither should score near zero. Discovery
multiplies rather than adds so that any single zeroed factor kills the term —
off-brief novelty is not discovery.

Discovery is clamped to [0, 1]; the composite to [-1, 1].
"""
from __future__ import annotations

import math
from typing import Iterable

from ..config import CreativityConfig
from ..primitives.embed import EmbedBackend, cosine
from ..types import Brief, Candidate, Learning, ScoreBreakdown


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def _length_complexity(text: str) -> float:
    """Cheap proxy for reading complexity: log-scale length normalized to [0, 1].

    Below 400 chars: easy (0.2). Around 2000 chars: medium (0.5). 8000+: hard (0.9).
    """
    n = max(1, len(text))
    return _clamp((math.log10(n) - 2.0) / 2.0, 0.0, 1.0)


def _trust_score(domain: str, preferred: Iterable[str], banned: Iterable[str]) -> float:
    """1.0 trusted, 0.5 neutral, 0.0 banned. Approximate by suffix match."""
    d = (domain or "").lower()
    for b in banned:
        if d.endswith(b.lower()):
            return 0.0
    for p in preferred:
        if d.endswith(p.lower()):
            return 1.0
    return 0.5


def _domain_paradigm_centroid(
    preferred_sources: list[str], embed: EmbedBackend
) -> list[float]:
    """Mean embedding of preferred-source domain strings — used for paradigm distance."""
    if not preferred_sources:
        return [0.0] * embed.dim
    vecs = embed.encode_batch(preferred_sources)
    out = [0.0] * embed.dim
    for v in vecs:
        for i, x in enumerate(v):
            out[i] += x
    return [x / len(vecs) for x in out]


def _max_cosine(vec: list[float], targets: list[list[float]]) -> float:
    best = 0.0
    for t in targets:
        c = cosine(vec, t)
        if c > best:
            best = c
    return best


class CandidateScorer:
    """Scores Candidates with the full Score(z) breakdown.

    Candidate isolation: each candidate is scored without reference to other candidates
    in the same batch. Existing learnings are an input but are pre-computed, not
    per-batch.
    """

    def __init__(
        self,
        config: CreativityConfig,
        embed: EmbedBackend,
        brief: Brief,
        learnings: list[Learning],
        preferred_sources: list[str],
        banned_domains: list[str],
        language: str = "ja",
    ):
        self.config = config
        self.embed = embed
        self.brief = brief
        self.preferred_sources = preferred_sources
        self.banned_domains = banned_domains
        self.language = language

        # Pre-compute embeddings (candidate isolation: these are batch-invariant)
        self._brief_vec = embed.encode(brief.text_for_embed)
        self._sub_q_vecs = embed.encode_batch(brief.sub_questions or [brief.original_query])
        self._learning_vecs = embed.encode_batch([l.text for l in learnings]) if learnings else []
        self._paradigm_centroid = _domain_paradigm_centroid(preferred_sources, embed)

    def score(self, c: Candidate) -> ScoreBreakdown:
        text = c.text_for_embed
        vec = self.embed.encode(text)

        # Relevance is topical fit alone: cosine to the brief.
        topical_fit = _clamp(cosine(vec, self._brief_vec))
        relevance = topical_fit

        # Discovery sub-terms
        domain_vec = self.embed.encode(c.domain or "")
        source_distance = _clamp(1.0 - cosine(domain_vec, self._paradigm_centroid))
        redundancy = _max_cosine(vec, self._learning_vecs) if self._learning_vecs else 0.0
        semantic_novelty = _clamp(1.0 - redundancy)
        novelty = math.sqrt(max(0.0, source_distance * semantic_novelty)) * topical_fit

        subtopic_coverage = 0.0
        if self._sub_q_vecs:
            subtopic_coverage = sum(cosine(vec, q) for q in self._sub_q_vecs) / len(self._sub_q_vecs)
            subtopic_coverage = _clamp(subtopic_coverage)
        marginal_coverage = max(0.0, subtopic_coverage - redundancy)

        complexity = _length_complexity(text)
        K0 = self.config.complexity.K0_default
        sigma = max(1e-6, self.config.complexity.sigma_default)
        depth_fit = _clamp(math.exp(-abs(complexity - K0) / sigma))

        discovery = _clamp(novelty * marginal_coverage * depth_fit)

        # Risk sub-terms
        trust = _trust_score(c.domain, self.preferred_sources, self.banned_domains)
        source_risk = _clamp(1.0 - trust)  # banned → 1.0, trusted → 0.0, neutral → 0.5

        # Peer-review soft adjustment (v0.1). None = unknown = no-op.
        if c.meta.peer_reviewed is True:
            source_risk = _clamp(source_risk - 0.10)
        elif c.meta.peer_reviewed is False:
            source_risk = _clamp(source_risk + 0.20)

        # ponytail: length-only proxy for "did we actually get usable text";
        # upgrade to a boilerplate/extraction-quality check if it misfires.
        content_gap = 0.0
        if not text.strip():
            content_gap = 1.0
        elif len(text) < 80:
            content_gap = 0.5

        reading_cost = _length_complexity(text) * 0.8  # very long → costly to read

        risk = _clamp(content_gap * 0.34 + source_risk * 0.33 + reading_cost * 0.33)

        # Composite
        w = self.config.weights
        total = w.relevance * relevance + w.discovery * discovery - w.risk * risk
        total = _clamp(total, -1.0, 1.0)

        # Reasons (short, for ledger / debugging)
        why_ranked = (
            f"rel={relevance:.2f} disc={discovery:.2f} (nov={novelty:.2f} "
            f"cov={marginal_coverage:.2f} depth={depth_fit:.2f}) risk={risk:.2f} domain={c.domain}"
        )
        why_not_higher = []
        if relevance < 0.40:
            why_not_higher.append(f"low relevance ({relevance:.2f})")
        if discovery < 0.20:
            why_not_higher.append(f"low discovery ({discovery:.2f})")
        if risk > 0.50:
            why_not_higher.append(f"high risk ({risk:.2f})")
        if not why_not_higher:
            why_not_higher.append("nothing dominant — solid mid-range candidate")

        return ScoreBreakdown(
            relevance=relevance,
            discovery=discovery,
            risk=risk,
            source_distance=source_distance,
            semantic_novelty=semantic_novelty,
            topical_fit=topical_fit,
            subtopic_coverage=subtopic_coverage,
            redundancy=redundancy,
            depth_fit=depth_fit,
            content_gap=content_gap,
            source_risk=source_risk,
            reading_cost=reading_cost,
            total=total,
            why_ranked=why_ranked,
            why_not_higher="; ".join(why_not_higher),
        )
