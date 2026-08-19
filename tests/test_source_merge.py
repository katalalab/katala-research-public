"""search_and_merge calls all sources, dedupes by URL, swallows individual errors."""
from __future__ import annotations

from katala_research.primitives.search import search_and_merge
from katala_research.types import CandidateMeta, SearchHit


class FakeSource:
    def __init__(self, name: str, hits: list[SearchHit] | Exception):
        self.name = name
        self._hits = hits

    def search(self, query: str, *, limit: int = 5) -> list[SearchHit]:
        if isinstance(self._hits, Exception):
            raise self._hits
        return self._hits[:limit]


def _hit(url: str, backend: str, peer_reviewed: bool | None = None) -> SearchHit:
    return SearchHit(
        url=url, title=f"title-{url}", backend=backend,
        meta=CandidateMeta(peer_reviewed=peer_reviewed),
    )


def test_merge_dedups_by_url():
    s1 = FakeSource("a", [_hit("https://example.com/x", "a")])
    s2 = FakeSource("b", [_hit("https://example.com/x", "b"),  # duplicate
                          _hit("https://example.com/y", "b")])
    out = search_and_merge([s1, s2], "q")
    urls = [h.url for h in out]
    assert urls == ["https://example.com/x", "https://example.com/y"]
    # First one (from s1) wins for the duplicate.
    assert next(h for h in out if h.url == "https://example.com/x").backend == "a"


def test_merge_swallows_source_errors():
    """A failing source must not block the rest."""
    s_bad = FakeSource("bad", RuntimeError("source down"))
    s_good = FakeSource("good", [_hit("https://x.com/1", "good")])
    out = search_and_merge([s_bad, s_good], "q")
    assert len(out) == 1
    assert out[0].url == "https://x.com/1"


def test_merge_preserves_meta():
    s = FakeSource("s", [
        _hit("https://x.com/1", "s", peer_reviewed=True),
        _hit("https://x.com/2", "s", peer_reviewed=False),
    ])
    out = search_and_merge([s], "q")
    assert out[0].meta.peer_reviewed is True
    assert out[1].meta.peer_reviewed is False


def test_merge_respects_per_source_limit():
    s = FakeSource("s", [_hit(f"https://x.com/{i}", "s") for i in range(10)])
    out = search_and_merge([s], "q", per_source_limit=3)
    assert len(out) == 3
