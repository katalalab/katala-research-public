"""Embedding primitives.

Default: sentence-transformers (`all-MiniLM-L6-v2`, ~90MB, fully local).
Fallback: hash-based DummyEmbed — consistent but not semantic; lets smoke tests run
without ML dependencies.
"""
from __future__ import annotations

import hashlib
import math
import re
from typing import Protocol


_WORD_RE = re.compile(r"[A-Za-z0-9]+", flags=re.UNICODE)


class EmbedBackend(Protocol):
    name: str
    dim: int

    def encode(self, text: str) -> list[float]: ...

    def encode_batch(self, texts: list[str]) -> list[list[float]]: ...


def cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    num = sum(x * y for x, y in zip(a, b))
    da = math.sqrt(sum(x * x for x in a))
    db = math.sqrt(sum(x * x for x in b))
    if da == 0.0 or db == 0.0:
        return 0.0
    return num / (da * db)


class SentenceTransformerEmbed:
    """Lazy-loaded sentence-transformers backend."""

    name = "sentence-transformers"

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer  # type: ignore

        self._model = SentenceTransformer(model_name)
        self.dim = int(self._model.get_sentence_embedding_dimension())

    def encode(self, text: str) -> list[float]:
        vec = self._model.encode(text or "", normalize_embeddings=True)
        return [float(x) for x in vec]

    def encode_batch(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vecs = self._model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
        return [[float(x) for x in v] for v in vecs]


class DummyEmbed:
    """Hash-bucketed pseudo-embedding for smoke tests.

    Not semantic — cosine on these vectors approximates Jaccard of token-level hashes.
    Good enough to exercise the pipeline; do NOT rely on for production scoring.
    """

    name = "dummy"
    dim = 128

    def _vec(self, text: str) -> list[float]:
        """Bag-of-words + char-trigrams hashed into self.dim buckets.

        Tokenizing on word boundaries (not whitespace) means "anti-filter-bubble"
        is split into ["anti", "filter", "bubble"] — so it overlaps with text
        containing the bare words. Char-trigrams add a robustness layer for
        morphological variations.
        """
        vec = [0.0] * self.dim
        if not text:
            return vec
        lowered = text.lower()
        # Word-level tokens (1.0 weight)
        for tok in _WORD_RE.findall(lowered):
            idx = int(hashlib.sha1(tok.encode()).hexdigest()[:4], 16) % self.dim
            vec[idx] += 1.0
        # Char-trigram tokens (0.5 weight) — small bonus signal
        padded = f"  {lowered}  "
        for i in range(len(padded) - 2):
            tri = padded[i : i + 3]
            if tri.strip():
                idx = int(hashlib.sha1(tri.encode()).hexdigest()[:4], 16) % self.dim
                vec[idx] += 0.5
        # L2 normalize
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec

    def encode(self, text: str) -> list[float]:
        return self._vec(text)

    def encode_batch(self, texts: list[str]) -> list[list[float]]:
        return [self._vec(t) for t in texts]


def build_embed(*, prefer_local_model: bool = True) -> EmbedBackend:
    if prefer_local_model:
        try:
            return SentenceTransformerEmbed()
        except Exception:
            pass
    return DummyEmbed()
